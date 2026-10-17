"""T3 attachments become Player capability only, never storage identity."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

from tests.unit.substrate.test_book_scene_plan import package_from_book
from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_spatial_types import _SpatialProjectionFrame
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_projection import player_world_detail
from wanxiang_substrate.playable.service_visual import (
    _attach_spatial_assets,
    _source_scene_key_allowed,
)


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
    assert scene["projection_only"] is True
    assert scene["spatial"] == {
        "ready": True,
        "projection_only": True,
        "asset_count": 1,
        "media_types": ["model/gltf-binary"],
    }
    assert "secret-object-id" not in str(detail)
    assert "a" * 64 not in str(detail)
    places = cast(list[dict[str, object]], visual["places"])
    assert places[0]["tier"] == "T3"


def test_player_world_detail_marks_t3_not_ready_without_attachment() -> None:
    package = package_from_book("spatial-empty", ("港口",))
    detail = player_world_detail(_profile(), package, include_visual=True)
    visual = detail["visual"]
    assert isinstance(visual, dict)
    scenes = cast(list[dict[str, object]], visual["scenes"])
    assert scenes[0]["spatial"] == {
        "ready": False,
        "projection_only": True,
        "asset_count": 0,
        "media_types": [],
    }


def test_t3_anchor_may_target_a_deferred_source_place() -> None:
    places = tuple(f"地点-{index}" for index in range(1, 9))
    package = package_from_book("spatial-long", places)
    initial = _plan_book_scene_assets(package)
    assert initial.deferred_scene_count == 5

    deferred_place = places[-1]
    targeted = _plan_book_scene_assets(
        package,
        max_preview_scenes=1,
        preferred_places=(deferred_place,),
    )
    deferred_scene_key = targeted.scene_requests[0].stable_key

    assert deferred_place not in {item.place_name for item in initial.scene_requests}
    assert _source_scene_key_allowed(package, deferred_scene_key)
    assert not _source_scene_key_allowed(package, "not-a-source-scene")


def test_spatial_attachment_cannot_upgrade_source_gated_rights_to_public() -> None:
    package = package_from_book("spatial-private", ("密室",))
    request = _plan_book_scene_assets(package).scene_requests[0]
    service = cast(
        PlayableService,
        SimpleNamespace(
            _packages={"profile": package},
            _spatial_asset_refs={},
            _spatial_projection_frames={},
        ),
    )
    public_ref = AssetRef(
        asset_id="public-object",
        content_hash="b" * 64,
        size=64,
        content_type="model/gltf-binary",
        rights="public",
    )
    gated_ref = AssetRef(
        asset_id="gated-object",
        content_hash="c" * 64,
        size=64,
        content_type="model/gltf-binary",
        rights="source-gated",
    )

    try:
        _attach_spatial_assets(service, "profile", request.stable_key, (public_ref,))
    except ValueError as exc:
        assert "rights" in str(exc)
    else:
        raise AssertionError("public T3 attachment must not widen source-gated rights")

    _attach_spatial_assets(service, "profile", request.stable_key, (gated_ref,))
    assert service._spatial_asset_refs["profile"][request.stable_key] == (gated_ref,)


def test_player_world_detail_projects_verified_t3_frame_without_storage_identity() -> None:
    package = package_from_book("spatial-frame", ("钟楼",))
    request = _plan_book_scene_assets(package).scene_requests[0]
    ref = AssetRef(
        asset_id="private-object",
        content_hash="d" * 64,
        size=256,
        content_type="model/ply",
        rights="source-gated",
    )
    frame = _SpatialProjectionFrame(
        up=(0.0, 1.0, 0.0),
        forward=(0.0, 0.0, -1.0),
        center=(1.0, 2.0, 3.0),
        scale=0.25,
        convention="provider-frame-v1",
    )

    detail = player_world_detail(
        _profile(),
        package,
        include_visual=True,
        spatial_assets={request.stable_key: (ref,)},
        spatial_frames={request.stable_key: frame},
    )

    visual = cast(dict[str, object], detail["visual"])
    scene = cast(list[dict[str, object]], visual["scenes"])[0]
    spatial = cast(dict[str, object], scene["spatial"])
    assert spatial["projection_only"] is True
    assert spatial["projection_frame"] == {
        "up": [0.0, 1.0, 0.0],
        "forward": [0.0, 0.0, -1.0],
        "center": [1.0, 2.0, 3.0],
        "scale": 0.25,
        "convention": "provider-frame-v1",
    }
    assert "private-object" not in str(spatial)
    assert "d" * 64 not in str(spatial)
