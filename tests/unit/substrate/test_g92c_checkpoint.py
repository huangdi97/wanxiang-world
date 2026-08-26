"""G92C atomic cursor checkpoint and resume tests."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.long_horizon import (
    CheckpointCrash,
    CrashPlan,
    LongRunCheckpointService,
    RecurringSchedule,
    RecurringScheduler,
    RunCheckpointStore,
)


def _scheduler() -> RecurringScheduler:
    scheduler = RecurringScheduler()
    scheduler.add(RecurringSchedule("pulse", "world.pulse", 5, 5, max_occurrences=4))
    return scheduler


def test_resume_restores_pending_cursor_without_replaying_due_events() -> None:
    scheduler = _scheduler()
    assert [item.due_tick for item in scheduler.advance_to(5)] == [5]
    service = LongRunCheckpointService(RunCheckpointStore())
    checkpoint = service.checkpoint(
        "run-1",
        "world-1",
        "branch-1",
        scheduler,
        state_hash="hash-5",
        event_head=7,
    )

    restarted = _scheduler()
    restored = service.resume("run-1", restarted)
    assert restored.fingerprint == checkpoint.fingerprint
    assert restarted.current_tick == 5
    assert [item.due_tick for item in restarted.advance_to(15)] == [10, 15]


def test_crash_injection_is_atomic_and_keeps_previous_checkpoint() -> None:
    store = RunCheckpointStore(crash_plan=CrashPlan((2,)))
    service = LongRunCheckpointService(store)
    scheduler = _scheduler()
    scheduler.advance_to(5)
    service.checkpoint("run-2", "world-1", "branch-1", scheduler, state_hash="h5", event_head=1)
    scheduler.advance_to(10)
    with pytest.raises(CheckpointCrash):
        service.checkpoint(
            "run-2", "world-1", "branch-1", scheduler, state_hash="h10", event_head=2
        )
    latest = store.latest("run-2")
    assert latest is not None and latest.checkpoint_seq == 1
    assert len(store.history("run-2")) == 1


def test_checkpoint_rejects_cursor_or_event_regression() -> None:
    store = RunCheckpointStore()
    service = LongRunCheckpointService(store)
    scheduler = _scheduler()
    scheduler.advance_to(10)
    service.checkpoint("run-3", "world-1", "branch-1", scheduler, state_hash="h10", event_head=2)
    latest = store.latest("run-3")
    assert latest is not None
    with pytest.raises(ContractError):
        store.save(replace(latest, checkpoint_seq=2, event_head=1))
