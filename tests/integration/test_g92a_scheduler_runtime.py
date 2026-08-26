"""G92A real-runtime proof: scheduler proposals enter the existing authority."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.long_horizon import RecurringSchedule, RecurringScheduler
from wanxiang_substrate.temporal.query import TemporalQuery
from wanxiang_substrate.temporal.resolver import (
    ACTION_ADVANCE_TO,
    ACTION_INSTANTIATE,
    register_temporal_resolvers,
)


def test_scheduler_occurrences_commit_through_existing_runtime(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_temporal_resolvers)
    world = runtime.create_world(instance_id=WorldInstanceId("g92a_runtime"))
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("g92a_calendar"),
            instance_id=world.instance_id,
            branch_id=world.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "calendar", "version": 1},
            world_time=WorldTime(1),
        )
    )

    scheduler = RecurringScheduler()
    scheduler.add(
        RecurringSchedule(
            schedule_id="calendar-ticks",
            action=ACTION_ADVANCE_TO,
            start_tick=10,
            interval_ticks=10,
            max_occurrences=3,
        )
    )
    occurrences = scheduler.advance_to(30)
    assert [item.due_tick for item in occurrences] == [10, 20, 30]

    for item in occurrences:
        state = runtime.current_state(world.instance_id, world.root_branch_id)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"g92a_tick_{item.occurrence}"),
                instance_id=world.instance_id,
                branch_id=world.root_branch_id,
                expected_revision=BranchRevision(state.revision.value),
                action_type=item.action,
                payload={"ticks": item.due_tick},
                world_time=WorldTime(item.due_tick),
            )
        )

    final = runtime.current_state(world.instance_id, world.root_branch_id)
    assert TemporalQuery(final).now() == 30
    assert len(runtime.events(world.instance_id, world.root_branch_id)) == 4
