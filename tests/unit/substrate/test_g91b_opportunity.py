"""G91B: opportunities are optional, bounded world proposals."""

from __future__ import annotations

import pytest
from wanxiang_substrate.reality.challenge import Opportunity, OpportunityLifecycle
from wanxiang_substrate.reality.errors import ChallengeValidationError


def _opportunity() -> Opportunity:
    return Opportunity(
        opportunity_id="opp_supply",
        kind="resource",
        condition="market_open",
        score=0.8,
        at_ticks=2,
        eligibility=("actor:alice", "market_open"),
        available_from=2,
        expires_at=12,
        reward_refs=("reward:trust",),
        risk_refs=("risk:reputation",),
        evidence_refs=("event:supply_delivered",),
        world_state_refs=("state:market",),
    )


def test_lifecycle_checks_actor_and_world_state_refs() -> None:
    lifecycle = OpportunityLifecycle()
    with pytest.raises(ChallengeValidationError):
        lifecycle.mark_eligible(
            _opportunity(), actor_id="bob", world_state_refs=("market_open",), at_ticks=2
        )
    eligible = lifecycle.mark_eligible(
        _opportunity(), actor_id="alice", world_state_refs=("market_open",), at_ticks=2
    )
    assert eligible.status == "eligible"
    offered = lifecycle.offer(eligible, at_ticks=3)
    assert offered.status == "offered"
    assert offered.actor_id == "alice"


def test_actor_can_ignore_without_goal_or_world_mutation() -> None:
    lifecycle = OpportunityLifecycle()
    offered = lifecycle.offer(
        lifecycle.mark_eligible(
            _opportunity(), actor_id="alice", world_state_refs=("market_open",), at_ticks=2
        ),
        at_ticks=3,
    )
    ignored = lifecycle.ignore(offered, decision_ref="decision:alice:ignored")
    assert ignored.status == "ignored"
    assert ignored.decision_ref == "decision:alice:ignored"
    assert ignored.reward_refs == offered.reward_refs
    assert ignored.risk_refs == offered.risk_refs
    assert not hasattr(lifecycle, "commit")
    assert not hasattr(ignored, "goal")


def test_accept_complete_and_expire_require_explicit_evidence() -> None:
    lifecycle = OpportunityLifecycle()
    offered = lifecycle.offer(
        lifecycle.mark_eligible(
            _opportunity(), actor_id="alice", world_state_refs=("market_open",), at_ticks=2
        ),
        at_ticks=3,
    )
    accepted = lifecycle.accept(offered, at_ticks=4)
    with pytest.raises(ChallengeValidationError):
        lifecycle.complete(accepted, evidence_refs=(), at_ticks=5)
    completed = lifecycle.complete(accepted, evidence_refs=("event:supply_delivered",), at_ticks=5)
    assert completed.status == "completed"
    assert completed.to_dict()["world_state_refs"] == ["state:market"]

    expired = lifecycle.expire(offered, at_ticks=12)
    assert expired.status == "expired"
