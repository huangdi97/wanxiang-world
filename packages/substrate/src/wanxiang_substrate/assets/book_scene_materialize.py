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
    if selected_provider.cost_units_per_asset < 0:
        raise ValueError("visual provider cost must be non-negative")
    if max_cost_units < 0:
        raise ValueError("visual budget must be non-negative")
    if selected_provider.requires_network and not allow_network:
        raise ValueError("network visual provider requires explicit allow_network")
    if selected_provider.requires_network and not plan.external_processing_allowed:
        raise ValueError("source rights do not allow external visual processing")
    if private_source and not selected_provider.private_safe:
        raise ValueError("private source requires a private-safe visual provider")

    asset_cache = cache or VisualAssetCache()
    # The cache is checked again inside this keyed guard: two concurrent
    # requests cannot both bill the provider for the same missing scene.
    cache_keys = (
        f"{request.cache_key}:{selected_provider.provider_id}@"
        f"{selected_provider.provider_version}"
        for request in plan.scene_requests
    )
    with asset_cache.generation_guard(cache_keys):
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
            if cached is not None:
                cached_asset = cached[0]
                if (
                    cached_asset.scene_key != request.stable_key
                    or cached_asset.place_name != request.place_name
                    or cached_asset.provider_id != selected_provider.provider_id
                    or cached_asset.provider_version != selected_provider.provider_version
                    or (request.style_key and cached_asset.style_key != request.style_key)
                ):
                    # An index row may exist but belong to another scene/provider.
                    # Never mislabel an unrelated image as source-grounded evidence.
                    cached = None
            if cached is None:
                misses.append(request)
            else:
                cached_rows[request.stable_key] = cached

        expected_cost = selected_provider.cost_units_per_asset * len(misses)
        if expected_cost > max_cost_units:
            raise ValueError(
                f"visual provider cost {expected_cost} exceeds budget {max_cost_units}"
            )

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
            if asset.scene_key != request.stable_key or asset.place_name != request.place_name:
                raise ValueError("visual provider returned mismatched source scene identity")
            if asset.provider_version != selected_provider.provider_version:
                raise ValueError("visual provider returned mismatched provider_version")
            if request.style_key and asset.style_key != request.style_key:
                raise ValueError("visual provider returned mismatched source style")
            if not asset.media_type.startswith("image/") or not asset.content:
                raise ValueError("visual provider must return non-empty image content")
            if len(asset.content) > 20 * 1024 * 1024:
                raise ValueError("visual provider image exceeds materialization size limit")
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
