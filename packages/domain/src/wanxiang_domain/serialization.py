"""Versioned serialization for canonical command/delta contracts.

Serialization/deserialization is a compatibility boundary (Engineering
Standards section 8): explicit schema versions, deterministic ordering for
hashes, validation on deserialize, and structured errors for unknown versions.
History/persistence contracts are serialized in `serialization_history.py`.
"""

from __future__ import annotations

from typing import Any

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    ProposedWorldDelta,
    RelationCreate,
    RelationDelete,
)
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import IncompatibleVersion
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import (
    ActorId,
    BranchId,
    CommandId,
    ComponentId,
    CorrelationId,
    EntityId,
    RelationId,
    WanxiangId,
    WorldInstanceId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import SchemaVersion

CONTRACTS_SCHEMA_VERSION = 1


def expect_version(data: dict[str, Any], expected: int = CONTRACTS_SCHEMA_VERSION) -> None:
    actual = data.get("schema_version")
    if actual != expected:
        raise IncompatibleVersion(
            f"incompatible schema version {actual!r}; this reader supports {expected}"
        )


def encode_id(value: WanxiangId) -> str:
    return value.value


def decode_id[T: WanxiangId](cls: type[T], value: str) -> T:
    return cls(value)


def _encode_components(components: tuple[ComponentData, ...]) -> list[dict[str, Any]]:
    return [
        {
            "component_id": encode_id(c.component_id),
            "component_type": c.component_type,
            "schema_version": c.schema_version.value,
            "fields": dict(c.fields),
        }
        for c in components
    ]


def _decode_components(items: list[dict[str, Any]]) -> tuple[ComponentData, ...]:
    return tuple(
        ComponentData(
            component_id=decode_id(ComponentId, item["component_id"]),
            component_type=item["component_type"],
            schema_version=SchemaVersion(item["schema_version"]),
            fields={str(k): v for k, v in item.get("fields", {}).items()},
        )
        for item in items
    )


def delta_to_primitive(delta: ProposedWorldDelta) -> dict[str, Any]:
    ops: list[dict[str, Any]] = []
    for op in delta.operations:
        if isinstance(op, EntityCreate):
            ops.append(
                {
                    "op": "entity_create",
                    "entity_id": encode_id(op.entity_id),
                    "entity_type": op.entity_type,
                    "components": _encode_components(op.components),
                }
            )
        elif isinstance(op, EntityUpdate):
            ops.append(
                {
                    "op": "entity_update",
                    "entity_id": encode_id(op.entity_id),
                    "components": _encode_components(op.components),
                }
            )
        elif isinstance(op, EntityDelete):
            ops.append({"op": "entity_delete", "entity_id": encode_id(op.entity_id)})
        elif isinstance(op, RelationCreate):
            ops.append(
                {
                    "op": "relation_create",
                    "relation_id": encode_id(op.relation_id),
                    "relation_type": op.relation_type,
                    "source_id": encode_id(op.source_id),
                    "target_id": encode_id(op.target_id),
                    "attributes": dict(op.attributes),
                }
            )
        else:
            ops.append({"op": "relation_delete", "relation_id": encode_id(op.relation_id)})
    return {
        "schema_version": CONTRACTS_SCHEMA_VERSION,
        "operations": ops,
    }


def delta_from_primitive(data: dict[str, Any]) -> ProposedWorldDelta:
    expect_version(data)
    ops: list[Any] = []
    for item in data.get("operations", []):
        kind = item["op"]
        if kind == "entity_create":
            ops.append(
                EntityCreate(
                    entity_id=decode_id(EntityId, item["entity_id"]),
                    entity_type=item["entity_type"],
                    components=_decode_components(item.get("components", [])),
                )
            )
        elif kind == "entity_update":
            ops.append(
                EntityUpdate(
                    entity_id=decode_id(EntityId, item["entity_id"]),
                    components=_decode_components(item.get("components", [])),
                )
            )
        elif kind == "entity_delete":
            ops.append(EntityDelete(entity_id=decode_id(EntityId, item["entity_id"])))
        elif kind == "relation_create":
            ops.append(
                RelationCreate(
                    relation_id=decode_id(RelationId, item["relation_id"]),
                    relation_type=item["relation_type"],
                    source_id=decode_id(EntityId, item["source_id"]),
                    target_id=decode_id(EntityId, item["target_id"]),
                    attributes={str(k): v for k, v in item.get("attributes", {}).items()},
                )
            )
        elif kind == "relation_delete":
            ops.append(RelationDelete(relation_id=decode_id(RelationId, item["relation_id"])))
        else:
            raise IncompatibleVersion(f"unknown delta operation {kind!r}")
    return ProposedWorldDelta(operations=tuple(ops))


def command_to_primitive(command: CommandEnvelope) -> dict[str, Any]:
    return {
        "schema_version": command.schema_version.value,
        "command_id": encode_id(command.command_id),
        "instance_id": encode_id(command.instance_id),
        "branch_id": encode_id(command.branch_id),
        "expected_revision": command.expected_revision.value,
        "action_type": command.action_type,
        "payload": dict(command.payload),
        "actor_id": encode_id(command.actor_id) if command.actor_id else None,
        "causation_id": encode_id(command.causation_id) if command.causation_id else None,
        "correlation_id": encode_id(command.correlation_id) if command.correlation_id else None,
        "world_time": command.world_time.ticks if command.world_time else None,
    }


def command_from_primitive(data: dict[str, Any]) -> CommandEnvelope:
    expect_version(data)
    return CommandEnvelope(
        command_id=decode_id(CommandId, data["command_id"]),
        instance_id=decode_id(WorldInstanceId, data["instance_id"]),
        branch_id=decode_id(BranchId, data["branch_id"]),
        expected_revision=BranchRevision(data["expected_revision"]),
        action_type=data["action_type"],
        payload={str(k): v for k, v in data.get("payload", {}).items()},
        actor_id=decode_id(ActorId, data["actor_id"]) if data.get("actor_id") else None,
        causation_id=decode_id(CommandId, data["causation_id"])
        if data.get("causation_id")
        else None,
        correlation_id=decode_id(CorrelationId, data["correlation_id"])
        if data.get("correlation_id")
        else None,
        world_time=WorldTime(data["world_time"]) if data.get("world_time") is not None else None,
        schema_version=SchemaVersion(data["schema_version"]),
    )
