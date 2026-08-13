"""M5 supplemental proofs (G06A-C): lifecycle persistence, multi-client queue
and crash recovery inside the hosted-world scenario.
"""

from __future__ import annotations

import pathlib
from collections.abc import Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.lifecycle.resolver import register_lifecycle_resolvers
from wanxiang_substrate.lifecycle.service import LifecycleService
from wanxiang_substrate.queue.queue import CommandQueue
from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget
from wanxiang_substrate.recovery.errors import BudgetExceeded
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

INSTANCE = WorldInstanceId("wld_m5g06")
TOWN = EntityId("town")


def make_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_temporal_resolvers(registry)
        register_lifecycle_resolvers(registry)
        registry.register("m5g06.instantiate", _instantiate)

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


@pytest.mark.integration
def test_m5_g06_lifecycle_queue_recovery() -> None:
    path = fresh_db_path()
    try:
        runtime = make_runtime(path)
        w = runtime.create_world(instance_id=INSTANCE)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId("cmd_m5g06_instantiate"),
                instance_id=INSTANCE,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(0),
                action_type="m5g06.instantiate",
                payload={},
                world_time=WorldTime(1),
            )
        )
        # Lifecycle persists independently of sessions.
        lifecycle = LifecycleService(runtime, INSTANCE, w.root_branch_id)
        lifecycle.set_mode("BACKGROUND_SIMULATION")
        lifecycle.advance(7)
        assert lifecycle.current().mode == "BACKGROUND_SIMULATION"
        assert lifecycle.current().tick == 7

        # Multi-client queue: idempotent retries + conflict surfacing.
        revision = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
        queue = CommandQueue(runtime=runtime)
        queue.enqueue(
            _cmd(
                w.root_branch_id,
                revision,
                "create_entity",
                {"entity_id": "a", "entity_type": "thing"},
                "cmd_a",
            )
        )
        queue.enqueue(
            _cmd(
                w.root_branch_id,
                revision,
                "create_entity",
                {"entity_id": "b", "entity_type": "thing"},
                "cmd_b",
            )
        )
        statuses = {r.command_id: r.status for r in queue.drain()}
        assert statuses["cmd_a"] == "accepted"
        assert statuses["cmd_b"] == "conflict"
        state = runtime.current_state(w.instance_id, w.root_branch_id)
        assert state.entity(EntityId("a")) is not None
        assert state.entity(EntityId("b")) is None

        # Crash/restart: replay preserves canonical hash.
        before_hash = runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash()
        runtime2 = make_runtime(path)
        events = runtime2.events(INSTANCE, w.root_branch_id)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        assert replayed.semantic_hash() == before_hash
        # Lifecycle mode is restored deterministically from the replayed state.
        restored = LifecycleService(runtime2, INSTANCE, w.root_branch_id)
        assert restored.current().mode == "BACKGROUND_SIMULATION"

        # Budget keeps the hosted loop bounded.
        tracker = BudgetTracker(ResourceBudget(max_commands=2))
        tracker.consume(commands=1)
        tracker.consume(commands=1)
        with pytest.raises(BudgetExceeded):
            tracker.consume(commands=1)
    finally:
        cleanup_db_file(path)
