"""Reality bridge substrate (G07A-G07E)."""

from wanxiang_substrate.reality.bridge import (
    FakeSensorAdapter,
    ManualReportAdapter,
    ObservationAdapter,
    RealityBridge,
)
from wanxiang_substrate.reality.challenge import (
    ChallengeCompiler,
    ChallengeSpec,
    DefaultOpportunityDetector,
    Opportunity,
    OpportunityDetector,
    OpportunityLifecycle,
    OpportunityStatus,
)
from wanxiang_substrate.reality.director import (
    DIRECTOR_MODES,
    DirectorAudit,
    DirectorDecision,
    DirectorMode,
    DirectorPolicy,
    DirectorProposal,
    DirectorReview,
    DirectorTransition,
    NarrativeDirector,
    NarrativeSignal,
    PerformanceDirector,
    WorldDirector,
)
from wanxiang_substrate.reality.errors import (
    ChallengeValidationError,
    DirectorError,
    ExperimentError,
    FusionPolicyError,
    InvalidObservation,
    RealityError,
)
from wanxiang_substrate.reality.experiment import (
    ExperimentRuntime,
    ExperimentSpec,
    Finding,
    RunMetric,
    ValidityEnvelope,
)
from wanxiang_substrate.reality.fusion import (
    FusionOutcome,
    FusionPolicy,
    FusionResult,
    ObservationFusion,
)
from wanxiang_substrate.reality.model import (
    NormalizedReading,
    PhysicalObservation,
)
from wanxiang_substrate.reality.pressure import (
    PRESSURE_DIMENSIONS,
    PRESSURE_PROFILE_SCHEMA_VERSION,
    PressureProfile,
)

__all__ = [
    "ChallengeCompiler",
    "ChallengeSpec",
    "ChallengeValidationError",
    "DIRECTOR_MODES",
    "DefaultOpportunityDetector",
    "DirectorAudit",
    "DirectorDecision",
    "DirectorError",
    "DirectorMode",
    "DirectorPolicy",
    "DirectorProposal",
    "DirectorReview",
    "DirectorTransition",
    "ExperimentError",
    "ExperimentRuntime",
    "ExperimentSpec",
    "FakeSensorAdapter",
    "Finding",
    "FusionOutcome",
    "FusionPolicy",
    "FusionPolicyError",
    "FusionResult",
    "InvalidObservation",
    "ManualReportAdapter",
    "NarrativeDirector",
    "NarrativeSignal",
    "NormalizedReading",
    "ObservationAdapter",
    "ObservationFusion",
    "Opportunity",
    "OpportunityDetector",
    "OpportunityLifecycle",
    "OpportunityStatus",
    "PerformanceDirector",
    "PhysicalObservation",
    "PRESSURE_DIMENSIONS",
    "PRESSURE_PROFILE_SCHEMA_VERSION",
    "PressureProfile",
    "RealityBridge",
    "RealityError",
    "RunMetric",
    "ValidityEnvelope",
    "WorldDirector",
]
