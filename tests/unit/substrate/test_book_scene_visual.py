"""Generic source-to-visual assets are deterministic and book-agnostic."""

# pyright: reportPrivateUsage=false

from wanxiang_substrate.assets.book_scene_plan import (
    _SourceSceneRequest,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_scene_visual import (
    _ProceduralSvgSceneProvider,
    _SceneVisualCache,
    _render_visual_plan,
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


def _plan(*requests: _SourceSceneRequest) -> _SourceVisualPlan:
    return _SourceVisualPlan(
        package_id="world:test",
        source_digest="a" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=requests,
        deferred_scene_count=0,
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

    def produce(self, request: _SourceSceneRequest):
        return _ProceduralSvgSceneProvider().produce(request)


def test_network_and_cost_are_denied_until_explicitly_authorized() -> None:
    plan = _plan(_request("远方", "remote"))
    provider = _RemoteLikeProvider()
    import pytest

    with pytest.raises(ValueError, match="allow_network"):
        _render_visual_plan(plan, provider=provider)
    with pytest.raises(ValueError, match="exceeds budget"):
        _render_visual_plan(plan, provider=provider, allow_network=True, max_cost_units=1)

    rendered = _render_visual_plan(
        plan,
        provider=provider,
        allow_network=True,
        max_cost_units=2,
    )
    assert rendered[0].place_name == "远方"


def test_visual_cache_reuses_content_addressed_asset_identity() -> None:
    plan = _plan(_request("旧城", "old-city"))
    visual = _render_visual_plan(plan)[0]
    cache = _SceneVisualCache()
    first = cache.store_visual(visual)
    second = cache.store_visual(visual)

    assert first == second
    assert first.asset_ref.asset_id == second.asset_ref.asset_id
    assert first.asset_ref.content_hash == visual.content_sha256
    assert first.asset_ref.rights == "source-gated"
    assert cache.store.get(first.asset_ref) == visual.content
