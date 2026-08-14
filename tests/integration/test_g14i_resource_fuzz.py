"""G14I: resource exhaustion, fuzz, long-run chaos & M11 qualification.

- Fuzzed structured commands never violate canonical invariants.
- A long event stream replays with stable hashes and bounded memory growth.
- Over-budget load fails predictably (QueueFull / BudgetExceeded), never corrupts.
- Repeated failures surface structured errors and the world keeps advancing.
"""

from __future__ import annotations

import pathlib
import random

import pytest
from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import WanxiangError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.queue.errors import QueueFull
from wanxiang_substrate.queue.queue import CommandQueue
from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget
from wanxiang_substrate.recovery.errors import BudgetExceeded


def _fuzz_command(
    rng: random.Random, instance: WorldInstanceId, branch: BranchId, revision: int, seq: int
) -> CommandEnvelope:
    action = rng.choice(
        ["create_entity", "transfer_resource", "set_status", "no_such_action", "", "x" * 500]
    )
    entity_id = rng.choice(["a", "b", "c", "", "!" * 40, "e" * 200])
    count = rng.choice([0, 1, -5, 10**9, 1.5, "x", None])
    return CommandEnvelope(
        command_id=CommandId(f"fuzz_{seq}"),
        instance_id=instance,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload={"entity_id": entity_id, "count": count},
        world_time=WorldTime(revision + 1),
    )


def _assert_stream_valid(
    runtime: WorldRuntime, instance: WorldInstanceId, branch: BranchId
) -> None:
    events = runtime.persistence.event_store.load(instance, branch)
    assert [e.event_seq.value for e in events] == list(range(1, len(events) + 1))
    assert [e.revision.value for e in events] == list(range(1, len(events) + 1))
    if events:
        ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)


def test_fuzzed_structured_commands_never_violate_invariants(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    rng = random.Random(20260814)
    revision = 0
    for seq in range(200):
        try:
            cmd = _fuzz_command(rng, iid, branch, revision, seq)
            result = runtime.submit_command(cmd)
            if result.duplicate is False:
                revision = result.state.revision.value
        except WanxiangError:
            pass  # structured rejection (construction or submit) is expected
        _assert_stream_valid(runtime, iid, branch)
    # Replay from clean state reproduces the committed hash.
    state = runtime.current_state(iid, branch)
    events = runtime.persistence.event_store.load(iid, branch)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()


def test_long_event_stream_replays_stably_and_growth_is_bounded(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    for i in range(1200):
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"long_{i}"),
                instance_id=iid,
                branch_id=branch,
                expected_revision=BranchRevision(i),
                action_type="create_entity",
                payload={"entity_id": f"e{i}", "count": i % 7},
                world_time=WorldTime(i + 1),
            )
        )
    events = runtime.persistence.event_store.load(iid, branch)
    assert len(events) == 1200
    _assert_stream_valid(runtime, iid, branch)
    # Semantic hash is stable across replay from clean state.
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == runtime.current_state(iid, branch).semantic_hash()
    # Growth is deterministic and linear in events (1200 entities, no runaway).
    assert len(replayed.entities()) == 1200


def test_over_budget_load_fails_predictably(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    queue = CommandQueue(capacity=2, runtime=runtime)
    queue.enqueue(
        CommandEnvelope(
            command_id=CommandId("q0"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "a", "count": 1},
            world_time=WorldTime(1),
        )
    )
    queue.enqueue(
        CommandEnvelope(
            command_id=CommandId("q1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(1),
            action_type="create_entity",
            payload={"entity_id": "b", "count": 1},
            world_time=WorldTime(2),
        )
    )
    with pytest.raises(QueueFull):
        queue.enqueue(
            CommandEnvelope(
                command_id=CommandId("q2"),
                instance_id=iid,
                branch_id=branch,
                expected_revision=BranchRevision(2),
                action_type="create_entity",
                payload={"entity_id": "c", "count": 1},
                world_time=WorldTime(3),
            )
        )
    # Resource budget exhaustion also fails predictably.
    tracker = BudgetTracker(ResourceBudget(max_commands=5))
    for _ in range(5):
        tracker.consume(commands=1)
    with pytest.raises(BudgetExceeded):
        tracker.consume(commands=1)


def test_repeated_failures_do_not_corrupt_world(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    failures = 0
    for i in range(50):
        try:
            runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"bad_{i}"),
                    instance_id=iid,
                    branch_id=branch,
                    expected_revision=BranchRevision(i),
                    action_type="no_such_action",
                    payload={},
                    world_time=WorldTime(i + 1),
                )
            )
        except WanxiangError:
            failures += 1
    assert failures == 50
    # No event was committed for the failures; the world is untouched.
    assert runtime.persistence.event_store.load(iid, branch) == ()
    # A valid command still works afterwards.
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("ok_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "alice", "count": 1},
            world_time=WorldTime(1),
        )
    )
    _assert_stream_valid(runtime, iid, branch)
