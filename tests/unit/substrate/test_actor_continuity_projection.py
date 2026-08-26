"""G89G: actor-only cognition and observer-safe continuity timeline."""

from __future__ import annotations

import pytest
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.actor_continuity import (
    ActionExplanation,
    ActorContinuityProjection,
    ActorGoal,
    ActorGoalStack,
    GoalProvenance,
    RelationshipDimensions,
    RelationshipGraph,
    RelationshipState,
)
from wanxiang_substrate.epistemic import BeliefAssertion, MemoryRecord


def inputs() -> tuple[
    ActorGoalStack,
    tuple[MemoryRecord, ...],
    tuple[BeliefAssertion, ...],
    RelationshipGraph,
    tuple[ActionExplanation, ...],
]:
    goal = ActorGoal(
        EntityId("goal_a"),
        EntityId("actor_a"),
        "short_term",
        "protect the letter",
        80,
        provenance=GoalProvenance("memory", ("memory_a",), "remembered threat"),
        created_at_ticks=1,
        updated_at_ticks=2,
    )
    stack, _ = ActorGoalStack.empty(EntityId("actor_a")).add_goal(
        goal, event_ref="goal:event", at_ticks=1, reason="chosen"
    )
    memory = MemoryRecord(
        EntityId("memory_a"), EntityId("actor_a"), "observation", "memory://private", 2
    )
    belief = BeliefAssertion(
        EntityId("belief_a"),
        EntityId("actor_a"),
        "the guard watches",
        0.8,
        3,
        source_ref="memory_a",
    )
    public, _ = RelationshipGraph().add(
        RelationshipState(
            "rel_public",
            EntityId("actor_a"),
            EntityId("observer"),
            "ally",
            RelationshipDimensions(trust=0.4),
            1,
            visibility="public",
        ),
        event_ref="rel:event",
        at_ticks=1,
        reason="public relation",
    )
    action = ActionExplanation(
        "action_a",
        EntityId("actor_a"),
        4,
        "moved the letter",
        goal_refs=("goal_a",),
        memory_refs=("memory_a",),
        public=True,
    )
    return stack, (memory,), (belief,), public, (action,)


@pytest.mark.unit
def test_actor_projection_contains_cognition_and_why_refs() -> None:
    stack, memories, beliefs, relations, actions = inputs()
    snapshot = ActorContinuityProjection().compose(
        viewer_actor_id=EntityId("actor_a"),
        target_actor_id=EntityId("actor_a"),
        at_ticks=5,
        goals=stack,
        memories=memories,
        beliefs=beliefs,
        relationships=relations,
        actions=actions,
    )
    categories = {item.category for item in snapshot.timeline()}
    assert {"goal", "memory", "belief", "relationship", "action"} <= categories
    action = next(item for item in snapshot.timeline() if item.category == "action")
    assert action.why_refs == ("goal_a", "memory_a")
    assert snapshot.redacted_categories == ()


@pytest.mark.unit
def test_observer_projection_redacts_private_cognition() -> None:
    stack, memories, beliefs, relations, actions = inputs()
    snapshot = ActorContinuityProjection().compose(
        viewer_actor_id=EntityId("observer"),
        target_actor_id=EntityId("actor_a"),
        at_ticks=5,
        goals=stack,
        memories=memories,
        beliefs=beliefs,
        relationships=relations,
        actions=actions,
    )
    assert snapshot.redacted_categories == ("goal", "memory", "belief")
    assert not any(item.category in {"goal", "memory", "belief"} for item in snapshot.timeline())
    assert all("private" not in item.summary for item in snapshot.timeline())
    assert any(item.category == "relationship" for item in snapshot.timeline())
    public_action = next(item for item in snapshot.timeline() if item.category == "action")
    assert public_action.why_refs == ()
