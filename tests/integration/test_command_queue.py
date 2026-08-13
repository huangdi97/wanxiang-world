"""G06B: idempotent multi-client command queue semantics."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.queue.errors import DuplicateQueuedCommand, QueueFull
from wanxiang_substrate.queue.queue import CommandQueue
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_queue")
TOWN = EntityId("town")


def make_queue_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        registry.register("queue.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(entity_id=TOWN, entity_type="spatial.place", components=()),
        )
    )


def _cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def queue_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_queue_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_queue_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="queue.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_conflicting_revisions_cannot_both_commit(
    queue_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = queue_world
    queue = CommandQueue(runtime=runtime)
    first = _cmd(
        w.root_branch_id, 1, "create_entity", {"entity_id": "a", "entity_type": "thing"}, "cmd_a"
    )
    second = _cmd(
        w.root_branch_id, 1, "create_entity", {"entity_id": "b", "entity_type": "thing"}, "cmd_b"
    )
    queue.enqueue(first)
    queue.enqueue(second)
    results = queue.drain()
    statuses = {r.command_id: r.status for r in results}
    assert statuses["cmd_a"] == "accepted"
    assert statuses["cmd_b"] == "conflict"
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(EntityId("a")) is not None
    assert state.entity(EntityId("b")) is None


@pytest.mark.integration
def test_retry_across_reconnect_produces_one_effect(
    queue_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = queue_world
    queue = CommandQueue(runtime=runtime)
    envelope = _cmd(
        w.root_branch_id, 1, "create_entity", {"entity_id": "x", "entity_type": "thing"}, "cmd_x"
    )
    queue.enqueue(envelope)
    queue.drain()
    # A reconnect retries the same command id; idempotency holds (no second effect).
    with pytest.raises(DuplicateQueuedCommand):
        queue.enqueue(envelope)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(EntityId("x")) is not None


@pytest.mark.integration
def test_committed_sequence_is_total_per_branch(
    queue_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = queue_world
    queue = CommandQueue(runtime=runtime)
    queue.enqueue(
        _cmd(
            w.root_branch_id,
            1,
            "create_entity",
            {"entity_id": "a", "entity_type": "thing"},
            "cmd_a",
        )
    )
    queue.enqueue(
        _cmd(
            w.root_branch_id,
            2,
            "create_entity",
            {"entity_id": "b", "entity_type": "thing"},
            "cmd_b",
        )
    )
    results = queue.drain()
    assert all(r.status == "accepted" for r in results)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(EntityId("a")) is not None
    assert state.entity(EntityId("b")) is not None


@pytest.mark.unit
def test_bounded_queue_backpressure() -> None:
    queue = CommandQueue(capacity=2)
    queue.enqueue(
        _cmd(
            BranchId("br1"), 0, "create_entity", {"entity_id": "a", "entity_type": "thing"}, "cmd_a"
        )
    )
    queue.enqueue(
        _cmd(
            BranchId("br1"), 1, "create_entity", {"entity_id": "b", "entity_type": "thing"}, "cmd_b"
        )
    )
    with pytest.raises(QueueFull):
        queue.enqueue(
            _cmd(
                BranchId("br1"),
                2,
                "create_entity",
                {"entity_id": "c", "entity_type": "thing"},
                "cmd_c",
            )
        )
    assert queue.pending_count() == 2
