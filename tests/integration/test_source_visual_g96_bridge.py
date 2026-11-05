"""Source-to-visual assets reuse the existing G96 projection boundary."""

# pyright: reportPrivateUsage=false

from wanxiang_substrate.assets.book_scene_plan import (
    _SourceSceneRequest,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_scene_projection import _visual_scene_state_from_book_assets
from wanxiang_substrate.assets.book_scene_visual import _materialize_visual_plan
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.world_lab import ActorPerspective, ReferenceVisualProvider


def _request(place: str, key: str) -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name=place,
        stable_key=key,
        spec=SemanticSceneSpec(
            spec_id=f"scene-{key}",
            semantic_id=f"place:{key}",
            kind="illustrated-environment",
        ),
        cache_key=f"cache-{key}",
    )


def test_generated_book_assets_project_through_existing_visual_provider_abi() -> None:
    plan = _SourceVisualPlan(
        package_id="world:bridge",
        source_digest="d" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("园林", "garden"), _request("书房", "study")),
        deferred_scene_count=0,
    )
    materialized = _materialize_visual_plan(plan)
    scene = _visual_scene_state_from_book_assets(
        plan,
        materialized.asset_refs,
        snapshot_ref="snapshot:book-visual",
        world_instance_ref="world:book-visual",
        branch_ref="branch:main",
        revision=4,
        world_time_ticks=21,
        state_hash="statehash:book-visual",
    )
    perspective = ActorPerspective(
        perspective_ref="perspective:reader",
        actor_ref="actor:reader",
        origin=(0.0, 0.0),
        view_radius=10.0,
        allowed_rights=("source-gated",),
    )
    provider = ReferenceVisualProvider("provider:reference-visual", "1.0.0")
    frame = provider.project(scene, perspective)

    assert frame.status == "projected"
    assert frame.projection_only is True
    assert len(frame.objects) == 2
    assert frame.asset_refs == tuple(
        sorted(materialized.asset_refs, key=lambda item: item.asset_id)
    )
    assert frame.snapshot_revision == 4
    assert frame.state_hash == "statehash:book-visual"
