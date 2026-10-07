"""R7 production agent-harness loop: real subprocess proposal -> authority outcome."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.experience_player_service import ExperiencePlayerService
from wanxiang_application import AgentSessionIdentity, HarnessWorldLoop
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_runtime.r7_agent_harness import JsonRpcAgentHarnessProvider
from wanxiang_substrate.actor_continuity.trajectory import ActorTrajectoryLedger

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "scripts" / "r7_reference_harness.py"


def _session(world_id: str, branch_id: str) -> AgentSessionIdentity:
    return AgentSessionIdentity(
        principal_id="principal:r7-loop",
        role="agent",
        world_id=world_id,
        branch_id=branch_id,
        actor_id="act_loop",
        capability_scope=("world.observe", "world.history", "world.propose"),
        rights_scope=("qualification",),
        secret_scope=(),
        audit_id="audit:r7-loop",
        session_expiry="2099-01-01T00:00:00Z",
    )


@pytest.mark.integration
def test_real_harness_loop_commits_then_reports_rejection() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_harness_loop"))
    branch = world.root_branch_id
    player = ExperiencePlayerService(runtime)
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_loop", "count": 0},
        "act_loop",
        "cmd_loop_seed",
    )
    before_commit = runtime.current_state(world.instance_id, branch)

    provider = JsonRpcAgentHarnessProvider(
        [sys.executable, str(HARNESS)],
        cwd=ROOT,
        request_timeout_seconds=30.0,
    )
    trajectory = ActorTrajectoryLedger()
    loop = HarnessWorldLoop(runtime, provider, trajectory_sink=trajectory.record_payload)
    session = _session(world.instance_id.value, branch.value)
    try:
        committed = loop.step(
            session,
            goal_hint="advance the world through a proposal",
            allowed_context={
                "targetRevision": "3",
                "pendingAction": "set_status",
                "entityId": "ent_loop",
                "targetStatus": "agent-loop-accepted",
            },
        )
        assert committed.status == "committed"
        assert committed.revision == 2
        assert committed.consequence_acknowledged is True
        assert committed.trajectory_recorded is True
        after_commit = runtime.current_state(world.instance_id, branch)
        assert after_commit.revision.value == 2
        assert after_commit.semantic_hash() != before_commit.semantic_hash()

        before_reject = after_commit
        rejected = loop.step(
            session,
            allowed_context={
                "targetRevision": "3",
                "pendingAction": "unsupported_action",
                "entityId": "ent_loop",
            },
        )
        assert rejected.status == "rejected"
        assert rejected.revision == before_reject.revision.value
        assert rejected.state_hash == before_reject.semantic_hash()
        assert rejected.consequence_acknowledged is True
        assert rejected.trajectory_recorded is True
        assert (
            runtime.current_state(world.instance_id, branch).semantic_hash()
            == before_reject.semantic_hash()
        )
        records = trajectory.entries()
        assert len(records) == 2
        assert records[0].world_event_refs
        assert records[1].world_event_refs == ()
        assert records[0].provider_id == "agent-harness-rpc"
        assert not hasattr(records[0], "prompt")
        assert not hasattr(records[0], "memory_content")
    finally:
        loop.close()
