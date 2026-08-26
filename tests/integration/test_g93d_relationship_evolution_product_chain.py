"""G93D: relationship evolution follows a real runtime event and replays."""

from __future__ import annotations

import pathlib
from dataclasses import replace
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.actor_continuity.relationship_graph import RelationshipGraph
from wanxiang_substrate.actor_continuity.relationship_model import (
    RelationshipDimensions,
    RelationshipState,
)
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.relationship_evolution import (
    RelationshipDeltaRule,
    RelationshipEvolutionEvent,
    apply_relationship_proposal,
    propose_relationship_evolution,
    relationship_behavior_feedback,
)
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Relationship Chain\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate. Bob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g93d_relationship_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93d_relationship_source",
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
        provenance="synthetic:g93d",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type != "profile":
                continue
            display_name = component.fields.get("display_name")
            if isinstance(display_name, str):
                found[display_name] = entity.entity_id.value
    return found


@pytest.mark.integration
def test_relationship_evolution_replays_from_real_product_event(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g93d_relationship", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g93d_owner", visibility="private")
    character = playable.entry.create_character(
        "g93d_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93d_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g93d_owner",
        mode="embodiment",
        session_id="session_g93d_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    record = playable.store.get_instance(instance.value)
    branch = BranchId(record.branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    alice = EntityId(actors["Alice"])
    bob = EntityId(actors["Bob"])
    action = playable.action(
        instance.value,
        viewer_id="g93d_owner",
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "active"},
    )
    before = runtime.current_state(instance, branch)
    state = RelationshipState(
        "relation_g93d_product",
        alice,
        bob,
        "literary",
        RelationshipDimensions(),
        valid_from=0,
        event_refs=(action.event_id,),
    )
    graph, _ = RelationshipGraph().add(
        state, event_ref=action.event_id, at_ticks=0, reason="source relation"
    )
    proposal = propose_relationship_evolution(
        proposal_id="shared_watch",
        state=state,
        event=RelationshipEvolutionEvent(
            action.event_id,
            state.relationship_id,
            alice,
            bob,
            "shared_aid",
            0.8,
            10,
            (source.content_ref,),
        ),
        rules=(RelationshipDeltaRule("shared_aid", "trust", 0.5, maximum_step=0.2),),
        provenance=EvolutionProvenance(
            origin_ref=f"package:{package.package_id}",
            source_refs=(source.content_ref,),
            event_refs=(action.event_id,),
            producer="runtime_projection",
        ),
    )
    updated, _ = apply_relationship_proposal(graph, replace(proposal, approved=True))
    assert RelationshipGraph.replay(updated.revisions) == updated
    assert relationship_behavior_feedback(proposal.after, at_ticks=10).cooperation_bias > 0
    assert runtime.current_state(instance, branch).semantic_hash() == before.semantic_hash()
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash()
        == before.semantic_hash()
    )
