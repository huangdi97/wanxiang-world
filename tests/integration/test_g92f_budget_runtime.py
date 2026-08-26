"""G92F budget admission and LOD degradation on a real Runtime world."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.long_horizon import (
    ActorActivityInput,
    BudgetKey,
    CostBudgetLedger,
    CostLimit,
    CostUsage,
    LODState,
    SimulationLODRuntime,
)
from wanxiang_substrate.temporal.resolver import ACTION_INSTANTIATE, register_temporal_resolvers


def test_budget_degradation_keeps_real_world_truth_untouched(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_temporal_resolvers)
    world = runtime.create_world(instance_id=WorldInstanceId("g92f_runtime"))
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("g92f_calendar"),
            instance_id=world.instance_id,
            branch_id=world.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "calendar", "version": 1},
            world_time=WorldTime(1),
        )
    )
    before = runtime.current_state(world.instance_id, world.root_branch_id)
    ledger = CostBudgetLedger()
    keys = (
        BudgetKey("world", world.instance_id.value),
        BudgetKey("actor", "actor_a"),
        BudgetKey("provider", "local-reference"),
    )
    for key in keys:
        ledger.register(
            key, CostLimit(max_calls=2, max_tokens=10, max_time_ms=100, max_storage_bytes=100)
        )
    ledger.admit(keys, CostUsage(tokens=8, calls=1), requested_lod="L0")
    decision = ledger.admit(keys, CostUsage(tokens=3), requested_lod="L0")
    lod = SimulationLODRuntime()
    state = LODState("actor_a", "L0", before.semantic_hash(), "memory://actor_a")
    transition = lod.transition(state, lod.score(ActorActivityInput("actor_a", 100, 100, 1, 0, 0)))
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert decision.status == "degraded" and decision.recommended_lod == "L1"
    assert transition.to_level == "L1"
    assert after.semantic_hash() == before.semantic_hash()
    assert len(runtime.events(world.instance_id, world.root_branch_id)) == 1
