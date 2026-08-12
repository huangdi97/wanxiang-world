"""Agency resolvers: order lifecycle + actor state through the M1 authority."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData, FieldValue
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.agency.components import (
    ORDER_COMPONENT,
    actor_state_component,
    order_component,
)
from wanxiang_substrate.agency.errors import OrderStateConflict
from wanxiang_substrate.agency.query import AgencyQuery

ACTION_ISSUE_ORDER = "agency.issue_order"
ACTION_RECEIVE_ORDER = "agency.receive_order"
ACTION_ACCEPT_ORDER = "agency.accept_order"
ACTION_REJECT_ORDER = "agency.reject_order"
ACTION_EXECUTE_ORDER = "agency.execute_order"
ACTION_REPORT_ORDER = "agency.report_order"
ACTION_SET_ACTOR_STATE = "agency.set_actor_state"
ACTION_INSTANTIATE = "agency.instantiate"


def register_agency_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_ISSUE_ORDER, _issue_order)
    registry.register(ACTION_RECEIVE_ORDER, _transition(ORDER_COMPONENT, "received"))
    registry.register(ACTION_ACCEPT_ORDER, _transition(ORDER_COMPONENT, "accepted"))
    registry.register(ACTION_REJECT_ORDER, _transition(ORDER_COMPONENT, "rejected"))
    registry.register(ACTION_EXECUTE_ORDER, _execute_order)
    registry.register(ACTION_REPORT_ORDER, _transition(ORDER_COMPONENT, "reported"))
    registry.register(ACTION_SET_ACTOR_STATE, _set_actor_state)
    registry.register(ACTION_INSTANTIATE, _instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _payload_field(payload: Mapping[str, object], key: str) -> dict[str, FieldValue]:
    value = payload.get(key, "{}")
    if not isinstance(value, str):
        raise ValidationRejected(f"payload field {key!r} must be a JSON string")
    try:
        decoded = json.loads(value)
    except ValueError as exc:
        raise ValidationRejected(f"payload field {key!r} is not valid JSON") from exc
    if not isinstance(decoded, dict):
        raise ValidationRejected(f"payload field {key!r} must encode a mapping")
    decoded_map = cast(dict[str, object], decoded)
    result: dict[str, FieldValue] = {}
    for k, v in decoded_map.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            result[str(k)] = v
    return result


def _issue_order(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    order_id = EntityId(_str(payload, "order_id"))
    issuer = EntityId(_str(payload, "issuer_id"))
    receiver = EntityId(_str(payload, "receiver_id"))
    action_type = _str(payload, "action_type")
    order_payload = _payload_field(payload, "payload")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=order_id,
                entity_type="agency.order",
                components=(
                    order_component(order_id, issuer, receiver, action_type, order_payload),
                ),
            ),
        )
    )


def _transition(component_type: str, next_state: str):
    def handler(
        command: CommandEnvelope, state: InMemoryCanonicalState | None
    ) -> ProposedWorldDelta:
        if state is None:
            raise ValidationRejected("order transition requires current state")
        payload = dict(command.payload)
        order_id = EntityId(_str(payload, "order_id"))
        query = AgencyQuery(state)
        order = query.order(order_id)
        if order is None:
            raise ValidationRejected(f"order {order_id.value} does not exist")
        if not order.can_transition_to(next_state):  # type: ignore[arg-type]
            raise OrderStateConflict(
                f"order {order_id.value} cannot transition from {order.state} to {next_state}"
            )
        entity = state.entity(order_id)
        assert entity is not None
        current = next(
            (c for c in entity.components.values() if c.component_type == component_type), None
        )
        if current is None:
            raise ValidationRejected(f"entity {order_id.value} is not an order")
        fields = dict(current.fields)
        fields["state"] = next_state
        updated = ComponentData(
            component_id=current.component_id,
            component_type=component_type,
            schema_version=current.schema_version,
            fields=fields,
        )
        return ProposedWorldDelta(
            operations=(EntityUpdate(entity_id=order_id, components=(updated,)),)
        )

    return handler


def _execute_order(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("execute requires current state")
    payload = dict(command.payload)
    order_id = EntityId(_str(payload, "order_id"))
    outcome = _str(payload, "outcome")
    deviation = payload.get("deviation")
    query = AgencyQuery(state)
    order = query.order(order_id)
    if order is None:
        raise ValidationRejected(f"order {order_id.value} does not exist")
    if not order.can_transition_to("executed"):
        raise OrderStateConflict(
            f"order {order_id.value} cannot transition from {order.state} to executed"
        )
    entity = state.entity(order_id)
    assert entity is not None
    current = next(
        (c for c in entity.components.values() if c.component_type == ORDER_COMPONENT), None
    )
    if current is None:
        raise ValidationRejected(f"entity {order_id.value} is not an order")
    fields = dict(current.fields)
    fields["state"] = "executed"
    fields["deviation"] = deviation
    fields["outcome"] = outcome
    updated = ComponentData(
        component_id=current.component_id,
        component_type=ORDER_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(operations=(EntityUpdate(entity_id=order_id, components=(updated,)),))


def _set_actor_state(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    active = payload.get("active", True)
    if not isinstance(active, bool):
        raise ValidationRejected("active must be a boolean")
    policy = str(payload.get("controller_policy") or "deterministic")
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=actor_id,
                components=(actor_state_component(actor_id, active, policy),),
            ),
        )
    )


def _instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic agency fixture."""
    from wanxiang_substrate.agency.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
