"""World laboratory evidence contracts (M92).

The laboratory is a proposal/evidence surface over the existing runtime.  It
does not own canonical state, event history, branches, or commit authority.
"""

from wanxiang_substrate.world_lab.artifact import (
    ARTIFACT_SCHEMA_VERSION,
    WorldRunArtifact,
    sanitize_metadata,
)
from wanxiang_substrate.world_lab.batch import (
    BatchExecutor,
    BatchWorldlineExecutor,
    WorldlineBatchExecutor,
)
from wanxiang_substrate.world_lab.batch_aggregate import (
    BatchAggregate,
    BatchExecution,
    MetricSummary,
    aggregate_results,
)
from wanxiang_substrate.world_lab.batch_models import (
    BATCH_SCHEMA_VERSION,
    BatchCheckpoint,
    BatchPlan,
    BatchRunResult,
)
from wanxiang_substrate.world_lab.comparator import WorldlineComparator
from wanxiang_substrate.world_lab.comparison_models import (
    COMPARISON_SCHEMA_VERSION,
    METRIC_CATEGORIES,
    CategoryComparison,
    LabWorldlineComparison,
    MetricCategory,
    MetricDifference,
    TrajectoryPoint,
    WorldlineMeasurement,
)
from wanxiang_substrate.world_lab.consistency_models import (
    REALITY_CONSISTENCY_SCHEMA_VERSION,
    RealityConsistencyResult,
    RealityConsistencyStatus,
    RealityOutputKind,
    RealityReconciliationProposal,
    ReconciliationAction,
)
from wanxiang_substrate.world_lab.external_engine import (
    EXTERNAL_ENGINE_SCHEMA_VERSION,
    BlockedExternalEngineAdapter,
    ExternalEngineAdapter,
    ExternalEngineAvailability,
    ExternalEngineCapability,
    ExternalEngineKind,
)
from wanxiang_substrate.world_lab.fork import (
    FORK_SCHEMA_VERSION,
    ForkedInterventionRun,
    ForkInterventionRunner,
    ForkProvenance,
    ForkRun,
    InterventionLedger,
    InterventionLedgerEntry,
    InterventionRun,
)
from wanxiang_substrate.world_lab.perspective_provider import PerspectiveVisualProvider
from wanxiang_substrate.world_lab.physical_models import (
    PHYSICAL_PROVIDER_SCHEMA_VERSION,
    PhysicalBody,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
    PhysicalWorldSnapshot,
    ReadonlyPhysicalSnapshot,
    SimulationRequest,
)
from wanxiang_substrate.world_lab.physical_outputs import (
    PhysicalProviderHealth,
    PhysicalProviderStatus,
    PhysicalResolution,
    PhysicalResolutionStatus,
    PhysicalSimulationResolution,
)
from wanxiang_substrate.world_lab.physical_provider import PhysicalWorldProvider
from wanxiang_substrate.world_lab.provider_evidence import MultiProviderRun, ProviderInvocation
from wanxiang_substrate.world_lab.provider_models import (
    PROVIDER_SCHEMA_VERSION,
    AssignmentMode,
    ProviderAssignment,
    ProviderAssignmentPolicy,
    ProviderRunInput,
)
from wanxiang_substrate.world_lab.provider_runner import (
    MixedPopulationProviderRunner,
    MultiProviderWorldlineRunner,
)
from wanxiang_substrate.world_lab.qualification import WorldLabQualifier
from wanxiang_substrate.world_lab.qualification_models import (
    QUALIFICATION_SCHEMA_VERSION,
    LabQualification,
    QualificationCheck,
    QualificationStatus,
)
from wanxiang_substrate.world_lab.reality_consistency import RealityConsistencyChecker
from wanxiang_substrate.world_lab.reference_physical import ReferencePhysicalProvider
from wanxiang_substrate.world_lab.reference_visual import ReferenceVisualProvider
from wanxiang_substrate.world_lab.registry import ExperimentRegistry
from wanxiang_substrate.world_lab.registry_models import (
    REGISTRY_SCHEMA_VERSION,
    ExperimentDefinition,
    ExperimentRun,
    RunStatus,
)
from wanxiang_substrate.world_lab.validation_models import (
    DEFAULT_WORLDNESS_MAPPING,
    VALIDATION_LEVELS,
    VALIDATION_SCHEMA_VERSION,
    ValidationCheck,
    ValidationLevel,
    ValidationProfile,
    ValidationReport,
    ValidationStatus,
)
from wanxiang_substrate.world_lab.validation_stack import ValidationStack
from wanxiang_substrate.world_lab.visual_models import (
    VISUAL_PROVIDER_SCHEMA_VERSION,
    ActorPerspective,
    VisualActorPerspective,
    VisualSceneObject,
    VisualSceneState,
)
from wanxiang_substrate.world_lab.visual_outputs import (
    VisualProjectedObject,
    VisualProjectionFrame,
    VisualProjectionStatus,
    VisualProviderHealth,
    VisualProviderStatus,
)
from wanxiang_substrate.world_lab.visual_provider import VisualWorldProvider

