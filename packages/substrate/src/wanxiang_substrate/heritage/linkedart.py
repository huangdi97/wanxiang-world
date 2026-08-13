"""Linked Art / CIDOC CRM mapping profile (G10B).

Maps HeritageObject production/acquisition/custody/conservation events with
Actor/Place/TimeSpan provenance links and JSON-LD/external IDs. A bounded,
documented mapping profile.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.heritage.errors import MappingError

EventKind = Literal["production", "acquisition", "custody", "conservation"]


@dataclass(frozen=True, slots=True)
class LinkedArtEvent:
    event_id: str
    object_id: str
    kind: EventKind
    actor: str = ""
    place: str = ""
    timespan: str = ""
    external_id: str = ""
    provenance_ref: str = ""

    def __post_init__(self) -> None:
        if self.kind not in ("production", "acquisition", "custody", "conservation"):
            raise MappingError(f"unknown event kind {self.kind!r}")


@dataclass(frozen=True, slots=True)
class HeritageObjectMapping:
    object_id: str
    external_ids: tuple[str, ...] = ()
    events: tuple[LinkedArtEvent, ...] = ()
    mapping_profile: str = "linked-art-cidoc-subset-v1"


class LinkedArtMapper:
    """Maps bounded heritage objects to Linked Art / CIDOC event structures."""

    def __init__(self) -> None:
        self._objects: dict[str, HeritageObjectMapping] = {}

    def map_object(
        self,
        object_id: str,
        *,
        external_ids: tuple[str, ...] = (),
        events: tuple[LinkedArtEvent, ...] = (),
    ) -> HeritageObjectMapping:
        mapping = HeritageObjectMapping(
            object_id=object_id,
            external_ids=external_ids,
            events=events,
        )
        self._objects[object_id] = mapping
        return mapping

    def get(self, object_id: str) -> HeritageObjectMapping | None:
        return self._objects.get(object_id)

    def provenance_chain(self, object_id: str) -> tuple[LinkedArtEvent, ...]:
        mapping = self.get(object_id)
        if mapping is None:
            return ()
        return tuple(sorted(mapping.events, key=lambda e: (e.timespan, e.event_id)))
