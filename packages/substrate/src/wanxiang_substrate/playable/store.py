"""Storage port for product descriptors, separate from canonical world history."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from wanxiang_domain.errors import ContractError, NotFound

from wanxiang_substrate.playable.models import PlayableWorldProfile


@dataclass(frozen=True, slots=True)
class ExperienceInstanceRecord:
    """Product index for a runtime instance; canonical history stays in runtime."""

    instance_id: str
    profile_id: str
    owner_id: str
    branch_id: str
    mode: str = "observer"
    actor_id: str = ""
    session_id: str = ""
    lease_id: str = ""
    last_revision: int = 0
    updated_seq: int = 0

    def __post_init__(self) -> None:
        if not self.instance_id or not self.profile_id or not self.owner_id or not self.branch_id:
            raise ContractError("instance index requires instance, profile, owner and branch refs")
        if self.mode not in {"observer", "character", "embodiment"}:
            raise ContractError(f"unsupported instance mode {self.mode!r}")
        if self.last_revision < 0 or self.updated_seq < 0:
            raise ContractError("instance counters cannot be negative")


class PlayableStore(Protocol):
    """Persistence port for experience metadata only."""

    def save_profile(self, profile: PlayableWorldProfile) -> None: ...

    def get_profile(self, profile_id: str) -> PlayableWorldProfile: ...

    def list_profiles(self) -> tuple[PlayableWorldProfile, ...]: ...

    def save_instance(self, instance: ExperienceInstanceRecord) -> None: ...

    def get_instance(self, instance_id: str) -> ExperienceInstanceRecord: ...

    def list_instances(self) -> tuple[ExperienceInstanceRecord, ...]: ...


class InMemoryPlayableStore:
    """Deterministic store used by the reference product and unit tests."""

    def __init__(self) -> None:
        self._profiles: dict[str, PlayableWorldProfile] = {}
        self._instances: dict[str, ExperienceInstanceRecord] = {}

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

    def save_instance(self, instance: ExperienceInstanceRecord) -> None:
        if instance.profile_id not in self._profiles:
            raise NotFound(f"playable profile {instance.profile_id!r} not found")
        self._instances[instance.instance_id] = instance

    def get_instance(self, instance_id: str) -> ExperienceInstanceRecord:
        try:
            return self._instances[instance_id]
        except KeyError as exc:
            raise NotFound(f"playable instance {instance_id!r} not found") from exc

    def list_instances(self) -> tuple[ExperienceInstanceRecord, ...]:
        return tuple(self._instances[key] for key in sorted(self._instances))
