"""Evolution substrate (M29)."""

# Re-exported names are listed in the dedicated public catalog.
# ruff: noqa: F401
# pyright: reportUnusedImport=false, reportUnsupportedDunderAll=false

from wanxiang_substrate.evolution._public import __all__
from wanxiang_substrate.evolution.actor_evolution import (
    ActorEvolutionState,
    ActorEvolutionTracker,
    PersonaDelta,
    TrajectoryEntry,
)
from wanxiang_substrate.evolution.capability_growth import (
    CapabilityCandidate,
    CapabilityPrerequisite,
    CapabilityPromotionProposal,
    CapabilityValidation,
    create_capability_candidate,
    promote_capability_candidate,
    validate_capability_candidate,
)
from wanxiang_substrate.evolution.cross_world import (
    CrossWorldCandidate,
    CrossWorldDistiller,
)
from wanxiang_substrate.evolution.delta import (
    EVOLUTION_DELTA_SCHEMA_VERSION,
    BeliefDelta,
    CapabilityEvolutionDelta,
    EvolutionCommitPolicy,
    EvolutionCommitReceipt,
    EvolutionDelta,
    EvolutionDeltaKind,
    EvolutionOrigin,
    EvolutionProvenance,
    OrganizationDelta,
    RelationshipDelta,
    StateDelta,
)
from wanxiang_substrate.evolution.distillation import (
    BehaviorRecord,
    CandidateEnvelope,
    SocialPatternDistiller,
)
from wanxiang_substrate.evolution.explainability import (
    EvolutionExplainabilityProjection,
    EvolutionExplanation,
    ExplainableSubjectKind,
    TrajectoryExplanationLink,
    advance_explainability_projection,
    explain_delta,
    link_actor_trajectory,
)
from wanxiang_substrate.evolution.habit_candidate import (
    SkillCandidate,
    create_habit_candidate,
    create_skill_candidate,
    decay_habit_candidate,
    evaluate_habit_candidate,
)
from wanxiang_substrate.evolution.habit_candidate_model import (
    HabitCandidate,
    HabitEvaluation,
    HabitKind,
    HabitPromotionPolicy,
)
from wanxiang_substrate.evolution.institution_candidate import (
    create_institution_candidate,
    review_institution_candidate,
)
from wanxiang_substrate.evolution.institution_promotion import (
    MIN_STABILITY,
    InstitutionCandidate,
    InstitutionPromotionChain,
)
from wanxiang_substrate.evolution.norm_candidate import (
    create_norm_candidate,
    evaluate_norm_candidate,
)
from wanxiang_substrate.evolution.norm_candidate_model import (
    NormCandidate,
    NormEvaluation,
    NormOutcomeEvidence,
    NormPromotionPolicy,
    NormScope,
)
from wanxiang_substrate.evolution.ontology_candidate import (
    OntologyCandidatePolicy,
    create_ontology_candidate,
    review_ontology_candidate,
)
from wanxiang_substrate.evolution.ontology_law import (
    LawCandidate,
    OntologyCandidate,
    OntologyLawEvolution,
)
from wanxiang_substrate.evolution.organization_lifecycle import (
    AUTHORITY_PERMISSIONS,
    DEFAULT_AUTHORITY_POLICY,
    ORGANIZATION_ACTIONS,
    OrganizationAction,
    OrganizationAuthorityPolicy,
    OrganizationLifecycleEvent,
    OrganizationLifecycleProjection,
    OrganizationLifecycleProposal,
    OrganizationLifecycleState,
    OrganizationResource,
    OrganizationState,
    OrganizationStatus,
    apply_organization_proposal,
    create_organization_proposal,
    empty_organization,
    organization_state_from_canonical,
    propose_dissolve,
    propose_join,
    propose_leave,
    propose_permission_grant,
    propose_permission_revoke,
    propose_role_change,
    propose_split,
    review_organization_proposal,
    split_child_projection,
)
from wanxiang_substrate.evolution.pattern_detector import (
    RepeatedPatternDetector,
    detect_repeated_patterns,
)
from wanxiang_substrate.evolution.pattern_detector_model import (
    PatternCounterexample,
    PatternDetection,
    RepeatedPatternPolicy,
)
from wanxiang_substrate.evolution.pattern_observation import (
    PatternKind,
    PatternObservation,
    PatternObservationStore,
    PatternStatistics,
)
from wanxiang_substrate.evolution.persona_adaptation import (
    PERSONA_TRAITS,
    PersonaAdaptationPolicy,
    PersonaAdaptationProposal,
    PersonaObservation,
    PersonaTraitState,
    propose_persona_adaptation,
    review_persona_adaptation,
)
from wanxiang_substrate.evolution.platform_feedback import (
    PlatformFeedbackLab,
    SandboxReport,
    VersionedRelease,
)
from wanxiang_substrate.evolution.policy_stack import (
    EvolutionPolicyStack,
    PlatformPolicy,
    WorldPolicy,
    reject_world_platform_mutation,
)
from wanxiang_substrate.evolution.promotion import (
    APPROVAL_LEVELS,
    PROMOTION_LEVELS,
    LevelRequirement,
    PromotionEvidence,
    PromotionLevel,
    PromotionPolicy,
    validate_promotion,
)
from wanxiang_substrate.evolution.qualification import (
    EvolutionProjectionSnapshot,
    EvolutionRunComparison,
    compare_evolution,
)
from wanxiang_substrate.evolution.relationship_evolution import (
    RELATIONSHIP_DIMENSIONS,
    RelationshipBehaviorFeedback,
    RelationshipDeltaRule,
    RelationshipEvolutionEvent,
    RelationshipEvolutionProposal,
    RelationshipProviderProposal,
    apply_relationship_proposal,
    propose_relationship_evolution,
    relationship_behavior_feedback,
)
from wanxiang_substrate.evolution.reputation import (
    REPUTATION_EVIDENCE_KINDS,
    REPUTATION_SCOPES,
    REPUTATION_SIGNALS,
    SOCIAL_ROLE_REVIEWERS,
    ReputationEvent,
    ReputationEvidenceKind,
    ReputationPolicy,
    ReputationProjection,
    ReputationScope,
    ReputationSignal,
    ReputationState,
    ReputationUpdateProposal,
    SocialRole,
    SocialRoleAssignment,
    SocialRoleProjection,
    SocialRoleProposal,
    advance_reputation_projection,
    advance_social_role_projection,
    apply_reputation_proposal,
    assign_social_role,
    empty_reputation_projection,
    initial_reputation_state,
    propose_reputation_update,
    propose_social_role,
    reputation_field,
    review_reputation_proposal,
    review_social_role_proposal,
)
from wanxiang_substrate.evolution.scheduler import (
    EVOLUTION_SCALES,
    EvolutionCadence,
    EvolutionScheduler,
)
from wanxiang_substrate.evolution.telemetry import (
    CrossWorldDataset,
    TelemetryEnvelope,
    TelemetryPolicy,
)
