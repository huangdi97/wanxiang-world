"""G92E real-runtime state continuity across LOD projections."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.long_horizon import (
    ActorActivityInput,
    LODState,
    SimulationLODRuntime,
)
from wanxiang_substrate.temporal.resolver import ACTION_INSTANTIATE, register_temporal_resolvers


def test_lod_projection_does_not_duplicate_or_mutate_canonical_state(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_temporal_resolvers)
    world = runtime.create_world(instance_id=WorldInstanceId("g92e_runtime"))
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("g92e_calendar"),
            instance_id=world.instance_id,
            branch_id=world.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "calendar", "version": 1},
            world_time=WorldTime(1),
        )
    )
    before = runtime.current_state(world.instance_id, world.root_branch_id)
    state_hash = before.semantic_hash()
    lod = SimulationLODRuntime()
    actor_state = LODState("actor_a", "L0", state_hash, "memory://actor_a")
    low_score = lod.score(ActorActivityInput("actor_a", 1001, 0, proximity=1))
    down = lod.transition(actor_state, low_score)
    up = lod.promote_to_active(
        LODState(
            actor_state.actor_id, down.to_level, down.state_ref, actor_state.memory_summary_ref
        ),
        lod.score(ActorActivityInput("actor_a", 100, 100, 1, 1, 1)),
    )
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert down.to_level == "L3"
    assert up.to_level == "L0"
    assert up.state_ref == state_hash
    assert after.semantic_hash() == state_hash
    assert len(runtime.events(world.instance_id, world.root_branch_id)) == 1
