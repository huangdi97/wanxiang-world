"""T3 attachments become Player capability only, never storage identity."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_projection import player_world_detail

from tests.unit.substrate.test_book_scene_plan import package_from_book


def _profile() -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id="profile-spatial",
        world_package_ref="world:spatial",
        scenario_ref="scenario",
        runtime_profile_ref="runtime",
        experience_package_ref="experience",
        projection_profile_ref="projection",
        owner_id="owner",
        display_name="空间世界",
    )


def test_player_world_detail_surfaces_t3_readiness_without_storage_identity() -> None:
    package = package_from_book("spatial", ("机关桥",))
    request = _plan_book_scene_assets(package).scene_requests[0]
    ref = AssetRef(
        asset_id="secret-object-id",
        content_hash="a" * 64,
        size=128,
        content_type="model/gltf-binary",
        rights="source-gated",
    )

    detail = player_world_detail(
        _profile(),
        package,
        include_visual=True,
        spatial_assets={request.stable_key: (ref,)},
    )
    visual = detail["visual"]
    assert isinstance(visual, dict)
    scenes = cast(list[dict[str, object]], visual["scenes"])
    scene = scenes[0]
    assert scene["spatial"] == {
        "ready": True,
        "asset_count": 1,
        "media_types": ["model/gltf-binary"],
    }
    assert "secret-object-id" not in str(detail)
    assert "a" * 64 not in str(detail)


def test_player_world_detail_marks_t3_not_ready_without_attachment() -> None:
    package = package_from_book("spatial-empty", ("港口",))
    detail = player_world_detail(_profile(), package, include_visual=True)
    visual = detail["visual"]
    assert isinstance(visual, dict)
    scenes = cast(list[dict[str, object]], visual["scenes"])
    assert scenes[0]["spatial"] == {
        "ready": False,
        "asset_count": 0,
        "media_types": [],
    }
