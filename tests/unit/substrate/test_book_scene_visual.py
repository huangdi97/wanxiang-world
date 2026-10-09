"""Generic source-to-visual assets are deterministic and book-agnostic."""

# pyright: reportPrivateUsage=false

import hashlib

import pytest
from wanxiang_substrate.assets.book_scene_plan import (
    _SourceSceneRequest,
    _SourceTopologyRelation,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_scene_visual import (
    _materialize_visual_plan,
    _ProceduralSvgSceneProvider,
    _render_visual_plan,
    _render_world_atlas,
    _SceneVisualAsset,
    _VisualAssetCache,
)
from wanxiang_substrate.assets.foundry import SemanticSceneSpec


def _request(place: str, key: str) -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name=place,
        stable_key=key,
        spec=SemanticSceneSpec(
            spec_id=f"scene-{key}",
            semantic_id=f"place:{key}",
            kind="illustrated-environment",
            requirements=(f"source_place_name:{place}",),
        ),
        cache_key=f"cache-{key}",
    )


def _plan(
    *requests: _SourceSceneRequest,
    external_processing_allowed: bool = False,
    delivery_rights: str = "source-gated",
) -> _SourceVisualPlan:
    return _SourceVisualPlan(
        package_id="world:test",
        source_digest="a" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=requests,
        deferred_scene_count=0,
        delivery_rights=delivery_rights,
        external_processing_allowed=external_processing_allowed,
    )


def test_two_unrelated_places_use_same_provider_but_different_visuals() -> None:
    provider = _ProceduralSvgSceneProvider()
    garden = provider.produce(_request("园林", "garden"))
    fortress = provider.produce(_request("堡垒", "fortress"))

    assert garden.provider_id == fortress.provider_id == "procedural-svg-v1"
    assert garden.media_type == fortress.media_type == "image/svg+xml"
    assert garden.content != fortress.content
    assert garden.content_sha256 != fortress.content_sha256
    assert "园林".encode() in garden.content
    assert "堡垒".encode() in fortress.content
    assert garden.data_uri().startswith("data:image/svg+xml;base64,")
    assert garden.illustrative is True


def test_render_visual_plan_is_deterministic_and_cost_free_by_construction() -> None:
    study = _request("书房", "study")
    dock = _request("码头", "dock")
    shared_style = "story-style"
    study = _SourceSceneRequest(
        study.place_name,
        study.stable_key,
        study.spec,
        study.cache_key,
        style_key=shared_style,
    )
    dock = _SourceSceneRequest(
        dock.place_name,
        dock.stable_key,
        dock.spec,
        dock.cache_key,
        style_key=shared_style,
    )
    plan = _plan(study, dock)
    first = _render_visual_plan(plan)
    second = _render_visual_plan(plan)

    assert first == second
    assert [item.place_name for item in first] == ["书房", "码头"]
    assert len({item.content_sha256 for item in first}) == 2
    assert {item.style_key for item in first} == {shared_style}


def test_non_ready_plan_never_generates_pixels() -> None:
    blocked = _SourceVisualPlan(
        package_id="world:blocked",
        source_digest="b" * 64,
        status="RIGHTS_BLOCKED",
        scene_requests=(_request("私有地点", "private"),),
        deferred_scene_count=0,
    )
    assert _render_visual_plan(blocked) == ()


class _RemoteLikeProvider:
    provider_id = "remote-test"
    requires_network = True
    cost_units_per_asset = 2
    private_safe = False

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        base = _ProceduralSvgSceneProvider().produce(request)
        return _SceneVisualAsset(
            scene_key=base.scene_key,
            place_name=base.place_name,
            provider_id=self.provider_id,
            media_type=base.media_type,
            content=base.content,
            content_sha256=hashlib.sha256(base.content).hexdigest(),
            cache_key=f"{request.cache_key}:{self.provider_id}",
            illustrative=base.illustrative,
            style_key=base.style_key,
        )


def test_network_and_cost_are_denied_until_explicitly_authorized() -> None:
    plan = _plan(
        _request("远方", "remote"),
        external_processing_allowed=True,
    )
    provider = _RemoteLikeProvider()

    with pytest.raises(ValueError, match="allow_network"):
        _render_visual_plan(plan, provider=provider)
    with pytest.raises(ValueError, match="exceeds budget"):
        _render_visual_plan(plan, provider=provider, allow_network=True, max_cost_units=1)
    with pytest.raises(ValueError, match="private-safe"):
        _render_visual_plan(
            plan,
            provider=provider,
            allow_network=True,
            max_cost_units=2,
            private_source=True,
        )

    rendered = _render_visual_plan(
        plan,
        provider=provider,
        allow_network=True,
        max_cost_units=2,
    )
    assert rendered[0].place_name == "远方"


def test_visual_cache_reuses_content_addressed_asset_identity_and_avoids_provider_call() -> None:
    plan = _plan(_request("旧城", "old-city"))
    cache = _VisualAssetCache()

    first = _materialize_visual_plan(plan, cache=cache)
    second = _materialize_visual_plan(plan, cache=cache)

    assert first.provider_calls == 1
    assert first.cache_hits == 0
    assert second.provider_calls == 0
    assert second.cache_hits == 1
    assert first.assets == second.assets
    assert first.asset_refs == second.asset_refs
    assert first.asset_refs[0].content_hash == first.assets[0].content_sha256
    assert first.asset_refs[0].rights == "source-gated"
    assert cache.store.get(first.asset_refs[0]) == first.assets[0].content


class _BadDigestProvider(_RemoteLikeProvider):
    requires_network = False
    cost_units_per_asset = 0

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        good = super().produce(request)
        return _SceneVisualAsset(
            scene_key=good.scene_key,
            place_name=good.place_name,
            provider_id=good.provider_id,
            media_type=good.media_type,
            content=good.content,
            content_sha256="0" * 64,
            cache_key=good.cache_key,
        )


def test_provider_output_integrity_is_verified_before_storage() -> None:
    with pytest.raises(ValueError, match="invalid content digest"):
        _materialize_visual_plan(_plan(_request("荒原", "bad")), provider=_BadDigestProvider())


def test_remote_provider_is_blocked_by_source_rights_even_with_network_permission() -> None:
    with pytest.raises(ValueError, match="external visual processing"):
        _render_visual_plan(
            _plan(_request("私密地点", "private-remote")),
            provider=_RemoteLikeProvider(),
            allow_network=True,
            max_cost_units=2,
        )


def test_world_atlas_uses_places_and_only_source_grounded_relations() -> None:
    plan = _SourceVisualPlan(
        package_id="world:atlas",
        source_digest="c" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("园林", "garden"), _request("书房", "study")),
        deferred_scene_count=1,
        topology_relations=(
            _SourceTopologyRelation("园林", "书房", "route", ("book#1",), 0.8),
        ),
        place_names=("园林", "书房", "码头"),
    )
    atlas = _render_world_atlas(plan)

    assert atlas is not None
    assert atlas.provider_id == "narrative-atlas-v1"
    assert atlas.media_type == "image/svg+xml"
    assert "园林".encode() in atlas.content
    assert "书房".encode() in atlas.content
    assert "码头".encode() in atlas.content
    assert b"<line " in atlas.content
    assert "关系不等于地理坐标".encode() in atlas.content
