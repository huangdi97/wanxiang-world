"""Deterministic and provider-backed goal reprioritization policies."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace
from typing import Protocol

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.actor_continuity.goal_model import GoalRevisionEvent
from wanxiang_substrate.actor_continuity.goal_stack import ActorGoalStack
from wanxiang_substrate.actor_continuity.reprioritization_model import (
    GoalEvidence,
    GoalReprioritizationContext,
    GoalReprioritizationProposal,
)


class GoalReprioritizationPolicy(Protocol):
    """A read-only policy that can only return proposed priority changes."""

    def propose(
        self, context: GoalReprioritizationContext
    ) -> tuple[GoalReprioritizationProposal, ...]: ...


class DeterministicGoalReprioritizationPolicy:
    """Reference policy: deadline and evidence changes are stable and bounded."""

    def __init__(self, ref: str = "reference-v1") -> None:
        if not ref.strip():
            raise ContractError("deterministic policy ref cannot be blank")
        self._ref = ref

    def propose(
        self, context: GoalReprioritizationContext
    ) -> tuple[GoalReprioritizationProposal, ...]:
        evidence_by_goal: dict[str, list[GoalEvidence]] = {}
        for item in sorted(context.evidence, key=lambda item: item.evidence_ref):
            evidence_by_goal.setdefault(item.goal_id.value, []).append(item)
        proposals: list[GoalReprioritizationProposal] = []
        for goal in context.stack.ordered():
            if goal.status != "active":
                continue
            evidence = evidence_by_goal.get(goal.goal_id.value, [])
            delta = sum(item.impact for item in evidence)
            refs = [item.evidence_ref for item in evidence]
            if goal.deadline_ticks is not None:
                remaining = goal.deadline_ticks - context.now_ticks
                if remaining <= 0:
                    delta += 25
                    refs.append(f"deadline:{goal.goal_id.value}")
                elif remaining <= 10:
                    delta += 10
                    refs.append(f"deadline:{goal.goal_id.value}")
            delta = max(-50, min(50, delta))
            target = max(0, min(100, goal.priority + delta))
            if target == goal.priority:
                continue
            proposals.append(
                GoalReprioritizationProposal(
                    proposal_ref=(
                        f"goal-priority:{context.seed}:{context.stack.revision}:"
                        f"{goal.goal_id.value}"
                    ),
                    actor_id=context.actor_id,
                    goal_id=goal.goal_id,
                    base_revision=context.stack.revision,
                    from_priority=goal.priority,
                    to_priority=target,
                    policy_ref=f"{self._ref}:seed={context.seed}",
                    reason=f"bounded deterministic evidence update for {goal.goal_id.value}",
                    evidence_refs=tuple(sorted(set(refs))),
                )
            )
        return tuple(proposals)


class GoalProposalProvider(Protocol):
    """Untrusted provider port; it has no stack or commit mutation method."""

    def propose(
        self, context: GoalReprioritizationContext
    ) -> Iterable[GoalReprioritizationProposal]: ...


class ProviderGoalReprioritizationPolicy:
    """Validate provider proposals and return them without applying them."""

    def __init__(self, provider: GoalProposalProvider, ref: str = "provider") -> None:
        if not ref.strip():
            raise ContractError("provider policy ref cannot be blank")
        self._provider = provider
        self._ref = ref

    def propose(
        self, context: GoalReprioritizationContext
    ) -> tuple[GoalReprioritizationProposal, ...]:
        raw = tuple(self._provider.propose(context))
        checked: list[GoalReprioritizationProposal] = []
        seen: set[str] = set()
        for proposal in raw:
            if proposal.proposal_ref in seen:
                raise ContractError("provider returned duplicate proposal refs")
            seen.add(proposal.proposal_ref)
            goal = context.stack.goal(proposal.goal_id)
            if proposal.actor_id != context.actor_id or goal is None:
                raise ContractError("provider proposal targets an unknown actor or goal")
            if proposal.base_revision != context.stack.revision:
                raise ContractError("provider proposal is based on a stale goal stack")
            if proposal.from_priority != goal.priority:
                raise ContractError("provider proposal has a stale source priority")
            checked.append(replace(proposal, policy_ref=f"{self._ref}:{proposal.policy_ref}"))
        return tuple(sorted(checked, key=lambda item: item.proposal_ref))


def apply_goal_reprioritization(
    stack: ActorGoalStack,
    proposal: GoalReprioritizationProposal,
    *,
    event_ref: str,
    at_ticks: int,
) -> tuple[ActorGoalStack, GoalRevisionEvent]:
    """Apply one checked proposal to the actor projection only."""
    if proposal.actor_id != stack.actor_id or proposal.base_revision != stack.revision:
        raise ContractError("goal proposal is stale or targets a different actor")
    goal = stack.goal(proposal.goal_id)
    if goal is None or goal.priority != proposal.from_priority:
        raise ContractError("goal proposal source priority does not match stack")
    return stack.reprioritize(
        proposal.goal_id,
        proposal.to_priority,
        event_ref=event_ref,
        at_ticks=at_ticks,
        reason=proposal.reason,
        evidence_refs=proposal.evidence_refs,
    )
