"""Museum object biography & reconstruction scenarios (G10D).

Current Museum / Historical Context / Object Biography / Conservation Lab
instances are distinct; reconstruction outputs carry truth labels; curator
mode is the review gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ReconstructionLabel = Literal["evidence", "reconstructed", "creative"]


@dataclass(frozen=True, slots=True)
class BiographyEntry:
    entry_id: str
    kind: str
    summary: str
    label: ReconstructionLabel = "evidence"
    rights: str = "public"


class MuseumBiography:
    """Replayable object biography with reconstruction truth labels."""

    def __init__(self) -> None:
        self._entries: dict[str, BiographyEntry] = {}

    def add(self, entry: BiographyEntry) -> BiographyEntry:
        self._entries[entry.entry_id] = entry
        return entry

    def entries(self) -> tuple[BiographyEntry, ...]:
        return tuple(sorted(self._entries.values(), key=lambda e: e.entry_id))

    def require_rights(self, entry_id: str, *, curator: bool = False) -> None:
        entry = self._entries.get(entry_id)
        if entry is None:
            raise ValueError(f"unknown biography entry {entry_id!r}")
        if entry.rights != "public" and not curator:
            raise ValueError(f"entry {entry_id!r} requires curator review")


class MuseumScenario:
    """Distinct museum instances (current/historical/biography/lab)."""

    def __init__(
        self,
        object_id: str,
        *,
        current_instance: str,
        historical_instance: str,
        biography_instance: str,
        lab_instance: str,
    ) -> None:
        self._object_id = object_id
        self._instances = {
            "current": current_instance,
            "historical_context": historical_instance,
            "object_biography": biography_instance,
            "conservation_lab": lab_instance,
        }

    def instances(self) -> dict[str, str]:
        return dict(self._instances)

    def curator_note(self, note: str) -> dict[str, object]:
        return {
            "object_id": self._object_id,
            "mode": "curator",
            "note": note,
            "projection_only": True,
        }
