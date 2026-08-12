"""G03C: agency value-object invariants + policy contract."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.agency.model import IntentCandidate, Order
from wanxiang_substrate.agency.policy import DeterministicPolicy, RulePolicy


@pytest.mark.unit
def test_order_lifecycle_transitions() -> None:
    order = Order(EntityId("o"), EntityId("i"), EntityId("r"), "move", {"to": "hall"})
    assert order.can_transition_to("received") is True
    received = Order(EntityId("o"), EntityId("i"), EntityId("r"), "move", {}, state="received")
    assert received.can_transition_to("accepted") is True
    assert received.can_transition_to("rejected") is True
    assert received.can_transition_to("executed") is False
    executed = Order(EntityId("o"), EntityId("i"), EntityId("r"), "move", {}, state="executed")
    assert executed.can_transition_to("reported") is True
    reported = Order(EntityId("o"), EntityId("i"), EntityId("r"), "move", {}, state="reported")
    assert reported.can_transition_to("executed") is False


@pytest.mark.unit
def test_order_validation() -> None:
    with pytest.raises(ContractError):
        Order(EntityId("o"), EntityId("i"), EntityId("r"), "", {})
    with pytest.raises(ContractError):
        Order(EntityId("o"), EntityId("i"), EntityId("r"), "move", {}, state="bogus")  # type: ignore[arg-type]


@pytest.mark.unit
def test_policies_return_intent_candidate_only() -> None:
    context = type(
        "Ctx", (), {"actor_id": EntityId("a"), "observations": (object(),), "beliefs": ()}
    )()
    for policy in (
        DeterministicPolicy("body.rest", {"ticks": 5}),
        RulePolicy("body.rest", "has_obs"),
    ):
        candidate = policy.propose(context)  # type: ignore[arg-type]
        assert candidate is None or isinstance(candidate, IntentCandidate)
    assert DeterministicPolicy("body.rest").propose(context).action_type == "body.rest"  # type: ignore[union-attr]


@pytest.mark.unit
def test_rule_policy_needs_observation() -> None:
    empty = type("Ctx", (), {"actor_id": EntityId("a"), "observations": (), "beliefs": ()})()
    rule = RulePolicy("body.rest", "has_obs")
    assert rule.propose(empty) is None  # type: ignore[arg-type]
