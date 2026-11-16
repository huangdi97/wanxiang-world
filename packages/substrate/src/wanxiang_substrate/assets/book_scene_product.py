"""Product-tier visual materialization: cached provider assets win, then T0 fallback.

A provider becoming ineligible or failing must not discard already-paid cached
assets: those are local delivery and remain reusable without re-billing.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from dataclasses import replace

from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_fallback import (
    _merge_provider_cache_hits,
    _provider_identity,
    _VisualProviderFailure,
    _VisualProviderIneligible,
)
from wanxiang_substrate.assets.book_scene_materialize import _materialize_visual_plan
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan
from wanxiang_substrate.assets.book_scene_types import (
    SceneImageProvider,
    _SceneVisualAsset,
    _VisualMaterialization,
)
from wanxiang_substrate.assets.storage import AssetRef


def _materialize_product_visual_plan(
    plan: _SourceVisualPlan,
    provider: SceneImageProvider | None = None,
    *,
    cache: VisualAssetCache | None = None,
    allow_network: bool = False,
    max_cost_units: int = 0,
    rights: str | None = None,
    private_source: bool = False,
    allow_provider_generation: bool = True,
) -> _VisualMaterialization:
    """Use cached/T1 visuals when possible; otherwise expose a metered T0 fallback."""
    asset_cache = cache or VisualAssetCache()
    selected = provider

    def provider_hits(
        active: SceneImageProvider,
    ) -> tuple[dict[str, tuple[_SceneVisualAsset, AssetRef]], tuple[_SourceSceneRequest, ...]]:
        delivery_rights = rights or plan.delivery_rights
        hits: dict[str, tuple[_SceneVisualAsset, AssetRef]] = {}
        missing: list[_SourceSceneRequest] = []
        for request in plan.scene_requests:
            cached = asset_cache.get_for(request, active, rights=delivery_rights)
            if cached is None:
                missing.append(request)
            else:
                hits[request.stable_key] = cached
        return hits, tuple(missing)

    def fallback(
        active: SceneImageProvider,
        *,
        reason: str,
        provider_calls: int,
        cost_units: int,
    ) -> _VisualMaterialization:
        hits, missing = provider_hits(active)
        rendered = _materialize_visual_plan(
            replace(plan, scene_requests=missing),
            provider=None,
            cache=asset_cache,
            allow_network=False,
            max_cost_units=0,
            rights=rights,
            private_source=private_source,
        )
        assets, refs = _merge_provider_cache_hits(
            tuple(plan.scene_requests),
            hits,
            rendered,
        )
        return _VisualMaterialization(
            assets=assets,
            asset_refs=refs,
            provider_calls=provider_calls + rendered.provider_calls,
            cache_hits=len(hits) + rendered.cache_hits,
            cost_units=cost_units,
            fallback_from_provider=_provider_identity(active),
            fallback_reason=reason,
        )

    try:
        return _materialize_visual_plan(
            plan,
            provider=selected,
            cache=asset_cache,
            allow_network=allow_network,
            max_cost_units=max_cost_units,
            rights=rights,
            private_source=private_source,
            allow_provider_generation=allow_provider_generation,
        )
    except _VisualProviderIneligible as ineligible:
        if selected is None:
            raise
        return fallback(selected, reason=ineligible.reason, provider_calls=0, cost_units=0)
    except _VisualProviderFailure as failure:
        if selected is None:
            raise
        return fallback(
            selected,
            reason="provider_failure",
            provider_calls=failure.provider_calls,
            cost_units=failure.cost_units,
        )
