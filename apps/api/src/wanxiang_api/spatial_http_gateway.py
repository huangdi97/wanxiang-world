"""Deployment configuration for the vendor-neutral T3 HTTP gateway."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
from dataclasses import dataclass

from wanxiang_substrate.spatial import (
    SpatialGenerationProvider,
    build_http_spatial_provider,
)

from wanxiang_api.visual_http_gateway import _bool_env, _int_env

_KNOWN_MEDIA_TYPES = frozenset(
    {
        "application/x-ply",
        "image/jpeg",
        "image/png",
        "image/webp",
        "model/gltf-binary",
        "model/ply",
    }
)


@dataclass(frozen=True, slots=True)
class SpatialHttpRuntime:
    provider: SpatialGenerationProvider | None
    allow_network: bool
    max_cost_units: int


def _media_types_env() -> frozenset[str]:
    raw = os.environ.get(
        "WANXIANG_SPATIAL_ALLOWED_MEDIA_TYPES",
        "model/gltf-binary,application/x-ply,model/ply",
    )
    values = frozenset(item.strip() for item in raw.split(",") if item.strip())
    if not values or not values.issubset(_KNOWN_MEDIA_TYPES):
        raise ValueError(
            "WANXIANG_SPATIAL_ALLOWED_MEDIA_TYPES contains unsupported media types"
        )
    return values


def spatial_http_runtime_from_env() -> SpatialHttpRuntime:
    submit_endpoint = os.environ.get("WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT", "").strip()
    poll_endpoint = os.environ.get("WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT", "").strip()
    allow_network = _bool_env("WANXIANG_SPATIAL_ALLOW_NETWORK")
    max_cost_units = _int_env("WANXIANG_SPATIAL_MAX_COST_UNITS", default=0)
    if not submit_endpoint and not poll_endpoint:
        if allow_network:
            raise ValueError(
                "WANXIANG_SPATIAL_ALLOW_NETWORK requires spatial HTTP endpoints"
            )
        return SpatialHttpRuntime(None, False, max_cost_units)
    if not submit_endpoint or not poll_endpoint:
        raise ValueError("spatial HTTP gateway requires both submit and poll endpoints")
    provider = build_http_spatial_provider(
        submit_endpoint=submit_endpoint,
        poll_endpoint=poll_endpoint,
        bearer_token=os.environ.get("WANXIANG_SPATIAL_HTTP_BEARER_TOKEN", ""),
        provider_id=(
            os.environ.get("WANXIANG_SPATIAL_PROVIDER_ID", "http-json-spatial").strip()
            or "http-json-spatial"
        ),
        provider_version=(
            os.environ.get("WANXIANG_SPATIAL_PROVIDER_VERSION", "1").strip() or "1"
        ),
        timeout_seconds=float(
            _int_env("WANXIANG_SPATIAL_HTTP_TIMEOUT_SECONDS", default=60)
        ),
        cost_units_per_job=_int_env("WANXIANG_SPATIAL_COST_UNITS", default=1),
        private_safe=_bool_env("WANXIANG_SPATIAL_PRIVATE_SAFE"),
        allowed_media_types=_media_types_env(),
    )
    return SpatialHttpRuntime(provider, allow_network, max_cost_units)
