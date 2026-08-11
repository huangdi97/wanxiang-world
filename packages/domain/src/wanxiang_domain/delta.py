"""ProposedWorldDelta and its typed operations.

A ProposedWorldDelta is the only thing Commit Authority accepts as input. It
cannot hide arbitrary mutations: every operation is typed. Components may carry
flexible payload fields, but identity/version/ordering metadata stays typed.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from wanxiang_domain.entity import ComponentData, FieldValue
from wanxiang_domain.ids import EntityId, RelationId


@dataclass(frozen=True, slots=True)
class EntityCreate:
    entity_id: EntityId
    entity_type: str
    components: tuple[ComponentData, ...] = ()


@dataclass(frozen=True, slots=True)
class EntityUpdate:
    entity_id: EntityId
    components: tuple[ComponentData, ...] = ()


@dataclass(frozen=True, slots=True)
class EntityDelete:
    entity_id: EntityId


@dataclass(frozen=True, slots=True)
class RelationCreate:
    relation_id: RelationId
    relation_type: str
    source_id: EntityId
    target_id: EntityId
    attributes: Mapping[str, FieldValue] = field(default_factory=dict[str, FieldValue])


@dataclass(frozen=True, slots=True)
class RelationDelete:
    relation_id: RelationId


DeltaOperation = EntityCreate | EntityUpdate | EntityDelete | RelationCreate | RelationDelete


@dataclass(frozen=True, slots=True)
class ProposedWorldDelta:
    """Typed, immutable set of operations proposed against a branch revision."""

    operations: tuple[DeltaOperation, ...] = ()

    def is_empty(self) -> bool:
        return not self.operations
