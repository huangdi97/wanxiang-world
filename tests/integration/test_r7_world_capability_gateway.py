"""R7 World Capability Gateway: query/proposal boundary tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.experience_player_service import ExperiencePlayerService
from wanxiang_application.gateway import AgentSessionIdentity, WorldCapabilityGateway
from wanxiang_domain.errors import PermissionDenied, ValidationRejected
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
        capability_scope=(
            "world.observe",
            "world.history",
            "world.inspect",
            "world.entities",
            "world.relations",
            "world.worldline",
            "world.branch.diff",
            "world.capabilities",
            "world.propose",
            "world.fork",
            "world.experiment",
            "world.simulation",
            "world.order",
            "cap.r7.double",
        ),
        rights_scope=("public",),
        secret_scope=(),
        audit_id="audit:r7-gateway",
        session_expiry="2099-01-01T00:00:00Z",
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
    assert dict(observed.state) == {}
    history = gateway.query_history(session)
    assert [item.revision for item in history] == [1]

    metadata = gateway.inspect_world_metadata(session)
    assert metadata["world_id"] == world.instance_id.value
    assert metadata["revision"] == 1
    assert metadata["state_hash"] == observed.state_hash

    schema = gateway.inspect_world_schema(session)
    assert schema["schema_version"] == 1
    assert schema["action_types"] == runtime.action_types()

    entities = gateway.query_entities(session)
    assert tuple(item["id"] for item in entities) == ("ent_gateway",)
    assert gateway.query_relations(session) == ()

    worldline = gateway.query_worldline(session)
    assert worldline["branch_id"] == branch.value
    assert worldline["parent_branch_id"] is None

    capabilities = gateway.list_capabilities(session)
    assert "world.observe" in capabilities["session_scopes"]
    assert "set_status" in capabilities["action_types"]

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

    simulation = gateway.request_simulation(
        session,
        simulation_id="sim:r7-counterfactual",
        parameters={"horizon": 3},
    )
    assert simulation.operation == "request_simulation"

    order = gateway.submit_order(
        session,
        order_type="external.notification",
        parameters={"target": "reference-only"},
    )
    assert order.operation == "submit_order"
    assert runtime.current_state(world.instance_id, branch).revision.value == 1

    skill = gateway.describe_skill(session)
    assert skill.allowed_actions == runtime.action_types()
    assert "propose_action" in skill.allowed_operations
    assert skill.actor_lease_present is True
    assert skill.secret_scope_present is False

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


@pytest.mark.integration
def test_gateway_scope_and_expiry_fail_closed() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_gateway_scope"))
    branch = world.root_branch_id
    gateway = WorldCapabilityGateway(
        runtime,
        now=lambda: datetime(2026, 10, 7, tzinfo=UTC),
    )

    expired = AgentSessionIdentity(
        principal_id="principal:expired",
        role="agent",
        world_id=world.instance_id.value,
        branch_id=branch.value,
        audit_id="audit:expired",
        session_expiry="2026-10-06T00:00:00Z",
        capability_scope=("world.observe",),
        rights_scope=("public",),
    )
    with pytest.raises(PermissionDenied, match="expired"):
        gateway.observe(expired)

    scoped = AgentSessionIdentity(
        principal_id="principal:scoped",
        role="agent",
        world_id=world.instance_id.value,
        branch_id=branch.value,
        audit_id="audit:scoped",
        session_expiry="2099-01-01T00:00:00Z",
        capability_scope=("world.observe",),
        rights_scope=("public",),
    )
    assert gateway.observe(scoped).revision == 0
    with pytest.raises(PermissionDenied, match="world.propose"):
        gateway.propose_action(
            scoped,
            expected_revision=0,
            action_type="create_entity",
            payload={"entity_id": "ent_forbidden", "count": 0},
        )


@pytest.mark.integration
def test_gateway_raw_canonical_state_requires_explicit_right() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_gateway_rights"))
    branch = world.root_branch_id
    player = ExperiencePlayerService(runtime)
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_gateway_rights", "count": 1},
        "act_gateway",
        "cmd_gateway_rights_seed",
    )
    gateway = WorldCapabilityGateway(runtime)
    public_session = _session(world.instance_id.value, branch.value)
    assert dict(gateway.observe(public_session).state) == {}

    privileged = AgentSessionIdentity(
        principal_id="principal:auditor",
        role="auditor",
        world_id=world.instance_id.value,
        branch_id=branch.value,
        audit_id="audit:canonical-read",
        session_expiry="2099-01-01T00:00:00Z",
        capability_scope=("world.observe",),
        rights_scope=("world.canonical.read",),
    )
    raw = dict(gateway.observe(privileged).state)
    assert raw["instance_id"] == world.instance_id.value
    assert raw["branch_id"] == branch.value
    assert raw["revision"] == 1
