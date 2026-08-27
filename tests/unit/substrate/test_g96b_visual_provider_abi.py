"""G96B: visual provider ABI is projection-only and schema-verifiable."""

from __future__ import annotations

import inspect

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.world_lab import (
    ActorPerspective,
    VisualProjectedObject,
    VisualProjectionFrame,
    VisualProviderHealth,
    VisualSceneObject,
    VisualSceneState,
    VisualWorldProvider,
)


def _asset() -> AssetRef:
    return AssetRef(
        asset_id="asset:g96b:gate",
        content_hash="hash:g96b:gate",
        size=12,
        content_type="image/png",
        rights="public",
    )


def _scene() -> VisualSceneState:
    asset = _asset()
    return VisualSceneState(
        scene_ref="scene:g96b",
        snapshot_ref="snapshot:g96b",
        world_instance_ref="world:g96b",
        branch_ref="branch:g96b",
        revision=3,
        world_time_ticks=9,
        state_hash="statehash:g96b",
        objects=(
            VisualSceneObject(
                object_ref="object:g96b",
                entity_ref="entity:g96b",
                position=(1.0, 2.0),
                asset_ref=asset,
                audience_refs=("actor:alice",),
                event_refs=("event:g96b",),
            ),
        ),
        asset_refs=(asset,),
        event_refs=("event:g96b",),
    )


def test_scene_perspective_and_frame_round_trip_without_audience_metadata() -> None:
    scene = _scene()
    perspective = ActorPerspective(
        perspective_ref="perspective:g96b",
        actor_ref="actor:alice",
        origin=(0.0, 0.0),
        view_radius=10.0,
        allowed_rights=("public",),
    )
    frame = VisualProjectionFrame(
        frame_ref="frame:g96b",
        provider_id="provider:reference-visual",
        provider_version="1.0.0",
        scene_ref=scene.scene_ref,
        snapshot_ref=scene.snapshot_ref,
        snapshot_revision=scene.revision,
        actor_ref=perspective.actor_ref,
        perspective_ref=perspective.perspective_ref,
        status="projected",
        objects=(
            VisualProjectedObject(
                object_ref="object:g96b",
                entity_ref="entity:g96b",
                position=(1.0, 2.0),
                asset_ref=_asset(),
            ),
        ),
        asset_refs=(_asset(),),
        event_refs=scene.event_refs,
        state_hash=scene.state_hash,
    )

    assert VisualSceneState.from_dict(scene.to_dict()) == scene
    assert ActorPerspective.from_dict(perspective.to_dict()) == perspective
    assert VisualProjectionFrame.from_dict(frame.to_dict()) == frame
    assert not hasattr(frame.objects[0], "audience_refs")
    assert frame.projection_hash


def test_visual_health_and_protocol_have_no_canonical_write_surface() -> None:
    health = VisualProviderHealth(
        provider_id="provider:reference-visual",
        version="1.0.0",
        available=True,
        deterministic=True,
        capabilities=("scene-projection", "asset-refs"),
    )
    assert VisualProviderHealth.from_dict(health.to_dict()) == health

    members = {
        name
        for name, _ in inspect.getmembers(VisualWorldProvider, inspect.isfunction)
        if not name.startswith("_")
    }
    assert members == {"health", "project"}
    assert not members.intersection({"append", "apply", "commit", "mutate", "submit"})


def test_non_projected_frame_cannot_contain_visible_objects() -> None:
    with pytest.raises(ContractError, match="non-projected"):
        VisualProjectionFrame(
            frame_ref="frame:g96b:rejected",
            provider_id="provider:g96b",
            provider_version="1",
            scene_ref="scene:g96b",
            snapshot_ref="snapshot:g96b",
            snapshot_revision=0,
            actor_ref="actor:g96b",
            perspective_ref="perspective:g96b",
            status="rejected",
            objects=(
                VisualProjectedObject(
                    object_ref="object:g96b",
                    entity_ref="entity:g96b",
                    position=(0.0, 0.0),
                ),
            ),
            state_hash="statehash:g96b",
        )
