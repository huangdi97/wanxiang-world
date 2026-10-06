"""R7 World Capability Gateway: query/proposal boundary tests."""

from __future__ import annotations

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.experience_player_service import ExperiencePlayerService
from wanxiang_application.gateway import AgentSessionIdentity, WorldCapabilityGateway
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import WorldInstanceId


def _session(
    world_id: str,
    branch_id: str,
    *,
    actor_id: str = "act_gateway",
) -> AgentSessionIdentity:
    return AgentSessionIdentity(
        principal_id="principal:test-agent",
        role="agent",
        world_id=world_id,
        branch_id=branch_id,
        actor_id=actor_id,
        capability_scope=("world.observe", "world.propose"),
        rights_scope=("public",),
        secret_scope=(),
        audit_id="audit:r7-gateway",
    )


@pytest.mark.integration
def test_gateway_observe_history_and_proposal_have_no_reality_effect() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_gateway"))
    branch = world.root_branch_id
    player = ExperiencePlayerService(runtime)
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_gateway", "count": 1},
        "act_gateway",
        "cmd_gateway_seed",
    )
    gateway = WorldCapabilityGateway(runtime)
    session = _session(world.instance_id.value, branch.value)

    observed = gateway.observe(session)
    assert observed.revision == 1
    assert observed.state_hash == runtime.current_state(world.instance_id, branch).semantic_hash()
    history = gateway.query_history(session)
    assert [item.revision for item in history] == [1]

    proposal = gateway.propose_action(
        session,
        expected_revision=1,
        action_type="set_status",
        payload={"entity_id": "ent_gateway", "status": "proposed-only"},
    )
    assert proposal.command.expected_revision.value == 1
    assert runtime.current_state(world.instance_id, branch).revision.value == 1

    request = gateway.request_fork(session, at_revision=1)
    assert request.operation == "fork_worldline"
    assert len(runtime.persistence.branches.list(world.instance_id)) == 1

    experiment = gateway.request_experiment(
        session,
        capability_id="cap.r7.double",
        parameters={"input": 5},
    )
    assert experiment.operation == "request_experiment"
    assert runtime.current_state(world.instance_id, branch).revision.value == 1

    assert not hasattr(gateway, "commit")
    assert not hasattr(gateway, "force_commit")


@pytest.mark.integration
def test_gateway_branch_diff_and_actor_lease_guard() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_gateway_diff"))
    branch = world.root_branch_id
    player = ExperiencePlayerService(runtime)
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_gateway_diff", "count": 0},
        "act_gateway",
        "cmd_gateway_diff_seed",
    )
    child = runtime.create_branch(world.instance_id, branch)
    player.act(
        world.instance_id,
        child.branch_id,
        1,
        "set_status",
        {"entity_id": "ent_gateway_diff", "status": "child-only"},
        "act_gateway",
        "cmd_gateway_diff_child",
    )

    gateway = WorldCapabilityGateway(runtime)
    session = _session(world.instance_id.value, branch.value)
    diff = gateway.query_branch_diff(session, child.branch_id.value)
    assert diff["updated_entities"] == ("ent_gateway_diff",)

    no_actor = _session(world.instance_id.value, branch.value, actor_id="")
    with pytest.raises(ValidationRejected, match="actor lease"):
        gateway.propose_action(
            no_actor,
            expected_revision=1,
            action_type="set_status",
            payload={"entity_id": "ent_gateway_diff", "status": "forbidden"},
        )
