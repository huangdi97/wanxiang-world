"""Deployment env wiring for the governed T3 HTTP adapter."""

from __future__ import annotations

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_api.spatial_http_gateway import spatial_http_runtime_from_env


def _set_endpoints(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT",
        "https://gateway.example/spatial/submit",
    )
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT",
        "https://gateway.example/spatial/poll",
    )


def test_spatial_http_runtime_is_disabled_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in (
        "WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT",
        "WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT",
        "WANXIANG_SPATIAL_ALLOW_NETWORK",
    ):
        monkeypatch.delenv(name, raising=False)

    runtime = spatial_http_runtime_from_env()

    assert runtime.provider is None
    assert runtime.allow_network is False
    assert runtime.max_cost_units == 0


def test_spatial_http_runtime_builds_governed_provider_from_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_endpoints(monkeypatch)
    monkeypatch.setenv("WANXIANG_SPATIAL_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_SPATIAL_MAX_COST_UNITS", "11")
    monkeypatch.setenv("WANXIANG_SPATIAL_COST_UNITS", "7")
    monkeypatch.setenv("WANXIANG_SPATIAL_PROVIDER_ID", "provider:world-gateway")
    monkeypatch.setenv("WANXIANG_SPATIAL_PROVIDER_VERSION", "2026-10")
    monkeypatch.setenv("WANXIANG_SPATIAL_ALLOWED_MEDIA_TYPES", "model/gltf-binary,model/ply")

    runtime = spatial_http_runtime_from_env()

    assert runtime.provider is not None
    assert runtime.provider.provider_id == "provider:world-gateway"
    assert runtime.provider.provider_version == "2026-10"
    assert runtime.provider.cost_units_per_job == 7
    assert runtime.provider.allowed_media_types == frozenset({"model/gltf-binary", "model/ply"})
    assert runtime.allow_network is True
    assert runtime.max_cost_units == 11


def test_create_app_autoloads_spatial_http_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_endpoints(monkeypatch)
    monkeypatch.setenv("WANXIANG_SPATIAL_ALLOW_NETWORK", "true")
    monkeypatch.setenv("WANXIANG_SPATIAL_MAX_COST_UNITS", "9")

    app = create_app(build_reference_runtime())

    assert app.state.spatial_asset_provider is not None
    assert app.state.spatial_asset_allow_network is True
    assert app.state.spatial_asset_max_cost_units == 9


def test_spatial_http_runtime_fails_closed_for_partial_or_unsafe_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT",
        "https://gateway.example/spatial/submit",
    )
    monkeypatch.delenv("WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT", raising=False)
    with pytest.raises(ValueError, match="both submit and poll"):
        spatial_http_runtime_from_env()

    _set_endpoints(monkeypatch)
    monkeypatch.setenv("WANXIANG_SPATIAL_ALLOWED_MEDIA_TYPES", "application/octet-stream")
    with pytest.raises(ValueError, match="unsupported media types"):
        spatial_http_runtime_from_env()
