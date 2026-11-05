"""Deployment env wiring for the direct TokenHub T2 panorama adapter."""

from __future__ import annotations

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_api.panorama_tokenhub_runtime import panorama_tokenhub_runtime_from_env


def _set_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "WANXIANG_PANORAMA_TOKENHUB_ENDPOINT",
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/world2-panorama",
    )
    monkeypatch.setenv("WANXIANG_PANORAMA_TOKENHUB_API_KEY", "test-key")
    monkeypatch.setenv(
        "WANXIANG_PANORAMA_TOKENHUB_ARTIFACT_HOSTS",
        "aigc-output-image-file.example,assets.example",
    )


def test_panorama_tokenhub_runtime_is_disabled_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in (
        "WANXIANG_PANORAMA_TOKENHUB_ENDPOINT",
        "WANXIANG_PANORAMA_TOKENHUB_API_KEY",
        "WANXIANG_PANORAMA_TOKENHUB_ARTIFACT_HOSTS",
        "WANXIANG_PANORAMA_ALLOW_NETWORK",
    ):
        monkeypatch.delenv(name, raising=False)

    runtime = panorama_tokenhub_runtime_from_env()

    assert runtime.provider is None
    assert runtime.allow_network is False
    assert runtime.max_cost_units == 0


def test_panorama_tokenhub_runtime_builds_explicit_budgeted_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv("WANXIANG_PANORAMA_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_PANORAMA_MAX_COST_UNITS", "1000000")

    runtime = panorama_tokenhub_runtime_from_env()

    assert runtime.provider is not None
    assert runtime.provider.provider_id == "tencent-tokenhub-panorama"
    assert runtime.provider.provider_version == "hy-world2-panorama"
    assert runtime.provider.presentation_kind == "panorama"
    assert runtime.provider.cost_units_per_asset == 500000
    assert runtime.allow_network is True
    assert runtime.max_cost_units == 1000000


def test_create_app_autoloads_tokenhub_panorama_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv("WANXIANG_PANORAMA_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_PANORAMA_MAX_COST_UNITS", "500000")

    app = create_app(build_reference_runtime())

    assert app.state.panorama_asset_provider is not None
    assert app.state.panorama_asset_provider.presentation_kind == "panorama"
    assert app.state.panorama_asset_allow_network is True
    assert app.state.panorama_asset_max_cost_units == 500000


def test_panorama_tokenhub_runtime_fails_closed_for_partial_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WANXIANG_PANORAMA_ALLOW_NETWORK", "true")
    monkeypatch.delenv("WANXIANG_PANORAMA_TOKENHUB_ENDPOINT", raising=False)
    with pytest.raises(ValueError, match="requires WANXIANG_PANORAMA_TOKENHUB_ENDPOINT"):
        panorama_tokenhub_runtime_from_env()

    _set_runtime(monkeypatch)
    monkeypatch.delenv("WANXIANG_PANORAMA_TOKENHUB_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key"):
        panorama_tokenhub_runtime_from_env()
