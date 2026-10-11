"""Deployment configuration for the vendor-neutral T1 HTTP gateway."""

from __future__ import annotations

import os
from dataclasses import dataclass

from wanxiang_substrate.assets.book_scene_http_gateway import build_http_scene_provider
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider


def _bool_env(name: str, *, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    value = raw.strip().casefold()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean flag")


def _int_env(name: str, *, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


@dataclass(frozen=True, slots=True)
class VisualHttpRuntime:
    provider: SceneImageProvider | None
    allow_network: bool
    max_cost_units: int


def visual_http_runtime_from_env() -> VisualHttpRuntime:
    endpoint = os.environ.get("WANXIANG_VISUAL_HTTP_ENDPOINT", "").strip()
    allow_network = _bool_env("WANXIANG_VISUAL_ALLOW_NETWORK")
    max_cost_units = _int_env("WANXIANG_VISUAL_MAX_COST_UNITS", default=0)
    if not endpoint:
        if allow_network:
            raise ValueError(
                "WANXIANG_VISUAL_ALLOW_NETWORK requires WANXIANG_VISUAL_HTTP_ENDPOINT"
            )
        return VisualHttpRuntime(None, False, max_cost_units)
    provider = build_http_scene_provider(
        endpoint=endpoint,
        bearer_token=os.environ.get("WANXIANG_VISUAL_HTTP_BEARER_TOKEN", ""),
        provider_id=(
            os.environ.get("WANXIANG_VISUAL_PROVIDER_ID", "http-json-image").strip()
            or "http-json-image"
        ),
        provider_version=(
            os.environ.get("WANXIANG_VISUAL_PROVIDER_VERSION", "1").strip() or "1"
        ),
        timeout_seconds=float(
            _int_env("WANXIANG_VISUAL_HTTP_TIMEOUT_SECONDS", default=60)
        ),
        cost_units_per_asset=_int_env("WANXIANG_VISUAL_COST_UNITS", default=1),
        private_safe=_bool_env("WANXIANG_VISUAL_PRIVATE_SAFE"),
    )
    return VisualHttpRuntime(provider, allow_network, max_cost_units)
