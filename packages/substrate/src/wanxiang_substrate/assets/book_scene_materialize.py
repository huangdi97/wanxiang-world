# pyright: reportPrivateUsage=false, reportUnusedFunction=false

"""Governed materialization of source-derived scene visual assets."""

from __future__ import annotations

import hashlib

from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_fallback import (
    _provider_failure,
    _provider_identity,
    _VisualProviderFailure,
)
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
        f"{request.cache_key}:{selected_provider.provider_id}@{selected_provider.provider_version}"
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
        for attempted_calls, request in enumerate(misses, start=1):
            try:
                asset = selected_provider.produce(request)
            except Exception as exc:
                raise _provider_failure(
                    f"visual provider execution failed: {type(exc).__name__}",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                ) from exc
            expected_cache_key = (
                f"{request.cache_key}:{selected_provider.provider_id}@"
                f"{selected_provider.provider_version}"
            )
            if asset.provider_id != selected_provider.provider_id:
                raise _provider_failure(
                    "visual provider returned mismatched provider_id",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
            if asset.cache_key != expected_cache_key:
                raise _provider_failure(
                    "visual provider returned mismatched cache_key",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
            if hashlib.sha256(asset.content).hexdigest() != asset.content_sha256:
                raise _provider_failure(
                    "visual provider returned invalid content digest",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
            if asset.scene_key != request.stable_key or asset.place_name != request.place_name:
                raise _provider_failure(
                    "visual provider returned mismatched source scene identity",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
            if asset.provider_version != selected_provider.provider_version:
                raise _provider_failure(
                    "visual provider returned mismatched provider_version",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
            if request.style_key and asset.style_key != request.style_key:
                raise _provider_failure(
                    "visual provider returned mismatched source style",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
            if not asset.media_type.startswith("image/") or not asset.content:
                raise _provider_failure(
                    "visual provider must return non-empty image content",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
            if len(asset.content) > 20 * 1024 * 1024:
                raise _provider_failure(
                    "visual provider image exceeds materialization size limit",
                    attempted_calls=attempted_calls,
                    cache_hits=len(cached_rows),
                    provider=selected_provider,
                )
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


def _materialize_product_visual_plan(
    plan: _SourceVisualPlan,
    provider: SceneImageProvider | None = None,
    *,
    cache: VisualAssetCache | None = None,
    allow_network: bool = False,
    max_cost_units: int = 0,
    rights: str | None = None,
    private_source: bool = False,
) -> _VisualMaterialization:
    """Use T1 when eligible; otherwise expose an explicit, metered T0 fallback."""
    if max_cost_units < 0:
        raise ValueError("visual budget must be non-negative")
    selected = provider
    fallback_from = ""
    fallback_reasons: list[str] = []
    if selected is not None:
        if selected.cost_units_per_asset < 0:
            raise ValueError("visual provider cost must be non-negative")
        if selected.requires_network and not allow_network:
            fallback_reasons.append("network_not_allowed")
        if selected.requires_network and not plan.external_processing_allowed:
            fallback_reasons.append("source_external_processing_not_allowed")
        if private_source and not selected.private_safe:
            fallback_reasons.append("private_source_provider_not_safe")
        if selected.cost_units_per_asset * len(plan.scene_requests) > max_cost_units:
            fallback_reasons.append("budget_insufficient")
        if fallback_reasons:
            fallback_from = _provider_identity(selected)
            selected = None

    try:
        result = _materialize_visual_plan(
            plan,
            provider=selected,
            cache=cache,
            allow_network=allow_network if selected is not None else False,
            max_cost_units=max_cost_units if selected is not None else 0,
            rights=rights,
            private_source=private_source,
        )
    except _VisualProviderFailure as failure:
        if selected is None:
            raise
        fallback = _materialize_visual_plan(
            plan,
            provider=None,
            cache=cache,
            allow_network=False,
            max_cost_units=0,
            rights=rights,
            private_source=private_source,
        )
        return _VisualMaterialization(
            assets=fallback.assets,
            asset_refs=fallback.asset_refs,
            provider_calls=failure.provider_calls + fallback.provider_calls,
            cache_hits=failure.cache_hits + fallback.cache_hits,
            cost_units=failure.cost_units,
            fallback_from_provider=_provider_identity(selected),
            fallback_reason="provider_failure",
        )

    if not fallback_from:
        return result
    return _VisualMaterialization(
        assets=result.assets,
        asset_refs=result.asset_refs,
        provider_calls=result.provider_calls,
        cache_hits=result.cache_hits,
        cost_units=result.cost_units,
        fallback_from_provider=fallback_from,
        fallback_reason=",".join(fallback_reasons),
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
