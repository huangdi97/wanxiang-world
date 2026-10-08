"""G89A: actor goal stack contracts and deterministic replay."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.actor_continuity import (
    ActorGoal,
    ActorGoalStack,
    GoalProvenance,
)


def goal(goal_id: str, actor: str = "actor_a", *, tier: str = "long_term") -> ActorGoal:
    return ActorGoal(
        goal_id=EntityId(goal_id),
        actor_id=EntityId(actor),
        tier=tier,  # type: ignore[arg-type]
        statement=f"work toward {goal_id}",
        priority=60,
        provenance=GoalProvenance("observation", (f"obs:{goal_id}",), "actor noticed a need"),
        created_at_ticks=1,
        updated_at_ticks=1,
    )


@pytest.mark.unit
def test_goal_stack_serializes_five_tiers_and_dependencies() -> None:
    stack = ActorGoalStack.empty(EntityId("actor_a"))
    stack, created = stack.add_goal(
        goal("goal_root", tier="life_motive"), event_ref="evt_goal_1", at_ticks=1, reason="chosen"
    )
    dependent = ActorGoal(
        goal_id=EntityId("goal_child"),
        actor_id=EntityId("actor_a"),
        tier="intent",
        statement="take the next safe step",
        priority=80,
        dependencies=(EntityId("goal_root"),),
        provenance=GoalProvenance("belief", ("belief:1",), "current belief"),
        created_at_ticks=2,
        updated_at_ticks=2,
    )
    stack, second = stack.add_goal(dependent, event_ref="evt_goal_2", at_ticks=2, reason="planned")
    encoded = stack.serialize()
    restored = ActorGoalStack.deserialize(encoded)
    assert restored == stack
    assert ActorGoalStack.replay(EntityId("actor_a"), (created, second)) == stack
    assert restored.ready() == (restored.goal(EntityId("goal_root")),)
    assert "canonical" not in encoded
    assert "world_fact" not in encoded


@pytest.mark.unit
def test_goal_revision_has_provenance_and_is_not_a_world_fact() -> None:
    stack, _ = ActorGoalStack.empty(EntityId("actor_a")).add_goal(
        goal("goal_1"), event_ref="evt_goal_1", at_ticks=1, reason="chosen"
    )
    changed, event = stack.reprioritize(
        EntityId("goal_1"),
        90,
        event_ref="evt_goal_2",
        at_ticks=3,
        reason="new observation changed urgency",
        evidence_refs=("obs:2",),
    )
    assert event.kind == "reprioritized"
    assert event.before is not None and event.before.priority == 60
    assert changed.goal(EntityId("goal_1")).priority == 90  # type: ignore[union-attr]
    assert changed.revisions[1].evidence_refs == ("obs:2",)
    with pytest.raises(ContractError):
        changed.apply(event)
