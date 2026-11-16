"""Fail-closed deployment selection for the single active T3 spatial backend."""

from __future__ import annotations

import os

from wanxiang_substrate.spatial import SpatialGenerationProvider

from wanxiang_api.spatial_http_gateway import spatial_http_runtime_from_env
from wanxiang_api.spatial_tokenhub_runtime import spatial_tokenhub_runtime_from_env


def select_spatial_runtime(
    *, allow_network: bool, max_cost_units: int
) -> tuple[SpatialGenerationProvider | None, bool, int]:
    """Resolve exactly one environment-backed spatial provider, if configured."""
    tokenhub = spatial_tokenhub_runtime_from_env()
    http_configured = any(
        os.environ.get(name, "").strip()
        for name in (
            "WANXIANG_SPATIAL_HTTP_SUBMIT_ENDPOINT",
            "WANXIANG_SPATIAL_HTTP_POLL_ENDPOINT",
        )
    )
    if tokenhub.provider is not None and http_configured:
        raise ValueError(
            "configure either direct TokenHub spatial runtime or spatial HTTP gateway, not both"
        )
    runtime = tokenhub if tokenhub.provider is not None else spatial_http_runtime_from_env()
    selected_allow_network = allow_network or runtime.allow_network
    selected_max_cost_units = max_cost_units or runtime.max_cost_units
    return runtime.provider, selected_allow_network, selected_max_cost_units
