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
    "DEFAULT_WORLDNESS_MAPPING",
    "VALIDATION_LEVELS",
    "VALIDATION_SCHEMA_VERSION",
    "ValidationCheck",
    "ValidationLevel",
    "ValidationProfile",
    "ValidationReport",
    "ValidationStack",
    "ValidationStatus",
]
