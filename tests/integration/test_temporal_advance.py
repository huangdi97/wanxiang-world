"""G02B: temporal advance/schedules through the M1 Commit Authority path."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.temporal.errors import (
    BackwardTimeError,
    ScheduleConflict,
    TimeWindowViolation,
)
from wanxiang_substrate.temporal.fixture import (
    DAY,
    DEADLINE_REPORT,
    INSTANCE,
    build_calendar_fixture_commands,
)
from wanxiang_substrate.temporal.query import TemporalQuery
from wanxiang_substrate.temporal.resolver import (
    ACTION_ADVANCE,
    ACTION_SCHEDULE_APPOINTMENT,
    ACTION_SET_DEADLINE,
    register_temporal_resolvers,
)


def make_temporal_runtime(path: pathlib.Path) -> WorldRuntime:
    return make_world_runtime(path, extra_resolvers=register_temporal_resolvers)


def cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def calendar() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_temporal_runtime(path)
    world = runtime.create_world(instance_id=INSTANCE)
    for command in build_calendar_fixture_commands(world.root_branch_id):
        runtime.submit_command(command)
    yield runtime, world
    cleanup_db_file(path)


def _now(runtime: WorldRuntime, world: CreateWorldResult) -> int:
    return TemporalQuery(runtime.current_state(world.instance_id, world.root_branch_id)).now()


@pytest.mark.integration
def test_advance_is_monotonic(calendar: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, world = calendar
    assert _now(runtime, world) == 0
    runtime.submit_command(cmd(world.root_branch_id, 1, ACTION_ADVANCE, {"ticks": 50}, "cmd_t1"))
    assert _now(runtime, world) == 50
    runtime.submit_command(cmd(world.root_branch_id, 2, ACTION_ADVANCE, {"ticks": 150}, "cmd_t2"))
    assert _now(runtime, world) == 200


@pytest.mark.integration
def test_backward_advance_is_structured_failure(
    calendar: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, world = calendar
    runtime.submit_command(cmd(world.root_branch_id, 1, ACTION_ADVANCE, {"ticks": 100}, "cmd_t1"))
    before = _now(runtime, world)
    with pytest.raises(BackwardTimeError):
        runtime.submit_command(
            cmd(world.root_branch_id, 2, ACTION_ADVANCE, {"ticks": -5}, "cmd_bad")
        )
    assert _now(runtime, world) == before


@pytest.mark.integration
def test_schedule_appointment_and_conflict(
    calendar: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, world = calendar
    runtime.submit_command(
        cmd(
            world.root_branch_id,
            1,
            ACTION_SCHEDULE_APPOINTMENT,
            {
                "appointment_id": "appt_b_noon",
                "actor_id": "actor_b",
                "activity": "lunch",
                "start_ticks": DAY + 40,
                "end_ticks": DAY + 50,
            },
            "cmd_sched",
        )
    )
    # actor_a already has a morning meeting overlapping this new slot
    with pytest.raises(ScheduleConflict):
        runtime.submit_command(
            cmd(
                world.root_branch_id,
                2,
                ACTION_SCHEDULE_APPOINTMENT,
                {
                    "appointment_id": "appt_a_noon",
                    "actor_id": "actor_a",
                    "activity": "lunch",
                    "start_ticks": DAY + 15,
                    "end_ticks": DAY + 25,
                },
                "cmd_conflict",
            )
        )
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    assert TemporalQuery(state).appointment(EntityId("appt_a_noon")) is None


@pytest.mark.integration
def test_time_window_violation(calendar: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, world = calendar
    with pytest.raises(TimeWindowViolation):
        runtime.submit_command(
            cmd(
                world.root_branch_id,
                1,
                ACTION_SCHEDULE_APPOINTMENT,
                {
                    "appointment_id": "appt_outside",
                    "actor_id": "actor_b",
                    "activity": "late",
                    "start_ticks": 90,
                    "end_ticks": 120,
                    "window_start": 100,
                    "window_end": 110,
                },
                "cmd_window",
            )
        )


@pytest.mark.integration
def test_deadline_becomes_due_and_replay_deterministic(
    calendar: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, world = calendar
    runtime.submit_command(
        cmd(world.root_branch_id, 1, ACTION_ADVANCE, {"ticks": 2 * DAY}, "cmd_t1")
    )
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    due = TemporalQuery(state).due_deadlines()
    assert any(d.deadline_id == DEADLINE_REPORT for d in due)
    events = runtime.events(world.instance_id, world.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
    assert any(d.deadline_id == DEADLINE_REPORT for d in TemporalQuery(replayed).due_deadlines())


@pytest.mark.integration
def test_due_events_remain_due_exactly_once_after_restart() -> None:
    path = fresh_db_path()
    try:
        runtime1 = make_temporal_runtime(path)
        world1 = runtime1.create_world(instance_id=INSTANCE)
        for command in build_calendar_fixture_commands(world1.root_branch_id):
            runtime1.submit_command(command)
        runtime1.submit_command(
            cmd(world1.root_branch_id, 1, ACTION_ADVANCE, {"ticks": 2 * DAY}, "cmd_t1")
        )
        runtime1.submit_command(
            cmd(
                world1.root_branch_id,
                2,
                ACTION_SET_DEADLINE,
                {"deadline_id": "deadline_extra", "target_id": "actor_b", "due_ticks": DAY},
                "cmd_dl",
            )
        )
        before = TemporalQuery(
            runtime1.current_state(world1.instance_id, world1.root_branch_id)
        ).due_deadlines()
        assert len(before) == 2

        # Persistence restart: a fresh runtime over the SAME database file.
        runtime2 = make_temporal_runtime(path)
        state2 = runtime2.current_state(world1.instance_id, world1.root_branch_id)
        due = TemporalQuery(state2).due_deadlines()
        assert len(due) == 2  # both deadlines remain due exactly once
        assert len({d.deadline_id for d in due}) == 2
    finally:
        cleanup_db_file(path)
