"""G93H: accelerated 30d source world yields bounded three-plane evolution."""

from __future__ import annotations

import pathlib
from dataclasses import replace
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import SubmitCommandResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.ids import ActorId, BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.actor_continuity.relationship_graph import RelationshipGraph
from wanxiang_substrate.actor_continuity.relationship_model import (
    RelationshipDimensions,
    RelationshipState,
)
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
from wanxiang_substrate.evolution.actor_evolution import ActorEvolutionTracker
from wanxiang_substrate.evolution.delta import EvolutionCommitPolicy, EvolutionProvenance
from wanxiang_substrate.evolution.organization_lifecycle import (
    apply_organization_proposal,
    create_organization_proposal,
    organization_state_from_canonical,
    propose_join,
    propose_role_change,
    review_organization_proposal,
)
from wanxiang_substrate.evolution.organization_model import (
    OrganizationLifecycleState,
    OrganizationResource,
)
from wanxiang_substrate.evolution.persona_adaptation import (
    PersonaAdaptationPolicy,
    PersonaObservation,
    PersonaTraitState,
    propose_persona_adaptation,
    review_persona_adaptation,
)
from wanxiang_substrate.evolution.qualification import (
    EvolutionProjectionSnapshot,
    compare_evolution,
)
from wanxiang_substrate.evolution.relationship_evolution import (
    RelationshipDeltaRule,
    RelationshipEvolutionEvent,
    apply_relationship_proposal,
    propose_relationship_evolution,
)
from wanxiang_substrate.institution.model import Role
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

DAY = 100
HORIZON_DAYS = 30
OWNER = "g93h_owner"


def _source() -> SourceRecord:
    content = (
        "# M90 Evolution Town\nCharacter: Alice\nCharacter: Bob\nCharacter: Carol\n"
        "Alice kept watch at the gate. Bob carried the letter. Carol opened the archive.\n"
        "relationship: Alice -> Bob\norganization: the gate circle\n"
        "rule: repeated witnessed duties affect trust, roles, and memory\n"
    )
    return SourceRecord(
        source_id="g93h_m90_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93h_m90_source",
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
        provenance="synthetic:g93h",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)
    register_temporal_resolvers(registry)
    register_epistemic_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                name = component.fields.get("display_name")
                if isinstance(name, str):
                    found[name] = entity.entity_id.value
    return found


def _commit(
    runtime: WorldRuntime,
    instance: WorldInstanceId,
    branch: BranchId,
    *,
    command_id: str,
    action_type: str,
    payload: dict[str, FieldValue],
    world_time: int,
    actor_id: str | None = None,
) -> SubmitCommandResult:
    current = runtime.current_state(instance, branch)
    return runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance,
            branch_id=branch,
            expected_revision=current.revision,
            action_type=action_type,
            payload=payload,
            actor_id=ActorId(actor_id) if actor_id else None,
            world_time=WorldTime(world_time),
        )
    )


def _relationship_fingerprint(graph: RelationshipGraph, relationship_id: str) -> str:
    state = graph.state(relationship_id)
    assert state is not None
    return semantic_sha256(
        {
            "relationship_id": state.relationship_id,
            "source": state.source_actor_id.value,
            "target": state.target_actor_id.value,
            "dimensions": state.dimensions.to_dict(),
            "valid_from": state.valid_from,
            "event_refs": list(state.event_refs),
        }
    )


def _organization_fingerprint(organization: OrganizationLifecycleState) -> str:
    return semantic_sha256(
        {
            "organization_id": organization.organization_id.value,
            "status": organization.status,
            "roles": [
                (role.role_id.value, role.name, list(role.permissions))
                for role in organization.roles
            ],
            "memberships": [
                (
                    item.membership_id.value,
                    item.actor_id.value,
                    item.role_id.value,
                    item.start_ticks,
                    item.end_ticks,
                )
                for item in organization.memberships
            ],
            "history_refs": list(organization.history_refs),
            "resources": [
                (item.resource_id.value, item.kind, item.quantity)
                for item in organization.resources
            ],
        }
    )