__all__ = [
    "ARTIFACT_SCHEMA_VERSION",
    "BATCH_SCHEMA_VERSION",
    "FORK_SCHEMA_VERSION",
    "ExperimentDefinition",
    "ExperimentRegistry",
    "ExperimentRun",
    "BatchAggregate",
    "BatchCheckpoint",
    "BatchExecution",
    "BatchExecutor",
    "BatchPlan",
    "BatchRunResult",
    "BatchWorldlineExecutor",
    "COMPARISON_SCHEMA_VERSION",
    "REALITY_CONSISTENCY_SCHEMA_VERSION",
    "BlockedExternalEngineAdapter",
    "EXTERNAL_ENGINE_SCHEMA_VERSION",
    "ExternalEngineAdapter",
    "ExternalEngineAvailability",
    "ExternalEngineCapability",
    "ExternalEngineKind",
    "RealityConsistencyChecker",
    "RealityConsistencyResult",
    "RealityConsistencyStatus",
    "RealityOutputKind",
    "RealityReconciliationProposal",
    "ReconciliationAction",
    "LabWorldlineComparison",
    "METRIC_CATEGORIES",
    "CategoryComparison",
    "ForkInterventionRunner",
    "ForkProvenance",
    "ForkRun",
    "ForkedInterventionRun",
    "InterventionLedger",
    "InterventionLedgerEntry",
    "InterventionRun",
    "MetricSummary",
    "MetricCategory",
    "MetricDifference",
    "REGISTRY_SCHEMA_VERSION",
    "RunStatus",
    "WorldRunArtifact",
    "WorldlineComparator",
    "WorldlineMeasurement",
    "TrajectoryPoint",
    "sanitize_metadata",
    "WorldlineBatchExecutor",
    "aggregate_results",
    "AssignmentMode",
    "MixedPopulationProviderRunner",
    "MultiProviderRun",
    "MultiProviderWorldlineRunner",
    "PROVIDER_SCHEMA_VERSION",
    "ProviderAssignment",
    "ProviderAssignmentPolicy",
    "ProviderInvocation",
    "ProviderRunInput",
    "PHYSICAL_PROVIDER_SCHEMA_VERSION",
    "PhysicalBody",
    "PhysicalProviderHealth",
    "PhysicalProviderStatus",
    "PhysicalResolution",
    "PhysicalResolutionStatus",
    "PhysicalSimulationRequest",
    "PhysicalSimulationResolution",
    "PhysicalSnapshot",
    "PhysicalWorldProvider",
    "ReferencePhysicalProvider",
    "ReferenceVisualProvider",
    "PerspectiveVisualProvider",
    "PhysicalWorldSnapshot",
    "ReadonlyPhysicalSnapshot",
    "SimulationRequest",
    "LabQualification",
    "QUALIFICATION_SCHEMA_VERSION",
    "QualificationCheck",
    "QualificationStatus",
    "WorldLabQualifier",
    "DEFAULT_WORLDNESS_MAPPING",
    "VALIDATION_LEVELS",
    "VALIDATION_SCHEMA_VERSION",
    "ValidationCheck",
    "ValidationLevel",
    "ValidationProfile",
    "ValidationReport",
    "ValidationStack",
    "ValidationStatus",
    "VISUAL_PROVIDER_SCHEMA_VERSION",
    "ActorPerspective",
    "VisualActorPerspective",
    "VisualProjectedObject",
    "VisualProjectionFrame",
    "VisualProjectionStatus",
    "VisualProviderHealth",
    "VisualProviderStatus",
    "VisualSceneObject",
    "VisualSceneState",
    "VisualWorldProvider",
]
