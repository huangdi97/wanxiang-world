"""G02D: property ? condition facets stay within bounds after valid transitions."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st
from tests.conftest import cleanup_db_file, fresh_db_path
from tests.integration.test_body_condition import make_body_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.body.fixture import HEALTHY, INSTANCE, build_condition_fixture_commands
from wanxiang_substrate.body.query import BodyQuery


@settings(max_examples=8, deadline=None)
@given(st.lists(st.integers(min_value=0, max_value=50), min_size=1, max_size=10))
def test_energy_stays_bounded_after_exerts(exerts: list[int]) -> None:
    path = fresh_db_path()
    try:
        runtime = make_body_runtime(path)
        world = runtime.create_world(instance_id=INSTANCE)
        for command in build_condition_fixture_commands(world.root_branch_id):
            runtime.submit_command(command)
        revision = 1
        for index, cost in enumerate(exerts):
            result = runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"prop_b{index}"),
                    instance_id=INSTANCE,
                    branch_id=world.root_branch_id,
                    expected_revision=BranchRevision(revision),
                    action_type="body.exert",
                    payload={"actor_id": HEALTHY.value, "energy_cost": cost},
                    world_time=WorldTime(revision + 1),
                )
            )
            revision += 1
            condition = BodyQuery(result.state).condition(HEALTHY)
            assert condition is not None
            assert 0 <= condition.energy <= 100
    finally:
        cleanup_db_file(path)
