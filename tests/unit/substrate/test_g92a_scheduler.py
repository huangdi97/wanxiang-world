"""G92A deterministic long-horizon scheduler contract tests."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.long_horizon import (
    ActorAvailability,
    AvailabilityWindow,
    RecurringSchedule,
    RecurringScheduler,
)


def test_priority_queue_and_catch_up_are_deterministic() -> None:
    def build() -> RecurringScheduler:
        scheduler = RecurringScheduler()
        scheduler.add(
            RecurringSchedule(
                schedule_id="low",
                action="actor.rest",
                start_tick=2,
                interval_ticks=3,
                priority=1,
                actor_id="alice",
            )
        )
        scheduler.add(
            RecurringSchedule(
                schedule_id="high",
                action="actor.duty",
                start_tick=2,
                interval_ticks=4,
                priority=9,
                actor_id="alice",
            )
        )
        return scheduler

    first = build()
    second = build()
    events = first.advance_to(8)
    assert [event.schedule_id for event in events] == ["high", "low", "low", "high", "low"]
    assert [event.due_tick for event in events] == [2, 2, 5, 6, 8]
    assert all(event.catch_up for event in events[:-1])
    assert [event.to_dict() for event in events] == [
        event.to_dict() for event in second.advance_to(8)
    ]
    assert first.current_tick == 8


def test_availability_is_observable_without_dropping_due_occurrences() -> None:
    scheduler = RecurringScheduler(
        availability=ActorAvailability(
            windows=(AvailabilityWindow("alice", start_tick=4, end_tick=7),)
        )
    )
    scheduler.add(
        RecurringSchedule(
            schedule_id="alice-duty",
            action="actor.duty",
            start_tick=2,
            interval_ticks=2,
            actor_id="alice",
            max_occurrences=3,
        )
    )
    events = scheduler.advance_to(6)
    assert [(event.due_tick, event.available) for event in events] == [
        (2, False),
        (4, True),
        (6, True),
    ]
    assert scheduler.pending() == ()


def test_scheduler_rejects_duplicate_ids_and_time_regression() -> None:
    scheduler = RecurringScheduler()
    schedule = RecurringSchedule("one", "world.tick", 1, 1)
    scheduler.add(schedule)
    with pytest.raises(ContractError):
        scheduler.add(schedule)
    scheduler.advance_to(2)
    with pytest.raises(ContractError):
        scheduler.advance_to(1)
