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


@dataclass(frozen=True, slots=True)
class CharacterRecord:
    """User-owned character identity; cognition and world truth remain elsewhere."""

    character_id: str
    owner_id: str
    display_name: str
    compatible_profile_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.character_id or not self.owner_id or not self.display_name.strip():
            raise ContractError("character requires id, owner and display name")
        if len(set(self.compatible_profile_ids)) != len(self.compatible_profile_ids):
            raise ContractError("character profile compatibility refs must be unique")

    def compatible_with(self, profile_id: str) -> bool:
        return not self.compatible_profile_ids or profile_id in self.compatible_profile_ids


class PlayableStore(Protocol):
    """Persistence port for experience metadata only."""

    def save_profile(self, profile: PlayableWorldProfile) -> None: ...

    def get_profile(self, profile_id: str) -> PlayableWorldProfile: ...

    def list_profiles(self) -> tuple[PlayableWorldProfile, ...]: ...

    def save_instance(self, instance: ExperienceInstanceRecord) -> None: ...

    def get_instance(self, instance_id: str) -> ExperienceInstanceRecord: ...

    def list_instances(self) -> tuple[ExperienceInstanceRecord, ...]: ...

    def save_character(self, character: CharacterRecord) -> None: ...

    def get_character(self, character_id: str) -> CharacterRecord: ...

    def list_characters(self, owner_id: str) -> tuple[CharacterRecord, ...]: ...


class InMemoryPlayableStore:
    """Deterministic store used by the reference product and unit tests."""

    def __init__(self) -> None:
        self._profiles: dict[str, PlayableWorldProfile] = {}
        self._instances: dict[str, ExperienceInstanceRecord] = {}
        self._characters: dict[str, CharacterRecord] = {}

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

    def save_character(self, character: CharacterRecord) -> None:
        current = self._characters.get(character.character_id)
        if current is not None and current != character:
            raise ContractError(
                f"character {character.character_id!r} is immutable at this version"
            )
        self._characters[character.character_id] = character

    def get_character(self, character_id: str) -> CharacterRecord:
        try:
            return self._characters[character_id]
        except KeyError as exc:
            raise NotFound(f"character {character_id!r} not found") from exc

    def list_characters(self, owner_id: str) -> tuple[CharacterRecord, ...]:
        return tuple(
            self._characters[key]
            for key in sorted(self._characters)
            if self._characters[key].owner_id == owner_id
        )
