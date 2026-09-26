"""Wanxiang R7 versioned reality semantics: contracts, profiles, runtime lock."""

from wanxiang_reality.contracts import (
    SERVICE_CONTRACTS,
    ServiceContract,
    contract_manifest,
    get_contract,
    manifest_digest,
)
from wanxiang_reality.errors import (
    ContractError,
    ProfileError,
    RuntimeLockError,
    VersionError,
    WanxiangRealityError,
)
from wanxiang_reality.hashing import canonical_digest
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
from wanxiang_reality.registry import ProfilePin, RealityProfileRegistry
from wanxiang_reality.rpc import HistoryAuthority, serve_stdio
from wanxiang_reality.rpc_support import HistoryEvent, RpcError, seam_digest
from wanxiang_reality.versions import Version

__version__ = "0.1.0"

__all__ = [
    "SERVICE_CONTRACTS",
    "Approval",
    "ContractError",
    "DriftReport",
    "HistoryAuthority",
    "HistoryEvent",
    "LockedSnapshot",
    "MigrationArtifact",
    "MigrationOutcome",
    "MigrationPlan",
    "ProfileError",
    "ProfilePin",
    "RealityProfile",
    "RealityProfileRegistry",
    "ReplayOutcome",
    "RpcError",
    "RuntimeLock",
    "RuntimeLockError",
    "ServiceContract",
    "Version",
    "VersionError",
    "WanxiangRealityError",
    "WorldProfile",
    "build_runtime_lock",
    "canonical_digest",
    "compare_replay",
    "contract_manifest",
    "dry_run_artifact",
    "get_contract",
    "manifest_digest",
    "migrate_worldline",
    "plan_migration",
    "profile_hash",
    "seam_digest",
    "serve_stdio",
]
