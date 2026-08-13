"""Heritage object semantic twin (G10C).

PhysicalHeritageObject, DigitalSurrogate, SemanticHeritageTwin and
ReconstructionModel are distinct; ConservationState/History is versioned with
rights/provenance.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.heritage.errors import TwinError


@dataclass(frozen=True, slots=True)
class ConservationEntry:
    """A versioned conservation state with provenance."""

    entry_id: str
    state: str
    version: int
    rights: str = "public"
    provenance_ref: str = ""


class ConservationHistory:
    """Append-only conservation history (replayable)."""

    def __init__(self) -> None:
        self._entries: dict[str, ConservationEntry] = {}

    def add(self, entry: ConservationEntry) -> ConservationEntry:
        if entry.entry_id in self._entries:
            raise TwinError(f"conservation entry {entry.entry_id!r} already exists")
        self._entries[entry.entry_id] = entry
        return entry

    def entries(self) -> tuple[ConservationEntry, ...]:
        return tuple(sorted(self._entries.values(), key=lambda e: e.version))


class HeritageTwin:
    """Distinct object, surrogate, twin and reconstruction identities."""

    def __init__(
        self,
        physical_id: str,
        *,
        digital_surrogate: str = "",
        twin_id: str = "",
        reconstruction_id: str = "",
    ) -> None:
        self._physical_id = physical_id
        self._digital_surrogate = digital_surrogate
        self._twin_id = twin_id
        self._reconstruction_id = reconstruction_id
        self._conservation = ConservationHistory()

    @property
    def physical_id(self) -> str:
        return self._physical_id

    def identities(self) -> dict[str, str]:
        """Physical object, digital surrogate, twin, reconstruction are distinct."""
        return {
            "physical": self._physical_id,
            "digital_surrogate": self._digital_surrogate,
            "semantic_twin": self._twin_id,
            "reconstruction": self._reconstruction_id,
        }

    def add_conservation(self, entry: ConservationEntry) -> ConservationEntry:
        return self._conservation.add(entry)

    def conservation_history(self) -> tuple[ConservationEntry, ...]:
        return self._conservation.entries()

    def require_distinct(self) -> None:
        ids = list(self.identities().values())
        if len({v for v in ids if v}) != len([v for v in ids if v]):
            raise TwinError("object identities must be distinct")
