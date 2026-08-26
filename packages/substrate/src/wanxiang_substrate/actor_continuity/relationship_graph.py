"""Replayable, permission-filtered relationship projection."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.relationship_model import (
    RelationshipState,
)


@dataclass(frozen=True, slots=True)
class RelationshipRevisionEvent:
    """Actor-projection event carrying before/after relationship state."""

    event_ref: str
    sequence: int
    at_ticks: int
    reason: str
    after: RelationshipState
    before: RelationshipState | None = None

    def __post_init__(self) -> None:
        if not self.event_ref.strip() or not self.reason.strip():
            raise ContractError("relationship revision requires ref and reason")
        if self.sequence < 1 or self.at_ticks < 0:
            raise ContractError("relationship revision sequence/time is invalid")
        if self.before is not None and self.before.relationship_id != self.after.relationship_id:
            raise ContractError("relationship revision ids do not match")


@dataclass(frozen=True, slots=True)
class RelationshipGraph:
    """Immutable relation timeline with actor-scoped read projections."""

    states: tuple[RelationshipState, ...] = ()
    revisions: tuple[RelationshipRevisionEvent, ...] = ()

    def _current(self, relationship_id: str) -> RelationshipState | None:
        matches = [
            (index, item)
            for index, item in enumerate(self.states)
            if item.relationship_id == relationship_id
        ]
        return max(matches, key=lambda pair: (pair[1].valid_from, pair[0]), default=(0, None))[1]

    def state(
        self, relationship_id: str, *, at_ticks: int | None = None
    ) -> RelationshipState | None:
        candidates = [item for item in self.states if item.relationship_id == relationship_id]
        if at_ticks is not None:
            candidates = [item for item in candidates if item.active_at(at_ticks)]
        if not candidates:
            return None
        return max(enumerate(candidates), key=lambda pair: (pair[1].valid_from, pair[0]))[1]

    def visible_to(
        self, viewer_actor_id: EntityId, *, at_ticks: int | None = None, admin: bool = False
    ) -> tuple[RelationshipState, ...]:
        latest: dict[str, RelationshipState] = {}
        for item in self.states:
            if at_ticks is not None and not item.active_at(at_ticks):
                continue
            if not item.visible_to(viewer_actor_id, admin=admin):
                continue
            current = latest.get(item.relationship_id)
            if current is None or item.valid_from >= current.valid_from:
                latest[item.relationship_id] = item
        return tuple(latest[key] for key in sorted(latest))

    def add(
        self,
        state: RelationshipState,
        *,
        event_ref: str,
        at_ticks: int,
        reason: str,
    ) -> tuple[RelationshipGraph, RelationshipRevisionEvent]:
        if self._current(state.relationship_id) is not None:
            raise ContractError("relationship already exists")
        event = RelationshipRevisionEvent(
            event_ref=event_ref,
            sequence=len(self.revisions) + 1,
            at_ticks=at_ticks,
            reason=reason,
            after=state,
        )
        return self.apply(event), event

    def revise(
        self,
        state: RelationshipState,
        *,
        event_ref: str,
        at_ticks: int,
        reason: str,
    ) -> tuple[RelationshipGraph, RelationshipRevisionEvent]:
        before = self._current(state.relationship_id)
        if before is None:
            raise ContractError("relationship does not exist")
        if state.valid_from < before.valid_from:
            raise ContractError("relationship revision moves backwards in time")
        event = RelationshipRevisionEvent(
            event_ref=event_ref,
            sequence=len(self.revisions) + 1,
            at_ticks=at_ticks,
            reason=reason,
            before=before,
            after=state,
        )
        return self.apply(event), event

    def apply(self, event: RelationshipRevisionEvent) -> RelationshipGraph:
        if event.sequence != len(self.revisions) + 1:
            raise ContractError("relationship revision sequence does not match graph")
        current = self._current(event.after.relationship_id)
        if event.before is None:
            if current is not None:
                raise ContractError("relationship creation collides with existing state")
        elif current != event.before:
            raise ContractError("relationship revision before value does not match graph")
        return RelationshipGraph(
            states=self.states + (event.after,),
            revisions=self.revisions + (event,),
        )

    @classmethod
    def replay(cls, events: tuple[RelationshipRevisionEvent, ...]) -> RelationshipGraph:
        graph = cls()
        for event in events:
            graph = graph.apply(event)
        return graph
