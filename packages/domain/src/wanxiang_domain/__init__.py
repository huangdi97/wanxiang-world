"""Wanxiang domain core: pure semantic contracts and invariants.

Framework-independent. No FastAPI/SQLAlchemy/Alembic/LLM imports are allowed
(architecturally enforced).
"""

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.constitution import (
    ROOT_CONSTITUTION,
    ConstitutionManifest,
    ConstitutionVersion,
    constitution_from_primitive,
    legacy_default_constitution,
)
from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    ProposedWorldDelta,
    RelationCreate,
    RelationDelete,
)
from wanxiang_domain.entity import ComponentData, EntityState, FieldValue, RelationState
from wanxiang_domain.errors import (
    Conflict,
    ContractError,
    CorruptEventStream,
    DuplicateCommandConflict,
    ExternalDataBlocked,
    ExternalDependencyError,
    IncompatibleVersion,
    NotFound,
    PermissionDenied,
    PersistenceError,
    ReplayError,
    RightsDenied,
    StaleRevision,
    ValidationRejected,
    WanxiangError,
)
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.evidence import ClaimRef, EvidenceRef
from wanxiang_domain.hashing import canonical_json, semantic_sha256
from wanxiang_domain.hierarchy import (
    BranchAncestry,
    BranchMetadata,
    BranchRevision,
    EventSeq,
)
from wanxiang_domain.ids import (
    ActorId,
    BranchId,
    ClaimId,
    CommandId,
    ComponentId,
    CorrelationId,
    EntityId,
    EventId,
    EvidenceId,
    ProjectionId,
    RelationId,
    RunId,
    SessionId,
    SnapshotId,
    TraceId,
    WanxiangId,
    WorldInstanceId,
)
from wanxiang_domain.reality_root import REALITY_ROOT_SEMANTICS, RealityRootContract
from wanxiang_domain.rights import RightsDecision, RightsEnvelope
from wanxiang_domain.run import RunMetadata
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.state import CanonicalState
from wanxiang_domain.time import CommitTimestamp, WorldTime
from wanxiang_domain.versions import PackageVersion, RuntimeVersion, SchemaVersion

__version__ = "0.1.0"

__all__ = [
    "ActorId",
    "BranchAncestry",
    "BranchId",
    "BranchMetadata",
    "BranchRevision",
    "CanonicalState",
    "ClaimId",
    "ClaimRef",
    "CommittedEvent",
    "CommandEnvelope",
    "CommandId",
    "CommitTimestamp",
    "ComponentData",
    "ComponentId",
    "Conflict",
    "ContractError",
    "CorrelationId",
    "CorruptEventStream",
    "DuplicateCommandConflict",
    "EntityCreate",
    "EntityDelete",
    "EntityId",
    "EntityState",
    "EntityUpdate",
    "EventId",
    "EventSeq",
    "EvidenceId",
    "EvidenceRef",
    "ExternalDataBlocked",
    "ExternalDependencyError",
    "FieldValue",
    "IncompatibleVersion",
    "NotFound",
    "PackageVersion",
    "PermissionDenied",
    "PersistenceError",
    "ProjectionId",
    "ProposedWorldDelta",
    "RelationCreate",
    "RelationDelete",
    "RelationId",
    "RelationState",
    "ReplayError",
    "REALITY_ROOT_SEMANTICS",
    "RealityRootContract",
    "ROOT_CONSTITUTION",
    "ConstitutionManifest",
    "ConstitutionVersion",
    "constitution_from_primitive",
    "legacy_default_constitution",
    "RightsDenied",
    "RuntimeVersion",
    "RightsEnvelope",
    "RightsDecision",
    "RunId",
    "RunMetadata",
    "SchemaVersion",
    "SessionId",
    "SnapshotId",
    "SnapshotMetadata",
    "StaleRevision",
    "TraceId",
    "ValidationRejected",
    "WanxiangError",
    "WanxiangId",
    "WorldInstanceId",
    "WorldTime",
    "canonical_json",
    "semantic_sha256",
]
