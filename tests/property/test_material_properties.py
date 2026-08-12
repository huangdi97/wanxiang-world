"""G02C: property ? no containment cycles; conserved custody (one holder)."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st
from tests.conftest import cleanup_db_file, fresh_db_path
from tests.integration.test_material_custody import make_material_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.material.fixture import INSTANCE, LETTER, build_package_fixture_commands
from wanxiang_substrate.material.query import MaterialQuery

HOLDERS = ("messenger", "recipient", "writer")


@settings(max_examples=8, deadline=None)
@given(st.lists(st.sampled_from(HOLDERS), min_size=1, max_size=8))
def test_custody_is_conserved_and_never_duplicated(holders: list[str]) -> None:
    path = fresh_db_path()
    try:
        runtime = make_material_runtime(path)
        world = runtime.create_world(instance_id=INSTANCE)
        for command in build_package_fixture_commands(world.root_branch_id):
            runtime.submit_command(command)
        revision = 1
        for index, holder in enumerate(holders):
            state = runtime.current_state(world.instance_id, world.root_branch_id)
            current = MaterialQuery(state).custodian(LETTER)
            assert current is not None
            from_custodian = current.value
            result = runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"prop_m{index}"),
                    instance_id=INSTANCE,
                    branch_id=world.root_branch_id,
                    expected_revision=BranchRevision(revision),
                    action_type="material.transfer",
                    payload={
                        "item_id": LETTER.value,
                        "from_custodian": from_custodian,
                        "to_custodian": holder,
                    },
                    world_time=WorldTime(revision + 1),
                )
            )
            revision += 1
            query = MaterialQuery(result.state)
            custodian = query.custodian(LETTER)
            assert custodian is not None
            assert custodian == EntityId(holder)
    finally:
        cleanup_db_file(path)
