"""G96C: real SQLite state supplies isolated actor projection frames."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_substrate.world_lab import (
    ActorPerspective,
    PerspectiveVisualProvider,
    VisualSceneObject,
    VisualSceneState,
)


def test_two_actor_views_preserve_sqlite_reality(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    world = runtime.create_world()
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    before_hash = state.semantic_hash()
    before_events = runtime.events(world.instance_id, world.root_branch_id)
    scene = VisualSceneState(
        scene_ref="scene:g96c:runtime",
        snapshot_ref="snapshot:g96c:runtime",
        world_instance_ref=world.instance_id.value,
        branch_ref=world.root_branch_id.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=before_hash,
        objects=(
            VisualSceneObject(
                object_ref="object:g96c:runtime:alice",
                entity_ref="entity:g96c:runtime:alice-private",
                position=(1.0, 1.0),
                audience_refs=("actor:alice",),
                event_refs=("event:g96c:runtime:alice",),
            ),
            VisualSceneObject(
                object_ref="object:g96c:runtime:bob",
                entity_ref="entity:g96c:runtime:bob-private",
                position=(1.0, -1.0),
                audience_refs=("actor:bob",),
                event_refs=("event:g96c:runtime:bob",),
            ),
        ),
        event_refs=("event:g96c:runtime:alice", "event:g96c:runtime:bob"),
    )
    provider = PerspectiveVisualProvider("provider:g96c:runtime", "1.0.0")
    alice = provider.project(
        scene,
        ActorPerspective(
            perspective_ref="perspective:g96c:runtime:alice",
            actor_ref="actor:alice",
            origin=(0.0, 0.0),
            view_radius=3.0,
        ),
    )
    bob = provider.project(
        scene,
        ActorPerspective(
            perspective_ref="perspective:g96c:runtime:bob",
            actor_ref="actor:bob",
            origin=(0.0, 0.0),
            view_radius=3.0,
        ),
    )

    assert [item.entity_ref for item in alice.objects] == ["entity:g96c:runtime:alice-private"]
    assert [item.entity_ref for item in bob.objects] == ["entity:g96c:runtime:bob-private"]
    assert alice.event_refs == ("event:g96c:runtime:alice",)
    assert bob.event_refs == ("event:g96c:runtime:bob",)
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert after.semantic_hash() == before_hash
    assert runtime.events(world.instance_id, world.root_branch_id) == before_events
