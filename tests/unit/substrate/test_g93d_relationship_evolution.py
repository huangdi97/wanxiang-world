"""G93D: relationship rules, clamps, provider proposals, and replay history."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.actor_continuity.relationship_graph import RelationshipGraph
from wanxiang_substrate.actor_continuity.relationship_model import (
    RelationshipDimensions,
    RelationshipState,
)
from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.relationship_evolution import (
    RelationshipDeltaRule,
    RelationshipEvolutionEvent,
    RelationshipProviderProposal,
    apply_relationship_proposal,
    propose_relationship_evolution,
    relationship_behavior_feedback,
)

SOURCE = EntityId("actor_source")
TARGET = EntityId("actor_target")
PROVENANCE = EvolutionProvenance(
    origin_ref="run:g93d",
    source_refs=("source:g93d",),
    event_refs=("event:g93d:seed",),
    producer="runtime_projection",
)


def _state() -> RelationshipState:
    return RelationshipState(
        relationship_id="relation_g93d",
        source_actor_id=SOURCE,
        target_actor_id=TARGET,
        relation_type="co-worker",
        dimensions=RelationshipDimensions(trust=0.0, hostility=0.0),
        valid_from=0,
        event_refs=("event:g93d:seed",),
    )


def _event() -> RelationshipEvolutionEvent:
    return RelationshipEvolutionEvent(
        event_ref="event:g93d:aid",
        relationship_id="relation_g93d",
        source_actor_id=SOURCE,
        target_actor_id=TARGET,
        signal="shared_aid",
        strength=1.0,
        at_ticks=10,
        evidence_refs=("observation:g93d:aid",),
    )


def _proposal():
    return propose_relationship_evolution(
        proposal_id="aid_10",
        state=_state(),
        event=_event(),
        rules=(RelationshipDeltaRule("shared_aid", "trust", 1.0, maximum_step=0.2),),
        provenance=PROVENANCE,
    )


def test_event_rule_produces_clamped_typed_delta_and_future_feedback() -> None:
    proposal = _proposal()
    assert proposal.delta.kind == "relationship"
    assert proposal.delta.before == 0.0
    assert proposal.delta.after == 0.2
    assert proposal.after.dimensions.trust == 0.2
    feedback = relationship_behavior_feedback(proposal.after, at_ticks=10)
    assert feedback.cooperation_bias > 0.0
    assert feedback.avoidance_bias == 0.0
    assert "event:g93d:aid" in feedback.source_refs


def test_provider_output_is_proposal_only_and_commit_authority_is_rejected() -> None:
    proposal = _proposal()
    provider = RelationshipProviderProposal(
        "provider:local", replace(proposal, provider_ref="provider:local")
    )
    assert provider.proposal.approved is False
    with pytest.raises(PermissionDenied, match="cannot produce"):
        RelationshipProviderProposal("commit_authority", proposal)
    with pytest.raises(PermissionDenied, match="requires explicit review"):
        apply_relationship_proposal(RelationshipGraph(), proposal)


def test_approved_relationship_history_replays_equal() -> None:
    state = _state()
    graph, initial = RelationshipGraph().add(
        state, event_ref="event:g93d:seed", at_ticks=0, reason="initial relation"
    )
    proposal = replace(_proposal(), approved=True)
    updated, revision = apply_relationship_proposal(graph, proposal)
    assert revision.before == state
    replayed = RelationshipGraph.replay(updated.revisions)
    assert replayed == updated
    assert updated.state("relation_g93d", at_ticks=10) == proposal.after
    assert len(updated.revisions) == 2
    assert initial.after == state


def test_stale_or_ambiguous_rules_are_rejected() -> None:
    proposal = _proposal()
    with pytest.raises(ContractError, match="stale"):
        apply_relationship_proposal(
            RelationshipGraph(states=(replace(proposal.before, valid_from=1),)),
            replace(proposal, approved=True),
        )
    with pytest.raises(ContractError, match="exactly one"):
        propose_relationship_evolution(
            proposal_id="ambiguous",
            state=_state(),
            event=_event(),
            rules=(
                RelationshipDeltaRule("shared_aid", "trust", 0.5),
                RelationshipDeltaRule("shared_aid", "affection", 0.5),
            ),
            provenance=PROVENANCE,
        )
