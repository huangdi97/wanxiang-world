"""RuntimeLock as a real worldline runtime invariant (R7).

A ``StoredLock`` pins a process to its exact composition; this module only reads
it, and treats any drift from the current facts as a refusal, never a rewrite.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from wanxiang_reality.errors import (
    LockDriftError,
    LockMissingError,
    VersionError,
    WorldlineOpenError,
)
from wanxiang_reality.hashing import canonical_digest
from wanxiang_reality.lock_store import LockStore, StoredLock
from wanxiang_reality.profiles import (
    RealityProfile,
    RuntimeLock,
    WorldProfile,
    build_runtime_lock,
    profile_hash,
)
from wanxiang_reality.versions import Version

WORLDLINE_OPEN_SCHEMA = "wanxiang.r7.worldline-open.v1"


@dataclass(frozen=True, slots=True)
class WorldlineLockIdentity:
    """The four identifiers that name one world instance's worldline."""

    world_id: str
    world_definition_version: str
    world_instance_id: str
    worldline_id: str

    def __post_init__(self) -> None:
        values = (
            self.world_id,
            self.world_definition_version,
            self.world_instance_id,
            self.worldline_id,
        )
        if not all(value.strip() for value in values):
            raise WorldlineOpenError("worldline identity fields must not be empty")


@dataclass(frozen=True, slots=True)
class RuntimeFacts:
    composition_runtime: str
    composition_runtime_version: str
    service_contract_versions: dict[str, str]
    provider_versions: dict[str, str]
    artifact_hashes: dict[str, str]
    schema_versions: dict[str, str]
    runtime_config_hash: str


@dataclass(frozen=True, slots=True)
class LockDrift:
    dimension: str
    expected: str
    actual: str


class OpenStatus(StrEnum):
    CREATED = "CREATED"
    OPENED = "OPENED"
    MIGRATION_REQUIRED = "MIGRATION_REQUIRED"


@dataclass(frozen=True, slots=True)
class OpenOutcome:
    """The deterministic result of opening (or refusing to open) a worldline."""

    status: OpenStatus
    identity: WorldlineLockIdentity
    lock: RuntimeLock
    lock_digest: str
    revision: int
    drift: tuple[LockDrift, ...] = ()
    baseline_profile_ref: str = ""
    target_profile_ref: str = ""

    def outcome_digest(self) -> str:
        """Return a canonical digest so a replay can be compared bit for bit."""
        return canonical_digest(
            {
                "schema": WORLDLINE_OPEN_SCHEMA,
                "status": self.status.value,
                "identity": {
                    "world_id": self.identity.world_id,
                    "world_definition_version": self.identity.world_definition_version,
                    "world_instance_id": self.identity.world_instance_id,
                    "worldline_id": self.identity.worldline_id,
                },
                "lock_digest": self.lock_digest,
                "revision": self.revision,
                "drift": [
                    {"dimension": d.dimension, "expected": d.expected, "actual": d.actual}
                    for d in self.drift
                ],
                "baseline_profile_ref": self.baseline_profile_ref,
                "target_profile_ref": self.target_profile_ref,
            }
        )


def open_worldline(
    *,
    identity: WorldlineLockIdentity,
    reality: RealityProfile,
    world: WorldProfile,
    facts: RuntimeFacts,
    store: LockStore,
    create_if_missing: bool,
) -> OpenOutcome:
    """Open a worldline against its persisted runtime lock, or create the lock.

    No stored lock: raise :class:`LockMissingError` unless ``create_if_missing``;
    otherwise build and write a fresh lock at revision 1. A stored lock is only
    read: identity is checked, then every bound dimension is compared and any
    disagreement raises :class:`LockDriftError` (fail-closed, nothing written).
    A major ``reality`` upgrade is not drift: it returns
    :class:`OpenStatus.MIGRATION_REQUIRED` and writes nothing, so the caller must
    use the existing :func:`wanxiang_reality.migration.plan_migration` path with
    the pinned profile, ``baseline_lock=outcome.lock`` and a built target lock.
    """
    stored = store.read(identity.worldline_id)
    if stored is not None:
        return _open_existing(identity, reality, world, facts, stored)
    if not create_if_missing:
        raise LockMissingError(f"worldline {identity.worldline_id} has no persisted runtime lock")
    if identity.world_definition_version != str(world.version):
        raise WorldlineOpenError(
            f"identity definition version {identity.world_definition_version!r} "
            f"does not match the world profile {world.version}"
        )
    lock = _build_lock(identity, reality, world, facts)
    store.write(
        StoredLock(
            worldline_id=identity.worldline_id,
            revision=1,
            written_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            lock=lock,
            lock_digest=lock.lock_digest(),
        ),
        expected_revision=None,
    )
    return OpenOutcome(OpenStatus.CREATED, identity, lock, lock.lock_digest(), 1)


