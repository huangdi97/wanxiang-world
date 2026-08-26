"""Actor continuity projections: goals, cognition and relationships."""

from wanxiang_substrate.actor_continuity.goal_model import (
    ActorGoal,
    ActorGoalStatus,
    GoalProvenance,
    GoalRevisionEvent,
    GoalRevisionKind,
    GoalTier,
    Intent,
    LifeMotive,
    LongTermGoal,
    MediumTermGoal,
    ShortTermGoal,
)
from wanxiang_substrate.actor_continuity.goal_stack import ActorGoalStack
from wanxiang_substrate.actor_continuity.passport_model import (
    CharacterPassport,
    InterworldCompatibility,
    PassportDecision,
    PassportEntry,
    PassportPortability,
    PassportTranslationContext,
    PassportTranslationProposal,
)
from wanxiang_substrate.actor_continuity.passport_policy import (
    DeterministicPassportTranslationPolicy,
    PassportTranslationPolicy,
)
from wanxiang_substrate.actor_continuity.projection import (
    ActionExplanation,
    ActorContinuityProjection,
    ActorContinuitySnapshot,
    ContinuityTimelineItem,
)
from wanxiang_substrate.actor_continuity.qualification_model import (
    ContinuityActorBundle,
    ContinuityCheckpoint,
    ContinuityQualificationResult,
)
from wanxiang_substrate.actor_continuity.qualification_run import (
    ContinuityQualificationSeed,
    SevenDayContinuityQualification,
)
from wanxiang_substrate.actor_continuity.relationship_graph import (
    RelationshipGraph,
    RelationshipRevisionEvent,
)
from wanxiang_substrate.actor_continuity.relationship_model import (
    Relationship,
    RelationshipDimensions,
    RelationshipState,
    RelationshipVisibility,
)
from wanxiang_substrate.actor_continuity.reprioritization_model import (
    GoalEvidence,
    GoalPriorityProposal,
    GoalReprioritizationContext,
    GoalReprioritizationProposal,
)
from wanxiang_substrate.actor_continuity.reprioritization_policy import (
    DeterministicGoalReprioritizationPolicy,
    GoalProposalProvider,
    GoalReprioritizationPolicy,
    ProviderGoalReprioritizationPolicy,
    apply_goal_reprioritization,
)

__all__ = [
    "ActorGoal",
    "ActorGoalStack",
    "ActorGoalStatus",
    "GoalProvenance",
    "GoalEvidence",
    "GoalPriorityProposal",
    "GoalProposalProvider",
    "GoalReprioritizationContext",
    "GoalRevisionEvent",
    "GoalRevisionKind",
    "GoalReprioritizationPolicy",
    "GoalReprioritizationProposal",
    "GoalTier",
    "Intent",
    "LifeMotive",
    "LongTermGoal",
    "MediumTermGoal",
    "ShortTermGoal",
    "DeterministicGoalReprioritizationPolicy",
    "CharacterPassport",
    "ActionExplanation",
    "ActorContinuityProjection",
    "ActorContinuitySnapshot",
    "ContinuityTimelineItem",
    "ContinuityActorBundle",
    "ContinuityCheckpoint",
    "ContinuityQualificationResult",
    "ContinuityQualificationSeed",
    "SevenDayContinuityQualification",
    "DeterministicPassportTranslationPolicy",
    "InterworldCompatibility",
    "PassportDecision",
    "PassportEntry",
    "PassportPortability",
    "PassportTranslationContext",
    "PassportTranslationPolicy",
    "PassportTranslationProposal",
    "ProviderGoalReprioritizationPolicy",
    "Relationship",
    "RelationshipDimensions",
    "RelationshipGraph",
    "RelationshipRevisionEvent",
    "RelationshipState",
    "RelationshipVisibility",
    "apply_goal_reprioritization",
]
