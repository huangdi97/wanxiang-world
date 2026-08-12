"""G03C: actor & organization runtime ? order lifecycle and policies."""

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
from wanxiang_substrate.agency.errors import OrderStateConflict
from wanxiang_substrate.agency.fixture import (
    COMMANDER,
    INSTANCE,
    SOLDIER_A,
    SOLDIER_B,
    build_organization_fixture_commands,
)
from wanxiang_substrate.agency.query import AgencyQuery
from wanxiang_substrate.agency.resolver import register_agency_resolvers
from wanxiang_substrate.institution.resolver import register_institution_resolvers
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers


def make_agency_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_temporal_resolvers(registry)
        register_institution_resolvers(registry)
        register_agency_resolvers(registry)

    return make_world_runtime(path, extra_resolvers=register)


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
def org() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_agency_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    for command in build_organization_fixture_commands(w.root_branch_id):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_order_lifecycle_full(org: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = org
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "agency.issue_order",
            {
                "order_id": "order_1",
                "issuer_id": COMMANDER.value,
                "receiver_id": SOLDIER_A.value,
                "action_type": "spatial.move",
                "payload": '{"entity_id": "soldier_a", "target_place_id": "hall"}',
            },
            "cmd_issue",
        )
    )
    runtime.submit_command(
        cmd(w.root_branch_id, 2, "agency.receive_order", {"order_id": "order_1"}, "cmd_recv")
    )
    runtime.submit_command(
        cmd(w.root_branch_id, 3, "agency.accept_order", {"order_id": "order_1"}, "cmd_accept")
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            4,
            "agency.execute_order",
            {"order_id": "order_1", "outcome": "done", "deviation": "delayed"},
            "cmd_exec",
        )
    )
    runtime.submit_command(
        cmd(w.root_branch_id, 5, "agency.report_order", {"order_id": "order_1"}, "cmd_report")
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = AgencyQuery(state)
    order = query.order(EntityId("order_1"))
    assert order is not None and order.state == "reported"
    assert order.deviation == "delayed"


@pytest.mark.integration
def test_invalid_transition_rejected(org: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = org
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "agency.issue_order",
            {
                "order_id": "order_x",
                "issuer_id": COMMANDER.value,
                "receiver_id": SOLDIER_A.value,
                "action_type": "body.rest",
                "payload": "{}",
            },
            "cmd_issue",
        )
    )
    # Cannot execute an order that was never received/accepted.
    with pytest.raises(OrderStateConflict):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                2,
                "agency.execute_order",
                {"order_id": "order_x", "outcome": "done"},
                "cmd_bad",
            )
        )


@pytest.mark.integration
def test_actor_states_and_organization_views(org: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = org
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = AgencyQuery(state)
    assert query.is_active(SOLDIER_A) is True
    # Commander is a member of the club (officer role).
    assert COMMANDER in query.organization_members(EntityId("club"))
    assert SOLDIER_A not in query.organization_members(EntityId("club"))
    # Deactivate soldier B.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "agency.set_actor_state",
            {"actor_id": SOLDIER_B.value, "active": False},
            "cmd_deactivate",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert AgencyQuery(state).is_active(SOLDIER_B) is False


@pytest.mark.integration
def test_deterministic_policy_proposes_stable_candidate(
    org: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = org
    from wanxiang_substrate.agency.policy import DeterministicPolicy, RulePolicy

    context = type(
        "Ctx",
        (),
        {"actor_id": SOLDIER_A, "observations": (object(),), "beliefs": ()},
    )()
    first = DeterministicPolicy("body.rest", {"ticks": 5}).propose(context)  # type: ignore[arg-type]
    second = DeterministicPolicy("body.rest", {"ticks": 5}).propose(context)  # type: ignore[arg-type]
    assert first == second
    assert RulePolicy("body.rest", "has_obs").propose(context) is not None  # type: ignore[arg-type]
    # Deterministic policy output is propose-only: no state mutation happened.
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert AgencyQuery(state).order(EntityId("order_1")) is None
