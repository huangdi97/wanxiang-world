"""G96B: visual projection reads runtime evidence without writing reality."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_substrate.world_lab import (
    ActorPerspective,
    VisualProjectedObject,
    VisualProjectionFrame,
    VisualProviderHealth,
    VisualSceneObject,
    VisualSceneState,
    VisualWorldProvider,
)


class _ProbeVisualProvider:
    def health(self) -> VisualProviderHealth:
        return VisualProviderHealth(
            provider_id="provider:g96b:probe",
            version="1.0.0",
            available=True,
            deterministic=True,
            capabilities=("scene-projection",),
        )

    def project(
        self,
        scene: VisualSceneState,
        perspective: ActorPerspective,
    ) -> VisualProjectionFrame:
        visible = tuple(
            VisualProjectedObject(item.object_ref, item.entity_ref, item.position, item.asset_ref)
            for item in scene.objects
            if not item.audience_refs or perspective.actor_ref in item.audience_refs
        )
        return VisualProjectionFrame(
            frame_ref=f"frame:{perspective.actor_ref}:{scene.revision}",
            provider_id="provider:g96b:probe",
            provider_version="1.0.0",
            scene_ref=scene.scene_ref,
            snapshot_ref=scene.snapshot_ref,
            snapshot_revision=scene.revision,
            actor_ref=perspective.actor_ref,
            perspective_ref=perspective.perspective_ref,
            status="projected",
            objects=visible,
            asset_refs=tuple(item.asset_ref for item in visible if item.asset_ref is not None),
            event_refs=scene.event_refs,
            state_hash=scene.state_hash,
        )


def test_projection_cannot_mutate_runtime_reality(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    world = runtime.create_world()
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    scene = VisualSceneState(
        scene_ref="scene:g96b:runtime",
        snapshot_ref="snapshot:g96b:runtime",
        world_instance_ref=world.instance_id.value,
        branch_ref=world.root_branch_id.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=state.semantic_hash(),
        objects=(
            VisualSceneObject(
                object_ref="object:g96b:runtime",
                entity_ref="entity:g96b:runtime",
                position=(0.0, 0.0),
                audience_refs=("actor:alice",),
            ),
        ),
    )
    perspective = ActorPerspective(
        perspective_ref="perspective:g96b:runtime",
        actor_ref="actor:alice",
        origin=(0.0, 0.0),
        view_radius=2.0,
    )
    provider: VisualWorldProvider = _ProbeVisualProvider()
    before_hash = state.semantic_hash()
    frame = provider.project(scene, perspective)
    after = runtime.current_state(world.instance_id, world.root_branch_id)

    assert provider.health().available is True
    assert frame.projection_only is True
    assert frame.visible_objects[0].entity_ref == "entity:g96b:runtime"
    assert before_hash == after.semantic_hash()
    assert runtime.events(world.instance_id, world.root_branch_id) == ()
