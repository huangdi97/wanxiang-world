"""Pure temporal value objects and invariants (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

AppointmentState = Literal["pending", "active", "done"]
DeadlineState = Literal["pending", "met", "missed"]


def _validate_ticks(value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ContractError("world clock ticks must be a non-negative integer")


@dataclass(frozen=True, slots=True)
class WorldClock:
    """Monotonic world clock (independent of wall clock)."""

    ticks: int
    paused: bool = False

    def __post_init__(self) -> None:
        _validate_ticks(self.ticks)

    def advance(self, delta: int) -> WorldClock:
        if delta < 0:
            raise ContractError("world clock cannot advance by a negative delta")
        return WorldClock(ticks=self.ticks + delta, paused=self.paused)


@dataclass(frozen=True, slots=True)
class Calendar:
    """Synthetic calendar: a day length in ticks and a named day cycle."""

    day_length_ticks: int
    day_names: tuple[str, ...] = ("day_0", "day_1")

    def __post_init__(self) -> None:
        if self.day_length_ticks <= 0:
            raise ContractError("day length must be positive")
        if not self.day_names:
            raise ContractError("calendar needs at least one day name")

    def day_of(self, ticks: int) -> int:
        if ticks < 0:
            raise ContractError("ticks must be non-negative")
        return ticks // self.day_length_ticks

    def day_name(self, ticks: int) -> str:
        return self.day_names[self.day_of(ticks) % len(self.day_names)]


@dataclass(frozen=True, slots=True)
class Appointment:
    appointment_id: EntityId
    actor_id: EntityId
    activity: str
    start_ticks: int
    end_ticks: int
    state: AppointmentState = "pending"
    window: TimeWindowConstraint | None = None

    def __post_init__(self) -> None:
        if self.start_ticks < 0 or self.end_ticks < 0:
            raise ContractError("appointment ticks must be non-negative")
        if self.end_ticks <= self.start_ticks:
            raise ContractError("appointment end must be after start")
        if not self.activity:
            raise ContractError("appointment activity must be non-empty")
        if self.window is not None:
            self.window.assert_allows(self.start_ticks, self.end_ticks)


@dataclass(frozen=True, slots=True)
class Deadline:
    deadline_id: EntityId
    target_id: EntityId
    due_ticks: int
    state: DeadlineState = "pending"

    def __post_init__(self) -> None:
        if self.due_ticks < 0:
            raise ContractError("deadline due ticks must be non-negative")


@dataclass(frozen=True, slots=True)
class RecurringEvent:
    recurring_id: EntityId
    activity: str
    anchor_ticks: int
    interval_ticks: int
    state: Literal["active", "suspended"] = "active"

    def __post_init__(self) -> None:
        if self.anchor_ticks < 0:
            raise ContractError("recurrence anchor must be non-negative")
        if self.interval_ticks <= 0:
            raise ContractError("recurrence interval must be positive")
        if not self.activity:
            raise ContractError("recurrence activity must be non-empty")

    def occurrences(self, horizon_ticks: int, *, cap: int = 100) -> tuple[int, ...]:
        """Deterministic bounded expansion of due times within the horizon."""
        if horizon_ticks < self.anchor_ticks:
            return ()
        result: list[int] = []
        due = self.anchor_ticks
        while due <= horizon_ticks and len(result) < cap:
            result.append(due)
            due += self.interval_ticks
        return tuple(result)


@dataclass(frozen=True, slots=True)
class TimeWindowConstraint:
    """A schedule must fit entirely inside [start, end]."""

    start_ticks: int
    end_ticks: int

    def __post_init__(self) -> None:
        if self.start_ticks < 0 or self.end_ticks < 0:
            raise ContractError("window ticks must be non-negative")
        if self.end_ticks <= self.start_ticks:
            raise ContractError("window end must be after start")

    def assert_allows(self, appointment_start: int, appointment_end: int) -> None:
        if appointment_start < self.start_ticks or appointment_end > self.end_ticks:
            raise ContractError("appointment does not fit in the time window")
