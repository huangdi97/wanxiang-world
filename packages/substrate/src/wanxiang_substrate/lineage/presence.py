"""Interworld Identity and Presence (G31E).

A subject can be present in another world WITHOUT its history being synced
back by default: entering generates an explicit presence + translation policy,
and return/sync requires an explicit policy. Identity conflicts are rejected
unless a mapped policy is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId, WorldInstanceId, WorldlineId

TranslationPolicy = Literal["mirror", "isolated", "mapped"]
SyncPolicy = Literal["none", "one_way_out", "explicit_only"]


@dataclass(frozen=True, slots=True)
class OriginIdentity:
    """The home identity of a subject (its canonical world/lineage)."""

    entity_id: EntityId
    origin_worldline_id: WorldlineId
    origin_instance_id: WorldInstanceId
    canonical_ref: str

    def to_primitive(self) -> dict[str, object]:
        return {
            "entity_id": self.entity_id.value,
            "origin_worldline_id": self.origin_worldline_id.value,
            "origin_instance_id": self.origin_instance_id.value,
            "canonical_ref": self.canonical_ref,
        }


@dataclass(frozen=True, slots=True)
class PresenceRef:
    """A subject's presence in a host world with explicit policies."""

    presence_id: str
    entity_id: EntityId
    host_worldline_id: WorldlineId
    origin: OriginIdentity
    translation_policy: TranslationPolicy = "isolated"
    sync_policy: SyncPolicy = "none"
    mapped_local_id: EntityId | None = None

    def __post_init__(self) -> None:
        if self.translation_policy not in ("mirror", "isolated", "mapped"):
            raise ContractError(f"unknown translation policy {self.translation_policy!r}")
        if self.sync_policy not in ("none", "one_way_out", "explicit_only"):
            raise ContractError(f"unknown sync policy {self.sync_policy!r}")
        if self.translation_policy == "mapped" and self.mapped_local_id is None:
            raise ContractError("mapped translation requires mapped_local_id")

    def to_primitive(self) -> dict[str, object]:
        return {
            "presence_id": self.presence_id,
            "entity_id": self.entity_id.value,
            "host_worldline_id": self.host_worldline_id.value,
            "origin": self.origin.to_primitive(),
            "translation_policy": self.translation_policy,
            "sync_policy": self.sync_policy,
            "mapped_local_id": self.mapped_local_id.value if self.mapped_local_id else None,
        }


class PresenceRegistry:
    """Thin registry of interworld presences (no history sync by default)."""

    def __init__(self) -> None:
        self._presences: dict[str, PresenceRef] = {}

    def enter(
        self,
        presence_id: str,
        origin: OriginIdentity,
        host_worldline_id: WorldlineId,
        *,
        translation_policy: TranslationPolicy = "isolated",
        sync_policy: SyncPolicy = "none",
        existing_local: bool = False,
    ) -> PresenceRef:
        """Enter a host world with an explicit policy.

        existing_local=True means the host world already has an entity with the
        origin's id: only a mapped policy is accepted; otherwise rejected.
        """
        if presence_id in self._presences:
            raise ContractError(f"presence {presence_id!r} already exists")
        if existing_local and translation_policy != "mapped":
            raise ContractError(
                "identity conflict: host world already has this id; "
                "a mapped translation policy is required"
            )
        mapped_local = None
        if translation_policy == "mapped":
            mapped_local = EntityId(f"{origin.entity_id.value}_{host_worldline_id.value}")
        presence = PresenceRef(
            presence_id=presence_id,
            entity_id=origin.entity_id,
            host_worldline_id=host_worldline_id,
            origin=origin,
            translation_policy=translation_policy,
            sync_policy=sync_policy,
            mapped_local_id=mapped_local,
        )
        self._presences[presence_id] = presence
        return presence

    def leave(self, presence_id: str) -> PresenceRef:
        presence = self._presences.pop(presence_id, None)
        if presence is None:
            raise ContractError(f"presence {presence_id!r} not found")
        return presence

    def get(self, presence_id: str) -> PresenceRef | None:
        return self._presences.get(presence_id)

    def can_sync_back(self, presence: PresenceRef) -> bool:
        """Return/sync to the origin requires an explicit sync policy."""
        return presence.sync_policy in ("one_way_out", "explicit_only")
