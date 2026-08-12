"""Deterministic body/condition queries over canonical state (read-only)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.body.components import (
    BODY_CONDITION_COMPONENT,
    CONDITION_VISIBILITY_COMPONENT,
)
from wanxiang_substrate.body.model import BodyCondition, Facet, MobilityCapability, visible_facets


class BodyQuery:
    """Read-only body/condition projection over the canonical state."""

    def __init__(self, state: InMemoryCanonicalState) -> None:
        self._conditions: dict[EntityId, BodyCondition] = {}
        self._private: dict[EntityId, frozenset[Facet]] = {}
        self._scan(state)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                if component.component_type == BODY_CONDITION_COMPONENT:
                    self._conditions[entity.entity_id] = BodyCondition(
                        health=_int(component.fields, "health", 100),
                        energy=_int(component.fields, "energy", 100),
                        sleep=_int(component.fields, "sleep", 100),
                        pain=_int(component.fields, "pain", 0),
                        mobility=_int(component.fields, "mobility", 100),
                    )
                elif component.component_type == CONDITION_VISIBILITY_COMPONENT:
                    raw = component.fields.get("private", "")
                    if isinstance(raw, str):
                        self._private[entity.entity_id] = frozenset(
                            cast(Facet, f) for f in raw.split(",") if f
                        )

    def condition(self, actor_id: EntityId) -> BodyCondition | None:
        return self._conditions.get(actor_id)

    def mobility(self, actor_id: EntityId) -> MobilityCapability:
        condition = self.condition(actor_id)
        if condition is None:
            return "unrestricted"
        return condition.mobility_capability()

    def can_move(self, actor_id: EntityId) -> bool:
        condition = self.condition(actor_id)
        if condition is None:
            return True
        return condition.mobility_capability() != "immobile" and not condition.is_fatigued()

    def is_fatigued(self, actor_id: EntityId) -> bool:
        condition = self.condition(actor_id)
        return condition.is_fatigued() if condition is not None else False

    def public_condition(self, actor_id: EntityId) -> dict[str, int]:
        condition = self.condition(actor_id)
        if condition is None:
            return {}
        return visible_facets(condition, self._private.get(actor_id, frozenset()))


def _int(fields: Mapping[str, object], key: str, default: int) -> int:
    value = fields.get(key, default)
    return value if isinstance(value, int) and not isinstance(value, bool) else default
