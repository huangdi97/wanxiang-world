"""G02B: property ? committed world time never decreases."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st
from tests.conftest import cleanup_db_file, fresh_db_path
from tests.integration.test_temporal_advance import make_temporal_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.temporal.fixture import INSTANCE, build_calendar_fixture_commands
from wanxiang_substrate.temporal.query import TemporalQuery


@settings(max_examples=8, deadline=None)
@given(st.lists(st.integers(min_value=1, max_value=200), min_size=1, max_size=12))
def test_committed_world_time_never_decreases(deltas: list[int]) -> None:
    path = fresh_db_path()
    try:
        runtime = make_temporal_runtime(path)
        world = runtime.create_world(instance_id=INSTANCE)
        for command in build_calendar_fixture_commands(world.root_branch_id):
            runtime.submit_command(command)
        revision = 1
        previous = 0
        for index, delta in enumerate(deltas):
            result = runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"prop_t{index}"),
                    instance_id=INSTANCE,
                    branch_id=world.root_branch_id,
                    expected_revision=BranchRevision(revision),
                    action_type="temporal.advance",
                    payload={"ticks": delta},
                    world_time=WorldTime(revision + 1),
                )
            )
            revision += 1
            now = TemporalQuery(result.state).now()
            assert now >= previous
            previous = now
    finally:
        cleanup_db_file(path)
