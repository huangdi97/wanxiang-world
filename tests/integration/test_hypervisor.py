"""G31D: World Hypervisor multi-instance isolation."""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, ComponentId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.host.host import WorldHost
from wanxiang_substrate.host.hypervisor import RuntimeProfile, WorldHypervisor
from wanxiang_substrate.recovery.budget import ResourceBudget


def _make_host(path: pathlib.Path) -> WorldHost:
    runtime = make_world_runtime(path)
    created = runtime.create_world()
    return WorldHost(runtime, created.instance_id, created.root_branch_id)


def _submit(
    instance_id: WorldInstanceId,
    branch_id: object,
    action: str,
    payload: dict[str, object],
    revision: int,
    command_id: str,
) -> CommandEnvelope:

    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=instance_id,
        branch_id=branch_id,  # type: ignore[arg-type]
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,  # type: ignore[arg-type]
        world_time=WorldTime(revision + 1),
    )


@pytest.mark.integration
def test_two_instances_same_local_ids_do_not_pollute() -> None:
    path_a = fresh_db_path()
    path_b = fresh_db_path()
    try:
        hypervisor = WorldHypervisor()
        host_a = _make_host(path_a)
        host_b = _make_host(path_b)
        hypervisor.bind(host_a, profile=RuntimeProfile(name="profile_a"))
        hypervisor.bind(host_b, profile=RuntimeProfile(name="profile_b"))

        hypervisor.submit(
            host_a.handle.instance_id,
            _submit(
                host_a.handle.instance_id,
                host_a.handle.root_branch_id,
                "create_entity",
                {"entity_id": "alice", "count": 10},
                0,
                "cmd_a1",
            ),
        )
        hypervisor.submit(
            host_b.handle.instance_id,
            _submit(
                host_b.handle.instance_id,
                host_b.handle.root_branch_id,
                "create_entity",
                {"entity_id": "alice", "count": 5},
                0,
                "cmd_b1",
            ),
        )

        state_a = hypervisor.host(host_a.handle.instance_id).query(host_a.handle.root_branch_id)
        state_b = hypervisor.host(host_b.handle.instance_id).query(host_b.handle.root_branch_id)
        alice_a = state_a.entity(EntityId("alice"))
        alice_b = state_b.entity(EntityId("alice"))
        assert alice_a is not None and alice_b is not None
        assert alice_a.components is not alice_b.components
        count_a = alice_a.components[ComponentId("res_alice")].fields["count"]
        count_b = alice_b.components[ComponentId("res_alice")].fields["count"]
        assert count_a == 10 and count_b == 5  # same local id, isolated state
    finally:
        cleanup_db_file(path_a)
        cleanup_db_file(path_b)


@pytest.mark.integration
def test_concurrent_commands_route_to_correct_instance() -> None:
    path_a = fresh_db_path()
    path_b = fresh_db_path()
    try:
        hypervisor = WorldHypervisor()
        host_a = _make_host(path_a)
        host_b = _make_host(path_b)
        hypervisor.bind(host_a)
        hypervisor.bind(host_b)

        # Interleave commands across the two instances.
        hypervisor.submit(
            host_a.handle.instance_id,
            _submit(
                host_a.handle.instance_id,
                host_a.handle.root_branch_id,
                "create_entity",
                {"entity_id": "x", "count": 1},
                0,
                "cmd_x1",
            ),
        )
        hypervisor.submit(
            host_b.handle.instance_id,
            _submit(
                host_b.handle.instance_id,
                host_b.handle.root_branch_id,
                "create_entity",
                {"entity_id": "y", "count": 2},
                0,
                "cmd_y1",
            ),
        )
        state_a = hypervisor.host(host_a.handle.instance_id).query(host_a.handle.root_branch_id)
        state_b = hypervisor.host(host_b.handle.instance_id).query(host_b.handle.root_branch_id)
        assert state_a.entity(EntityId("x")) is not None
        assert state_a.entity(EntityId("y")) is None
        assert state_b.entity(EntityId("y")) is not None
        assert state_b.entity(EntityId("x")) is None

        # A command addressed to the wrong route is rejected.
        wrong = _submit(
            host_a.handle.instance_id,
            host_a.handle.root_branch_id,
            "create_entity",
            {"entity_id": "z", "count": 1},
            0,
            "cmd_wrong",
        )
        with pytest.raises(ContractError):
            hypervisor.submit(host_b.handle.instance_id, wrong)
    finally:
        cleanup_db_file(path_a)
        cleanup_db_file(path_b)


@pytest.mark.integration
def test_profile_and_budget_binding() -> None:
    path = fresh_db_path()
    try:
        hypervisor = WorldHypervisor()
        host = _make_host(path)
        budget = ResourceBudget(max_commands=2)
        hypervisor.bind(host, profile=RuntimeProfile(name="tight", budget=budget))
        assert hypervisor.profile(host.handle.instance_id).name == "tight"
        # Second command exceeds the per-instance budget.
        from wanxiang_substrate.recovery.errors import BudgetExceeded

        with pytest.raises(BudgetExceeded):
            for i in range(3):
                hypervisor.submit(
                    host.handle.instance_id,
                    _submit(
                        host.handle.instance_id,
                        host.handle.root_branch_id,
                        "create_entity",
                        {"entity_id": f"e{i}", "count": 1},
                        i,
                        f"cmd_b{i}",
                    ),
                )
    finally:
        cleanup_db_file(path)
