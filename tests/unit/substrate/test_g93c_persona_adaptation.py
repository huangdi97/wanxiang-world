"""G93C: slow-variable, windowed, review-gated persona adaptation."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.persona_adaptation import (
    PersonaAdaptationPolicy,
    PersonaObservation,
    PersonaTraitState,
    propose_persona_adaptation,
    review_persona_adaptation,
)

ACTOR = EntityId("actor_persona")
PROVENANCE = EvolutionProvenance(
    origin_ref="run:g93c",
    source_refs=("source:g93c",),
    event_refs=("event:g93c:seed",),
    producer="runtime_projection",
)


def _observations() -> tuple[PersonaObservation, ...]:
    return tuple(
        PersonaObservation(
            observation_id=f"persona_obs_{index}",
            actor_id=ACTOR,
            trait="caution",
            direction="increase",
            strength=0.8,
            at_ticks=tick,
            event_ref=f"event:g93c:{index}",
        )
        for index, tick in enumerate((5, 15, 25), start=1)
    )


def _proposal():
    return propose_persona_adaptation(
        proposal_id="caution_window",
        current=PersonaTraitState(ACTOR, "caution", value=0.0),
        observations=_observations(),
        now_ticks=30,
        provenance=PROVENANCE,
        policy=PersonaAdaptationPolicy(window_ticks=30, minimum_span_ticks=10),
    )


def test_long_window_produces_bounded_single_trait_persona_delta() -> None:
    proposal = _proposal()
    assert proposal.trait == "caution"
    assert proposal.review_required is True
    assert proposal.status == "review"
    assert 0.0 < proposal.after <= 0.1
    assert abs(proposal.after - proposal.before) <= 0.1
    assert len(proposal.evidence_refs) == 3
    assert proposal.persona_delta.to_value == f"{proposal.after:.6f}"


def test_one_event_cannot_rewrite_full_persona() -> None:
    with pytest.raises(ContractError, match="multi-event"):
        propose_persona_adaptation(
            proposal_id="one_event",
            current=PersonaTraitState(ACTOR, "caution", value=-1.0),
            observations=(_observations()[0],),
            now_ticks=5,
            provenance=PROVENANCE,
        )


def test_short_window_and_neutral_evidence_are_rejected() -> None:
    observations = tuple(
        PersonaObservation(
            f"short_{index}", ACTOR, "resolve", "increase", 1.0, tick, f"event:short:{index}"
        )
        for index, tick in enumerate((10, 11, 12), start=1)
    )
    with pytest.raises(ContractError, match="too short"):
        propose_persona_adaptation(
            proposal_id="short_window",
            current=PersonaTraitState(ACTOR, "resolve"),
            observations=observations,
            now_ticks=12,
            provenance=PROVENANCE,
        )


def test_review_is_explicit_immutable_and_policy_bound() -> None:
    proposal = _proposal()
    approved = review_persona_adaptation(proposal, reviewer="reviewer", approved=True)
    assert approved.status == "approved"
    assert approved.review_required is False
    assert proposal.status == "review"
    with pytest.raises(PermissionDenied, match="not authorized"):
        review_persona_adaptation(proposal, reviewer="provider", approved=True)
