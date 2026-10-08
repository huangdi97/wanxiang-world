"""G93A: source package -> playable runtime -> typed evolution proposals."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.delta import (
    BeliefDelta,
    CapabilityEvolutionDelta,
    EvolutionCommitPolicy,
    EvolutionDelta,
    EvolutionProvenance,
    OrganizationDelta,
    PersonaDelta,
    RelationshipDelta,
    StateDelta,
)
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Evolution Chain\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate. Bob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g93a_evolution_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93a_evolution_source",
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
        provenance="synthetic:g93a",
        access="private",
    )


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


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)


@pytest.mark.integration
def test_taxonomy_follows_real_source_playable_commit_chain(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g93a_evolution", (source,), profile="book").package
    assert package.evidence_coverage > 0.0

    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g93a_owner", visibility="private")
    character = playable.entry.create_character(
        "g93a_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93a_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g93a_owner",
        mode="embodiment",
        session_id="session_g93a_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    record = playable.store.get_instance(instance.value)
    branch = BranchId(record.branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    alice = EntityId(actors["Alice"])
    bob = EntityId(actors["Bob"])

    committed = playable.action(
        instance.value,
        viewer_id="g93a_owner",
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "active"},
    )
    event_ref = committed.event_id
    before_taxonomy = runtime.current_state(instance, branch)
    provenance = EvolutionProvenance(
        origin_ref=f"package:{package.package_id}",
        source_refs=(source.content_ref,),
        event_refs=(event_ref,),
        producer="runtime_projection",
    )
    deltas: tuple[EvolutionDelta, ...] = (
        StateDelta("g93a_state", alice, "status", "idle", "active", "committed action", provenance),
        BeliefDelta(
            "g93a_belief",
            alice,
            EntityId("belief_g93a"),
            "support",
            0.2,
            0.7,
            "unknown",
            "supported",
            "observed watch",
            provenance,
        ),
        RelationshipDelta(
            "g93a_relationship",
            "relationship_g93a",
            alice,
            bob,
            "trust",
            0.0,
            0.3,
            "shared event",
            provenance,
        ),
        CapabilityEvolutionDelta(
            "g93a_capability",
            alice,
            "watchkeeping",
            0,
            1,
            0.0,
            0.2,
            0.0,
            0.6,
            "repeated practice",
            provenance,
        ),
        PersonaDelta(
            actor_id=alice,
            trait="temperament",
            from_value="open",
            to_value="watchful",
            rationale="repeated observed duty",
            evidence_refs=(event_ref,),
            delta_id="g93a_persona",
            provenance=provenance,
        ),
        OrganizationDelta(
            "g93a_organization",
            EntityId("org_g93a"),
            "joined",
            alice,
            None,
            "watcher",
            "accepted duty",
            provenance,
        ),
    )
    for delta in deltas:
        EvolutionCommitPolicy.validate_proposal(delta)
        receipt = EvolutionCommitPolicy.receipt(
            delta,
            event_ref=event_ref,
            branch_revision=committed.revision,
            authority_ref=f"commit-authority:{instance.value}",
        )
        assert receipt.delta_id == delta.delta_id

    after_taxonomy = runtime.current_state(instance, branch)
    assert after_taxonomy.semantic_hash() == before_taxonomy.semantic_hash()
    assert len(runtime.events(instance, branch)) == committed.revision
    assert {delta.kind for delta in deltas} == {
        "state",
        "belief",
        "relationship",
        "capability",
        "persona",
        "organization",
    }
