"""SYNTHETIC micro-world resolvers (demo fixture, NOT core product domains).

This module is explicitly synthetic: it provides a tiny deterministic domain
(two+ entities holding a transferable resource) to exercise the authoritative
mutation path for M1. Real domain packs (narrative/household/heritage/...) are
separate packages and never hard-code into Core.
"""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

ACTION_CREATE_ENTITY = "create_entity"
ACTION_TRANSFER_RESOURCE = "transfer_resource"
ACTION_SET_STATUS = "set_status"

_RESOURCE = "resource"
_STATUS = "status"
_SCHEMA = SchemaVersion(1)


def register_synthetic_resolvers(registry: ResolverRegistry) -> None:
    """Register the synthetic micro-world actions on a resolver registry."""
    registry.register(ACTION_CREATE_ENTITY, _resolve_create_entity)
    registry.register(ACTION_TRANSFER_RESOURCE, _resolve_transfer_resource)
    registry.register(ACTION_SET_STATUS, _resolve_set_status)


def _payload(command: CommandEnvelope) -> dict[str, object]:
    return dict(command.payload)


def _str(payload: dict[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: dict[str, object], key: str, default: int | None = None) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _resource_component(entity: EntityId, count: int) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"res_{entity.value}"),
        component_type=_RESOURCE,
        schema_version=_SCHEMA,
        fields={"count": count},
    )


def _resolve_create_entity(
    command: CommandEnvelope, _state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = _payload(command)
    entity_id = EntityId(_str(payload, "entity_id"))
    count = _int(payload, "count", 0)
    if count < 0:
        raise ValidationRejected("count must be non-negative")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=entity_id,
                entity_type="person",
                components=(_resource_component(entity_id, count),),
            ),
        )
    )


def _resolve_transfer_resource(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = _payload(command)
    source = EntityId(_str(payload, "source_id"))
    target = EntityId(_str(payload, "target_id"))
    amount = _int(payload, "amount")
    if amount <= 0:
        raise ValidationRejected("amount must be positive")
    if state is None:
        raise ValidationRejected("transfer requires current state")
    source_entity = state.entity(source)
    if source_entity is None:
        raise ValidationRejected(f"source entity {source.value} does not exist")
    source_component = source_entity.components.get(ComponentId(f"res_{source.value}"))
    if source_component is None:
        raise ValidationRejected(f"source entity {source.value} has no resource")
    current = source_component.fields.get("count", 0)
    if not isinstance(current, int) or isinstance(current, bool):
        raise ValidationRejected(f"source entity {source.value} has a non-integer resource count")
    if current < amount:
        raise ValidationRejected(
            f"insufficient resource: {source.value} has {current}, needs {amount}"
        )
    target_entity = state.entity(target)
    if target_entity is None:
        raise ValidationRejected(f"target entity {target.value} does not exist")
    target_component = target_entity.components.get(ComponentId(f"res_{target.value}"))
    target_value = target_component.fields.get("count", 0) if target_component else 0
    target_current = (
        target_value if isinstance(target_value, int) and not isinstance(target_value, bool) else 0
    )
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=source,
                components=(_resource_component(source, current - amount),),
            ),
            EntityUpdate(
                entity_id=target,
                components=(_resource_component(target, target_current + amount),),
            ),
        )
    )


def _resolve_set_status(
    command: CommandEnvelope, _state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = _payload(command)
    entity_id = EntityId(_str(payload, "entity_id"))
    status = _str(payload, "status")
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=entity_id,
                components=(
                    ComponentData(
                        component_id=ComponentId(f"status_{entity_id.value}"),
                        component_type=_STATUS,
                        schema_version=_SCHEMA,
                        fields={"value": status},
                    ),
                ),
            ),
        )
    )
