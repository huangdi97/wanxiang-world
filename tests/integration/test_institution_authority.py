"""G02E: institution authority/duties/permissions affect allowed actions."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.institution.errors import (
    DutyAlreadyComplete,
    PermissionDeniedByInstitution,
)
from wanxiang_substrate.institution.fixture import (
    ALICE,
    BOB,
    DUTY_STEWARD,
    ROOM,
    build_institution_fixture_commands,
)
from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.institution.resolver import (
    ACTION_COMPLETE_DUTY,
    ACTION_DEFINE_ROLE,
    ACTION_GRANT_PERMISSION,
    ACTION_GRANT_ROLE,
    register_institution_resolvers,
)
from wanxiang_substrate.spatial.fixture import build_house_fixture_commands
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers

COMBINED = WorldInstanceId("wld_combined_inst")


def make_institution_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_institution_resolvers(registry)
        from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

        register_temporal_resolvers(registry)

    return make_world_runtime(path, extra_resolvers=register)


def cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
    actor_id: str | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=COMBINED,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=dict(payload),
        actor_id=ActorId(actor_id) if actor_id else None,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def club() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_institution_runtime(path)
    w = runtime.create_world(instance_id=COMBINED)
    for command in build_house_fixture_commands(w.root_branch_id, instance_id=COMBINED):
        runtime.submit_command(command)
    for command in build_institution_fixture_commands(
        w.root_branch_id, start_revision=1, instance_id=COMBINED
    ):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_authorized_actor_enters_restricted_room(
    club: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = club
    # Alice has the member role + enter.study permission; moves hall->study.
    result = runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            "spatial.move",
            {"entity_id": ALICE.value, "target_place_id": ROOM.value},
            "cmd_alice_study",
            actor_id=ALICE.value,
        )
    )
    state = result.state
    from wanxiang_substrate.spatial.query import SpatialQuery

    assert SpatialQuery(state).location(ALICE) == ROOM


@pytest.mark.integration
def test_unauthorized_actor_rejected_with_rule_reference(
    club: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = club
    # Bob has no membership/permission for the restricted study.
    with pytest.raises(PermissionDeniedByInstitution):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                2,
                "spatial.move",
                {"entity_id": BOB.value, "target_place_id": ROOM.value},
                "cmd_bob_study",
                actor_id=BOB.value,
            )
        )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    decision = InstitutionQuery(state, now_ticks=0).check_permission(BOB, "enter.study")
    assert decision.allow is False
    assert decision.rule_refs == ()


@pytest.mark.integration
def test_permission_decision_has_provenance(
    club: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = club
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = InstitutionQuery(state, now_ticks=0)
    decision = query.check_permission(ALICE, "enter.study", "study")
    assert decision.allow is True
    assert "role:member" in decision.rule_refs
    assert decision.provenance  # membership/permission ids recorded


@pytest.mark.integration
def test_duty_lifecycle(club: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = club
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = InstitutionQuery(state, now_ticks=0)
    assert query.due_duties(ALICE) == ()
    # Advance time so the steward duty becomes due, then complete it.
    from wanxiang_substrate.temporal.resolver import ACTION_ADVANCE

    runtime.submit_command(
        cmd(w.root_branch_id, 2, ACTION_ADVANCE, {"ticks": 600}, "cmd_adv", actor_id=ALICE.value)
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = InstitutionQuery(state, now_ticks=600)
    assert any(d.duty_id == DUTY_STEWARD for d in query.due_duties(ALICE))
    runtime.submit_command(
        cmd(w.root_branch_id, 3, ACTION_COMPLETE_DUTY, {"duty_id": DUTY_STEWARD.value}, "cmd_done")
    )
    with pytest.raises(DutyAlreadyComplete):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                4,
                ACTION_COMPLETE_DUTY,
                {"duty_id": DUTY_STEWARD.value},
                "cmd_done2",
            )
        )


@pytest.mark.integration
def test_role_permission_history_replays(club: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = club
    # Define a second role + grant membership to Bob with a short expiry.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_DEFINE_ROLE,
            {"role_id": "role_guest", "name": "guest", "permissions": "read"},
            "cmd_guest_role",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            3,
            ACTION_GRANT_ROLE,
            {
                "membership_id": "membership_bob",
                "actor_id": BOB.value,
                "role_id": "role_guest",
                "institution_id": "club",
                "start_ticks": 0,
                "end_ticks": 10,
            },
            "cmd_bob_membership",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = InstitutionQuery(state, now_ticks=5)
    assert query.check_permission(BOB, "read").allow is True
    expired = InstitutionQuery(state, now_ticks=50)
    assert expired.check_permission(BOB, "read").allow is False
    # Replay reproduces the same history.
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
    assert InstitutionQuery(replayed, now_ticks=5).check_permission(BOB, "read").allow is True


@pytest.mark.integration
def test_delegated_permission_grants_access(
    club: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = club
    # Alice (authorized) delegates enter.study to Bob for a window.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_GRANT_PERMISSION,
            {
                "permission_id": "permission_bob",
                "actor_id": BOB.value,
                "permission": "enter.study",
                "target": "study",
                "granter_id": ALICE.value,
                "start_ticks": 0,
                "end_ticks": 100,
            },
            "cmd_delegate",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    decision = InstitutionQuery(state, now_ticks=5).check_permission(BOB, "enter.study", "study")
    assert decision.allow is True
    assert "delegated_permission" in decision.rule_refs
    assert any(p.startswith("granted_by:") for p in decision.provenance)
