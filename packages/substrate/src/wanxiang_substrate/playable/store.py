"""Storage port for product descriptors, separate from canonical world history."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from wanxiang_domain.errors import ContractError, NotFound

from wanxiang_substrate.playable.models import PlayableWorldProfile


class PlayableStore(Protocol):
    """Persistence port for experience metadata only."""

    def save_profile(self, profile: PlayableWorldProfile) -> None: ...

    def get_profile(self, profile_id: str) -> PlayableWorldProfile: ...

    def list_profiles(self) -> tuple[PlayableWorldProfile, ...]: ...


class InMemoryPlayableStore:
    """Deterministic store used by the reference product and unit tests."""

    def __init__(self) -> None:
        self._profiles: dict[str, PlayableWorldProfile] = {}

    def save_profile(self, profile: PlayableWorldProfile) -> None:
        profile.validate()
        current = self._profiles.get(profile.profile_id)
        if current is not None and current != profile:
            raise ContractError(f"profile {profile.profile_id!r} is immutable at this version")
        self._profiles[profile.profile_id] = profile

    def get_profile(self, profile_id: str) -> PlayableWorldProfile:
        try:
            return self._profiles[profile_id]
        except KeyError as exc:
            raise NotFound(f"playable profile {profile_id!r} not found") from exc

    def list_profiles(self) -> tuple[PlayableWorldProfile, ...]:
        return tuple(self._profiles[key] for key in sorted(self._profiles))

    def replace_for_test(self, profiles: Iterable[PlayableWorldProfile]) -> None:
        """Load a complete deterministic fixture without exposing mutation APIs."""
        replacement = {}
        for profile in profiles:
            profile.validate()
            replacement[profile.profile_id] = profile
        self._profiles = replacement
