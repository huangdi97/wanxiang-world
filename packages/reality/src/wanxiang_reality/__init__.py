"""Wanxiang R7 versioned reality semantics: contracts, profiles, runtime lock."""

from wanxiang_reality.bundles import (
    BundlePatch,
    ResolvedBundleStack,
    RuntimeArtifact,
    WorldBundle,
    resolve_bundle_stack,
)
from wanxiang_reality.contracts import (
    SERVICE_CONTRACTS,
    ServiceContract,
    contract_manifest,
    get_contract,
    manifest_digest,
)
from wanxiang_reality.errors import (
    ContractError,
    LockDriftError,
    LockImmutableError,
    LockMissingError,
    LockStoreError,
    LockTamperedError,
    ProfileError,
    RuntimeLockError,
    VersionError,
    WanxiangRealityError,
    WorldlineOpenError,
)
from wanxiang_reality.hashing import canonical_digest
from wanxiang_reality.lock_store import (
    LOCK_STORE_SCHEMA,
    FileLockStore,
    LockStore,
    MemoryLockStore,
    StoredLock,
    lock_projection,
    memory_lock_store,
)
from wanxiang_reality.migration import (
    DriftReport,
    LockedSnapshot,
    MigrationPlan,
    ReplayOutcome,
    compare_replay,
    plan_migration,
)
from wanxiang_reality.migration_apply import (
    Approval,
    MigrationArtifact,
    MigrationOutcome,
    dry_run_artifact,
    migrate_worldline,
)
from wanxiang_reality.profiles import (
    RealityProfile,
    RuntimeLock,
    WorldProfile,
    build_runtime_lock,
    profile_hash,
)
from wanxiang_reality.reference_profiles import (
    REFERENCE_REALITY_PROFILE_ID,
    REFERENCE_WORLD_PROFILE_ID,
    reference_provider_versions,
    reference_reality_profile,
    reference_schema_versions,
    reference_world_profile,
)
from wanxiang_reality.registry import ProfilePin, RealityProfileRegistry
from wanxiang_reality.rpc import HistoryAuthority, serve_stdio
from wanxiang_reality.rpc_support import HistoryEvent, RpcError, seam_digest
from wanxiang_reality.versions import Version
from wanxiang_reality.worldline_open import (
    WORLDLINE_OPEN_SCHEMA,
    LockDrift,
    OpenOutcome,
    OpenStatus,
    RuntimeFacts,
    WorldlineLockIdentity,
    open_worldline,
)

__version__ = "0.1.0"

__all__ = [
    "LOCK_STORE_SCHEMA",
    "REFERENCE_REALITY_PROFILE_ID",
    "REFERENCE_WORLD_PROFILE_ID",
    "SERVICE_CONTRACTS",
    "WORLDLINE_OPEN_SCHEMA",
    "Approval",
    "BundlePatch",
    "ContractError",
    "DriftReport",
    "FileLockStore",
    "HistoryAuthority",
    "HistoryEvent",
    "LockDrift",
    "LockDriftError",
    "LockImmutableError",
    "LockMissingError",
    "LockStore",
    "LockStoreError",
    "LockTamperedError",
    "LockedSnapshot",
    "MemoryLockStore",
    "MigrationArtifact",
    "MigrationOutcome",
    "MigrationPlan",
    "OpenOutcome",
    "OpenStatus",
    "ProfileError",
    "ProfilePin",
    "RealityProfile",
    "RealityProfileRegistry",
    "ResolvedBundleStack",
    "RuntimeArtifact",
    "ReplayOutcome",
    "RpcError",
    "RuntimeFacts",
    "RuntimeLock",
    "RuntimeLockError",
    "ServiceContract",
    "StoredLock",
    "Version",
    "VersionError",
    "WanxiangRealityError",
    "WorldBundle",
    "WorldProfile",
    "WorldlineLockIdentity",
    "WorldlineOpenError",
    "build_runtime_lock",
    "canonical_digest",
    "compare_replay",
    "contract_manifest",
    "dry_run_artifact",
    "get_contract",
    "lock_projection",
    "manifest_digest",
    "memory_lock_store",
    "migrate_worldline",
    "open_worldline",
    "plan_migration",
    "profile_hash",
    "reference_provider_versions",
    "reference_reality_profile",
    "reference_schema_versions",
    "reference_world_profile",
    "resolve_bundle_stack",
    "seam_digest",
    "serve_stdio",
]
