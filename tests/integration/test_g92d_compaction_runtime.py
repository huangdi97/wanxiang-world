"""G92D real-runtime golden replay before/after logical compaction."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.long_horizon import CompactionPolicy, CompactionService
from wanxiang_substrate.temporal.resolver import (
    ACTION_ADVANCE_TO,
    ACTION_INSTANTIATE,
    register_temporal_resolvers,
)


def test_compaction_references_preserve_runtime_event_history(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_temporal_resolvers)
    world = runtime.create_world(instance_id=WorldInstanceId("g92d_runtime"))
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("g92d_calendar"),
            instance_id=world.instance_id,
            branch_id=world.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "calendar", "version": 1},
            world_time=WorldTime(1),
        )
    )
    for index, tick in enumerate((10, 20, 30), start=1):
        state = runtime.current_state(world.instance_id, world.root_branch_id)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"g92d_tick_{index}"),
                instance_id=world.instance_id,
                branch_id=world.root_branch_id,
                expected_revision=BranchRevision(state.revision.value),
                action_type=ACTION_ADVANCE_TO,
                payload={"ticks": tick},
                world_time=WorldTime(tick),
            )
        )
    before = runtime.restore_and_replay(world.instance_id, world.root_branch_id).state
    snapshot = runtime.create_checkpoint(world.instance_id, world.root_branch_id)
    events_before = runtime.events(world.instance_id, world.root_branch_id)
    after = runtime.restore_and_replay(world.instance_id, world.root_branch_id).state
    manifest = CompactionService(CompactionPolicy(retain_recent_events=2)).compact(
        events_before,
        snapshot,
        replay_hash_before=before.semantic_hash(),
        replay_hash_after=after.semantic_hash(),
    )
    events_after = runtime.events(world.instance_id, world.root_branch_id)
    assert manifest.replay_hash == before.semantic_hash()
    assert before.semantic_hash() == after.semantic_hash()
    assert len(events_after) == len(events_before)
    assert tuple(event.event_seq.value for event in events_after) == tuple(
        event.event_seq.value for event in events_before
    )