@pytest.mark.integration
def test_m90_30d_evolution_has_nonzero_bounded_changes_without_source_mutation(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authored = OneClickAuthoring().run("job_g93h_m90", (source,), profile="book")
    assert authored.package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id=OWNER, visibility="private")
    character = playable.entry.create_character(
        OWNER,
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93h_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id=OWNER,
        mode="embodiment",
        session_id="session_g93h_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    assert {"Alice", "Bob", "Carol"}.issubset(actors)
    alice = EntityId(actors["Alice"])
    bob = EntityId(actors["Bob"])
    carol = EntityId(actors["Carol"])
    entry_action = playable.action(
        instance.value,
        viewer_id=OWNER,
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "active"},
    )
    _commit(
        runtime,
        instance,
        branch,
        command_id="g93h_temporal_calendar",
        action_type="temporal.instantiate",
        payload={"fixture": "calendar", "version": 1},
        world_time=runtime.current_state(instance, branch).revision.value + 1,
    )
    baseline_state = runtime.current_state(instance, branch)
    baseline_events = runtime.events(instance, branch)
    baseline_event_refs = tuple(item.event_id.value for item in baseline_events)
    baseline_replay = runtime.restore_and_replay(instance, branch).state.semantic_hash()
    relationship_id = "relationship_g93h_m90"
    relationship = RelationshipState(
        relationship_id=relationship_id,
        source_actor_id=alice,
        target_actor_id=bob,
        relation_type="gate-partners",
        dimensions=RelationshipDimensions(),
        valid_from=0,
        event_refs=(entry_action.event_id,),
    )
    relationship_graph, _ = RelationshipGraph().add(
        relationship,
        event_ref=entry_action.event_id,
        at_ticks=0,
        reason="source-created relationship baseline",
    )
    organization_id = EntityId("org_g93h_m90")
    baseline_organization = organization_state_from_canonical(
        baseline_state,
        organization_id,
        resources=(OrganizationResource(EntityId("resource_g93h_m90"), "ledger", 30),),
    )
    actor_tracker = ActorEvolutionTracker(alice)
    actor_baseline = actor_tracker.state
    status_refs: dict[tuple[str, int], str] = {}
    for day in range(1, HORIZON_DAYS + 1):
        current_tick = day * DAY
        _commit(
            runtime,
            instance,
            branch,
            command_id=f"g93h_clock_{day:02d}",
            action_type="temporal.advance_to",
            payload={"ticks": current_tick},
            world_time=current_tick,
        )
        for name, actor in (("alice", alice), ("bob", bob), ("carol", carol)):
            status = _commit(
                runtime,
                instance,
                branch,
                command_id=f"g93h_status_{day:02d}_{name}",
                action_type="set_status",
                payload={"entity_id": actor.value, "status": "active"},
                world_time=current_tick,
                actor_id=actor.value,
            )
            if day in (5, 15, 20, 30):
                status_refs[(name, day)] = status.event.event_id.value
            _commit(
                runtime,
                instance,
                branch,
                command_id=f"g93h_memory_{day:02d}_{name}",
                action_type="epistemic.record_observation",
                payload={
                    "memory_id": f"g93h_memory_{name}_{day:02d}",
                    "actor_id": actor.value,
                    "content_ref": f"memory://g93h/{actor.value}/day-{day:02d}",
                    "at_ticks": current_tick,
                    "salience": 0.5,
                    "source_obs_ref": f"observation://g93h/{actor.value}/{day:02d}",
                },
                world_time=current_tick,
                actor_id=actor.value,
            )

    evolved_state = runtime.current_state(instance, branch)
    evolved_events = runtime.events(instance, branch)
    evolved_replay = runtime.restore_and_replay(instance, branch).state.semantic_hash()
    assert evolved_state.revision.value == len(evolved_events)
    assert evolved_state.revision.value > baseline_state.revision.value
    assert source.payload == _source().payload
    assert source.content_hash == _source().content_hash

    common_provenance = EvolutionProvenance(
        origin_ref=f"package:{authored.package.package_id}",
        source_refs=(source.content_ref,),
        event_refs=(status_refs[("alice", 5)],),
        producer="runtime_projection",
    )
    persona_policy = PersonaAdaptationPolicy(
        window_ticks=HORIZON_DAYS * DAY,
        minimum_observations=3,
        minimum_span_ticks=7,
        maximum_abs_change=0.1,
    )
    persona_current = PersonaTraitState(actor_id=alice, trait="caution")
    persona_observations = tuple(
        PersonaObservation(
            observation_id=f"g93h_caution_{day}",
            actor_id=alice,
            trait="caution",
            direction="increase",
            strength=0.6,
            at_ticks=day * DAY,
            event_ref=status_refs[("alice", day)],
        )
        for day in (5, 15, 30)
    )
    persona_proposal = propose_persona_adaptation(
        proposal_id="g93h_persona",
        current=persona_current,
        observations=persona_observations,
        now_ticks=HORIZON_DAYS * DAY,
        provenance=common_provenance,
        policy=persona_policy,
    )
    persona_approved = review_persona_adaptation(
        persona_proposal,
        reviewer="policy",
        approved=True,
        policy=persona_policy,
    )
    actor_evolved = actor_tracker.apply_persona(
        persona_approved.persona_delta,
        provenance_ref=status_refs[("alice", 30)],
    )
    EvolutionCommitPolicy.validate_proposal(persona_approved.persona_delta)

    relationship_event = RelationshipEvolutionEvent(
        event_ref=status_refs[("alice", 15)],
        relationship_id=relationship_id,
        source_actor_id=alice,
        target_actor_id=bob,
        signal="shared_aid",
        strength=0.8,
        at_ticks=15 * DAY,
        evidence_refs=(source.content_ref,),
    )
    relationship_proposal = propose_relationship_evolution(
        proposal_id="g93h_relationship_15",
        state=relationship,
        event=relationship_event,
        rules=(RelationshipDeltaRule("shared_aid", "trust", 0.5, maximum_step=0.2),),
        provenance=common_provenance,
    )
    relationship_graph, _ = apply_relationship_proposal(
        relationship_graph, replace(relationship_proposal, approved=True)
    )
    relationship_event_30 = replace(
        relationship_event,
        event_ref=status_refs[("alice", 30)],
        at_ticks=30 * DAY,
    )
    relationship_proposal_30 = propose_relationship_evolution(
        proposal_id="g93h_relationship_30",
        state=relationship_proposal.after,
        event=relationship_event_30,
        rules=(RelationshipDeltaRule("shared_aid", "trust", 0.5, maximum_step=0.2),),
        provenance=EvolutionProvenance(
            origin_ref=common_provenance.origin_ref,
            source_refs=common_provenance.source_refs,
            event_refs=(status_refs[("alice", 30)],),
            producer=common_provenance.producer,
        ),
    )
    relationship_graph, _ = apply_relationship_proposal(
        relationship_graph, replace(relationship_proposal_30, approved=True)
    )
    EvolutionCommitPolicy.validate_proposal(relationship_proposal.delta)
    EvolutionCommitPolicy.validate_proposal(relationship_proposal_30.delta)

    admin = Role(
        EntityId("role_admin_g93h"),
        "admin",
        ("organization.manage_members", "organization.manage_roles"),
    )
    member = Role(EntityId("role_member_g93h"), "member")
    steward = Role(EntityId("role_steward_g93h"), "steward")
    create = create_organization_proposal(
        baseline_organization,
        proposal_id="g93h_org_create",
        founder_id=alice,
        founder_role=admin,
        additional_roles=(member, steward),
        membership_id=EntityId("membership_g93h_alice"),
        event_ref=status_refs[("alice", 5)],
        at_ticks=5 * DAY,
        provenance=common_provenance,
        resources=baseline_organization.resources,
    )
    organization = apply_organization_proposal(
        baseline_organization, review_organization_proposal(create, reviewer="policy")
    )
    join_bob = propose_join(
        organization,
        proposal_id="g93h_org_bob",
        initiator_id=bob,
        member_id=bob,
        membership_id=EntityId("membership_g93h_bob"),
        role_id=member.role_id,
        event_ref=status_refs[("bob", 15)],
        at_ticks=15 * DAY,
        provenance=common_provenance,
    )
    organization = apply_organization_proposal(
        organization, review_organization_proposal(join_bob, reviewer="policy")
    )
    join_carol = propose_join(
        organization,
        proposal_id="g93h_org_carol",
        initiator_id=carol,
        member_id=carol,
        membership_id=EntityId("membership_g93h_carol"),
        role_id=member.role_id,
        event_ref=status_refs[("carol", 20)],
        at_ticks=20 * DAY,
        provenance=common_provenance,
    )
    organization = apply_organization_proposal(
        organization, review_organization_proposal(join_carol, reviewer="policy")
    )
    role_change = propose_role_change(
        organization,
        proposal_id="g93h_org_role",
        initiator_id=alice,
        member_id=bob,
        new_role_id=steward.role_id,
        event_ref=status_refs[("alice", 30)],
        at_ticks=30 * DAY,
        provenance=common_provenance,
    )
    organization = apply_organization_proposal(
        organization, review_organization_proposal(role_change, reviewer="policy")
    )
    for proposal in (create, join_bob, join_carol, role_change):
        EvolutionCommitPolicy.validate_proposal(proposal.delta)

    baseline_snapshot = EvolutionProjectionSnapshot(
        run_id="run:g93h_m90",
        elapsed_days=0,
        world_ticks=0,
        source_ref=source.content_ref,
        source_content_hash=source.content_hash,
        package_ref=authored.package.package_id,
        canonical_hash=baseline_state.semantic_hash(),
        replay_hash=baseline_replay,
        canonical_revision=baseline_state.revision.value,
        canonical_event_refs=baseline_event_refs,
        actor_fingerprints=((alice.value, actor_baseline.persona_hash()),),
        relationship_fingerprints=(
            (
                relationship_id,
                _relationship_fingerprint(
                    RelationshipGraph(states=(relationship,)), relationship_id
                ),
            ),
        ),
        organization_fingerprints=(
            (organization_id.value, _organization_fingerprint(baseline_organization)),
        ),
        evidence_refs=(source.content_ref,),
        validated_delta_ids=(),
    )
    evolved_snapshot = EvolutionProjectionSnapshot(
        run_id="run:g93h_m90",
        elapsed_days=HORIZON_DAYS,
        world_ticks=HORIZON_DAYS * DAY,
        source_ref=source.content_ref,
        source_content_hash=source.content_hash,
        package_ref=authored.package.package_id,
        canonical_hash=evolved_state.semantic_hash(),
        replay_hash=evolved_replay,
        canonical_revision=evolved_state.revision.value,
        canonical_event_refs=tuple(item.event_id.value for item in evolved_events),
        actor_fingerprints=((alice.value, actor_evolved.persona_hash()),),
        relationship_fingerprints=(
            (relationship_id, _relationship_fingerprint(relationship_graph, relationship_id)),
        ),
        organization_fingerprints=(
            (organization_id.value, _organization_fingerprint(organization)),
        ),
        evidence_refs=tuple(dict.fromkeys((source.content_ref,) + tuple(status_refs.values()))),
        validated_delta_ids=(
            persona_approved.persona_delta.delta_id,
            relationship_proposal.delta.delta_id,
            relationship_proposal_30.delta.delta_id,
            create.delta.delta_id,
            join_bob.delta.delta_id,
            join_carol.delta.delta_id,
            role_change.delta.delta_id,
        ),
    )
    comparison = compare_evolution(baseline_snapshot, evolved_snapshot)
    assert comparison.qualified is True
    assert comparison.nonzero_projection_change is True
    assert comparison.source_unchanged is True
    assert comparison.canonical_history_preserved is True
    assert comparison.replay_equal is True
    assert actor_evolved.persona_hash() != actor_baseline.persona_hash()
    assert relationship_graph.state(relationship_id) != relationship
    assert organization.active_members(30 * DAY) == (alice, bob, carol)
    assert organization.roles_for(bob, 30 * DAY) == (steward,)
    assert source.payload == _source().payload
    assert source.content_hash == _source().content_hash
    assert (
        runtime.current_state(instance, branch).semantic_hash() == evolved_snapshot.canonical_hash
    )
    assert (
        runtime.current_state(instance, branch).revision.value
        == evolved_snapshot.canonical_revision
    )
    assert (
        tuple(item.event_id.value for item in runtime.events(instance, branch))
        == evolved_snapshot.canonical_event_refs
    )
    assert (
        ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
        .replay(runtime.events(instance, branch))
        .semantic_hash()
        == evolved_snapshot.canonical_hash
    )
