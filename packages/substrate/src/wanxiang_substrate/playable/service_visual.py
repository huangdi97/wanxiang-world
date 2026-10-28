"""Visual projection helpers for PlayableService.

These functions mutate only the service's derived visual cache/catalog, never
canonical world state or History.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wanxiang_domain.errors import ContractError, NotFound

from wanxiang_substrate.assets.book_scene_budget import VisualBudgetLedger
from wanxiang_substrate.assets.book_scene_identity import _source_scene_key
from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_scene_visual import (
    _materialize_product_visual_plan,
    _materialize_visual_plan,
    _SceneImageProvider,
    _SceneVisualAsset,
    _VisualMaterialization,
)
from wanxiang_substrate.assets.book_spatial_frame import (
    _projection_frame_from_mapping,
    _projection_frame_to_dict,
)
from wanxiang_substrate.assets.book_spatial_types import _SpatialProjectionFrame
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.compile.assembler import WorldPackageDraft

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _ledger_for(service: PlayableService, profile_id: str) -> VisualBudgetLedger:
    ledger = service._visual_budget
    if ledger is None:
        ledger = VisualBudgetLedger()
        service._visual_budget = ledger
    return ledger


def visual_budget_usage(service: PlayableService, profile_id: str) -> int:
    """Public read of one world's recorded paid on-demand visual calls."""
    return _ledger_for(service, profile_id).used(profile_id)


def _visual_access_allowed(
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
) -> bool:
    profile = service.plaza.require_access(profile_id, viewer_id)
    if profile.owner_id and viewer_id == profile.owner_id:
        return True
    package = service._packages.get(profile_id)
    if package is None:
        return False
    return package.draft.compiler_metadata.get("visual_asset_rights_v1", "source-gated") == "public"


def _visible_visual_assets(
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
) -> tuple[_SceneVisualAsset, ...]:
    profile = service.plaza.require_access(profile_id, viewer_id)
    assets = service._visual_assets.get(profile_id, ())
    refs = service._visual_asset_refs.get(profile_id, ())
    if profile.owner_id and viewer_id == profile.owner_id:
        return assets
    return tuple(asset for asset, ref in zip(assets, refs, strict=True) if ref.rights == "public")


def _visible_spatial_assets(
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
) -> dict[str, tuple[AssetRef, ...]]:
    profile = service.plaza.require_access(profile_id, viewer_id)
    rows = service._spatial_asset_refs.get(profile_id, {})
    if profile.owner_id and viewer_id == profile.owner_id:
        return dict(rows)
    return {
        scene_key: tuple(ref for ref in refs if ref.rights == "public")
        for scene_key, refs in rows.items()
        if any(ref.rights == "public" for ref in refs)
    }


def _visible_spatial_projection_frames(
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
) -> dict[str, _SpatialProjectionFrame]:
    visible_assets = _visible_spatial_assets(service, profile_id, viewer_id=viewer_id)
    frames = service._spatial_projection_frames.get(profile_id, {})
    return {scene_key: frame for scene_key, frame in frames.items() if scene_key in visible_assets}


def _spatial_attachment_policy(
    package: WorldPackageDraft,
) -> tuple[str, frozenset[str]]:
    plan = _plan_book_scene_assets(package, max_preview_scenes=0)
    scene_keys = frozenset(
        _source_scene_key(plan.source_digest, place) for place in plan.place_names
    )
    return plan.delivery_rights, scene_keys


def _source_scene_key_allowed(package: WorldPackageDraft, scene_key: str) -> bool:
    _, scene_keys = _spatial_attachment_policy(package)
    return scene_key in scene_keys


def _attach_spatial_assets(
    service: PlayableService,
    profile_id: str,
    scene_key: str,
    asset_refs: tuple[AssetRef, ...],
    projection_frame: _SpatialProjectionFrame | None = None,
) -> None:
    package = service._packages.get(profile_id)
    if package is None:
        raise NotFound(f"playable package {profile_id!r} not found")
    if not asset_refs:
        raise ValueError("spatial attachment requires at least one asset")
    delivery_rights, scene_keys = _spatial_attachment_policy(package)
    if scene_key not in scene_keys:
        raise NotFound(f"spatial scene {scene_key!r} not found")
    if any(ref.rights != delivery_rights for ref in asset_refs):
        raise ValueError("spatial asset rights must match source-derived delivery rights")
    service._spatial_asset_refs.setdefault(profile_id, {})[scene_key] = asset_refs
    frames = service._spatial_projection_frames.setdefault(profile_id, {})
    if projection_frame is None:
        frames.pop(scene_key, None)
    else:
        frames[scene_key] = _projection_frame_from_mapping(
            _projection_frame_to_dict(projection_frame)
        )


def _visual_fidelity_rank(asset: _SceneVisualAsset) -> int:
    """Keep the shared scene catalog monotonic under ordinary visual requests."""
    if asset.presentation_kind == "panorama":
        return 2
    if asset.media_type == "image/svg+xml":
        return 0
    return 1


