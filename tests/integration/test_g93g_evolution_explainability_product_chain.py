"""G93G: real product-chain event feeds queryable evolution explanations."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.actor_evolution import ActorEvolutionTracker
from wanxiang_substrate.evolution.delta import (
    EvolutionCommitPolicy,
    EvolutionProvenance,
    OrganizationDelta,
    PersonaDelta,
    RelationshipDelta,
)
from wanxiang_substrate.evolution.explainability import (
    EvolutionExplainabilityProjection,
    advance_explainability_projection,
    explain_delta,
    link_actor_trajectory,
)
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Explainability Chain\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate. Bob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: reviewed causes remain queryable\n"
    )
    return SourceRecord(
        source_id="g93g_explainability_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93g_explainability_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="qualification",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g93g",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                name = component.fields.get("display_name")
                if isinstance(name, str):
                    found[name] = entity.entity_id.value
    return found


@pytest.mark.integration
def test_explainability_uses_real_event_and_preserves_canonical_replay(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g93g_explainability", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g93g_owner", visibility="private")
    character = playable.entry.create_character(
        "g93g_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93g_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g93g_owner",
        mode="embodiment",
        session_id="session_g93g_alice",
        character_id=character.character_id,
    )
    instance_id = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance_id.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance_id, branch))
    alice = EntityId(actors["Alice"])
    bob = EntityId(actors["Bob"])
    committed = playable.action(
        instance_id.value,
        viewer_id="g93g_owner",
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "active"},
    )
    canonical_before = runtime.current_state(instance_id, branch)
    before_hash = canonical_before.semantic_hash()
    before_revision = canonical_before.revision.value
    event_ref = committed.event_id
    provenance = EvolutionProvenance(
        origin_ref=f"package:{package.package_id}",
        source_refs=(source.content_ref,),
        event_refs=(event_ref,),
        producer="runtime_projection",
    )
    persona = PersonaDelta(
        actor_id=alice,
        trait="caution",
        from_value="open",
        to_value="watchful",
        rationale="observed gate duty",
        evidence_refs=(event_ref,),
        delta_id="persona_g93g_product",
        provenance=provenance,
    )
    relationship = RelationshipDelta(
        delta_id="relationship_g93g_product",
        relationship_id="relationship_g93g_product",
        source_actor_id=alice,
        target_actor_id=bob,
        dimension="trust",
        before=0.0,
        after=0.2,
        reason="observed shared gate duty",
        provenance=provenance,
    )
    organization = OrganizationDelta(
        delta_id="organization_g93g_product",
        organization_id=EntityId("org_g93g_product"),
        lifecycle="role_changed",
        actor_id=alice,
        from_role="member",
        to_role="keeper",
        reason="reviewed keeper duty",
        provenance=provenance,
    )
    for delta in (persona, relationship, organization):
        EvolutionCommitPolicy.validate_proposal(delta)

    tracker = ActorEvolutionTracker(alice)
    actor_state = tracker.apply_persona(persona, provenance_ref=event_ref)
    persona_explanation = explain_delta(
        persona,
        explanation_id="explanation_g93g_persona_product",
        projection_ref="actor:alice:persona",
        at_ticks=1,
        trajectory_refs=(event_ref,),
    )
    persona_link = link_actor_trajectory(actor_state, persona_explanation, trajectory_seq=1)
    projection = advance_explainability_projection(
        EvolutionExplainabilityProjection(),
        persona_explanation,
        trajectory_links=(persona_link,),
    )
    relationship_explanation = explain_delta(
        relationship,
        explanation_id="explanation_g93g_relationship_product",
        projection_ref="relationship:alice:bob",
        at_ticks=1,
    )
    projection = advance_explainability_projection(projection, relationship_explanation)
    organization_explanation = explain_delta(
        organization,
        explanation_id="explanation_g93g_organization_product",
        projection_ref="organization:g93g_product",
        at_ticks=1,
    )
    projection = advance_explainability_projection(projection, organization_explanation)
    assert projection.by_delta(persona.delta_id) is persona_explanation
    assert projection.for_subject(relationship.relationship_id) == (relationship_explanation,)
    assert projection.for_subject(organization.organization_id.value) == (organization_explanation,)
    assert all(event_ref in item.event_refs for item in projection.explanations)
    assert all(source.content_ref in item.source_refs for item in projection.explanations)
    assert projection.links_for(alice) == (persona_link,)
    assert runtime.current_state(instance_id, branch).semantic_hash() == before_hash
    assert runtime.current_state(instance_id, branch).revision.value == before_revision
    assert len(runtime.events(instance_id, branch)) == committed.revision
    assert runtime.restore_and_replay(instance_id, branch).state.semantic_hash() == before_hash
