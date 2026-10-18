"""Rehydrate the in-process Player catalog from a durable store.

Packages are persisted when a world is registered. On startup this rebuilds
only derived catalogs (`_packages` / `_experiences` / `_installs`); it never
creates canonical worlds or appends events, because `instantiate_preview`
reuses the existing runtime world by its stable preview id.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_substrate.playable.experience import experience_from_profile
from wanxiang_substrate.playable.service_registration import _install_visual

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def restore_playable_service(service: PlayableService) -> int:
    """Restore derived package/experience/install maps; return world count."""

    packages = service.store.load_packages()
    restored = 0
    for profile in service.store.list_profiles():
        package = packages.get(profile.profile_id)
        if package is None:
            continue
        service._packages[profile.profile_id] = package
        service._experiences[profile.profile_id] = experience_from_profile(profile)
        service._installs[profile.profile_id] = _install_visual(
            service,
            profile,
            package,
            provider=None,
            allow_network=False,
            max_cost_units=0,
        )
        restored += 1
    return restored
