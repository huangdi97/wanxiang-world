"""Deployment configuration for direct TokenHub Hy-World T3 generation."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
from dataclasses import dataclass

from wanxiang_substrate.assets.book_spatial_tokenhub import (
    build_tokenhub_spatial_provider,
)
from wanxiang_substrate.spatial import SpatialGenerationProvider

from wanxiang_api.visual_http_gateway import _bool_env, _int_env


@dataclass(frozen=True, slots=True)
class SpatialTokenHubRuntime:
    provider: SpatialGenerationProvider | None
    allow_network: bool
    max_cost_units: int


def _artifact_hosts() -> frozenset[str]:
    raw = os.environ.get("WANXIANG_SPATIAL_TOKENHUB_ARTIFACT_HOSTS", "")
    return frozenset(item.strip() for item in raw.split(",") if item.strip())


def spatial_tokenhub_runtime_from_env() -> SpatialTokenHubRuntime:
    submit_endpoint = os.environ.get(
        "WANXIANG_SPATIAL_TOKENHUB_SUBMIT_ENDPOINT", ""
    ).strip()
    tasks_endpoint = os.environ.get(
        "WANXIANG_SPATIAL_TOKENHUB_TASKS_ENDPOINT", ""
    ).strip()
    allow_network = _bool_env("WANXIANG_SPATIAL_ALLOW_NETWORK")
    max_cost_units = _int_env("WANXIANG_SPATIAL_MAX_COST_UNITS", default=0)

    if not submit_endpoint and not tasks_endpoint:
        return SpatialTokenHubRuntime(None, False, max_cost_units)
    if not submit_endpoint or not tasks_endpoint:
        raise ValueError(
            "TokenHub spatial runtime requires both submit and tasks endpoints"
        )
    provider = build_tokenhub_spatial_provider(
        submit_endpoint=submit_endpoint,
        tasks_endpoint=tasks_endpoint,
        bearer_token=os.environ.get("WANXIANG_SPATIAL_TOKENHUB_API_KEY", ""),
        artifact_hosts=_artifact_hosts(),
        timeout_seconds=float(
            _int_env("WANXIANG_SPATIAL_TOKENHUB_TIMEOUT_SECONDS", default=120)
        ),
        cost_units_per_job=_int_env(
            "WANXIANG_SPATIAL_TOKENHUB_COST_UNITS", default=8_000_000
        ),
        private_safe=_bool_env("WANXIANG_SPATIAL_PRIVATE_SAFE"),
    )
    return SpatialTokenHubRuntime(provider, allow_network, max_cost_units)
