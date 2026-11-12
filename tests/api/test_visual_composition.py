"""Visual generation dependencies are explicit and fail closed at app composition."""

from __future__ import annotations

import pytest
from wanxiang_api.app import create_app
from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider


def test_visual_composition_defaults_to_local_zero_budget_without_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("WANXIANG_VISUAL_HTTP_ENDPOINT", raising=False)
    monkeypatch.delenv("WANXIANG_VISUAL_ALLOW_NETWORK", raising=False)
    app = create_app()

    assert isinstance(app.state.visual_asset_cache, VisualAssetCache)
    assert app.state.visual_asset_provider is None
    assert app.state.visual_asset_allow_network is False
    assert app.state.visual_asset_max_cost_units == 0
    assert app.state.visual_asset_max_deferred_generations == 24


def test_visual_composition_accepts_explicit_provider_cache_and_budget() -> None:
    cache = VisualAssetCache()
    provider = SceneImageProvider()

    app = create_app(
        visual_cache=cache,
        visual_provider=provider,
        visual_allow_network=True,
        visual_max_cost_units=7,
    )

    assert app.state.visual_asset_cache is cache
    assert app.state.visual_asset_provider is provider
    assert app.state.visual_asset_allow_network is True
    assert app.state.visual_asset_max_cost_units == 7


def test_visual_composition_rejects_unsafe_or_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="requires an injected visual_provider"):
        create_app(visual_allow_network=True)
    with pytest.raises(ValueError, match="must be non-negative"):
        create_app(visual_max_cost_units=-1)


def test_visual_composition_builds_http_provider_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "WANXIANG_VISUAL_HTTP_ENDPOINT",
        "https://images.internal.example/v1/scene",
    )
    monkeypatch.setenv("WANXIANG_VISUAL_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_VISUAL_MAX_COST_UNITS", "9")
    monkeypatch.setenv("WANXIANG_VISUAL_COST_UNITS", "3")
    monkeypatch.setenv("WANXIANG_VISUAL_PROVIDER_ID", "gateway:test")
    monkeypatch.setenv("WANXIANG_VISUAL_PROVIDER_VERSION", "2026-10")
    monkeypatch.setenv("WANXIANG_VISUAL_MAX_DEFERRED_GENERATIONS", "5")

    app = create_app()

    assert app.state.visual_asset_provider is not None
    assert app.state.visual_asset_provider.provider_id == "gateway:test"
    assert app.state.visual_asset_provider.provider_version == "2026-10"
    assert app.state.visual_asset_provider.cost_units_per_asset == 3
    assert app.state.visual_asset_allow_network is True
    assert app.state.visual_asset_max_cost_units == 9
    assert app.state.visual_asset_max_deferred_generations == 5


def test_visual_composition_rejects_remote_http_or_network_without_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WANXIANG_VISUAL_HTTP_ENDPOINT", "http://example.com/generate")
    with pytest.raises(ValueError, match="HTTPS or loopback HTTP"):
        create_app()

    monkeypatch.delenv("WANXIANG_VISUAL_HTTP_ENDPOINT")
    monkeypatch.setenv("WANXIANG_VISUAL_ALLOW_NETWORK", "true")
    with pytest.raises(ValueError, match="requires WANXIANG_VISUAL_HTTP_ENDPOINT"):
        create_app()
