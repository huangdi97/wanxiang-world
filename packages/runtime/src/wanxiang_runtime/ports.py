"""Ports at the runtime/persistence boundary.

Only Commit Authority appends committed events. `EventStore` is the full
append/load contract with ordering, idempotency and integrity semantics;
`EventAppendPort` is the minimal append seam used by Commit Authority.
In-memory adapters support unit/contract tests; durable adapters implement the
same contract (GOAL_01C/01E).
"""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.errors import (
    Conflict,
    CorruptEventStream,
    DuplicateCommandConflict,
    PersistenceError,
)
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


class EventStore(Protocol):
    """Full event-stream contract: ordered append, range load, idempotency, integrity."""

    def append(self, event: CommittedEvent) -> None: ...

    def load(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        from_seq: int | None = None,
        to_seq: int | None = None,
    ) -> tuple[CommittedEvent, ...]: ...

    def last_event_seq(self, instance_id: WorldInstanceId, branch_id: BranchId) -> EventSeq: ...

    def command_result_event(self, command_id: CommandId) -> CommittedEvent | None: ...

    def has_command(self, command_id: CommandId) -> bool: ...

    def integrity_check(self, instance_id: WorldInstanceId, branch_id: BranchId) -> None: ...


class InMemoryEventStore:
    """All-or-nothing in-memory adapter with optional failure injection.

    Enforces per-branch strict event-sequence ordering, unique event ids and
    command-id idempotency. Ordering is by `event_seq`, never wall-clock.
    """

    def __init__(self) -> None:
        self._streams: dict[tuple[str, str], list[CommittedEvent]] = {}
        self._by_command: dict[str, CommittedEvent] = {}
        self.fail_append = False

    def append(self, event: CommittedEvent) -> None:
        if self.fail_append:
            raise PersistenceError("simulated append failure")
        key = (event.instance_id.value, event.branch_id.value)
        stream = self._streams.setdefault(key, [])
        expected = EventSeq(len(stream) + 1)
        if event.event_seq != expected:
            raise Conflict(
                f"out-of-order append: expected seq {expected.value}, got {event.event_seq.value}"
            )
        if any(existing.event_id == event.event_id for existing in stream):
            raise Conflict(f"duplicate event id {event.event_id.value}")
        if event.command_id.value in self._by_command:
            raise DuplicateCommandConflict(f"command {event.command_id.value} already committed")
        stream.append(event)
        self._by_command[event.command_id.value] = event

    def load(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        from_seq: int | None = None,
        to_seq: int | None = None,
    ) -> tuple[CommittedEvent, ...]:
        stream = self._streams.get((instance_id.value, branch_id.value), [])
        lower = from_seq if from_seq is not None else 0
        upper = to_seq if to_seq is not None else 2**63 - 1
        return tuple(event for event in stream if lower <= event.event_seq.value <= upper)

    def last_event_seq(self, instance_id: WorldInstanceId, branch_id: BranchId) -> EventSeq:
        stream = self._streams.get((instance_id.value, branch_id.value), [])
        return EventSeq(stream[-1].event_seq.value) if stream else EventSeq(0)

    def command_result_event(self, command_id: CommandId) -> CommittedEvent | None:
        return self._by_command.get(command_id.value)

    def has_command(self, command_id: CommandId) -> bool:
        return command_id.value in self._by_command

    def integrity_check(self, instance_id: WorldInstanceId, branch_id: BranchId) -> None:
        stream = self._streams.get((instance_id.value, branch_id.value), [])
        expected_seq = 1
        seen_event_ids: set[str] = set()
        for event in stream:
            if event.event_seq.value != expected_seq:
                raise CorruptEventStream(
                    f"expected event seq {expected_seq}, got {event.event_seq.value}"
                )
            if event.event_id.value in seen_event_ids:
                raise CorruptEventStream(f"duplicate event id {event.event_id.value}")
            seen_event_ids.add(event.event_id.value)
            expected_seq += 1
