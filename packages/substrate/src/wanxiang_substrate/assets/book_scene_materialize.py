# pyright: reportPrivateUsage=false, reportUnusedFunction=false

"""Governed materialization of source-derived scene visual assets."""

from __future__ import annotations

import hashlib

from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan
from wanxiang_substrate.assets.book_scene_render import _ProceduralSvgSceneProvider
from wanxiang_substrate.assets.book_scene_types import (
    SceneImageProvider,
    _SceneVisualAsset,
    _VisualMaterialization,
)
from wanxiang_substrate.assets.storage import AssetRef


def _materialize_visual_plan(
    plan: _SourceVisualPlan,
    provider: SceneImageProvider | None = None,
    *,
    cache: VisualAssetCache | None = None,
    allow_network: bool = False,
    max_cost_units: int = 0,
    rights: str | None = None,
    private_source: bool = False,
) -> _VisualMaterialization:
    """Generate only cache misses, under explicit network/cost governance."""
    if plan.status not in {"READY_FOR_ASSET_PROVIDER", "BUDGET_ZERO"}:
        return _VisualMaterialization((), (), 0, 0, 0)

    selected_provider = provider or _ProceduralSvgSceneProvider()
    if selected_provider.requires_network and not allow_network:
        raise ValueError("network visual provider requires explicit allow_network")
    if selected_provider.requires_network and not plan.external_processing_allowed:
        raise ValueError("source rights do not allow external visual processing")
    if private_source and not selected_provider.private_safe:
        raise ValueError("private source requires a private-safe visual provider")

    asset_cache = cache or VisualAssetCache()
    delivery_rights = rights or plan.delivery_rights
    resolved_assets: list[_SceneVisualAsset] = []
    resolved_refs: list[AssetRef] = []
    misses: list[_SourceSceneRequest] = []
    cached_rows: dict[str, tuple[_SceneVisualAsset, AssetRef]] = {}

    for request in plan.scene_requests:
        provider_cache_key = (
            f"{request.cache_key}:{selected_provider.provider_id}@"
            f"{selected_provider.provider_version}"
        )
        cached = asset_cache.get(provider_cache_key, rights=delivery_rights)
        if cached is None:
            misses.append(request)
        else:
            cached_rows[request.stable_key] = cached

    expected_cost = selected_provider.cost_units_per_asset * len(misses)
    if expected_cost > max_cost_units:
        raise ValueError(f"visual provider cost {expected_cost} exceeds budget {max_cost_units}")

    generated: dict[str, tuple[_SceneVisualAsset, AssetRef]] = {}
    for request in misses:
        asset = selected_provider.produce(request)
        expected_cache_key = (
            f"{request.cache_key}:{selected_provider.provider_id}@"
            f"{selected_provider.provider_version}"
        )
        if asset.provider_id != selected_provider.provider_id:
            raise ValueError("visual provider returned mismatched provider_id")
        if asset.cache_key != expected_cache_key:
            raise ValueError("visual provider returned mismatched cache_key")
        if hashlib.sha256(asset.content).hexdigest() != asset.content_sha256:
            raise ValueError("visual provider returned invalid content digest")
        ref = asset_cache.put(asset, rights=delivery_rights)
        generated[request.stable_key] = (asset, ref)

    for request in plan.scene_requests:
        asset, ref = cached_rows.get(request.stable_key) or generated[request.stable_key]
        resolved_assets.append(asset)
        resolved_refs.append(ref)

    return _VisualMaterialization(
        assets=tuple(resolved_assets),
        asset_refs=tuple(resolved_refs),
        provider_calls=len(misses),
        cache_hits=len(plan.scene_requests) - len(misses),
        cost_units=expected_cost,
    )


def _render_visual_plan(
    plan: _SourceVisualPlan,
    provider: SceneImageProvider | None = None,
    *,
    allow_network: bool = False,
    max_cost_units: int = 0,
    private_source: bool = False,
) -> tuple[_SceneVisualAsset, ...]:
    """Compatibility helper returning assets without exposing cache details."""
    return _materialize_visual_plan(
        plan,
        provider,
        allow_network=allow_network,
        max_cost_units=max_cost_units,
        private_source=private_source,
    ).assets
