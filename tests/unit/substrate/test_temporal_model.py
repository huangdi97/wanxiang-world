"""G02B: temporal value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.temporal.model import (
    Appointment,
    Calendar,
    RecurringEvent,
    TimeWindowConstraint,
    WorldClock,
)


@pytest.mark.unit
def test_world_clock_is_monotonic() -> None:
    clock = WorldClock(ticks=5)
    assert clock.advance(3).ticks == 8
    with pytest.raises(ContractError):
        clock.advance(-1)
    with pytest.raises(ContractError):
        WorldClock(ticks=-1)


@pytest.mark.unit
def test_calendar_day_cycle() -> None:
    cal = Calendar(day_length_ticks=100)
    assert cal.day_of(0) == 0
    assert cal.day_of(199) == 1
    assert cal.day_of(200) == 2
    assert cal.day_name(150) == cal.day_names[1]
    with pytest.raises(ContractError):
        Calendar(day_length_ticks=0)


@pytest.mark.unit
def test_appointment_validation() -> None:
    with pytest.raises(ContractError):
        Appointment(EntityId("a"), EntityId("x"), "work", 10, 10)  # end <= start
    with pytest.raises(ContractError):
        Appointment(EntityId("a"), EntityId("x"), "", 10, 20)  # empty activity
    window = TimeWindowConstraint(0, 50)
    with pytest.raises(ContractError):
        Appointment(EntityId("a"), EntityId("x"), "work", 40, 60, window=window)


@pytest.mark.unit
def test_recurrence_deterministic_expansion() -> None:
    recurring = RecurringEvent(EntityId("r"), "duty", anchor_ticks=10, interval_ticks=10)
    assert recurring.occurrences(45) == (10, 20, 30, 40)
    assert recurring.occurrences(5) == ()
    with pytest.raises(ContractError):
        RecurringEvent(EntityId("r"), "duty", 0, 0)  # interval must be positive
    bounded = recurring.occurrences(10_000, cap=3)
    assert len(bounded) == 3


@pytest.mark.unit
def test_time_window_constraint() -> None:
    window = TimeWindowConstraint(10, 20)
    window.assert_allows(12, 18)
    with pytest.raises(ContractError):
        window.assert_allows(8, 18)
