"""Portable character identity snapshot and explicit portability entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.playable.store import CharacterRecord

PassportEntryKind = Literal["memory", "skill", "item"]
PortabilityFlag = Literal["portable", "conditional", "blocked"]
PassportPrivacy = Literal["public", "private"]
DecisionStatus = Literal["accepted", "conditional", "rejected"]


@dataclass(frozen=True, slots=True)
class PassportEntry:
    """One ref-only memory/skill/item with an explicit import policy."""

    entry_id: str
    kind: PassportEntryKind
    ref: str
    origin_world_ref: str
    portability: PortabilityFlag
    compatibility_tags: tuple[str, ...] = ()
    privacy: PassportPrivacy = "private"

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.entry_id, self.ref, self.origin_world_ref)):
            raise ContractError("passport entry requires id, ref, and origin world")
        if self.kind not in ("memory", "skill", "item"):
            raise ContractError(f"invalid passport entry kind {self.kind!r}")
        if self.portability not in ("portable", "conditional", "blocked"):
            raise ContractError(f"invalid passport portability {self.portability!r}")
        if self.privacy not in ("public", "private"):
            raise ContractError(f"invalid passport privacy {self.privacy!r}")
        if any(not tag.strip() for tag in self.compatibility_tags):
            raise ContractError("passport compatibility tags cannot be blank")
        if len(set(self.compatibility_tags)) != len(self.compatibility_tags):
            raise ContractError("passport compatibility tags must be unique")


@dataclass(frozen=True, slots=True)
class CharacterPassport:
    """Portable identity projection; CharacterRecord remains the product row."""

    character_id: str
    owner_id: str
    display_name: str
    origin_world_refs: tuple[str, ...] = ()
    entries: tuple[PassportEntry, ...] = ()
    compatible_profile_ids: tuple[str, ...] = ()
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.character_id or not self.owner_id or not self.display_name.strip():
            raise ContractError("passport identity requires character, owner, and display name")
        if self.schema_version != 1:
            raise ContractError("unsupported character passport schema")
        if any(not ref.strip() for ref in self.origin_world_refs):
            raise ContractError("passport origin refs cannot be blank")
        if len(set(self.origin_world_refs)) != len(self.origin_world_refs):
            raise ContractError("passport origin refs must be unique")
        if len({entry.entry_id for entry in self.entries}) != len(self.entries):
            raise ContractError("passport entry ids must be unique")
        if len(set(self.compatible_profile_ids)) != len(self.compatible_profile_ids):
            raise ContractError("passport profile compatibility refs must be unique")

    @classmethod
    def from_character(
        cls,
        character: CharacterRecord,
        *,
        origin_world_refs: tuple[str, ...],
        entries: tuple[PassportEntry, ...] = (),
    ) -> CharacterPassport:
        return cls(
            character_id=character.character_id,
            owner_id=character.owner_id,
            display_name=character.display_name,
            origin_world_refs=origin_world_refs,
            entries=entries,
            compatible_profile_ids=character.compatible_profile_ids,
        )

    def to_character_record(self) -> CharacterRecord:
        """Rebuild the existing product identity row without importing entries."""
        return CharacterRecord(
            character_id=self.character_id,
            owner_id=self.owner_id,
            display_name=self.display_name,
            compatible_profile_ids=self.compatible_profile_ids,
        )

    def visible_entries(
        self, requester_id: str, *, admin: bool = False
    ) -> tuple[PassportEntry, ...]:
        if admin or requester_id == self.owner_id:
            return self.entries
        return tuple(entry for entry in self.entries if entry.privacy == "public")

    def to_dict(self, requester_id: str, *, admin: bool = False) -> dict[str, object]:
        authorized = admin or requester_id == self.owner_id
        return {
            "schema_version": self.schema_version,
            "character_id": self.character_id,
            "display_name": self.display_name,
            "owner_id": self.owner_id if authorized else None,
            "origin_world_refs": list(self.origin_world_refs) if authorized else [],
            "compatible_profile_ids": list(self.compatible_profile_ids) if authorized else [],
            "entries": [
                {
                    "entry_id": entry.entry_id,
                    "kind": entry.kind,
                    "ref": entry.ref,
                    "origin_world_ref": entry.origin_world_ref,
                    "portability": entry.portability,
                    "compatibility_tags": list(entry.compatibility_tags),
                    "privacy": entry.privacy,
                }
                for entry in self.visible_entries(requester_id, admin=admin)
            ],
        }


@dataclass(frozen=True, slots=True)
class PassportTranslationContext:
    """Target-world capabilities used to decide a translation proposal."""

    requester_id: str
    target_world_ref: str
    target_profile_id: str
    supported_kinds: tuple[PassportEntryKind, ...]
    available_refs: tuple[str, ...] = ()
    compatibility_tags: tuple[str, ...] = ()
    admin: bool = False

    def __post_init__(self) -> None:
        if not self.requester_id or not self.target_world_ref or not self.target_profile_id:
            raise ContractError("passport translation context requires target refs")
        if any(kind not in ("memory", "skill", "item") for kind in self.supported_kinds):
            raise ContractError("translation context has an invalid entry kind")


@dataclass(frozen=True, slots=True)
class PassportDecision:
    entry_id: str
    status: DecisionStatus
    reason: str


@dataclass(frozen=True, slots=True)
class PassportTranslationProposal:
    """Explicit cross-world decisions; this object has no import operation."""

    passport_id: str
    target_world_ref: str
    policy_ref: str
    decisions: tuple[PassportDecision, ...]

    @property
    def accepted_entry_ids(self) -> tuple[str, ...]:
        return tuple(
            item.entry_id for item in self.decisions if item.status in ("accepted", "conditional")
        )


# Short aliases for clients that use compatibility terminology.
InterworldCompatibility = PassportTranslationContext
PassportPortability = PassportEntry
