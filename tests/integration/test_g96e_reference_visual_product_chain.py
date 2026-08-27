"""G96E: reference visual projection preserves real SQLite reality."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_substrate.world_lab import (
    ActorPerspective,
    ReferenceVisualProvider,
    VisualSceneObject,
    VisualSceneState,
)


def test_reference_visual_projection_does_not_mutate_sqlite_reality(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    world = runtime.create_world()
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    before_hash = state.semantic_hash()
    before_events = runtime.events(world.instance_id, world.root_branch_id)
    scene = VisualSceneState(
        scene_ref="scene_g96e_runtime",
        snapshot_ref="snapshot_g96e_runtime",
        world_instance_ref=world.instance_id.value,
        branch_ref=world.root_branch_id.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=before_hash,
        objects=(
            VisualSceneObject(
                object_ref="object_g96e_runtime_alice",
                entity_ref="entity_g96e_runtime_alice",
                position=(1.0, 0.0),
                audience_refs=("actor_alice",),
                event_refs=("event_g96e_runtime_alice",),
            ),
            VisualSceneObject(
                object_ref="object_g96e_runtime_public",
                entity_ref="entity_g96e_runtime_public",
                position=(0.0, 1.0),
                event_refs=("event_g96e_runtime_public",),
            ),
        ),
        event_refs=("event_g96e_runtime_alice", "event_g96e_runtime_public"),
    )
    provider = ReferenceVisualProvider("provider_g96e_runtime", "1.0.0")
    alice = provider.project(
        scene,
        ActorPerspective(
            perspective_ref="perspective_g96e_runtime_alice",
            actor_ref="actor_alice",
            origin=(0.0, 0.0),
            view_radius=2.0,
        ),
    )
    public = provider.project(
        scene,
        ActorPerspective(
            perspective_ref="perspective_g96e_runtime_public",
            actor_ref="actor_public",
            origin=(0.0, 0.0),
            view_radius=2.0,
        ),
    )

    assert {item.entity_ref for item in alice.objects} == {
        "entity_g96e_runtime_alice",
        "entity_g96e_runtime_public",
    }
    assert [item.entity_ref for item in public.objects] == ["entity_g96e_runtime_public"]
    assert alice.state_hash == public.state_hash == before_hash
    assert alice.frame_ref != public.frame_ref
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert after.semantic_hash() == before_hash
    assert runtime.events(world.instance_id, world.root_branch_id) == before_events
