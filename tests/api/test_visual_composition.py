"""Visual generation dependencies are explicit and fail closed at app composition."""

from __future__ import annotations

import pytest
from wanxiang_api.app import create_app
from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider


def test_visual_composition_defaults_to_local_zero_budget_without_provider() -> None:
    app = create_app()

    assert isinstance(app.state.visual_asset_cache, VisualAssetCache)
    assert app.state.visual_asset_provider is None
    assert app.state.visual_asset_allow_network is False
    assert app.state.visual_asset_max_cost_units == 0


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
