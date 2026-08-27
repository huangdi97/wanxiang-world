"""G96H: playable SQLite world crosses both reference provider bridges."""

from __future__ import annotations

import pathlib
from typing import cast

from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    ActorPerspective,
    PhysicalBody,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
    RealityConsistencyChecker,
    ReferencePhysicalProvider,
    ReferenceVisualProvider,
    VisualSceneObject,
    VisualSceneState,
)


def _source() -> SourceRecord:
    content = (
        "# G96H bridge qualification\nCharacter: Alice\nCharacter: Bob\n"
        "Alice keeps watch at the gate.\nBob carries a letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g96h_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g96h_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g96h",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=False,
            training_allowed=False,
        ),
        payload=content,
        provenance="fixture:g96h",
        access="private",
    )


def test_playable_world_crosses_reference_bridges_and_preserves_sqlite_reality(
    persist_db_path: pathlib.Path,
) -> None:
    authored = OneClickAuthoring().run("job_g96h", (_source(),), profile="book")
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable = PlayableService(runtime)
    profile = playable.register_package(
        authored.package, owner_id="owner_g96h", visibility="private"
    )
    alice = playable.entry.create_character(
        "owner_g96h",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    bob = playable.entry.create_character(
        "owner_g96h",
        "Bob",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_bob",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="owner_g96h",
        mode="embodiment",
        session_id="session_g96h",
        character_id=alice.character_id,
    )
    instance_payload = cast(dict[str, object], entered["instance"])
    instance_id = str(instance_payload["instance_id"])
    instance = WorldInstanceId(instance_id)
    record = playable.store.get_instance(instance_id)
    branch = BranchId(record.branch_id)
    action = playable.action(instance_id, viewer_id="owner_g96h", text="set status to awake")
    state = runtime.current_state(instance, branch)
    assert action.event_id
    assert state.semantic_hash() == action.state_hash
    assert len(state.entities()) >= 2
    before_hash = state.semantic_hash()
    before_events = runtime.events(instance, branch)

    entity_ids = tuple(entity.entity_id.value for entity in state.entities()[:2])
    event_ref = action.event_id
    scene = VisualSceneState(
        scene_ref=f"scene_g96h_{instance_id}",
        snapshot_ref=f"snapshot_g96h_{instance_id}",
        world_instance_ref=instance_id,
        branch_ref=branch.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=state.semantic_hash(),
        objects=(
            VisualSceneObject(
                object_ref="object_g96h_alice",
                entity_ref=entity_ids[0],
                position=(1.0, 0.0),
                audience_refs=(alice.character_id,),
                event_refs=(event_ref,),
            ),
            VisualSceneObject(
                object_ref="object_g96h_public",
                entity_ref=entity_ids[1],
                position=(0.0, 1.0),
                event_refs=(event_ref,),
            ),
        ),
        event_refs=(event_ref,),
    )
    visual_provider = ReferenceVisualProvider("provider_g96h_visual", "1.0.0")
    alice_frame = visual_provider.project(
        scene,
        ActorPerspective(
            perspective_ref="perspective_g96h_alice",
            actor_ref=alice.character_id,
            origin=(0.0, 0.0),
            view_radius=3.0,
        ),
    )
    bob_frame = visual_provider.project(
        scene,
        ActorPerspective(
            perspective_ref="perspective_g96h_bob",
            actor_ref=bob.character_id,
            origin=(0.0, 0.0),
            view_radius=3.0,
        ),
    )

    physical_snapshot = PhysicalSnapshot(
        snapshot_ref=f"physical_snapshot_g96h_{instance_id}",
        world_instance_ref=instance_id,
        branch_ref=branch.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=state.semantic_hash(),
        bodies=(
            PhysicalBody(
                body_ref=entity_ids[0],
                position=(0.0, 0.0),
                velocity=(0.25, 0.0),
            ),
        ),
    )
    physical_request = PhysicalSimulationRequest(
        request_id="request_g96h",
        snapshot_ref=physical_snapshot.snapshot_ref,
        snapshot_revision=physical_snapshot.revision,
        actor_ref=entity_ids[0],
        action="step",
        step_ticks=2,
    )
    physical_resolution = ReferencePhysicalProvider("provider_g96h_physical", "1.0.0").simulate(
        physical_snapshot, physical_request
    )

    checker = RealityConsistencyChecker()
    assert {item.object_ref for item in alice_frame.objects} == {
        "object_g96h_alice",
        "object_g96h_public",
    }
    assert [item.object_ref for item in bob_frame.objects] == ["object_g96h_public"]
    assert alice_frame.frame_ref != bob_frame.frame_ref
    assert checker.check_visual(scene, alice_frame).is_consistent
    assert checker.check_visual(scene, bob_frame).is_consistent
    assert checker.check_physical(physical_snapshot, physical_resolution).is_consistent
    assert checker.check_visual(scene, alice_frame).proposal.proposed_delta.is_empty()
    assert checker.check_physical(
        physical_snapshot, physical_resolution
    ).proposal.proposed_delta.is_empty()

    replayed = runtime.restore_and_replay(instance, branch)
    assert replayed.state.semantic_hash() == before_hash
    assert runtime.current_state(instance, branch).semantic_hash() == before_hash
    assert runtime.events(instance, branch) == before_events
