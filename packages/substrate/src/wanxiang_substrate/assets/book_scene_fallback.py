"""Product-tier visual provider failure accounting and fallback provenance."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false, reportUnusedFunction=false

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_types import (
    SceneImageProvider,
    _SceneVisualAsset,
    _VisualMaterialization,
)
from wanxiang_substrate.assets.storage import AssetRef


class _VisualProviderIneligible(ValueError):
    """Generation is disallowed, but already-cached provider assets may still be reused."""

    def __init__(self, message: str, *, reason: str) -> None:
        super().__init__(message)
        self.reason = reason


class _VisualProviderFailure(ValueError):
    """Provider failure plus conservative attempt/cost accounting for fallback."""

    def __init__(
        self,
        message: str,
        *,
        provider_calls: int,
        cache_hits: int,
        cost_units: int,
        provider_usage_units: int | None = None,
    ) -> None:
        super().__init__(message)
        self.provider_calls = provider_calls
        self.cache_hits = cache_hits
        self.cost_units = cost_units
        self.provider_usage_units = provider_usage_units


def _provider_failure(
    message: str,
    *,
    attempted_calls: int,
    cache_hits: int,
    provider: SceneImageProvider,
    observed_usage_units: int | None = None,
) -> _VisualProviderFailure:
    reserved = provider.cost_units_per_asset * attempted_calls
    return _VisualProviderFailure(
        message,
        provider_calls=attempted_calls,
        cache_hits=cache_hits,
        cost_units=max(reserved, observed_usage_units or 0),
        provider_usage_units=observed_usage_units,
    )


def _provider_identity(provider: SceneImageProvider) -> str:
    provider_id = provider.provider_id or "configured-provider"
    provider_version = provider.provider_version or "unknown"
    return f"{provider_id}@{provider_version}"


def _merge_provider_cache_hits(
    requests: tuple[_SourceSceneRequest, ...],
    provider_hits: dict[str, tuple[_SceneVisualAsset, AssetRef]],
    fallback: _VisualMaterialization,
) -> tuple[tuple[_SceneVisualAsset, ...], tuple[AssetRef, ...]]:
    """Combine paid cached provider assets with rendered fallback assets in plan order."""
    merged = dict(provider_hits)
    for asset, ref in zip(fallback.assets, fallback.asset_refs, strict=True):
        merged[asset.scene_key] = (asset, ref)
    return (
        tuple(merged[request.stable_key][0] for request in requests),
        tuple(merged[request.stable_key][1] for request in requests),
    )
