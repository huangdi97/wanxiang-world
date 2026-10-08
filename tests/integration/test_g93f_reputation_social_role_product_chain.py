"""G93F: real source-to-playable-to-preview-to-SQLite evidence feeds social views."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.delta import EvolutionCommitPolicy, EvolutionProvenance
from wanxiang_substrate.evolution.reputation import (
    ReputationEvent,
    ReputationProjection,
    SocialRole,
    SocialRoleProjection,
    advance_reputation_projection,
    advance_social_role_projection,
    apply_reputation_proposal,
    initial_reputation_state,
    propose_reputation_update,
    propose_social_role,
    review_reputation_proposal,
    review_social_role_proposal,
)
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Reputation Chain\nCharacter: Alice\nCharacter: Bob\nCharacter: Carol\n"
        "Alice kept watch at the gate. Bob carried the letter. Carol opened the archive.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g93f_reputation_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93f_reputation_source",
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
        provenance="synthetic:g93f",
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
def test_reputation_and_social_role_use_real_product_chain_without_canonical_mutation(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g93f_reputation", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g93f_owner", visibility="private")
    character = playable.entry.create_character(
        "g93f_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93f_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g93f_owner",
        mode="embodiment",
        session_id="session_g93f_alice",
        character_id=character.character_id,
    )
    instance_id = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance_id.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance_id, branch))
    alice = EntityId(actors["Alice"])
    bob = EntityId(actors["Bob"])
    committed = playable.action(
        instance_id.value,
        viewer_id="g93f_owner",
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "active"},
    )
    canonical_before = runtime.current_state(instance_id, branch)
    before_hash = canonical_before.semantic_hash()
    before_revision = canonical_before.revision.value
    provenance = EvolutionProvenance(
        origin_ref=f"package:{package.package_id}",
        source_refs=(source.content_ref,),
        event_refs=(committed.event_id,),
        producer="runtime_projection",
    )
    current = ReputationProjection(
        states=(
            initial_reputation_state(
                alice,
                dimension="trustworthiness",
                scope="local",
                scope_ref="archive:g93f",
                observer_actor_id=bob,
            ),
        )
    )
    social_event = ReputationEvent(
        event_ref=committed.event_id,
        observer_id=bob,
        subject_actor_id=alice,
        dimension="trustworthiness",
        signal="kept_commitment",
        valence=1.0,
        strength=0.8,
        scope="local",
        scope_ref="archive:g93f",
        at_ticks=1,
        evidence_ref=source.content_ref,
        evidence_kind="committed_event",
    )
    proposal = propose_reputation_update(
        proposal_id="product_reputation",
        current=current.states[0],
        events=(social_event,),
        provenance=provenance,
    )
    EvolutionCommitPolicy.validate_proposal(proposal.state_delta)
    assert committed.event_id in proposal.provenance.event_refs
    reviewed_reputation = review_reputation_proposal(proposal, reviewer="policy")
    updated_state = apply_reputation_proposal(current.states[0], reviewed_reputation)
    current = advance_reputation_projection(current, reviewed_reputation)
    assert current.state(alice, "trustworthiness", "local", "archive:g93f", bob) == updated_state

    role = SocialRole(
        role_id=EntityId("social_role_trusted_keeper_g93f"),
        name="trusted keeper",
        dimension="trustworthiness",
        minimum_score=0.1,
        scope="local",
        scope_ref="archive:g93f",
        observer_actor_id=bob,
    )
    role_proposal = propose_social_role(
        proposal_id="product_social_role",
        subject_actor_id=alice,
        role=role,
        reputation=updated_state,
        provenance=provenance,
    )
    role_projection = advance_social_role_projection(
        SocialRoleProjection(),
        review_social_role_proposal(role_proposal, reviewer="policy"),
    )
    assert role_projection.assignments[0].role.role_id == role.role_id
    assert runtime.current_state(instance_id, branch).semantic_hash() == before_hash
    assert runtime.current_state(instance_id, branch).revision.value == before_revision
    assert len(runtime.events(instance_id, branch)) == committed.revision
    assert runtime.restore_and_replay(instance_id, branch).state.semantic_hash() == before_hash
