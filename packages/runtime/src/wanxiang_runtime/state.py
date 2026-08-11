"""In-memory canonical world state and pure delta application.

`InMemoryCanonicalState` is immutable: mutation happens only by deriving a new
state via `apply_delta`, which validates invariants first. There is no public
mutator, so no caller can bypass Commit Authority semantics at the state level.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import cast

from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    ProposedWorldDelta,
    RelationCreate,
)
from wanxiang_domain.entity import EntityState, FieldValue, RelationState
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, ComponentId, EntityId, RelationId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

from wanxiang_runtime.invariants import check_delta_invariants


@dataclass(frozen=True, slots=True)
class InMemoryCanonicalState:
    """Authoritative read model derived from committed events (immutable)."""

    instance_id: WorldInstanceId
    branch_id: BranchId
    revision: BranchRevision
    schema_version: SchemaVersion
    rule_version: RuntimeVersion
    _entities: dict[EntityId, EntityState] = field(default_factory=dict[EntityId, EntityState])
    _relations: dict[RelationId, RelationState] = field(
        default_factory=dict[RelationId, RelationState]
    )

    def entity(self, entity_id: EntityId) -> EntityState | None:
        return self._entities.get(entity_id)

    def entities(self) -> tuple[EntityState, ...]:
        return tuple(sorted(self._entities.values(), key=lambda e: e.entity_id.value))

    def relation(self, relation_id: RelationId) -> RelationState | None:
        return self._relations.get(relation_id)

    def relations(self) -> tuple[RelationState, ...]:
        return tuple(sorted(self._relations.values(), key=lambda r: r.relation_id.value))

    def with_branch(self, branch_id: BranchId) -> InMemoryCanonicalState:
        """Derive a copy of this state tagged with a different branch id."""
        return InMemoryCanonicalState(
            instance_id=self.instance_id,
            branch_id=branch_id,
            revision=self.revision,
            schema_version=self.schema_version,
            rule_version=self.rule_version,
            _entities=dict(self._entities),
            _relations=dict(self._relations),
        )

    def with_revision(self, revision: BranchRevision) -> InMemoryCanonicalState:
        """Derive a copy of this state at a different branch revision."""
        return InMemoryCanonicalState(
            instance_id=self.instance_id,
            branch_id=self.branch_id,
            revision=revision,
            schema_version=self.schema_version,
            rule_version=self.rule_version,
            _entities=dict(self._entities),
            _relations=dict(self._relations),
        )

    def semantic_hash(self) -> str:
        """Deterministic canonical hash of entities, relations and revision."""
        payload = {
            "revision": self.revision.value,
            "entities": [
                {
                    "id": e.entity_id.value,
                    "type": e.entity_type,
                    "components": [
                        {
                            "id": c.component_id.value,
                            "type": c.component_type,
                            "version": c.schema_version.value,
                            "fields": dict(c.fields),
                        }
                        for c in sorted(e.components.values(), key=lambda c: c.component_id.value)
                    ],
                }
                for e in self.entities()
            ],
            "relations": [
                {
                    "id": r.relation_id.value,
                    "type": r.relation_type,
                    "source": r.source_id.value,
                    "target": r.target_id.value,
                    "attributes": dict(r.attributes),
                }
                for r in self.relations()
            ],
        }
        return semantic_sha256(payload)

    def apply(self, delta: ProposedWorldDelta) -> InMemoryCanonicalState:
        """Validate invariants and derive a new state applying ``delta`` (pure).

        Any invariant violation raises before a new state is returned; the input
        state is never modified. Revision is unchanged here; Commit Authority
        advances the revision when it commits.
        """
        check_delta_invariants(self, delta)
        entities = dict(self._entities)
        relations = dict(self._relations)
        for op in delta.operations:
            if isinstance(op, EntityCreate):
                entities[op.entity_id] = EntityState(
                    entity_id=op.entity_id,
                    entity_type=op.entity_type,
                    components={c.component_id: c for c in op.components},
                )
            elif isinstance(op, EntityUpdate):
                current = entities[op.entity_id]
                merged = dict(current.components)
                for component in op.components:
                    merged[component.component_id] = component
                entities[op.entity_id] = EntityState(
                    entity_id=current.entity_id,
                    entity_type=current.entity_type,
                    components=merged,
                )
            elif isinstance(op, EntityDelete):
                del entities[op.entity_id]
            elif isinstance(op, RelationCreate):
                relations[op.relation_id] = RelationState(
                    relation_id=op.relation_id,
                    relation_type=op.relation_type,
                    source_id=op.source_id,
                    target_id=op.target_id,
                    attributes=op.attributes,
                )
            else:
                del relations[op.relation_id]
        return InMemoryCanonicalState(
            instance_id=self.instance_id,
            branch_id=self.branch_id,
            revision=self.revision,
            schema_version=self.schema_version,
            rule_version=self.rule_version,
            _entities=entities,
            _relations=relations,
        )


def apply_delta(state: InMemoryCanonicalState, delta: ProposedWorldDelta) -> InMemoryCanonicalState:
    """Pure module-level alias for :meth:`InMemoryCanonicalState.apply`."""
    return state.apply(delta)


def state_to_primitive(state: InMemoryCanonicalState) -> dict[str, object]:
    """Serialize canonical state to a stable primitive (snapshot/API boundary)."""
    return {
        "instance_id": state.instance_id.value,
        "branch_id": state.branch_id.value,
        "revision": state.revision.value,
        "schema_version": state.schema_version.value,
        "rule_version": state.rule_version.value,
        "entities": [
            {
                "id": entity.entity_id.value,
                "type": entity.entity_type,
                "components": [
                    {
                        "id": component.component_id.value,
                        "type": component.component_type,
                        "version": component.schema_version.value,
                        "fields": dict(component.fields),
                    }
                    for component in entity.components.values()
                ],
            }
            for entity in state.entities()
        ],
        "relations": [
            {
                "id": relation.relation_id.value,
                "type": relation.relation_type,
                "source": relation.source_id.value,
                "target": relation.target_id.value,
                "attributes": dict(relation.attributes),
            }
            for relation in state.relations()
        ],
    }


def state_from_primitive(data: dict[str, object]) -> InMemoryCanonicalState:
    """Deserialize canonical state from a primitive with validation."""
    from wanxiang_domain.entity import ComponentData, EntityState, RelationState
    from wanxiang_domain.errors import ContractError

    def as_str(value: object, name: str) -> str:
        if not isinstance(value, str):
            raise ContractError(f"{name} must be a string")
        return value

    def as_int(value: object, name: str) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ContractError(f"{name} must be an int")
        return value

    def as_mapping(value: object, name: str) -> Mapping[str, object]:
        if not isinstance(value, Mapping):
            raise ContractError(f"{name} must be a mapping")
        return cast(Mapping[str, object], value)

    def as_list(value: object, name: str) -> list[dict[str, object]]:
        if not isinstance(value, list):
            raise ContractError(f"{name} must be a list")
        return [cast(dict[str, object], item) for item in cast(list[object], value)]

    def as_field(value: object, name: str) -> FieldValue:
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        raise ContractError(f"{name} must be a primitive value")

    entities: dict[EntityId, EntityState] = {}
    for item in as_list(data["entities"], "entities"):
        entity_id = EntityId(as_str(item["id"], "entity id"))
        components: dict[ComponentId, ComponentData] = {}
        for component in as_list(item["components"], "components"):
            component_id = ComponentId(as_str(component["id"], "component id"))
            components[component_id] = ComponentData(
                component_id=component_id,
                component_type=as_str(component["type"], "component type"),
                schema_version=SchemaVersion(as_int(component["version"], "component version")),
                fields={
                    as_str(key, "field key"): as_field(value, "field value")
                    for key, value in as_mapping(component["fields"], "fields").items()
                },
            )
        entities[entity_id] = EntityState(
            entity_id=entity_id,
            entity_type=as_str(item["type"], "entity type"),
            components=components,
        )

    relations: dict[RelationId, RelationState] = {}
    for item in as_list(data["relations"], "relations"):
        relation_id = RelationId(as_str(item["id"], "relation id"))
        relations[relation_id] = RelationState(
            relation_id=relation_id,
            relation_type=as_str(item["type"], "relation type"),
            source_id=EntityId(as_str(item["source"], "relation source")),
            target_id=EntityId(as_str(item["target"], "relation target")),
            attributes={
                as_str(key, "attribute key"): as_field(value, "attribute value")
                for key, value in as_mapping(item["attributes"], "attributes").items()
            },
        )

    return InMemoryCanonicalState(
        instance_id=WorldInstanceId(as_str(data["instance_id"], "instance id")),
        branch_id=BranchId(as_str(data["branch_id"], "branch id")),
        revision=BranchRevision(as_int(data["revision"], "revision")),
        schema_version=SchemaVersion(as_int(data["schema_version"], "schema version")),
        rule_version=RuntimeVersion(as_int(data["rule_version"], "rule version")),
        _entities=entities,
        _relations=relations,
    )
