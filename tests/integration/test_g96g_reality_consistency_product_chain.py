"""G96G: real SQLite reality remains unchanged through consistency checks."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
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


def test_visual_and_physical_outputs_are_checked_without_sqlite_mutation(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    world = runtime.create_world()
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    before_hash = state.semantic_hash()
    before_events = runtime.events(world.instance_id, world.root_branch_id)
    scene = VisualSceneState(
        scene_ref="scene_g96g_runtime",
        snapshot_ref="snapshot_g96g_runtime",
        world_instance_ref=world.instance_id.value,
        branch_ref=world.root_branch_id.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=before_hash,
        objects=(
            VisualSceneObject(
                object_ref="object_g96g_runtime_public",
                entity_ref="entity_g96g_runtime_public",
                position=(1.0, 0.0),
                event_refs=("event_g96g_runtime_public",),
            ),
        ),
        event_refs=("event_g96g_runtime_public",),
    )
    visual = ReferenceVisualProvider("provider_g96g_runtime_visual", "1.0.0").project(
        scene,
        ActorPerspective(
            perspective_ref="perspective_g96g_runtime",
            actor_ref="actor_g96g_runtime",
            origin=(0.0, 0.0),
            view_radius=2.0,
        ),
    )
    snapshot = PhysicalSnapshot(
        snapshot_ref="snapshot_g96g_runtime_physical",
        world_instance_ref=world.instance_id.value,
        branch_ref=world.root_branch_id.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=before_hash,
        bodies=(
            PhysicalBody(
                body_ref="entity_g96g_runtime_actor",
                position=(0.0, 0.0),
                velocity=(0.25, 0.0),
            ),
        ),
    )
    request = PhysicalSimulationRequest(
        request_id="request_g96g_runtime",
        snapshot_ref=snapshot.snapshot_ref,
        snapshot_revision=snapshot.revision,
        actor_ref="entity_g96g_runtime_actor",
        action="step",
        step_ticks=2,
    )
    physical = ReferencePhysicalProvider("provider_g96g_runtime_physical", "1.0.0").simulate(
        snapshot, request
    )
    checker = RealityConsistencyChecker()

    assert checker.check_visual(scene, visual).is_consistent
    assert checker.check_physical(snapshot, physical).is_consistent
    assert checker.check_visual(scene, visual).proposal.proposed_delta.is_empty()
    assert checker.check_physical(snapshot, physical).proposal.proposed_delta.is_empty()
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert after.semantic_hash() == before_hash
    assert runtime.events(world.instance_id, world.root_branch_id) == before_events
