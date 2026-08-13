"""Projection contracts separate from canonical types (G05D)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.ids import BranchId

ProjectionMode = Literal["text", "map", "debug"]


@dataclass(frozen=True, slots=True)
class ProjectionRequest:
    """A client projection request with actor/session perspective."""

    session_id: str
    actor_id: str
    branch_id: BranchId
    mode: ProjectionMode = "text"


@dataclass(frozen=True, slots=True)
class ProjectionItem:
    """A server-filtered DTO item (never raw canonical state)."""

    entity_id: str
    entity_type: str
    label: str
    redacted: bool = False
    redaction_reason: str = ""
    fields: tuple[tuple[str, str], ...] = ()

    def field(self, key: str) -> str | None:
        for field_key, value in self.fields:
            if field_key == key:
                return value
        return None


@dataclass(frozen=True, slots=True)
class ProjectionSnapshot:
    """Server-composed projection DTO with revision provenance."""

    session_id: str
    actor_id: str
    branch_id: BranchId
    mode: ProjectionMode
    revision: int
    items: tuple[ProjectionItem, ...]

    def entity(self, entity_id: str) -> ProjectionItem | None:
        for item in self.items:
            if item.entity_id == entity_id:
                return item
        return None
