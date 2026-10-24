"""Rehydrate the in-process Player catalog from a durable store.

Packages are persisted when a world is registered. On startup this rebuilds
only derived catalogs (`_packages` / `_experiences` / `_installs`); it never
creates canonical worlds or appends events, because `instantiate_preview`
reuses the existing runtime world by its stable preview id.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_substrate.assets.book_scene_cache_lookup import cached_visual_for
from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.playable.experience import experience_from_profile
from wanxiang_substrate.playable.service_registration import _install_visual

if TYPE_CHECKING:
    from wanxiang_substrate.compile.assembler import WorldPackageDraft
    from wanxiang_substrate.playable.service import PlayableService


def _reattach_cached_visuals(
    service: PlayableService,
    profile_id: str,
    package: WorldPackageDraft,
) -> int:
    """Reattach already-generated T1 assets without calling any provider."""

    plan = _plan_book_scene_assets(package, max_preview_scenes=12)
    assets = list(service._visual_assets.get(profile_id, ()))
    refs = list(service._visual_asset_refs.get(profile_id, ()))
    positions = {asset.scene_key: index for index, asset in enumerate(assets)}
    restored = 0
    for request in plan.scene_requests:
        cached = cached_visual_for(
            service._visual_cache,
            request,
            rights=plan.delivery_rights,
        )
        if cached is None:
            continue
        asset, ref = cached
        position = positions.get(asset.scene_key)
        if position is None:
            positions[asset.scene_key] = len(assets)
            assets.append(asset)
            refs.append(ref)
        else:
            assets[position] = asset
            refs[position] = ref
        restored += 1
    if restored:
        service._visual_assets[profile_id] = tuple(assets)
        service._visual_asset_refs[profile_id] = tuple(refs)
    return restored


def restore_playable_service(service: PlayableService) -> int:
    """Restore derived package/experience/install maps; return world count."""

    packages = service.store.load_packages()
    experiences = service.store.load_experiences()
    restored = 0
    for profile in service.store.list_profiles():
        package = packages.get(profile.profile_id)
        if package is None:
            continue
        service._packages[profile.profile_id] = package
        service._experiences[profile.profile_id] = experiences.get(
            profile.profile_id,
            experience_from_profile(profile),
        )
        service._installs[profile.profile_id] = _install_visual(
            service,
            profile,
            package,
            provider=None,
            allow_network=False,
            max_cost_units=0,
        )
        _reattach_cached_visuals(service, profile.profile_id, package)
        restored += 1
    return restored
