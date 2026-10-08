"""G96E: reference visual projection is structured and non-generative."""

from __future__ import annotations

from wanxiang_substrate.world_lab import (
    ActorPerspective,
    ReferenceVisualProvider,
    VisualSceneObject,
    VisualSceneState,
    VisualWorldProvider,
)


def _scene() -> VisualSceneState:
    return VisualSceneState(
        scene_ref="scene_g96e",
        snapshot_ref="snapshot_g96e",
        world_instance_ref="world_g96e",
        branch_ref="branch_g96e",
        revision=2,
        world_time_ticks=6,
        state_hash="statehash_g96e",
        objects=(
            VisualSceneObject(
                object_ref="object_g96e_public",
                entity_ref="entity_g96e_public",
                position=(1.0, 0.0),
                event_refs=("event_g96e_public",),
            ),
            VisualSceneObject(
                object_ref="object_g96e_alice",
                entity_ref="entity_g96e_alice",
                position=(1.0, 1.0),
                audience_refs=("actor_alice",),
                event_refs=("event_g96e_alice",),
            ),
        ),
        event_refs=("event_g96e_public", "event_g96e_alice"),
    )


def test_reference_provider_returns_structured_actor_frames() -> None:
    provider = ReferenceVisualProvider("provider_g96e", "1.0.0")
    scene = _scene()
    frame = provider.project(
        scene,
        ActorPerspective(
            perspective_ref="perspective_g96e_alice",
            actor_ref="actor_alice",
            origin=(0.0, 0.0),
            view_radius=4.0,
        ),
    )

    assert isinstance(provider, VisualWorldProvider)
    assert provider.health().deterministic is True
    assert provider.health().capabilities == (
        "actor-perspective",
        "event-refs",
        "non-generative",
        "state-refs",
        "structured-scene",
    )
    assert frame.snapshot_ref == scene.snapshot_ref
    assert frame.snapshot_revision == scene.revision
    assert frame.state_hash == scene.state_hash
    assert frame.event_refs == ("event_g96e_alice", "event_g96e_public")
    assert {item.entity_ref for item in frame.objects} == {
        "entity_g96e_public",
        "entity_g96e_alice",
    }
    assert frame.projection_hash
    assert not hasattr(provider, "commit")
    assert not hasattr(provider, "render")
