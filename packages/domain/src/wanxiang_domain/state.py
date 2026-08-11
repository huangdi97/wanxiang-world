"""CanonicalState boundary.

CanonicalState is the authoritative read model derived from committed events.
This module defines the boundary and the semantic-hash contract; concrete
implementations live in the runtime (GOAL_01B/01D).
"""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.entity import EntityState
from wanxiang_domain.ids import EntityId


class CanonicalState(Protocol):
    """Read-only canonical state view."""

    def entity(self, entity_id: EntityId) -> EntityState | None: ...

    def entities(self) -> tuple[EntityState, ...]: ...

    def semantic_hash(self) -> str: ...
