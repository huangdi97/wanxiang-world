"""G93G: evolution reasons, source/event lineage, and trajectory links."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.evolution.actor_evolution import ActorEvolutionTracker
from wanxiang_substrate.evolution.delta import (
    EvolutionProvenance,
    OrganizationDelta,
    PersonaDelta,
    RelationshipDelta,
    StateDelta,
)
from wanxiang_substrate.evolution.explainability import (
    EvolutionExplainabilityProjection,
    advance_explainability_projection,
    explain_delta,
    link_actor_trajectory,
)

ALICE = EntityId("actor_alice_g93g")
BOB = EntityId("actor_bob_g93g")
PROVENANCE = EvolutionProvenance(
    origin_ref="run:g93g",
    source_refs=("memory://g93g_source",),
    event_refs=("event:g93g:root",),
    producer="runtime_projection",
)


def _persona(event_ref: str = "event:g93g:persona") -> PersonaDelta:
    return PersonaDelta(
        actor_id=ALICE,
        trait="caution",
        from_value="open",
        to_value="watchful",
        rationale="repeated observed duty",
        evidence_refs=(event_ref,),
        delta_id="persona_g93g",
        provenance=EvolutionProvenance(
            origin_ref=PROVENANCE.origin_ref,
            source_refs=PROVENANCE.source_refs,
            event_refs=(event_ref,),
            producer=PROVENANCE.producer,
        ),
    )


def test_explanation_links_reason_sources_events_and_actor_trajectory() -> None:
    delta = _persona()
    tracker = ActorEvolutionTracker(ALICE)
    state = tracker.apply_persona(delta, provenance_ref="event:g93g:persona")
    explanation = explain_delta(
        delta,
        explanation_id="explanation_g93g_persona",
        projection_ref="actor:alice:persona",
        at_ticks=7,
        trajectory_refs=("event:g93g:persona",),
    )
    link = link_actor_trajectory(state, explanation, trajectory_seq=1)
    projection = advance_explainability_projection(
        EvolutionExplainabilityProjection(), explanation, trajectory_links=(link,)
    )
    found = projection.by_delta(delta.delta_id)
    assert found is explanation
    assert found is not None
    assert found.reason == "repeated observed duty"
    assert found.source_refs == ("memory://g93g_source",)
    assert found.event_refs == ("event:g93g:persona",)
    assert found.subject_kind == "actor"
    assert found.subject_ref == ALICE.value
    assert found.delta_fingerprint == delta.fingerprint()
    assert projection.links_for(ALICE) == (link,)
    assert projection.for_projection("actor:alice:persona") == (explanation,)
    assert projection.explanations[0].to_dict()["delta_kind"] == "persona"


def test_relationship_and_organization_reasons_are_queryable() -> None:
    relationship = RelationshipDelta(
        delta_id="relationship_g93g",
        relationship_id="relationship_alice_bob_g93g",
        source_actor_id=ALICE,
        target_actor_id=BOB,
        dimension="trust",
        before=0.0,
        after=0.2,
        reason="shared watch was observed",
        provenance=PROVENANCE,
    )
    organization = OrganizationDelta(
        delta_id="organization_g93g",
        organization_id=EntityId("org_g93g"),
        lifecycle="role_changed",
        actor_id=ALICE,
        from_role="member",
        to_role="keeper",
        reason="keeper duty was reviewed",
        provenance=PROVENANCE,
    )
    projection = EvolutionExplainabilityProjection()
    relationship_explanation = explain_delta(
        relationship,
        explanation_id="explanation_g93g_relationship",
        projection_ref="relationship:alice:bob",
        at_ticks=8,
    )
    projection = advance_explainability_projection(projection, relationship_explanation)
    organization_explanation = explain_delta(
        organization,
        explanation_id="explanation_g93g_organization",
        projection_ref="organization:g93g",
        at_ticks=9,
    )
    projection = advance_explainability_projection(projection, organization_explanation)
    assert projection.for_subject(relationship.relationship_id) == (relationship_explanation,)
    assert projection.for_subject(organization.organization_id.value) == (organization_explanation,)
    assert relationship_explanation.actor_refs == (ALICE.value, BOB.value)
    assert organization_explanation.actor_refs == (ALICE.value,)
    assert organization_explanation.reason == "keeper duty was reviewed"


def test_explainability_rejects_provider_only_reason_and_bad_trajectory_link() -> None:
    provider_only = EvolutionProvenance(origin_ref="provider:opaque", producer="provider")
    delta = StateDelta(
        delta_id="state_g93g_provider_only",
        subject_id=ALICE,
        field="status",
        before="idle",
        after="active",
        reason="provider said so",
        provenance=provider_only,
    )
    with pytest.raises(ContractError, match="source or event provenance"):
        explain_delta(
            delta,
            explanation_id="explanation_provider_only",
            projection_ref="actor:alice:state",
            at_ticks=1,
        )
    tracker = ActorEvolutionTracker(ALICE)
    persona = _persona()
    state = tracker.apply_persona(persona, provenance_ref="event:g93g:persona")
    explanation = explain_delta(
        persona,
        explanation_id="explanation_bad_link",
        projection_ref="actor:alice:persona",
        at_ticks=1,
        trajectory_refs=("event:g93g:other",),
    )
    with pytest.raises(ContractError, match="explicit explanation provenance"):
        link_actor_trajectory(state, explanation, trajectory_seq=1)
