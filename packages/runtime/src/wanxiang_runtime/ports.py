"""Ports at the runtime/persistence boundary.

Only Commit Authority appends committed events; the append port is the single
write seam for canonical history. In-memory adapters support unit-level
execution; durable adapters implement the same contract (GOAL_01C/01E).
"""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.errors import DuplicateCommandConflict, PersistenceError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import EventSeq
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId


class EventAppendPort(Protocol):
    """Append committed events durably and load them back."""

    def append(self, event: CommittedEvent) -> None: ...

    def load(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> tuple[CommittedEvent, ...]: ...

    def last_event_seq(self, instance_id: WorldInstanceId, branch_id: BranchId) -> EventSeq: ...

    def command_result_event(self, command_id: CommandId) -> CommittedEvent | None: ...


class InMemoryEventAppendLog:
    """All-or-nothing in-memory adapter with optional failure injection.

    `fail_append` simulates a persistence transaction failure to prove the
    atomicity contract: when append raises, no event is recorded.
    """

    def __init__(self) -> None:
        self._events: list[CommittedEvent] = []
        self.fail_append = False

    def append(self, event: CommittedEvent) -> None:
        if self.fail_append:
            raise PersistenceError("simulated append failure")
        if any(existing.event_id == event.event_id for existing in self._events):
            raise DuplicateCommandConflict(f"event {event.event_id.value} already appended")
        self._events.append(event)

    def load(self, instance_id: WorldInstanceId, branch_id: BranchId) -> tuple[CommittedEvent, ...]:
        return tuple(
            event
            for event in self._events
            if event.instance_id == instance_id and event.branch_id == branch_id
        )

    def last_event_seq(self, instance_id: WorldInstanceId, branch_id: BranchId) -> EventSeq:
        events = self.load(instance_id, branch_id)
        return EventSeq(events[-1].event_seq.value) if events else EventSeq(0)

    def command_result_event(self, command_id: CommandId) -> CommittedEvent | None:
        for event in reversed(self._events):
            if event.command_id == command_id:
                return event
        return None
