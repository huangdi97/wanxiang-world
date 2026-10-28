"""Deferred T3 anchors remain reachable in World Detail with a free T0 backdrop."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from tests.unit.substrate.test_book_scene_plan import package_from_book
from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_scene_visual import _render_visual_plan
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_world_detail import player_world_detail


def _profile() -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id="profile-deferred-spatial",
        world_package_ref="world:deferred-spatial",
        scenario_ref="scenario",
        runtime_profile_ref="runtime",
        experience_package_ref="experience",
        projection_profile_ref="projection",
        owner_id="owner",
        display_name="延迟空间世界",
    )


def test_t3_only_deferred_place_gets_projection_backdrop_and_detail_entry() -> None:
    places = tuple(f"地点-{index}" for index in range(1, 7))
    package = package_from_book("deferred-spatial-detail", places)
    initial_plan = _plan_book_scene_assets(package)
    initial_assets = _render_visual_plan(initial_plan)
    deferred_place = places[-1]
    assert deferred_place not in {asset.place_name for asset in initial_assets}

    targeted = _plan_book_scene_assets(
        package,
        max_preview_scenes=1,
        preferred_places=(deferred_place,),
    )
    scene_key = targeted.scene_requests[0].stable_key
    spatial_ref = AssetRef(
        asset_id="derived-spatial-object",
        content_hash="d" * 64,
        size=256,
        content_type="model/ply",
        rights="source-gated",
    )

    detail = player_world_detail(
        _profile(),
        package,
        include_visual=True,
        visual_assets=initial_assets,
        spatial_assets={scene_key: (spatial_ref,)},
    )
    visual = cast(dict[str, object], detail["visual"])
    rows = cast(list[dict[str, object]], visual["places"])
    deferred_row = next(row for row in rows if row["name"] == deferred_place)
    scenes = cast(list[dict[str, object]], visual["scenes"])
    deferred_scene = next(scene for scene in scenes if scene["place_name"] == deferred_place)

    assert deferred_row["generated"] is True
    assert deferred_row["tier"] == "T3"
    assert deferred_scene["tier"] == "T3"
    assert deferred_scene["media_type"] == "image/svg+xml"
    assert str(deferred_scene["data_uri"]).startswith("data:image/svg+xml;base64,")
    spatial = cast(dict[str, object], deferred_scene["spatial"])
    assert spatial["ready"] is True
    assert spatial["asset_count"] == 1
    assert len(scenes) == len(initial_assets) + 1
    assert "derived-spatial-object" not in str(detail)
