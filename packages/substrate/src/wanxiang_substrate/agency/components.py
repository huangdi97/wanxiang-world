"""Agency component schema (versioned) on the M1 component model."""

from __future__ import annotations

import json

from wanxiang_domain.entity import ComponentData, FieldValue
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

AGENCY_SCHEMA_VERSION = SchemaVersion(1)

ORDER_COMPONENT = "agency.order"
ACTOR_STATE_COMPONENT = "agency.actor_state"


def order_component(
    order_id: EntityId,
    issuer_id: EntityId,
    receiver_id: EntityId,
    action_type: str,
    payload: dict[str, FieldValue],
    state: str = "issued",
    deviation: str | None = None,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"order_{order_id.value}"),
        component_type=ORDER_COMPONENT,
        schema_version=AGENCY_SCHEMA_VERSION,
        fields={
            "order_id": order_id.value,
            "issuer_id": issuer_id.value,
            "receiver_id": receiver_id.value,
            "action_type": action_type,
            "payload": json.dumps(payload, sort_keys=True),
            "state": state,
            "deviation": deviation,
        },
    )


def actor_state_component(
    actor_id: EntityId, active: bool = True, controller_policy: str = "deterministic"
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"actor_state_{actor_id.value}"),
        component_type=ACTOR_STATE_COMPONENT,
        schema_version=AGENCY_SCHEMA_VERSION,
        fields={
            "actor_id": actor_id.value,
            "active": active,
            "controller_policy": controller_policy,
        },
    )