def _open_existing(
    identity: WorldlineLockIdentity,
    reality: RealityProfile,
    world: WorldProfile,
    facts: RuntimeFacts,
    stored: StoredLock,
) -> OpenOutcome:
    lock = stored.lock
    _verify_identity(identity, lock)
    drift, migration_required = _reality_profile_drift(reality, lock)
    if migration_required:
        return OpenOutcome(
            OpenStatus.MIGRATION_REQUIRED,
            identity,
            lock,
            stored.lock_digest,
            stored.revision,
            tuple(drift),
            lock.reality_profile_ref,
            f"{reality.profile_id}@{reality.version}",
        )
    drift += _runtime_facts_drift(identity, reality, world, facts, lock)
    if drift:
        dimensions = tuple(entry.dimension for entry in drift)
        raise LockDriftError(
            f"worldline {identity.worldline_id} refused: runtime lock drift on {list(dimensions)}",
            drifted_dimensions=dimensions,
        )
    return OpenOutcome(OpenStatus.OPENED, identity, lock, stored.lock_digest, stored.revision)


def _build_lock(
    identity: WorldlineLockIdentity,
    reality: RealityProfile,
    world: WorldProfile,
    facts: RuntimeFacts,
) -> RuntimeLock:
    lock = build_runtime_lock(
        reality,
        world,
        world_id=identity.world_id,
        world_instance_id=identity.world_instance_id,
        worldline_id=identity.worldline_id,
        composition_runtime=facts.composition_runtime,
        composition_runtime_version=facts.composition_runtime_version,
        service_contract_versions=facts.service_contract_versions,
        provider_versions=facts.provider_versions,
        artifact_hashes=facts.artifact_hashes,
        schema_versions=facts.schema_versions,
        migration_lineage=("genesis",),
        runtime_config_hash=facts.runtime_config_hash,
    )
    lock.validate()
    return lock


def _verify_identity(identity: WorldlineLockIdentity, lock: RuntimeLock) -> None:
    for field_name in ("world_id", "world_definition_version", "world_instance_id", "worldline_id"):
        supplied: object = getattr(identity, field_name)
        pinned: object = getattr(lock, field_name)
        if supplied != pinned:
            raise LockDriftError(
                f"worldline identity mismatch on {field_name}: supplied {supplied!r}, "
                f"lock pins {pinned!r}"
            )


def _reality_profile_drift(
    reality: RealityProfile, lock: RuntimeLock
) -> tuple[list[LockDrift], bool]:
    pinned_id, pinned_version = _split_profile_ref(lock.reality_profile_ref)
    if reality.profile_id != pinned_id:
        target = f"{reality.profile_id}@{reality.version}"
        return [LockDrift("reality_profile.ref", lock.reality_profile_ref, target)], False
    entries: list[LockDrift] = []
    if reality.version != pinned_version:
        entries.append(
            LockDrift("reality_profile.version", str(pinned_version), str(reality.version))
        )
        if reality.version.is_major_upgrade_from(pinned_version):
            return entries, True
    current_hash = profile_hash(reality)
    if current_hash != lock.reality_profile_hash:
        entries.append(LockDrift("reality_profile.hash", lock.reality_profile_hash, current_hash))
    return entries, False


def _runtime_facts_drift(
    identity: WorldlineLockIdentity,
    reality: RealityProfile,
    world: WorldProfile,
    facts: RuntimeFacts,
    lock: RuntimeLock,
) -> list[LockDrift]:
    expected = _build_lock(identity, reality, world, facts)
    singles = {
        "world_profile.ref": (lock.world_profile_ref, expected.world_profile_ref),
        "world_profile.hash": (lock.world_profile_hash, expected.world_profile_hash),
        "composition_runtime": (lock.composition_runtime, expected.composition_runtime),
        "composition_runtime.version": (
            lock.composition_runtime_version,
            expected.composition_runtime_version,
        ),
        "runtime_config_hash": (lock.runtime_config_hash, expected.runtime_config_hash),
    }
    entries = [LockDrift(d, p, a) for d, (p, a) in singles.items() if p != a]
    mappings = {
        "service_contract_versions": (
            lock.service_contract_versions,
            facts.service_contract_versions,
        ),
        "provider_versions": (lock.provider_versions, facts.provider_versions),
        "schema_versions": (lock.schema_versions, facts.schema_versions),
        "artifact_hashes": (lock.artifact_hashes, facts.artifact_hashes),
    }
    for dimension, (pinned, actual) in mappings.items():
        entries.extend(
            LockDrift(f"{dimension}.{key}", pinned.get(key, ""), actual.get(key, ""))
            for key in sorted(set(pinned) | set(actual))
            if pinned.get(key, "") != actual.get(key, "")
        )
    return entries


def _split_profile_ref(ref: str) -> tuple[str, Version]:
    profile_id, _, version_text = ref.rpartition("@")
    if not profile_id or not version_text:
        raise LockDriftError(f"malformed reality profile ref in lock: {ref!r}")
    try:
        return profile_id, Version.parse(version_text)
    except VersionError as exc:
        raise LockDriftError(f"malformed reality profile ref in lock: {ref!r}") from exc


__all__ = [
    "WORLDLINE_OPEN_SCHEMA",
    "LockDrift",
    "OpenOutcome",
    "OpenStatus",
    "RuntimeFacts",
    "WorldlineLockIdentity",
    "open_worldline",
]
