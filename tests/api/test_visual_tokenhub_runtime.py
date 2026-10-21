"""Deployment env wiring for the direct TokenHub Hy-Image T1 adapter."""

from __future__ import annotations

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_api.visual_tokenhub_runtime import visual_tokenhub_runtime_from_env


def _set_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "WANXIANG_VISUAL_TOKENHUB_ENDPOINT",
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/v3-generation",
    )
    monkeypatch.setenv("WANXIANG_VISUAL_TOKENHUB_API_KEY", "test-key")
    monkeypatch.setenv(
        "WANXIANG_VISUAL_TOKENHUB_ARTIFACT_HOSTS",
        "aigc-output-image-file.example,assets.example",
    )


def test_visual_tokenhub_runtime_is_disabled_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in (
        "WANXIANG_VISUAL_TOKENHUB_ENDPOINT",
        "WANXIANG_VISUAL_TOKENHUB_API_KEY",
        "WANXIANG_VISUAL_TOKENHUB_ARTIFACT_HOSTS",
        "WANXIANG_VISUAL_ALLOW_NETWORK",
    ):
        monkeypatch.delenv(name, raising=False)

    runtime = visual_tokenhub_runtime_from_env()

    assert runtime.provider is None
    assert runtime.allow_network is False
    assert runtime.max_cost_units == 0


def test_visual_tokenhub_runtime_builds_current_budgeted_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv("WANXIANG_VISUAL_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_VISUAL_MAX_COST_UNITS", "60000")

    runtime = visual_tokenhub_runtime_from_env()

    assert runtime.provider is not None
    assert runtime.provider.provider_id == "tencent-tokenhub-image"
    assert runtime.provider.provider_version == "hy-image-v3"
    assert runtime.provider.cost_units_per_asset == 20000
    assert runtime.allow_network is True
    assert runtime.max_cost_units == 60000


def test_create_app_autoloads_direct_tokenhub_t1_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv("WANXIANG_VISUAL_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_VISUAL_MAX_COST_UNITS", "20000")

    app = create_app(build_reference_runtime())

    assert app.state.visual_asset_provider is not None
    assert app.state.visual_asset_provider.provider_id == "tencent-tokenhub-image"
    assert app.state.visual_asset_allow_network is True
    assert app.state.visual_asset_max_cost_units == 20000


def test_visual_backend_configuration_rejects_tokenhub_and_http_gateway_together(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv(
        "WANXIANG_VISUAL_HTTP_ENDPOINT",
        "https://gateway.example/scene",
    )

    with pytest.raises(ValueError, match="not both"):
        create_app(build_reference_runtime())


def test_visual_tokenhub_runtime_fails_closed_for_missing_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.delenv("WANXIANG_VISUAL_TOKENHUB_API_KEY", raising=False)

    with pytest.raises(ValueError, match="API key"):
        visual_tokenhub_runtime_from_env()
