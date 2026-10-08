"""Deterministic epistemic queries over canonical state (actor-scoped)."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.epistemic.components import (
    BELIEF_COMPONENT,
    MEMORY_ACCESS_COMPONENT,
    MEMORY_COMPONENT,
)
from wanxiang_substrate.epistemic.errors import MemoryAccessDenied
from wanxiang_substrate.epistemic.model import (
    BeliefAssertion,
    MemoryKind,
    MemoryRecord,
)


class EpistemicQuery:
    """Read-only epistemic projection (beliefs, memories, authorization)."""

    def __init__(self, state: InMemoryCanonicalState, now_ticks: int = 0) -> None:
        self._beliefs: dict[EntityId, BeliefAssertion] = {}
        self._memories: dict[EntityId, MemoryRecord] = {}
        self._access: dict[EntityId, frozenset[EntityId]] = {}
        self._now = now_ticks
        self._scan(state)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                if component.component_type == BELIEF_COMPONENT:
                    belief = _belief_from(component.fields, entity.entity_id)
                    if belief is not None:
                        self._beliefs[belief.belief_id] = belief
                elif component.component_type == MEMORY_COMPONENT:
                    memory = memory_from_component(component.fields, entity.entity_id)
                    if memory is not None:
                        self._memories[memory.memory_id] = memory
                elif component.component_type == MEMORY_ACCESS_COMPONENT:
                    owner = component.fields.get("owner_id")
                    authorized = component.fields.get("authorized_actor")
                    if isinstance(owner, str) and isinstance(authorized, str):
                        owner_id = EntityId(owner)
                        granted = self._access.get(owner_id, frozenset())
                        self._access[owner_id] = granted | {EntityId(authorized)}

    # -- retrieval with authorization -------------------------------------

    def can_read_memory(self, owner: EntityId, requester: EntityId) -> bool:
        return requester == owner or requester in self._access.get(owner, frozenset())

    def require_memory_access(self, owner: EntityId, requester: EntityId) -> None:
        if not self.can_read_memory(owner, requester):
            raise MemoryAccessDenied(
                f"{requester.value} is not authorized to read {owner.value}'s memory"
            )

    # -- beliefs -----------------------------------------------------------

    def belief(self, belief_id: EntityId) -> BeliefAssertion | None:
        return self._beliefs.get(belief_id)

    def beliefs(
        self, actor_id: EntityId, *, include_inactive: bool = False
    ) -> tuple[BeliefAssertion, ...]:
        items = [
            b
            for b in self._beliefs.values()
            if b.actor_id == actor_id and (include_inactive or b.status == "active")
        ]
        return tuple(sorted(items, key=lambda b: (b.at_ticks, b.belief_id.value)))

    def belief_history(self, actor_id: EntityId, proposition: str) -> tuple[BeliefAssertion, ...]:
        return tuple(
            b for b in self.beliefs(actor_id, include_inactive=True) if b.proposition == proposition
        )

    def active_belief(self, actor_id: EntityId, proposition: str) -> BeliefAssertion | None:
        candidates = [b for b in self.beliefs(actor_id) if b.proposition == proposition]
        if not candidates:
            return None
        return max(candidates, key=lambda b: (b.at_ticks, b.confidence, b.belief_id.value))

    def contradictions(self, actor_id: EntityId, proposition: str) -> tuple[BeliefAssertion, ...]:
        """Retained contradictory beliefs on the same proposition."""
        return tuple(
            b
            for b in self.belief_history(actor_id, proposition)
            if b.status in ("active", "superseded")
        )

    # -- memories ----------------------------------------------------------

    def memories(
        self,
        actor_id: EntityId,
        *,
        kind: MemoryKind | None = None,
        include_forgotten: bool = False,
    ) -> tuple[MemoryRecord, ...]:
        items = [
            m
            for m in self._memories.values()
            if m.actor_id == actor_id
            and (kind is None or m.kind == kind)
            and (include_forgotten or not m.forgotten)
        ]
        return tuple(sorted(items, key=lambda m: (-m.salience, m.at_ticks, m.memory_id.value)))


def _str(fields: Mapping[str, object], key: str) -> str | None:
    value = fields.get(key)
    return value if isinstance(value, str) and value else None


def _float(fields: Mapping[str, object], key: str, default: float) -> float:
    value = fields.get(key, default)
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else default


def _int(fields: Mapping[str, object], key: str, default: int) -> int:
    value = fields.get(key, default)
    return value if isinstance(value, int) and not isinstance(value, bool) else default


def _belief_from(fields: Mapping[str, object], entity_id: EntityId) -> BeliefAssertion | None:
    belief_id_raw = _str(fields, "belief_id")
    actor = _str(fields, "actor_id")
    proposition = _str(fields, "proposition")
    if belief_id_raw is None or actor is None or proposition is None:
        return None
    supersedes_raw = _str(fields, "supersedes")
    corrected_raw = _str(fields, "corrected_by")
    return BeliefAssertion(
        belief_id=EntityId(belief_id_raw),
        actor_id=EntityId(actor),
        proposition=proposition,
        confidence=_float(fields, "confidence", 0.5),
        at_ticks=_int(fields, "at_ticks", 0),
        source_ref=_str(fields, "source_ref"),
        status=_str(fields, "status") or "active",  # type: ignore[arg-type]
        supersedes=EntityId(supersedes_raw) if supersedes_raw else None,
        corrected_by=EntityId(corrected_raw) if corrected_raw else None,
        stance=_str(fields, "stance") or "unknown",  # type: ignore[arg-type]
    )


def memory_from_component(fields: Mapping[str, object], entity_id: EntityId) -> MemoryRecord | None:
    memory_id_raw = _str(fields, "memory_id")
    actor = _str(fields, "actor_id")
    content_ref = _str(fields, "content_ref")
    if memory_id_raw is None or actor is None or content_ref is None:
        return None
    return MemoryRecord(
        memory_id=EntityId(memory_id_raw),
        actor_id=EntityId(actor),
        kind=_str(fields, "kind") or "observation",  # type: ignore[arg-type]
        content_ref=content_ref,
        at_ticks=_int(fields, "at_ticks", 0),
        salience=_float(fields, "salience", 0.5),
        source_obs_ref=_str(fields, "source_obs_ref"),
        forgotten=fields.get("forgotten") is True,
        source_perception_refs=_refs(fields, "source_perception_refs"),
        decay_rate=_float(fields, "decay_rate", 0.0),
        reinforcement_count=_int(fields, "reinforcement_count", 0),
        last_reinforced_ticks=_optional_int(fields, "last_reinforced_ticks"),
    )


def _refs(fields: Mapping[str, object], key: str) -> tuple[str, ...]:
    raw = fields.get(key)
    if not isinstance(raw, str) or not raw:
        return ()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return ()
    if not isinstance(value, list):
        return ()
    return tuple(item for item in cast(list[object], value) if isinstance(item, str) and item)


def _optional_int(fields: Mapping[str, object], key: str) -> int | None:
    value = fields.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else None