def _materialize_visual_place(
    service: PlayableService,
    profile_id: str,
    place_name: str,
    *,
    viewer_id: str,
    provider: _SceneImageProvider | None = None,
    allow_network: bool = False,
    max_cost_units: int = 0,
    max_deferred_generations: int = 0,
    fallback_to_t0: bool = True,
) -> _VisualMaterialization:
    profile = service.plaza.require_access(profile_id, viewer_id)
    if not _visual_access_allowed(service, profile_id, viewer_id=viewer_id):
        raise NotFound(f"visual world {profile_id!r} not found")
    package = service._packages.get(profile_id)
    if package is None:
        raise NotFound(f"playable package {profile_id!r} not found")
    normalized_place = place_name.strip()
    if not normalized_place or normalized_place not in package.draft.places:
        raise NotFound(f"visual place {place_name!r} not found")

    plan = _plan_book_scene_assets(
        package,
        max_preview_scenes=1,
        preferred_places=(normalized_place,),
    )
    if not plan.scene_requests or plan.scene_requests[0].place_name != normalized_place:
        raise NotFound(f"visual place {place_name!r} not found")
    if max_deferred_generations < 0:
        raise ValueError("deferred visual budget must be non-negative")

    request = plan.scene_requests[0]
    owner = bool(profile.owner_id) and viewer_id == profile.owner_id
    private_source = (
        package.draft.compiler_metadata.get("visual_private_source_v1", "true") == "true"
    )
    reserved_attempt = False
    reusing_idempotent_reservation = False
    if owner and provider is not None and max_deferred_generations > 0:
        cached = service._visual_cache.get_for(request, provider, rights=plan.delivery_rights)
        raw_provider_cost = cast(object, provider.cost_units_per_asset)
        provider_cost: int | None = (
            raw_provider_cost
            if (
                not isinstance(raw_provider_cost, bool)
                and isinstance(raw_provider_cost, int)
                and raw_provider_cost >= 0
            )
            else None
        )
        provider_eligible = (
            provider_cost is not None
            and provider_cost <= max_cost_units
            and (not provider.requires_network or allow_network)
            and (not provider.requires_network or plan.external_processing_allowed)
            and (not private_source or provider.private_safe)
        )
        if cached is None and provider_eligible:
            reservation_key = (
                f"{request.cache_key}:{provider.provider_id}@{provider.provider_version}"
            )
            ledger = _ledger_for(service, profile_id)
            try:
                reserved_attempt = ledger.reserve(
                    profile_id,
                    reservation_key,
                    max_deferred_generations,
                )
            except ValueError as exc:
                raise ContractError(str(exc)) from exc
            if (
                not reserved_attempt
                and service._visual_cache.get_for(request, provider, rights=plan.delivery_rights)
                is None
            ):
                if provider.generation_is_idempotent:
                    # The durable reservation already accounts for this logical
                    # generation. A provider that explicitly guarantees same-
                    # identity replay may retry without consuming another slot.
                    reusing_idempotent_reservation = True
                else:
                    raise ContractError(
                        "world on-demand visual attempt is already reserved; "
                        "automatic retry blocked"
                    )

    materializer = _materialize_product_visual_plan if fallback_to_t0 else _materialize_visual_plan
    materialized = materializer(
        plan,
        provider=provider,
        cache=service._visual_cache,
        allow_network=allow_network,
        max_cost_units=max_cost_units,
        private_source=private_source,
        rights=plan.delivery_rights,
        allow_provider_generation=owner,
    )
    if (
        owner
        and provider is not None
        and max_deferred_generations > 0
        and materialized.provider_calls > 0
        and not reserved_attempt
        and not reusing_idempotent_reservation
    ):
        _ledger_for(service, profile_id).record(profile_id, materialized.provider_calls)
    combined: dict[str, tuple[_SceneVisualAsset, AssetRef]] = {
        asset.scene_key: (asset, ref)
        for asset, ref in zip(
            service._visual_assets.get(profile_id, ()),
            service._visual_asset_refs.get(profile_id, ()),
            strict=True,
        )
    }
    for asset, ref in zip(materialized.assets, materialized.asset_refs, strict=True):
        existing = combined.get(asset.scene_key)
        if existing is not None and _visual_fidelity_rank(existing[0]) > _visual_fidelity_rank(
            asset
        ):
            continue
        combined[asset.scene_key] = (asset, ref)
    service._visual_assets[profile_id] = tuple(asset for asset, _ in combined.values())
    service._visual_asset_refs[profile_id] = tuple(ref for _, ref in combined.values())
    return materialized


def _attach_package_visuals(
    service: PlayableService,
    profile_id: str,
    package: WorldPackageDraft,
    *,
    provider: _SceneImageProvider | None = None,
    allow_network: bool = False,
    max_cost_units: int = 0,
) -> None:
    plan = _plan_book_scene_assets(package)
    materialized = _materialize_product_visual_plan(
        plan,
        provider=provider,
        cache=service._visual_cache,
        allow_network=allow_network,
        max_cost_units=max_cost_units,
        private_source=(
            package.draft.compiler_metadata.get("visual_private_source_v1", "true") == "true"
        ),
        rights=plan.delivery_rights,
    )
    service._visual_assets[profile_id] = materialized.assets
    service._visual_asset_refs[profile_id] = materialized.asset_refs
