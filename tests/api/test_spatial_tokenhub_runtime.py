"""Deployment env wiring for the direct TokenHub Hy-World T3 adapter."""

from __future__ import annotations

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_api.spatial_tokenhub_runtime import spatial_tokenhub_runtime_from_env


def _set_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_TOKENHUB_SUBMIT_ENDPOINT",
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/world2-scene",
    )
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_TOKENHUB_TASKS_ENDPOINT",
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/tasks",
    )
    monkeypatch.setenv("WANXIANG_SPATIAL_TOKENHUB_API_KEY", "test-key")
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_TOKENHUB_ARTIFACT_HOSTS",
        "assets.example,cdn.example",
    )


def test_spatial_tokenhub_runtime_is_disabled_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in (
        "WANXIANG_SPATIAL_TOKENHUB_SUBMIT_ENDPOINT",
        "WANXIANG_SPATIAL_TOKENHUB_TASKS_ENDPOINT",
        "WANXIANG_SPATIAL_TOKENHUB_API_KEY",
        "WANXIANG_SPATIAL_TOKENHUB_ARTIFACT_HOSTS",
    ):
        monkeypatch.delenv(name, raising=False)

    runtime = spatial_tokenhub_runtime_from_env()

    assert runtime.provider is None


def test_spatial_tokenhub_runtime_builds_budgeted_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv("WANXIANG_SPATIAL_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_SPATIAL_MAX_COST_UNITS", "16000000")

    runtime = spatial_tokenhub_runtime_from_env()

    assert runtime.provider is not None
    assert runtime.provider.provider_id == "tencent-tokenhub-spatial"
    assert runtime.provider.provider_version == "hy-world2-scene"
    assert runtime.provider.cost_units_per_job == 8000000
    assert runtime.allow_network is True
    assert runtime.max_cost_units == 16000000


def test_create_app_prefers_direct_tokenhub_spatial_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv("WANXIANG_SPATIAL_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_SPATIAL_MAX_COST_UNITS", "8000000")

    app = create_app(build_reference_runtime())

    assert app.state.spatial_asset_provider is not None
    assert app.state.spatial_asset_provider.provider_id == "tencent-tokenhub-spatial"
    assert app.state.spatial_asset_allow_network is True
    assert app.state.spatial_asset_max_cost_units == 8000000


def test_spatial_tokenhub_runtime_fails_closed_for_partial_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_TOKENHUB_SUBMIT_ENDPOINT",
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/world2-scene",
    )
    monkeypatch.delenv("WANXIANG_SPATIAL_TOKENHUB_TASKS_ENDPOINT", raising=False)
    with pytest.raises(ValueError, match="both submit and tasks endpoints"):
        spatial_tokenhub_runtime_from_env()

    _set_runtime(monkeypatch)
    monkeypatch.delenv("WANXIANG_SPATIAL_TOKENHUB_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key"):
        spatial_tokenhub_runtime_from_env()


def test_create_app_rejects_ambiguous_spatial_backend_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT",
        "https://gateway.example/spatial/submit",
    )
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT",
        "https://gateway.example/spatial/poll",
    )

    with pytest.raises(ValueError, match="not both"):
        create_app(build_reference_runtime())


def test_direct_tokenhub_does_not_mask_partial_http_gateway_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_runtime(monkeypatch)
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT",
        "https://gateway.example/spatial/submit",
    )
    monkeypatch.delenv("WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT", raising=False)

    with pytest.raises(ValueError, match="not both"):
        create_app(build_reference_runtime())
