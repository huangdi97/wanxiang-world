# pyright: reportPrivateUsage=false, reportUnusedFunction=false

"""Governed materialization of source-derived scene visual assets."""

from __future__ import annotations

import hashlib

from wanxiang_substrate.assets.book_generation_budget import _require_nonnegative_int
from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_fallback import (
    _provider_failure,
    _VisualProviderIneligible,
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
    allow_provider_generation: bool = True,
) -> _VisualMaterialization:
    """Generate only cache misses, under explicit network/cost governance."""
    if plan.status not in {"READY_FOR_ASSET_PROVIDER", "BUDGET_ZERO"}:
        return _VisualMaterialization((), (), 0, 0, 0)

    selected_provider = provider or _ProceduralSvgSceneProvider()
    _require_nonnegative_int(selected_provider.cost_units_per_asset, label="visual provider cost")
    _require_nonnegative_int(max_cost_units, label="visual budget")

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
            cached = asset_cache.get_for(request, selected_provider, rights=delivery_rights)
            if cached is None:
                misses.append(request)
            else:
                cached_rows[request.stable_key] = cached

        # Network, external-processing permission, provider privacy and budget
        # govern generation only. A cache hit is a local delivery operation and
        # must remain reusable during replay/offline browsing without re-billing.
        if misses and provider is not None and not allow_provider_generation:
            raise _VisualProviderIneligible(
                "viewer cannot trigger configured visual provider generation",
                reason="provider_generation_not_allowed",
            )
        if misses and selected_provider.requires_network and not allow_network:
            raise _VisualProviderIneligible(
                "network visual provider requires explicit allow_network",
                reason="network_not_allowed",
            )
        if misses and selected_provider.requires_network and not plan.external_processing_allowed:
            raise _VisualProviderIneligible(
                "source rights do not allow external visual processing",
                reason="source_external_processing_not_allowed",
            )
        if misses and private_source and not selected_provider.private_safe:
            raise _VisualProviderIneligible(
                "private source requires a private-safe visual provider",
                reason="private_source_provider_not_safe",
            )

        expected_cost = selected_provider.cost_units_per_asset * len(misses)
        if expected_cost > max_cost_units:
            raise _VisualProviderIneligible(
                f"visual provider cost {expected_cost} exceeds budget {max_cost_units}",
                reason="budget_insufficient",
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
            if (
                asset.presentation_kind not in {"still", "panorama"}
                or asset.presentation_kind != selected_provider.presentation_kind
            ):
                raise _provider_failure(
                    "visual provider returned mismatched presentation kind",
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

        generated_usage = [asset.provider_usage_units for asset, _ in generated.values()]
        provider_usage_units = (
            0
            if not misses
            else sum(value for value in generated_usage if value is not None)
            if all(value is not None for value in generated_usage)
            else None
        )
        return _VisualMaterialization(
            assets=tuple(resolved_assets),
            asset_refs=tuple(resolved_refs),
            provider_calls=len(misses),
            cache_hits=len(plan.scene_requests) - len(misses),
            cost_units=expected_cost,
            provider_usage_units=provider_usage_units,
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
