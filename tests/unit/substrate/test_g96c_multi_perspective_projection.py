"""G96C: actor views filter private knowledge, rights and occlusion."""

from __future__ import annotations

from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.world_lab import (
    ActorPerspective,
    PerspectiveVisualProvider,
    VisualSceneObject,
    VisualSceneState,
    VisualWorldProvider,
)


def _private_asset() -> AssetRef:
    return AssetRef(
        asset_id="asset:g96c:private",
        content_hash="hash:g96c:private",
        size=7,
        content_type="image/png",
        rights="private",
    )


def _scene() -> VisualSceneState:
    asset = _private_asset()
    return VisualSceneState(
        scene_ref="scene:g96c",
        snapshot_ref="snapshot:g96c",
        world_instance_ref="world:g96c",
        branch_ref="branch:g96c",
        revision=4,
        world_time_ticks=12,
        state_hash="statehash:g96c",
        objects=(
            VisualSceneObject(
                object_ref="object:g96c:wall",
                entity_ref="entity:g96c:wall",
                position=(1.5, 0.0),
                occlusion_radius=0.35,
                event_refs=("event:g96c:wall",),
            ),
            VisualSceneObject(
                object_ref="object:g96c:far",
                entity_ref="entity:g96c:far",
                position=(3.0, 0.0),
                event_refs=("event:g96c:far",),
            ),
            VisualSceneObject(
                object_ref="object:g96c:alice",
                entity_ref="entity:g96c:alice-secret",
                position=(2.0, 1.0),
                audience_refs=("actor:alice",),
                event_refs=("event:g96c:alice-private",),
            ),
            VisualSceneObject(
                object_ref="object:g96c:bob",
                entity_ref="entity:g96c:bob-secret",
                position=(2.0, -1.0),
                audience_refs=("actor:bob",),
                event_refs=("event:g96c:bob-private",),
            ),
            VisualSceneObject(
                object_ref="object:g96c:asset",
                entity_ref="entity:g96c:private-asset",
                position=(1.0, -1.0),
                asset_ref=asset,
                event_refs=("event:g96c:asset-private",),
            ),
        ),
        asset_refs=(asset,),
        event_refs=(
            "event:g96c:wall",
            "event:g96c:far",
            "event:g96c:alice-private",
            "event:g96c:bob-private",
            "event:g96c:asset-private",
        ),
    )


def _perspective(actor_ref: str) -> ActorPerspective:
    return ActorPerspective(
        perspective_ref=f"perspective:g96c:{actor_ref}",
        actor_ref=actor_ref,
        origin=(0.0, 0.0),
        view_radius=10.0,
        allowed_rights=("public",),
    )


def test_actor_views_isolate_private_knowledge_and_apply_filters() -> None:
    provider = PerspectiveVisualProvider("provider:g96c", "1.0.0")
    scene = _scene()
    alice = provider.project(scene, _perspective("actor:alice"))
    bob = provider.project(scene, _perspective("actor:bob"))

    alice_refs = {item.object_ref for item in alice.objects}
    bob_refs = {item.object_ref for item in bob.objects}
    assert "object:g96c:alice" in alice_refs
    assert "object:g96c:bob" not in alice_refs
    assert "object:g96c:bob" in bob_refs
    assert "object:g96c:alice" not in bob_refs
    assert "object:g96c:asset" not in alice_refs | bob_refs
    assert "object:g96c:far" not in alice_refs | bob_refs
    assert "event:g96c:alice-private" in alice.event_refs
    assert "event:g96c:alice-private" not in bob.event_refs
    assert "event:g96c:bob-private" in bob.event_refs
    assert "event:g96c:bob-private" not in alice.event_refs
    assert all("audience_refs" not in item.to_dict() for item in alice.objects + bob.objects)
    assert alice.frame_ref != bob.frame_ref
    assert alice.projection_hash != bob.projection_hash
    assert provider.project(scene, _perspective("actor:alice")) == alice


def test_provider_is_projection_only_and_protocol_conforming() -> None:
    provider = PerspectiveVisualProvider("provider:g96c", "1.0.0")
    assert isinstance(provider, VisualWorldProvider)
    assert provider.health().capabilities == (
        "actor-perspective",
        "occlusion-filter",
        "rights-filter",
    )
    assert not hasattr(provider, "commit")
    assert not hasattr(provider, "mutate")
