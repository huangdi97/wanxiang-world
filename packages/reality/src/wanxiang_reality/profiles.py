"""Versioned reality/world profiles and the R7 runtime lock.

The runtime lock is the master requirement of R7: a running world instance
must be able to name the exact reality profile, world profile, service
contracts, providers, artifacts and migration lineage it was composed from.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_reality.contracts import get_contract
from wanxiang_reality.errors import ContractError, ProfileError, RuntimeLockError, VersionError
from wanxiang_reality.hashing import canonical_digest
from wanxiang_reality.versions import Version

_REQUIRED_WORLD_DIMENSIONS = (
    "actors",
    "capabilities",
    "distribution",
    "experience",
    "memory",
    "projection",
    "simulation",
    "space",
    "time",
)


@dataclass(frozen=True, slots=True)
class RealityProfile:
    """A versioned set of service seams a world composition must bind."""

    profile_id: str
    version: Version
    required_seams: tuple[str, ...]
    optional_seams: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_reality_profile(self)


def _validate_reality_profile(profile: RealityProfile) -> None:
    if not profile.profile_id.strip():
        raise ProfileError("reality profile_id must not be empty")
    _require_sorted_unique("required_seams", profile.required_seams)
    _require_sorted_unique("optional_seams", profile.optional_seams)
    for seam_id in profile.required_seams:
        _require_known_seam(seam_id)
    overlap = sorted(set(profile.required_seams) & set(profile.optional_seams))
    if overlap:
        raise ProfileError(f"seams declared both required and optional: {overlap}")


def _require_sorted_unique(field_name: str, values: tuple[str, ...]) -> None:
    if list(values) != sorted(set(values)):
        raise ProfileError(f"{field_name} must be sorted and free of duplicates")


def _require_known_seam(seam_id: str) -> None:
    try:
        get_contract(seam_id)
    except ContractError as exc:
        raise ProfileError(f"unknown required seam: {seam_id!r}") from exc


@dataclass(frozen=True, slots=True)
class WorldProfile:
    """A versioned world definition bound to one reality profile."""

    profile_id: str
    version: Version
    reality_profile_ref: str
    providers: tuple[str, ...]
    dimensions: dict[str, str]

    def __post_init__(self) -> None:
        _validate_world_profile(self)


def _validate_world_profile(profile: WorldProfile) -> None:
    if not profile.profile_id.strip():
        raise ProfileError("world profile_id must not be empty")
    if not profile.reality_profile_ref.strip():
        raise ProfileError("world profile reality_profile_ref must not be empty")
    missing = sorted(set(_REQUIRED_WORLD_DIMENSIONS) - set(profile.dimensions))
    if missing:
        raise ProfileError(f"world profile is missing dimensions: {missing}")
    unexpected = sorted(set(profile.dimensions) - set(_REQUIRED_WORLD_DIMENSIONS))
    if unexpected:
        raise ProfileError(f"world profile has unknown dimensions: {unexpected}")
    empty = sorted(name for name, value in profile.dimensions.items() if not value.strip())
    if empty:
        raise ProfileError(f"world profile dimensions must be non-empty: {empty}")


@dataclass(frozen=True, slots=True)
class RuntimeLock:
    """The immutable pin of everything one world instance runs on."""

    world_id: str
    world_definition_version: str
    world_instance_id: str
    worldline_id: str
    reality_profile_ref: str
    reality_profile_hash: str
    world_profile_ref: str
    world_profile_hash: str
    composition_runtime: str
    composition_runtime_version: str
    service_contract_versions: dict[str, str]
    provider_versions: dict[str, str]
    artifact_hashes: dict[str, str]
    schema_versions: dict[str, str]
    migration_lineage: tuple[str, ...]
    runtime_config_hash: str

    def lock_digest(self) -> str:
        """Return the canonical sha256 digest of the lock projection."""
        return canonical_digest(_lock_projection(self))

    def validate(self) -> None:
        """Raise RuntimeLockError when the lock is incomplete or inconsistent."""
        required_text = (
            ("world_id", self.world_id),
            ("world_definition_version", self.world_definition_version),
            ("world_instance_id", self.world_instance_id),
            ("worldline_id", self.worldline_id),
            ("reality_profile_ref", self.reality_profile_ref),
            ("reality_profile_hash", self.reality_profile_hash),
            ("world_profile_ref", self.world_profile_ref),
            ("world_profile_hash", self.world_profile_hash),
            ("composition_runtime", self.composition_runtime),
            ("composition_runtime_version", self.composition_runtime_version),
            ("runtime_config_hash", self.runtime_config_hash),
        )
        for field_name, value in required_text:
            if not value.strip():
                raise RuntimeLockError(f"empty required field: {field_name}")
        _require_non_empty_mapping("service_contract_versions", self.service_contract_versions)
        _require_non_empty_mapping("provider_versions", self.provider_versions)
        for contract_id, version_text in self.service_contract_versions.items():
            try:
                Version.parse(version_text)
            except VersionError as exc:
                raise RuntimeLockError(
                    f"contract {contract_id!r} has invalid version {version_text!r}"
                ) from exc


def _require_non_empty_mapping(field_name: str, mapping: dict[str, str]) -> None:
    if not mapping:
        raise RuntimeLockError(f"{field_name} must not be empty")
    for key, value in mapping.items():
        if not key.strip() or not value.strip():
            raise RuntimeLockError(f"{field_name} must not contain empty keys or values")


def _reality_projection(profile: RealityProfile) -> dict[str, object]:
    return {
        "profile_id": profile.profile_id,
        "version": str(profile.version),
        "required_seams": list(profile.required_seams),
        "optional_seams": list(profile.optional_seams),
    }


def _world_projection(profile: WorldProfile) -> dict[str, object]:
    return {
        "profile_id": profile.profile_id,
        "version": str(profile.version),
        "reality_profile_ref": profile.reality_profile_ref,
        "providers": list(profile.providers),
        "dimensions": dict(profile.dimensions),
    }


def _lock_projection(lock: RuntimeLock) -> dict[str, object]:
    return {
        "world_id": lock.world_id,
        "world_definition_version": lock.world_definition_version,
        "world_instance_id": lock.world_instance_id,
        "worldline_id": lock.worldline_id,
        "reality_profile_ref": lock.reality_profile_ref,
        "reality_profile_hash": lock.reality_profile_hash,
        "world_profile_ref": lock.world_profile_ref,
        "world_profile_hash": lock.world_profile_hash,
        "composition_runtime": lock.composition_runtime,
        "composition_runtime_version": lock.composition_runtime_version,
        "service_contract_versions": dict(lock.service_contract_versions),
        "provider_versions": dict(lock.provider_versions),
        "artifact_hashes": dict(lock.artifact_hashes),
        "schema_versions": dict(lock.schema_versions),
        "migration_lineage": list(lock.migration_lineage),
        "runtime_config_hash": lock.runtime_config_hash,
    }


def profile_hash(profile: RealityProfile) -> str:
    """Return the canonical sha256 digest of the reality profile projection."""
    return canonical_digest(_reality_projection(profile))


def build_runtime_lock(
    reality: RealityProfile,
    world: WorldProfile,
    *,
    world_id: str,
    world_instance_id: str,
    worldline_id: str,
    composition_runtime: str,
    composition_runtime_version: str,
    service_contract_versions: dict[str, str],
    provider_versions: dict[str, str],
    artifact_hashes: dict[str, str],
    schema_versions: dict[str, str],
    migration_lineage: tuple[str, ...],
    runtime_config_hash: str,
) -> RuntimeLock:
    """Compose and validate a runtime lock from profiles and runtime facts.

    ``world_definition_version`` is taken from ``world.version``; both profile
    hashes are recomputed from the profiles instead of being caller-supplied.
    """
    lock = RuntimeLock(
        world_id=world_id,
        world_definition_version=str(world.version),
        world_instance_id=world_instance_id,
        worldline_id=worldline_id,
        reality_profile_ref=f"{reality.profile_id}@{reality.version}",
        reality_profile_hash=profile_hash(reality),
        world_profile_ref=f"{world.profile_id}@{world.version}",
        world_profile_hash=canonical_digest(_world_projection(world)),
        composition_runtime=composition_runtime,
        composition_runtime_version=composition_runtime_version,
        service_contract_versions=dict(service_contract_versions),
        provider_versions=dict(provider_versions),
        artifact_hashes=dict(artifact_hashes),
        schema_versions=dict(schema_versions),
        migration_lineage=migration_lineage,
        runtime_config_hash=runtime_config_hash,
    )
    lock.validate()
    return lock
