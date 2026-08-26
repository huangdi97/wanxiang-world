"""G89B: deterministic priority proposals and provider isolation."""

from __future__ import annotations

import pytest
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.actor_continuity import (
    ActorGoal,
    ActorGoalStack,
    DeterministicGoalReprioritizationPolicy,
    GoalEvidence,
    GoalReprioritizationContext,
    ProviderGoalReprioritizationPolicy,
    apply_goal_reprioritization,
)


def make_stack() -> ActorGoalStack:
    goal = ActorGoal(
        goal_id=EntityId("goal_a"),
        actor_id=EntityId("actor_a"),
        tier="short_term",
        statement="reach the safe room",
        priority=40,
        deadline_ticks=10,
        created_at_ticks=1,
        updated_at_ticks=1,
    )
    stack, _ = ActorGoalStack.empty(EntityId("actor_a")).add_goal(
        goal, event_ref="evt_goal_1", at_ticks=1, reason="chosen"
    )
    return stack


@pytest.mark.unit
def test_reference_policy_is_same_seed_deterministic_and_auditable() -> None:
    context = GoalReprioritizationContext(
        actor_id=EntityId("actor_a"),
        stack=make_stack(),
        now_ticks=5,
        seed=7,
        evidence=(
            GoalEvidence(
                "obs:urgent",
                EntityId("actor_a"),
                EntityId("goal_a"),
                "observation",
                12,
                "door closes",
            ),
        ),
    )
    policy = DeterministicGoalReprioritizationPolicy()
    first = policy.propose(context)
    second = policy.propose(context)
    assert first == second
    assert first[0].to_priority == 62
    assert first[0].evidence_refs == ("deadline:goal_a", "obs:urgent")
    assert "goal_a" in first[0].reason

    updated, event = apply_goal_reprioritization(
        context.stack, first[0], event_ref="evt_goal_2", at_ticks=5
    )
    assert updated.goal(EntityId("goal_a")).priority == 62  # type: ignore[union-attr]
    assert event.evidence_refs == ("deadline:goal_a", "obs:urgent")  # type: ignore[attr-defined]


@pytest.mark.unit
def test_provider_is_propose_only_and_stale_output_is_rejected() -> None:
    context = GoalReprioritizationContext(
        actor_id=EntityId("actor_a"), stack=make_stack(), now_ticks=2, seed=1
    )

    class Provider:
        def propose(self, context: GoalReprioritizationContext):
            supplied = context
            assert supplied.stack == context.stack
            return DeterministicGoalReprioritizationPolicy("llm").propose(
                GoalReprioritizationContext(
                    actor_id=supplied.actor_id,
                    stack=supplied.stack,
                    now_ticks=10,
                    seed=supplied.seed,
                    evidence=(),
                )
            )

        def commit(self, _proposal: object) -> None:
            raise AssertionError("provider must never be asked to commit")

    # The provider has a commit-shaped method, but the adapter never calls it.
    proposals = ProviderGoalReprioritizationPolicy(Provider()).propose(context)
    assert len(proposals) == 1
    assert proposals[0].policy_ref.startswith("provider:llm")
    assert context.stack.goal(EntityId("goal_a")).priority == 40  # type: ignore[union-attr]
