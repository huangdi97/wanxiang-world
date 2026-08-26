"""G93C: persona adaptation follows a real source/playable event trace."""

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
from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.persona_adaptation import (
    PersonaObservation,
    PersonaTraitState,
    propose_persona_adaptation,
    review_persona_adaptation,
)
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Persona Chain\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate. Bob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g93c_persona_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93c_persona_source",
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
        provenance="synthetic:g93c",
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
def test_persona_adaptation_is_slow_reviewed_and_projection_only(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g93c_persona", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g93c_owner", visibility="private")
    character = playable.entry.create_character(
        "g93c_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93c_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g93c_owner",
        mode="embodiment",
        session_id="session_g93c_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    record = playable.store.get_instance(instance.value)
    branch = BranchId(record.branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    actor = EntityId(actors["Alice"])
    action = playable.action(
        instance.value,
        viewer_id="g93c_owner",
        action_type="set_status",
        payload={"entity_id": actor.value, "status": "active"},
    )
    before = runtime.current_state(instance, branch)
    provenance = EvolutionProvenance(
        origin_ref=f"package:{package.package_id}",
        source_refs=(source.content_ref,),
        event_refs=(action.event_id,),
        producer="runtime_projection",
    )
    observations = tuple(
        PersonaObservation(
            observation_id=f"g93c_observation_{index}",
            actor_id=actor,
            trait="caution",
            direction="increase",
            strength=0.8,
            at_ticks=tick,
            event_ref=f"{action.event_id}:observation:{index}",
        )
        for index, tick in enumerate((10, 20, 30), start=1)
    )
    proposal = propose_persona_adaptation(
        proposal_id="g93c_caution_window",
        current=PersonaTraitState(actor, "caution"),
        observations=observations,
        now_ticks=30,
        provenance=provenance,
    )
    reviewed = review_persona_adaptation(proposal, reviewer="policy", approved=True)
    tracker = ActorEvolutionTracker(actor)
    tracker.apply_persona(reviewed.persona_delta, provenance_ref=action.event_id)
    assert tracker.state.trait("caution") == reviewed.persona_delta.to_value
    assert reviewed.status == "approved"
    assert runtime.current_state(instance, branch).semantic_hash() == before.semantic_hash()
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash()
        == before.semantic_hash()
    )
