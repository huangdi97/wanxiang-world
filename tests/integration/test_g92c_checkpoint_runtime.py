"""G92C real-runtime crash/resume and duplicate-command proof."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.long_horizon import (
    LongRunCheckpointService,
    RecurringSchedule,
    RecurringScheduler,
    RunCheckpointStore,
)
from wanxiang_substrate.temporal.query import TemporalQuery
from wanxiang_substrate.temporal.resolver import (
    ACTION_ADVANCE_TO,
    ACTION_INSTANTIATE,
    register_temporal_resolvers,
)


def test_resume_retries_are_idempotent_on_existing_runtime(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_temporal_resolvers)
    world = runtime.create_world(instance_id=WorldInstanceId("g92c_runtime"))
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("g92c_calendar"),
            instance_id=world.instance_id,
            branch_id=world.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "calendar", "version": 1},
            world_time=WorldTime(1),
        )
    )
    scheduler = RecurringScheduler()
    scheduler.add(RecurringSchedule("heartbeat", ACTION_ADVANCE_TO, 10, 10, max_occurrences=3))
    first = scheduler.advance_to(10)[0]
    first_command = CommandEnvelope(
        command_id=CommandId("g92c_tick_0"),
        instance_id=world.instance_id,
        branch_id=world.root_branch_id,
        expected_revision=BranchRevision(1),
        action_type=first.action,
        payload={"ticks": first.due_tick},
        world_time=WorldTime(first.due_tick),
    )
    runtime.submit_command(first_command)
    service = LongRunCheckpointService(RunCheckpointStore())
    service.checkpoint(
        "run-1",
        world.instance_id.value,
        world.root_branch_id.value,
        scheduler,
        state_hash=runtime.current_state(world.instance_id, world.root_branch_id).semantic_hash(),
        event_head=len(runtime.events(world.instance_id, world.root_branch_id)),
    )

    restarted_scheduler = RecurringScheduler()
    restarted_scheduler.add(
        RecurringSchedule("heartbeat", ACTION_ADVANCE_TO, 10, 10, max_occurrences=3)
    )
    service.resume("run-1", restarted_scheduler)
    duplicate = runtime.submit_command(first_command)
    assert duplicate.duplicate is True
    for item in restarted_scheduler.advance_to(30):
        state = runtime.current_state(world.instance_id, world.root_branch_id)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"g92c_tick_{item.occurrence}"),
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
    assert (
        runtime.restore_and_replay(world.instance_id, world.root_branch_id).state.semantic_hash()
        == final.semantic_hash()
    )
