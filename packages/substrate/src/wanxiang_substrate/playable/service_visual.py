"""Visual projection helpers for PlayableService.

These functions mutate only the service's derived visual cache/catalog, never
canonical world state or History.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_domain.errors import NotFound

from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_scene_visual import (
    _materialize_visual_plan,
    _SceneImageProvider,
    _SceneVisualAsset,
    _VisualMaterialization,
)
from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.compile.assembler import WorldPackageDraft

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def visual_access_allowed(
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
    return package.draft.compiler_metadata.get(
        "visual_asset_rights_v1", "source-gated"
    ) == "public"


def visible_visual_assets(
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
    return tuple(
        asset for asset, ref in zip(assets, refs, strict=True) if ref.rights == "public"
    )


def materialize_visual_place(
    service: PlayableService,
    profile_id: str,
    place_name: str,
    *,
    viewer_id: str,
    provider: _SceneImageProvider | None = None,
    allow_network: bool = False,
    max_cost_units: int = 0,
) -> _VisualMaterialization:
    service.plaza.require_access(profile_id, viewer_id)
    if not visual_access_allowed(service, profile_id, viewer_id=viewer_id):
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

    materialized = _materialize_visual_plan(
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
    combined: dict[str, tuple[_SceneVisualAsset, AssetRef]] = {
        asset.scene_key: (asset, ref)
        for asset, ref in zip(
            service._visual_assets.get(profile_id, ()),
            service._visual_asset_refs.get(profile_id, ()),
            strict=True,
        )
    }
    for asset, ref in zip(materialized.assets, materialized.asset_refs, strict=True):
        combined[asset.scene_key] = (asset, ref)
    service._visual_assets[profile_id] = tuple(asset for asset, _ in combined.values())
    service._visual_asset_refs[profile_id] = tuple(ref for _, ref in combined.values())
    return materialized


def attach_package_visuals(
    service: PlayableService,
    profile_id: str,
    package: WorldPackageDraft,
) -> None:
    plan = _plan_book_scene_assets(package)
    materialized = _materialize_visual_plan(
        plan,
        cache=service._visual_cache,
        rights=plan.delivery_rights,
    )
    service._visual_assets[profile_id] = materialized.assets
    service._visual_asset_refs[profile_id] = materialized.asset_refs
