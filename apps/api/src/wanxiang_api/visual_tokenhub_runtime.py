"""Deployment configuration for the direct TokenHub Hy-Image T1 adapter."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
from dataclasses import dataclass

from wanxiang_substrate.assets.book_scene_tokenhub_image import (
    build_tokenhub_image_provider,
)
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider

from wanxiang_api.visual_http_gateway import _bool_env, _int_env


@dataclass(frozen=True, slots=True)
class VisualTokenHubRuntime:
    provider: SceneImageProvider | None
    allow_network: bool
    max_cost_units: int


def _artifact_hosts() -> frozenset[str]:
    raw = os.environ.get("WANXIANG_VISUAL_TOKENHUB_ARTIFACT_HOSTS", "")
    return frozenset(item.strip() for item in raw.split(",") if item.strip())


def visual_tokenhub_runtime_from_env() -> VisualTokenHubRuntime:
    endpoint = os.environ.get("WANXIANG_VISUAL_TOKENHUB_ENDPOINT", "").strip()
    allow_network = _bool_env("WANXIANG_VISUAL_ALLOW_NETWORK")
    max_cost_units = _int_env("WANXIANG_VISUAL_MAX_COST_UNITS", default=0)
    if not endpoint:
        if allow_network:
            raise ValueError(
                "WANXIANG_VISUAL_ALLOW_NETWORK requires WANXIANG_VISUAL_TOKENHUB_ENDPOINT"
            )
        return VisualTokenHubRuntime(None, False, max_cost_units)
    provider = build_tokenhub_image_provider(
        endpoint=endpoint,
        bearer_token=os.environ.get("WANXIANG_VISUAL_TOKENHUB_API_KEY", ""),
        artifact_hosts=_artifact_hosts(),
        timeout_seconds=float(_int_env("WANXIANG_VISUAL_TOKENHUB_TIMEOUT_SECONDS", default=120)),
        cost_units_per_asset=_int_env(
            "WANXIANG_VISUAL_TOKENHUB_COST_UNITS",
            default=20_000,
        ),
        private_safe=_bool_env("WANXIANG_VISUAL_TOKENHUB_PRIVATE_SAFE"),
    )
    return VisualTokenHubRuntime(provider, allow_network, max_cost_units)
