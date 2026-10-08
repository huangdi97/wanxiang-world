"""Replay, recovery, and branch-isolation probes for one M98 run."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.hierarchy import BranchId
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

from m98_burn_in_support import commit, db_bytes


def sample(
    runtime: WorldRuntime,
    instance: WorldInstanceId,
    branch: BranchId,
    day: int,
    tick: int,
    path: Path,
) -> tuple[dict[str, Any], float, float]:
    state = runtime.current_state(instance, branch)
    start = time.perf_counter()
    replay = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(
        runtime.events(instance, branch)
    )
    replay_ms = (time.perf_counter() - start) * 1000.0
    start = time.perf_counter()
    recovered = runtime.restore_and_replay(instance, branch)
    recovery_ms = (time.perf_counter() - start) * 1000.0
    state_hash = state.semantic_hash()
    replay_hash = replay.semantic_hash()
    recovery_hash = recovered.state.semantic_hash()
    return (
        {
            "day": day,
            "world_tick": tick,
            "event_count": len(runtime.events(instance, branch)),
            "state_hash": state_hash,
            "replay_hash": replay_hash,
            "recovery_hash": recovery_hash,
            "replay_equal": replay_hash == state_hash,
            "recovery_equal": recovery_hash == state_hash,
            "storage_bytes": db_bytes(path),
        },
        replay_ms,
        recovery_ms,
    )


def branch_probe(
    runtime: WorldRuntime,
    instance: WorldInstanceId,
    branch: BranchId,
    actor: str,
    tick: int,
    run_id: str,
) -> dict[str, Any]:
    parent_hash = runtime.current_state(instance, branch).semantic_hash()
    parent_events = runtime.events(instance, branch)
    child = runtime.create_branch(instance, branch).branch_id
    commit(
        runtime,
        instance,
        child,
        command_id=f"{run_id}:child-probe",
        action_type="set_status",
        payload={"entity_id": actor, "status": "branch-only-probe"},
        world_time=tick,
        actor_id=actor,
    )
    child_state = runtime.current_state(instance, child)
    checks = {
        "parent_hash_unchanged": runtime.current_state(instance, branch).semantic_hash()
        == parent_hash,
        "parent_events_unchanged": runtime.events(instance, branch) == parent_events,
        "child_diverged": child_state.semantic_hash() != parent_hash,
        "child_replay_equal": runtime.restore_and_replay(instance, child).state.semantic_hash()
        == child_state.semantic_hash(),
    }
    return {
        "parent_branch": branch.value,
        "child_branch": child.value,
        **checks,
        "isolated": all(checks.values()),
    }


__all__ = ["branch_probe", "sample"]
