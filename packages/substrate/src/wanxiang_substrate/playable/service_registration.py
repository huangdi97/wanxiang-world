"""World registration helpers for PlayableService.

Registration updates the derived playable catalog and its visual projections;
it never mutates canonical world state or History.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_substrate.assets.book_scene_visual import _SceneImageProvider
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.experience import ExperiencePackage, experience_from_profile
from wanxiang_substrate.playable.factory import profile_from_world_package
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.service_visual import _attach_package_visuals
from wanxiang_substrate.preview import PreviewInstall, preview_install_id

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _install_visual(
    service: PlayableService,
    profile: PlayableWorldProfile,
    package: WorldPackageDraft,
    *,
    provider: _SceneImageProvider | None,
    allow_network: bool,
    max_cost_units: int,
) -> PreviewInstall:
    """Materialize derived visuals and return the install receipt for the profile."""

    _attach_package_visuals(
        service,
        profile.profile_id,
        package,
        provider=provider,
        allow_network=allow_network,
        max_cost_units=max_cost_units,
    )
    return PreviewInstall(
        preview_id=preview_install_id(package),
        package_id=package.package_id,
        draft_id=package.draft_id,
        package_hash=package.manifest.content_hash,
    )


def _register_package(
    service: PlayableService,
    package: WorldPackageDraft,
    *,
    owner_id: str = "",
    visibility: str = "public",
    display_name: str | None = None,
    description: str | None = None,
    scenario_name: str | None = None,
    opening_hint: str | None = None,
    allowed_actions: tuple[str, ...] = ("set_status",),
    visual_provider: _SceneImageProvider | None = None,
    visual_allow_network: bool = False,
    visual_max_cost_units: int = 0,
) -> PlayableWorldProfile:
    profile = profile_from_world_package(
        package,
        owner_id=owner_id,
        visibility=visibility,
        display_name=display_name,
        description=description,
        scenario_name=scenario_name,
        opening_hint=opening_hint,
    )
    experience = experience_from_profile(profile, allowed_actions=allowed_actions)
    service.store.save_profile(profile)
    service._packages[profile.profile_id] = package
    service._experiences[profile.profile_id] = experience
    service._installs[profile.profile_id] = _install_visual(
        service,
        profile,
        package,
        provider=visual_provider,
        allow_network=visual_allow_network,
        max_cost_units=visual_max_cost_units,
    )
    return profile


def _register_profile(
    service: PlayableService,
    profile: PlayableWorldProfile,
    package: WorldPackageDraft,
    experience: ExperiencePackage | None = None,
    *,
    visual_provider: _SceneImageProvider | None = None,
    visual_allow_network: bool = False,
    visual_max_cost_units: int = 0,
) -> None:
    profile.validate()
    service.store.save_profile(profile)
    service._packages[profile.profile_id] = package
    service._experiences[profile.profile_id] = experience or experience_from_profile(profile)
    service._installs[profile.profile_id] = _install_visual(
        service,
        profile,
        package,
        provider=visual_provider,
        allow_network=visual_allow_network,
        max_cost_units=visual_max_cost_units,
    )
