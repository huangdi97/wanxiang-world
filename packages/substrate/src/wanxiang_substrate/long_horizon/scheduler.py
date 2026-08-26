"""Deterministic recurring scheduler for long-horizon world time.

The scheduler is a proposal-side time service.  It owns no canonical state and
does not call Commit Authority; a runtime adapter may consume its immutable
occurrences as commands after normal validation.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from wanxiang_domain.errors import ContractError

SchedulePayload = tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class AvailabilityWindow:
    """Half-open world-time availability window for one actor."""

    actor_id: str
    start_tick: int
    end_tick: int

    def __post_init__(self) -> None:
        if not self.actor_id:
            raise ContractError("availability actor_id must be non-empty")
        if self.start_tick < 0 or self.end_tick <= self.start_tick:
            raise ContractError("availability window must have positive non-negative span")

    def contains(self, tick: int) -> bool:
        return self.start_tick <= tick < self.end_tick


@dataclass(frozen=True, slots=True)
class ActorAvailability:
    """Immutable availability calendar; actors without windows are available."""

    windows: tuple[AvailabilityWindow, ...] = ()

    def __post_init__(self) -> None:
        keys = [(item.actor_id, item.start_tick, item.end_tick) for item in self.windows]
        if keys != sorted(keys):
            raise ContractError("availability windows must be sorted deterministically")

    def is_available(self, actor_id: str | None, tick: int) -> bool:
        if actor_id is None:
            return True
        actor_windows = tuple(item for item in self.windows if item.actor_id == actor_id)
        return not actor_windows or any(item.contains(tick) for item in actor_windows)


@dataclass(frozen=True, slots=True)
class RecurringSchedule:
    """A recurring proposal source expressed in deterministic world ticks."""

    schedule_id: str
    action: str
    start_tick: int
    interval_ticks: int
    priority: int = 0
    actor_id: str | None = None
    payload: SchedulePayload = ()
    max_occurrences: int | None = None
    time_zone: str = "world"

    def __post_init__(self) -> None:
        if not self.schedule_id or not self.action:
            raise ContractError("schedule_id and action must be non-empty")
        if self.start_tick < 0 or self.interval_ticks < 1:
            raise ContractError("schedule start must be non-negative and interval positive")
        if self.max_occurrences is not None and self.max_occurrences < 1:
            raise ContractError("max_occurrences must be positive when provided")
        if not self.time_zone:
            raise ContractError("time_zone must be non-empty")
        if tuple(sorted(self.payload)) != self.payload:
            raise ContractError("schedule payload must be sorted deterministically")

    def due_tick(self, occurrence: int) -> int:
        if occurrence < 0:
            raise ContractError("occurrence must be non-negative")
        if self.max_occurrences is not None and occurrence >= self.max_occurrences:
            raise ContractError("occurrence exceeds schedule limit")
        return self.start_tick + occurrence * self.interval_ticks


@dataclass(frozen=True, slots=True)
class ScheduledOccurrence:
    """One emitted recurring occurrence, including catch-up and availability."""

    schedule_id: str
    occurrence: int
    due_tick: int
    action: str
    priority: int
    actor_id: str | None
    payload: SchedulePayload
    catch_up: bool
    available: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "schedule_id": self.schedule_id,
            "occurrence": self.occurrence,
            "due_tick": self.due_tick,
            "action": self.action,
            "priority": self.priority,
            "actor_id": self.actor_id,
            "payload": [list(item) for item in self.payload],
            "catch_up": self.catch_up,
            "available": self.available,
        }


@dataclass(frozen=True, slots=True)
class SchedulerCursor:
    """Read-only cursor evidence for a scheduler checkpoint."""

    current_tick: int
    pending: tuple[tuple[str, int, int], ...]


@dataclass(slots=True)
class RecurringScheduler:
    """Priority-queue scheduler with deterministic catch-up semantics."""

    start_tick: int = 0
    availability: ActorAvailability = field(default_factory=ActorAvailability)
    _current_tick: int = field(init=False)
    _sequence: int = field(init=False, default=0)
    _schedules: dict[str, RecurringSchedule] = field(
        init=False, default_factory=dict[str, RecurringSchedule]
    )
    _queue: list[tuple[int, int, str, int, int]] = field(
        init=False, default_factory=list[tuple[int, int, str, int, int]]
    )

    def __post_init__(self) -> None:
        if self.start_tick < 0:
            raise ContractError("scheduler start_tick must be non-negative")
        self._current_tick = self.start_tick

    @property
    def current_tick(self) -> int:
        return self._current_tick

    def add(self, schedule: RecurringSchedule) -> None:
        """Register a schedule and enqueue its first occurrence."""
        if schedule.schedule_id in self._schedules:
            raise ContractError(f"duplicate schedule {schedule.schedule_id!r}")
        self._schedules[schedule.schedule_id] = schedule
        self._enqueue(schedule, occurrence=0)

    def remove(self, schedule_id: str) -> None:
        """Remove future occurrences; already emitted occurrences remain evidence."""
        if schedule_id not in self._schedules:
            raise ContractError(f"unknown schedule {schedule_id!r}")
        del self._schedules[schedule_id]

    def advance_to(self, target_tick: int) -> tuple[ScheduledOccurrence, ...]:
        """Advance monotonically and emit every due occurrence, including catch-up."""
        if target_tick < self._current_tick:
            raise ContractError("scheduler cannot move world time backwards")
        emitted: list[ScheduledOccurrence] = []
        self._current_tick = target_tick
        while self._queue and self._queue[0][0] <= target_tick:
            due_tick, _negative_priority, schedule_id, occurrence, _sequence = heapq.heappop(
                self._queue
            )
            schedule = self._schedules.get(schedule_id)
            if schedule is None:
                continue
            emitted.append(
                ScheduledOccurrence(
                    schedule_id=schedule_id,
                    occurrence=occurrence,
                    due_tick=due_tick,
                    action=schedule.action,
                    priority=schedule.priority,
                    actor_id=schedule.actor_id,
                    payload=schedule.payload,
                    catch_up=due_tick < target_tick,
                    available=self.availability.is_available(schedule.actor_id, due_tick),
                )
            )
            next_occurrence = occurrence + 1
            if schedule.max_occurrences is None or next_occurrence < schedule.max_occurrences:
                self._enqueue(schedule, occurrence=next_occurrence)
        return tuple(emitted)

    def pending(self) -> tuple[tuple[str, int, int], ...]:
        """Return future queue entries as (schedule, occurrence, due_tick)."""
        return tuple(
            (schedule_id, occurrence, due_tick)
            for due_tick, _priority, schedule_id, occurrence, _sequence in sorted(self._queue)
            if schedule_id in self._schedules
        )

    def cursor(self) -> SchedulerCursor:
        return SchedulerCursor(self._current_tick, self.pending())

    def _enqueue(self, schedule: RecurringSchedule, *, occurrence: int) -> None:
        due_tick = schedule.due_tick(occurrence)
        heapq.heappush(
            self._queue,
            (due_tick, -schedule.priority, schedule.schedule_id, occurrence, self._sequence),
        )
        self._sequence += 1


__all__ = [
    "ActorAvailability",
    "AvailabilityWindow",
    "RecurringSchedule",
    "RecurringScheduler",
    "ScheduledOccurrence",
    "SchedulePayload",
    "SchedulerCursor",
]
