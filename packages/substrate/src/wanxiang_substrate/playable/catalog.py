"""Server-side World Plaza, My Worlds and Continue read models."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import NotFound

from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.store import ExperienceInstanceRecord, PlayableStore


@dataclass(frozen=True, slots=True)
class WorldCard:
    profile_id: str
    display_name: str
    world_package_ref: str
    scenario_ref: str
    visibility: str
    tags: tuple[str, ...]

    @classmethod
    def from_profile(cls, profile: PlayableWorldProfile) -> WorldCard:
        return cls(
            profile_id=profile.profile_id,
            display_name=profile.display_name or profile.profile_id,
            world_package_ref=profile.world_package_ref,
            scenario_ref=profile.scenario_ref,
            visibility=profile.visibility,
            tags=profile.tags,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "display_name": self.display_name,
            "world_package_ref": self.world_package_ref,
            "scenario_ref": self.scenario_ref,
            "visibility": self.visibility,
            "tags": list(self.tags),
        }


@dataclass(frozen=True, slots=True)
class SessionCard:
    instance_id: str
    profile_id: str
    branch_id: str
    mode: str
    actor_id: str
    last_revision: int
    updated_seq: int

    @classmethod
    def from_record(cls, record: ExperienceInstanceRecord) -> SessionCard:
        return cls(
            instance_id=record.instance_id,
            profile_id=record.profile_id,
            branch_id=record.branch_id,
            mode=record.mode,
            actor_id=record.actor_id,
            last_revision=record.last_revision,
            updated_seq=record.updated_seq,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "instance_id": self.instance_id,
            "profile_id": self.profile_id,
            "branch_id": self.branch_id,
            "mode": self.mode,
            "actor_id": self.actor_id,
            "last_revision": self.last_revision,
            "updated_seq": self.updated_seq,
        }


class WorldPlaza:
    """Authorization-aware catalog facade over the shared profile/instance port."""

    def __init__(self, store: PlayableStore) -> None:
        self._store = store

    def explore_worlds(self, viewer_id: str | None = None) -> tuple[WorldCard, ...]:
        return self._cards(viewer_id)

    def my_worlds(self, viewer_id: str) -> tuple[WorldCard, ...]:
        return self._cards(viewer_id, owned_only=True)

    def recent_sessions(self, viewer_id: str) -> tuple[SessionCard, ...]:
        sessions = [
            instance
            for instance in self._store.list_instances()
            if instance.owner_id == viewer_id
            and self._profile_visible(instance.profile_id, viewer_id)
        ]
        sessions.sort(key=lambda item: (-item.updated_seq, item.instance_id))
        return tuple(SessionCard.from_record(item) for item in sessions)

    def continue_last(self, viewer_id: str) -> SessionCard | None:
        sessions = self.recent_sessions(viewer_id)
        return sessions[0] if sessions else None

    def require_access(self, profile_id: str, viewer_id: str | None) -> PlayableWorldProfile:
        profile = self._store.get_profile(profile_id)
        if not profile.visible_to(viewer_id):
            raise NotFound(f"playable profile {profile_id!r} not found")
        return profile

    def _cards(self, viewer_id: str | None, *, owned_only: bool = False) -> tuple[WorldCard, ...]:
        profiles = [
            profile
            for profile in self._store.list_profiles()
            if profile.visible_to(viewer_id)
            and (not owned_only or bool(viewer_id and profile.owner_id == viewer_id))
        ]
        return tuple(WorldCard.from_profile(profile) for profile in profiles)

    def _profile_visible(self, profile_id: str, viewer_id: str | None) -> bool:
        try:
            return self._store.get_profile(profile_id).visible_to(viewer_id)
        except NotFound:
            return False
