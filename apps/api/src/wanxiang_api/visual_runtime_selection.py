"""Fail-closed deployment selection for the single active T1 image backend."""

from __future__ import annotations

import os

from wanxiang_substrate.assets.book_scene_types import SceneImageProvider

from wanxiang_api.visual_http_gateway import visual_http_runtime_from_env
from wanxiang_api.visual_tokenhub_runtime import visual_tokenhub_runtime_from_env


def _select_visual_runtime(
    *, allow_network: bool, max_cost_units: int
) -> tuple[SceneImageProvider | None, bool, int]:
    """Resolve exactly one environment-backed T1 image provider, if configured."""
    tokenhub_endpoint = os.environ.get("WANXIANG_VISUAL_TOKENHUB_ENDPOINT", "").strip()
    http_endpoint = os.environ.get("WANXIANG_VISUAL_HTTP_ENDPOINT", "").strip()
    if tokenhub_endpoint and http_endpoint:
        raise ValueError(
            "configure direct TokenHub visual or HTTP visual gateway, not both"
        )
    runtime = (
        visual_tokenhub_runtime_from_env()
        if tokenhub_endpoint
        else visual_http_runtime_from_env()
    )
    selected_allow_network = allow_network or runtime.allow_network
    selected_max_cost_units = max_cost_units or runtime.max_cost_units
    return runtime.provider, selected_allow_network, selected_max_cost_units
