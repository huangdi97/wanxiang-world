"""Deterministic agency queries over canonical state."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.agency.components import (
    ACTOR_STATE_COMPONENT,
    ORDER_COMPONENT,
)
from wanxiang_substrate.agency.model import Order
from wanxiang_substrate.institution.model import Membership
from wanxiang_substrate.institution.query import InstitutionQuery


class AgencyQuery:
    """Read-only agency projection (actors, orders, organization views)."""

    def __init__(self, state: InMemoryCanonicalState, now_ticks: int = 0) -> None:
        self._orders: dict[EntityId, Order] = {}
        self._actor_states: dict[EntityId, dict[str, object]] = {}
        self._now = now_ticks
        self._institution = InstitutionQuery(state, now_ticks=now_ticks)
        self._scan(state)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                if component.component_type == ORDER_COMPONENT:
                    order = _order_from(component.fields, entity.entity_id)
                    if order is not None:
                        self._orders[order.order_id] = order
                elif component.component_type == ACTOR_STATE_COMPONENT:
                    actor = component.fields.get("actor_id")
                    if isinstance(actor, str):
                        self._actor_states[EntityId(actor)] = dict(component.fields)

    def orders(
        self, actor_id: EntityId | None = None, *, state: str | None = None
    ) -> tuple[Order, ...]:
        items = [
            o
            for o in self._orders.values()
            if (actor_id is None or o.issuer_id == actor_id or o.receiver_id == actor_id)
            and (state is None or o.state == state)
        ]
        return tuple(sorted(items, key=lambda o: (o.order_id.value,)))

    def order(self, order_id: EntityId) -> Order | None:
        return self._orders.get(order_id)

    def actor_state(self, actor_id: EntityId) -> dict[str, object] | None:
        return self._actor_states.get(actor_id)

    def is_active(self, actor_id: EntityId) -> bool:
        state = self._actor_states.get(actor_id)
        return bool(state.get("active", True)) if state is not None else True

    def organization_members(self, organization_id: EntityId) -> tuple[EntityId, ...]:
        return tuple(
            sorted(
                {
                    m.actor_id
                    for m in self._all_memberships()
                    if m.institution_id == organization_id
                },
                key=lambda a: a.value,
            )
        )

    def _all_memberships(self) -> list[Membership]:
        known_actors = set(self._actor_states)
        for order in self._orders.values():
            known_actors.add(order.issuer_id)
            known_actors.add(order.receiver_id)
        result: list[Membership] = []
        for actor in known_actors:
            result.extend(self._institution.memberships(actor))
        return result


def _str(fields: Mapping[str, object], key: str) -> str | None:
    value = fields.get(key)
    return value if isinstance(value, str) and value else None


def _payload(fields: Mapping[str, object]) -> dict[str, FieldValue]:
    raw = fields.get("payload")
    if not isinstance(raw, str) or not raw:
        return {}
    try:
        decoded = json.loads(raw)
    except ValueError:
        return {}
    if not isinstance(decoded, dict):
        return {}
    decoded_map = cast(dict[str, object], decoded)
    result: dict[str, FieldValue] = {}
    for key, value in decoded_map.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            result[str(key)] = value
    return result


def _order_from(fields: Mapping[str, object], entity_id: EntityId) -> Order | None:
    order_id_raw = _str(fields, "order_id")
    issuer = _str(fields, "issuer_id")
    receiver = _str(fields, "receiver_id")
    action_type = _str(fields, "action_type")
    if order_id_raw is None or issuer is None or receiver is None or action_type is None:
        return None
    deviation = _str(fields, "deviation")
    return Order(
        order_id=EntityId(order_id_raw),
        issuer_id=EntityId(issuer),
        receiver_id=EntityId(receiver),
        action_type=action_type,
        payload=_payload(fields),  # type: ignore[arg-type]
        state=_str(fields, "state") or "issued",  # type: ignore[arg-type]
        deviation=deviation,
    )
