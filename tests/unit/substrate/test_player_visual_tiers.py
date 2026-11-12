"""Player visual fidelity tiers reflect projection capability, never Canon truth."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
from typing import cast

from tests.unit.substrate.test_book_scene_plan import package_from_book
from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_scene_types import _SceneVisualAsset
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_world_detail import player_world_detail


def _profile() -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id="profile-tier",
        world_package_ref="world:tier",
        scenario_ref="scenario",
        runtime_profile_ref="runtime",
        experience_package_ref="experience",
        projection_profile_ref="projection",
        owner_id="owner",
        display_name="层级世界",
    )


def _panorama(scene_key: str) -> _SceneVisualAsset:
    content = b"panorama-fixture"
    return _SceneVisualAsset(
        scene_key=scene_key,
        place_name="观景台",
        provider_id="provider:panorama",
        media_type="image/webp",
        content=content,
        content_sha256=hashlib.sha256(content).hexdigest(),
        cache_key="cache-panorama",
        provider_version="2026-10",
        presentation_kind="panorama",
    )


def test_panorama_projects_t2_and_verified_spatial_attachment_overrides_it() -> None:
    package = package_from_book("tier-panorama", ("观景台",))
    request = _plan_book_scene_assets(package).scene_requests[0]
    panorama = _panorama(request.stable_key)

    detail = player_world_detail(
        _profile(),
        package,
        include_visual=True,
        visual_assets=(panorama,),
    )
    visual = cast(dict[str, object], detail["visual"])
    place = cast(list[dict[str, object]], visual["places"])[0]
    scene = cast(list[dict[str, object]], visual["scenes"])[0]
    assert place["tier"] == "T2"
    assert scene["tier"] == "T2"
    assert scene["presentation_kind"] == "panorama"

    spatial_ref = AssetRef(
        asset_id="spatial",
        content_hash="a" * 64,
        size=128,
        content_type="model/ply",
        rights="source-gated",
    )
    upgraded = player_world_detail(
        _profile(),
        package,
        include_visual=True,
        visual_assets=(panorama,),
        spatial_assets={request.stable_key: (spatial_ref,)},
    )
    upgraded_visual = cast(dict[str, object], upgraded["visual"])
    upgraded_place = cast(list[dict[str, object]], upgraded_visual["places"])[0]
    upgraded_scene = cast(list[dict[str, object]], upgraded_visual["scenes"])[0]
    assert upgraded_place["tier"] == "T3"
    assert upgraded_scene["tier"] == "T3"
