"""Canonical state <-> primitive JSON codec for snapshot content."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.entity import ComponentData, EntityState, FieldValue, RelationState
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, ComponentId, EntityId, RelationId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState


def _as_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{name} must be a string")
    return value


def _as_int(value: object, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ContractError(f"{name} must be an int")
    return value


def _as_mapping(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be a mapping")
    return cast(Mapping[str, object], value)


def _as_list(value: object, name: str) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise ContractError(f"{name} must be a list")
    return [cast(dict[str, object], item) for item in cast(list[object], value)]


def _as_field_value(value: object, name: str) -> FieldValue:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ContractError(f"{name} must be a primitive value")


def state_to_primitive(state: InMemoryCanonicalState) -> dict[str, object]:
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
    entities: dict[EntityId, EntityState] = {}
    for item in _as_list(data["entities"], "entities"):
        entity_id = EntityId(_as_str(item["id"], "entity id"))
        components: dict[ComponentId, ComponentData] = {}
        for component in _as_list(item["components"], "components"):
            component_id = ComponentId(_as_str(component["id"], "component id"))
            components[component_id] = ComponentData(
                component_id=component_id,
                component_type=_as_str(component["type"], "component type"),
                schema_version=SchemaVersion(_as_int(component["version"], "component version")),
                fields={
                    _as_str(key, "field key"): _as_field_value(value, "field value")
                    for key, value in _as_mapping(component["fields"], "fields").items()
                },
            )
        entities[entity_id] = EntityState(
            entity_id=entity_id,
            entity_type=_as_str(item["type"], "entity type"),
            components=components,
        )

    relations: dict[RelationId, RelationState] = {}
    for item in _as_list(data["relations"], "relations"):
        relation_id = RelationId(_as_str(item["id"], "relation id"))
        relations[relation_id] = RelationState(
            relation_id=relation_id,
            relation_type=_as_str(item["type"], "relation type"),
            source_id=EntityId(_as_str(item["source"], "relation source")),
            target_id=EntityId(_as_str(item["target"], "relation target")),
            attributes={
                _as_str(key, "attribute key"): _as_field_value(value, "attribute value")
                for key, value in _as_mapping(item["attributes"], "attributes").items()
            },
        )

    return InMemoryCanonicalState(
        instance_id=WorldInstanceId(_as_str(data["instance_id"], "instance id")),
        branch_id=BranchId(_as_str(data["branch_id"], "branch id")),
        revision=BranchRevision(_as_int(data["revision"], "revision")),
        schema_version=SchemaVersion(_as_int(data["schema_version"], "schema version")),
        rule_version=RuntimeVersion(_as_int(data["rule_version"], "rule version")),
        _entities=entities,
        _relations=relations,
    )
