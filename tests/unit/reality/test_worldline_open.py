"""Behaviour of opening a worldline against its persisted runtime lock (R7)."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_reality.contracts import SERVICE_CONTRACTS
from wanxiang_reality.errors import LockDriftError, LockMissingError
from wanxiang_reality.lock_store import LockStore, MemoryLockStore, StoredLock, memory_lock_store
from wanxiang_reality.migration import LockedSnapshot, ReplayOutcome, plan_migration
from wanxiang_reality.profiles import (
    RealityProfile,
    RuntimeLock,
    WorldProfile,
    build_runtime_lock,
    profile_hash,
)
from wanxiang_reality.reference_profiles import (
    reference_provider_versions,
    reference_reality_profile,
    reference_schema_versions,
    reference_world_profile,
)
from wanxiang_reality.versions import Version
from wanxiang_reality.worldline_open import (
    OpenOutcome,
    OpenStatus,
    RuntimeFacts,
    WorldlineLockIdentity,
    open_worldline,
)

pytestmark = pytest.mark.unit

WORLDLINE = "wl_open"
SEAM = "wanxiang.history@1"


def _contract_versions() -> dict[str, str]:
    return {contract.contract_id: contract.api_version for contract in SERVICE_CONTRACTS}


def _identity(
    *,
    world_id: str = "world-1",
    world_definition_version: str = "1.0.0",
    world_instance_id: str = "instance-1",
    worldline_id: str = WORLDLINE,
) -> WorldlineLockIdentity:
    return WorldlineLockIdentity(
        world_id=world_id,
        world_definition_version=world_definition_version,
        world_instance_id=world_instance_id,
        worldline_id=worldline_id,
    )


def _facts(
    *,
    composition_runtime: str = "cordis",
    composition_runtime_version: str = "4.0.0-rc.10",
    service_contract_versions: dict[str, str] | None = None,
    provider_versions: dict[str, str] | None = None,
    artifact_hashes: dict[str, str] | None = None,
    schema_versions: dict[str, str] | None = None,
    runtime_config_hash: str = "cfg",
) -> RuntimeFacts:
    return RuntimeFacts(
        composition_runtime=composition_runtime,
        composition_runtime_version=composition_runtime_version,
        service_contract_versions=service_contract_versions or _contract_versions(),
        provider_versions=provider_versions or reference_provider_versions(),
        artifact_hashes=artifact_hashes if artifact_hashes is not None else {},
        schema_versions=schema_versions or reference_schema_versions(),
        runtime_config_hash=runtime_config_hash,
    )


_DRIFT_FACTS: dict[str, RuntimeFacts] = {
    "provider": _facts(
        provider_versions={**reference_provider_versions(), "provider.model.reference": "9.9.9"}
    ),
    "schema": _facts(
        schema_versions={**reference_schema_versions(), "wanxiang.schema.canonical": "9"}
    ),
    "contract": _facts(service_contract_versions={**_contract_versions(), SEAM: "2"}),
    "artifact": _facts(artifact_hashes={"artifact.new": "x"}),
    "runtime_config": _facts(runtime_config_hash="rotated"),
    "composition_runtime_version": _facts(composition_runtime_version="5.0.0"),
}

_MISMATCHED_IDENTITIES: dict[str, WorldlineLockIdentity] = {
    "world_id": _identity(world_id="other-world"),
    "world_definition_version": _identity(world_definition_version="9.9.9"),
    "world_instance_id": _identity(world_instance_id="other-instance"),
}


def _open(
    store: LockStore,
    *,
    reality: RealityProfile | None = None,
    world: WorldProfile | None = None,
    facts: RuntimeFacts | None = None,
    identity: WorldlineLockIdentity | None = None,
    create_if_missing: bool = False,
) -> OpenOutcome:
    return open_worldline(
        identity=identity if identity is not None else _identity(),
        reality=reality if reality is not None else reference_reality_profile(),
        world=world if world is not None else reference_world_profile(),
        facts=facts if facts is not None else _facts(),
        store=store,
        create_if_missing=create_if_missing,
    )


def _created_store() -> tuple[MemoryLockStore, OpenOutcome]:
    store = memory_lock_store()
    outcome = _open(store, create_if_missing=True)
    assert outcome.status is OpenStatus.CREATED
    return store, outcome


class _RecordStore:
    """A store that always returns one record, whatever worldline is asked for."""

    def __init__(self, stored: StoredLock) -> None:
        self._stored = stored

    def read(self, worldline_id: str) -> StoredLock | None:
        return self._stored

    def write(self, stored: StoredLock, *, expected_revision: int | None) -> None:
        raise AssertionError("opening a worldline must never write")


class _StubReplaySource:
    """Read-only replay source returning identical baseline/candidate outcomes."""

    def snapshot(self, worldline_id: str) -> LockedSnapshot:
        profile = reference_reality_profile()
        return LockedSnapshot(
            world_id="world-1",
            worldline_id=worldline_id,
            revision=1,
            state_hash="state-1",
            event_count=1,
            profile_ref=f"{profile.profile_id}@{profile.version}",
            lock_digest="0" * 64,
        )

    def replay(
        self, worldline_id: str, profile: RealityProfile, lock: RuntimeLock
    ) -> ReplayOutcome:
        return ReplayOutcome(
            world_id="world-1",
            worldline_id=worldline_id,
            history_head=1,
            state_hash="state-1",
            entity_ids=("entity-a",),
            branch_graph_digest="branch-1",
            lineage_digest="lineage-1",
            rights_evidence_digest="rights-1",
            projection={"status": "calm"},
            invariants={"commit_authority_exclusive": True},
        )


def test_creation_persists_a_lock_that_binds_every_required_dimension() -> None:
    store, outcome = _created_store()
    lock = outcome.lock
    reality = reference_reality_profile()

    assert lock.world_id == "world-1"
    assert lock.world_definition_version == "1.0.0"
    assert lock.world_instance_id == "instance-1"
    assert lock.worldline_id == WORLDLINE
    assert lock.reality_profile_ref == f"{reality.profile_id}@{reality.version}"
    assert lock.reality_profile_hash == profile_hash(reality)
    assert lock.service_contract_versions == _contract_versions()
    assert lock.provider_versions == reference_provider_versions()
    assert outcome.revision == 1
    assert store.read(WORLDLINE) is not None


def test_missing_lock_without_create_if_missing_is_refused() -> None:
    with pytest.raises(LockMissingError):
        _open(memory_lock_store())


@pytest.mark.parametrize("field", sorted(_MISMATCHED_IDENTITIES))
def test_identity_mismatch_on_a_field_is_refused(field: str) -> None:
    store, _ = _created_store()

    with pytest.raises(LockDriftError, match=field):
        _open(store, identity=_MISMATCHED_IDENTITIES[field])


def test_identity_mismatch_on_the_worldline_id_is_refused() -> None:
    _, created = _created_store()
    lock = created.lock
    stored = StoredLock(
        worldline_id=lock.worldline_id,
        revision=1,
        written_at="2026-01-01T00:00:00Z",
        lock=lock,
        lock_digest=lock.lock_digest(),
    )

    with pytest.raises(LockDriftError, match="worldline_id"):
        _open(_RecordStore(stored), identity=_identity(worldline_id="some-other-worldline"))


@pytest.mark.parametrize("case", sorted(_DRIFT_FACTS))
def test_runtime_fact_drift_is_refused_and_leaves_the_lock_untouched(case: str) -> None:
    store, _ = _created_store()
    before = store.read(WORLDLINE)

    with pytest.raises(LockDriftError):
        _open(store, facts=_DRIFT_FACTS[case])

    assert store.read(WORLDLINE) == before


def test_opening_an_existing_lock_is_deterministic_across_stores() -> None:
    creator = memory_lock_store()
    _open(creator, create_if_missing=True)

    first = _open(memory_lock_store_from(creator))
    second = _open(memory_lock_store_from(creator))

    assert first.status is OpenStatus.OPENED
    assert second.status is OpenStatus.OPENED
    assert first.outcome_digest() == second.outcome_digest()
    assert first.lock_digest == second.lock_digest


def memory_lock_store_from(source: MemoryLockStore) -> MemoryLockStore:
    """Build an independent second store over the same record (a process restart)."""
    store = memory_lock_store()
    stored = source.read(WORLDLINE)
    assert stored is not None
    store.write(stored, expected_revision=None)
    return store


def test_a_major_reality_upgrade_requires_migration_and_writes_nothing() -> None:
    store, created = _created_store()
    before = store.read(WORLDLINE)
    upgraded = replace(reference_reality_profile(), version=Version(2, 0, 0))

    outcome = _open(store, reality=upgraded)

    assert outcome.status is OpenStatus.MIGRATION_REQUIRED
    assert outcome.baseline_profile_ref == created.lock.reality_profile_ref
    assert outcome.target_profile_ref == f"{upgraded.profile_id}@{upgraded.version}"
    assert store.read(WORLDLINE) == before


def test_a_major_upgrade_leads_to_an_existing_plan_migration_path() -> None:
    store, created = _created_store()
    upgraded = replace(reference_reality_profile(), version=Version(2, 0, 0))
    outcome = _open(store, reality=upgraded)
    target_lock = build_runtime_lock(
        upgraded,
        reference_world_profile(),
        world_id="world-1",
        world_instance_id="instance-1",
        worldline_id=WORLDLINE,
        composition_runtime="cordis",
        composition_runtime_version="4.0.0-rc.10",
        service_contract_versions=_contract_versions(),
        provider_versions=reference_provider_versions(),
        artifact_hashes={},
        schema_versions=reference_schema_versions(),
        migration_lineage=("genesis",),
        runtime_config_hash="cfg",
    )

    plan = plan_migration(
        worldline_id=WORLDLINE,
        baseline_profile=reference_reality_profile(),
        target_profile=upgraded,
        baseline_lock=outcome.lock,
        target_lock=target_lock,
        source=_StubReplaySource(),
        migration_code_version="r7-migration-1",
    )

    assert created.lock.lock_digest() == outcome.lock_digest
    assert plan.recommendation in {"migrate", "fork"}


def test_a_same_major_version_bump_is_refused_as_drift_not_migrated() -> None:
    store, _ = _created_store()
    bumped = replace(reference_reality_profile(), version=Version(1, 1, 0))

    with pytest.raises(LockDriftError, match="reality_profile.version"):
        _open(store, reality=bumped)


def test_a_changed_profile_hash_is_refused_as_drift() -> None:
    store, _ = _created_store()
    fewer_seams = reference_reality_profile().required_seams[:-1]
    changed = replace(reference_reality_profile(), required_seams=fewer_seams)

    with pytest.raises(LockDriftError, match="reality_profile.hash"):
        _open(store, reality=changed)


def test_opening_a_worldline_can_never_repin_its_lock() -> None:
    store, created = _created_store()
    before = store.read(WORLDLINE)

    with pytest.raises(LockDriftError):
        _open(store, facts=_facts(runtime_config_hash="rotated"))

    reopened = _open(store)
    assert reopened.status is OpenStatus.OPENED
    assert reopened.lock_digest == created.lock_digest
    assert store.read(WORLDLINE) == before
