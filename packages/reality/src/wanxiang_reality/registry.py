"""RealityProfile registry: per-worldline pinning with no silent hot swap.

A worldline is created against one RealityProfile major line and stays on it. A
major upgrade never moves an existing worldline in place; it must go through the
shadow-replay migration path in :mod:`wanxiang_reality.migration`.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_reality.errors import ProfileError
from wanxiang_reality.profiles import RealityProfile, profile_hash
from wanxiang_reality.versions import Version


@dataclass(frozen=True, slots=True)
class ProfilePin:
    """The profile a worldline is pinned to, with the digest it was pinned at."""

    worldline_id: str
    profile_id: str
    version: Version
    digest: str

    @property
    def ref(self) -> str:
        """Canonical `profile_id@version` reference."""
        return f"{self.profile_id}@{self.version}"


class RealityProfileRegistry:
    """Versioned store of RealityProfiles plus the pin of every worldline."""

    def __init__(self) -> None:
        self._profiles: dict[str, RealityProfile] = {}
        self._defaults: dict[str, Version] = {}
        self._pins: dict[str, ProfilePin] = {}

    def register(self, profile: RealityProfile, *, default: bool = False) -> None:
        """Register a profile version. Re-registering the same version is a no-op."""
        key = f"{profile.profile_id}@{profile.version}"
        existing = self._profiles.get(key)
        if existing is not None and profile_hash(existing) != profile_hash(profile):
            raise ProfileError(f"profile {key} is already registered with different content")
        self._profiles[key] = profile
        if default:
            self._defaults[profile.profile_id] = profile.version

    def profile(self, profile_id: str, version: Version) -> RealityProfile:
        found = self._profiles.get(f"{profile_id}@{version}")
        if found is None:
            raise ProfileError(f"unknown reality profile {profile_id}@{version}")
        return found

    def versions(self, profile_id: str) -> tuple[Version, ...]:
        """All registered versions of one profile id, oldest major first."""
        return tuple(
            sorted(
                profile.version
                for profile in self._profiles.values()
                if profile.profile_id == profile_id
            )
        )

    def pin(self, worldline_id: str, profile: RealityProfile) -> ProfilePin:
        """Pin a new worldline to a profile version."""
        if not worldline_id:
            raise ProfileError("worldline_id is required")
        existing = self._pins.get(worldline_id)
        if existing is not None:
            raise ProfileError(
                f"worldline {worldline_id} is already pinned to {existing.ref}; "
                "use the migration path to change reality semantics"
            )
        pin = ProfilePin(
            worldline_id=worldline_id,
            profile_id=profile.profile_id,
            version=profile.version,
            digest=profile_hash(profile),
        )
        self._pins[worldline_id] = pin
        return pin

    def resolve(self, worldline_id: str) -> ProfilePin:
        """The pin of an existing worldline (never a default)."""
        found = self._pins.get(worldline_id)
        if found is None:
            raise ProfileError(f"worldline {worldline_id} has no reality profile pin")
        return found

    def default_profile(self, profile_id: str) -> RealityProfile | None:
        """Profile used for a *new* worldline; existing pins are never affected."""
        version = self._defaults.get(profile_id)
        if version is None:
            return None
        return self.profile(profile_id, version)

    def repin_after_migration(self, worldline_id: str, profile: RealityProfile) -> ProfilePin:
        """Replace a pin after an approved migration or fork.

        Only :func:`wanxiang_reality.migration.migrate_worldline` should call this,
        so an unapproved path cannot move a worldline between profile majors.
        """
        self.resolve(worldline_id)
        pin = ProfilePin(
            worldline_id=worldline_id,
            profile_id=profile.profile_id,
            version=profile.version,
            digest=profile_hash(profile),
        )
        self._pins[worldline_id] = pin
        return pin

    def worldlines(self) -> tuple[str, ...]:
        return tuple(sorted(self._pins))
