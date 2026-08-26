"""G92B background/offline policy tests."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.long_horizon import (
    BackgroundPolicy,
    BackgroundSimulation,
    RecurringSchedule,
    RecurringScheduler,
)
from wanxiang_substrate.playable.models import RuntimeProfile


def test_runtime_profile_controls_each_background_mode() -> None:
    profile = RuntimeProfile("long-run", time_scale=4)
    assert BackgroundPolicy(profile, "paused").world_ticks(10) == 0
    assert BackgroundPolicy(profile, "realtime").world_ticks(10) == 10
    assert BackgroundPolicy(profile, "accelerated").world_ticks(10) == 40
    assert BackgroundPolicy(profile, "background").world_ticks(10) == 40
    assert BackgroundPolicy(profile, "full_autonomy").world_ticks(10) == 40


def test_leave_run_reenter_is_session_independent() -> None:
    scheduler = RecurringScheduler()
    scheduler.add(RecurringSchedule("pulse", "world.pulse", 5, 5, max_occurrences=2))
    simulation = BackgroundSimulation(
        scheduler,
        BackgroundPolicy(RuntimeProfile("deterministic", time_scale=2), "accelerated"),
        world_ref="world-1",
        branch_ref="branch-1",
    )
    cursor = simulation.leave("interactive-session")
    run = simulation.run_offline(cursor, elapsed_ticks=5)
    assert [item.due_tick for item in run.occurrences] == [5, 10]
    assert run.world_ticks_advanced == 10
    assert run.session_independent is True
    assert simulation.reenter(run).to_dict()["world_tick"] == 10


def test_paused_mode_does_not_advance_and_stale_cursor_is_rejected() -> None:
    scheduler = RecurringScheduler()
    simulation = BackgroundSimulation(
        scheduler,
        BackgroundPolicy(RuntimeProfile("paused"), "paused"),
        world_ref="world-1",
        branch_ref="branch-1",
    )
    cursor = simulation.leave("session")
    run = simulation.run_offline(cursor, elapsed_ticks=100)
    assert run.world_ticks_advanced == 0
    assert run.occurrences == ()
    scheduler.advance_to(1)
    with pytest.raises(ContractError):
        simulation.run_offline(cursor, elapsed_ticks=1)
