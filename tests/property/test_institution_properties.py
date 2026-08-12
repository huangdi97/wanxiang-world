"""G02E: property ? expired roles cannot grant current authority."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st
from tests.conftest import cleanup_db_file, fresh_db_path
from tests.integration.test_institution_authority import COMBINED, make_institution_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.institution.fixture import (
    ROLE_MEMBER,
    build_institution_fixture_commands,
)
from wanxiang_substrate.institution.query import InstitutionQuery


@settings(max_examples=8, deadline=None)
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=6))
def test_expired_memberships_cannot_grant_authority(expiries: list[int]) -> None:
    path = fresh_db_path()
    try:
        runtime = make_institution_runtime(path)
        world = runtime.create_world(instance_id=COMBINED)
        for command in build_institution_fixture_commands(
            world.root_branch_id, instance_id=COMBINED
        ):
            runtime.submit_command(command)
        revision = 1
        for index, end in enumerate(expiries):
            runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"prop_i{index}"),
                    instance_id=COMBINED,
                    branch_id=world.root_branch_id,
                    expected_revision=BranchRevision(revision),
                    action_type="institution.grant_role",
                    payload={
                        "membership_id": f"membership_exp_{index}",
                        "actor_id": "exp_actor",
                        "role_id": ROLE_MEMBER.value,
                        "institution_id": "club",
                        "start_ticks": 0,
                        "end_ticks": end,
                    },
                    world_time=WorldTime(revision + 1),
                )
            )
            revision += 1
            # At a time far beyond the expiry, the role cannot grant permission.
            later = max(expiries) + 1
            state = runtime.current_state(world.instance_id, world.root_branch_id)
            decision = InstitutionQuery(state, now_ticks=later).check_permission(
                EntityId("exp_actor"), "enter.study"
            )
            assert decision.allow is False
    finally:
        cleanup_db_file(path)
