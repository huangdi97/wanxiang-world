"""R7 WorldHandle acceptance: safe public facade, never a commit shortcut."""

from __future__ import annotations

from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.experience_player_service import ExperiencePlayerService
from wanxiang_application.gateway_contract import AgentSessionIdentity
from wanxiang_application.world_handle import WorldHandle
from wanxiang_domain.ids import WorldInstanceId


def _session(world_id: str, branch_id: str) -> AgentSessionIdentity:
    return AgentSessionIdentity(
        principal_id="principal:handle",
        role="agent",
        world_id=world_id,
        branch_id=branch_id,
        audit_id="audit:r7-world-handle",
        session_expiry="2099-01-01T00:00:00Z",
        actor_id="act_handle",
        capability_scope=(
            "world.observe",
            "world.history",
            "world.propose",
            "world.fork",
            "world.experiment",
            "cap.r7.double",
        ),
        rights_scope=("public",),
    )


def test_world_handle_observes_and_proposes_without_committing() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_handle"))
    branch = world.root_branch_id
    player = ExperiencePlayerService(runtime)
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_handle", "count": 0},
        "act_handle",
        "cmd_handle_seed",
    )

    handle = WorldHandle(runtime, _session(world.instance_id.value, branch.value))
    metadata = handle.metadata()
    assert metadata.revision == 1
    assert metadata.world_id == world.instance_id.value

    proposal = handle.propose(
        expected_revision=1,
        action_type="set_status",
        payload={"entity_id": "ent_handle", "status": "proposal-only"},
    )
    assert proposal.command.expected_revision.value == 1
    assert runtime.current_state(world.instance_id, branch).revision.value == 1

    fork = handle.branch(at_revision=1)
    capability = handle.capability("cap.r7.double", parameters={"input": 5})
    assert fork.operation == "fork_worldline"
    assert capability.operation == "request_experiment"
    assert runtime.current_state(world.instance_id, branch).revision.value == 1

    assert not hasattr(handle, "commit")
    assert not hasattr(handle, "force_commit")
    assert not hasattr(handle, "runtime")
    assert not hasattr(handle, "raw_database")
    assert not hasattr(handle, "commit_capability")


def test_world_handle_history_and_skill_use_the_same_bound_session() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_handle_history"))
    handle = WorldHandle(
        runtime,
        _session(world.instance_id.value, world.root_branch_id.value),
    )

    assert handle.history() == ()
    skill = handle.skill()
    assert skill.world_id == world.instance_id.value
    assert "propose_action" in skill.allowed_operations
    assert skill.actor_lease_present is True
