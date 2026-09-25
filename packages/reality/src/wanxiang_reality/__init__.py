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
from wanxiang_reality.profiles import (
    RealityProfile,
    RuntimeLock,
    WorldProfile,
    build_runtime_lock,
    profile_hash,
)
from wanxiang_reality.versions import Version

__version__ = "0.1.0"

__all__ = [
    "SERVICE_CONTRACTS",
    "ContractError",
    "ProfileError",
    "RealityProfile",
    "RuntimeLock",
    "RuntimeLockError",
    "ServiceContract",
    "Version",
    "VersionError",
    "WanxiangRealityError",
    "WorldProfile",
    "build_runtime_lock",
    "canonical_digest",
    "contract_manifest",
    "get_contract",
    "manifest_digest",
    "profile_hash",
]
