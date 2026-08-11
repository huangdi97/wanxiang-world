"""Minimal Entity / Component / Relation contracts.

Identity, schema version and relationship metadata are typed; flexible payload
fields are allowed but must not carry identity/ordering semantics.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import ComponentId, EntityId, RelationId
from wanxiang_domain.versions import SchemaVersion

FieldValue = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class ComponentData:
    """A typed component attached to an entity, with explicit identity."""

    component_id: ComponentId
    component_type: str
    schema_version: SchemaVersion
    fields: Mapping[str, FieldValue] = field(default_factory=dict[str, FieldValue])

    def __post_init__(self) -> None:
        if not self.component_type:
            raise ContractError("component_type must be a non-empty string")


@dataclass(frozen=True, slots=True)
class EntityState:
    """Read-model representation of an entity (canonical state projection)."""

    entity_id: EntityId
    entity_type: str
    components: Mapping[ComponentId, ComponentData] = field(
        default_factory=dict[ComponentId, ComponentData]
    )

    def __post_init__(self) -> None:
        if not self.entity_type:
            raise ContractError("entity_type must be a non-empty string")


@dataclass(frozen=True, slots=True)
class RelationState:
    """Read-model representation of a typed relation between two entities."""

    relation_id: RelationId
    relation_type: str
    source_id: EntityId
    target_id: EntityId
    attributes: Mapping[str, FieldValue] = field(default_factory=dict[str, FieldValue])

    def __post_init__(self) -> None:
        if not self.relation_type:
            raise ContractError("relation_type must be a non-empty string")
