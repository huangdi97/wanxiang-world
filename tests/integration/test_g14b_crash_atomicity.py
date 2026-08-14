"""G14B: crash, atomicity & mid-commit recovery qualification.

Covers every important commit boundary deterministically:
- crash before append: no event, no state change, idempotent retry works;
- crash after append: restart reconstructs from authoritative event history;
- checkpoint does not break recovery (snapshot is an optimization);
- retry classification after restart: acknowledged -> same event, unknown -> commits;
- host lifecycle transition survives restart.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import PersistenceError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.temporal.components import CLOCK_ENTITY


def _cmd(
    instance: WorldInstanceId,
    branch: BranchId,
    revision: int,
    name: str,
    command_id: str | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id or f"cmd_{name}"),
        instance_id=instance,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type="create_entity",
        payload={"entity_id": name, "count": 1},
        world_time=WorldTime(revision + 1),
    )


def test_crash_before_append_leaves_no_trace() -> None:
    """Crash at the append boundary (test-only fail_append hook)."""
    from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
    from wanxiang_domain.entity import ComponentData
    from wanxiang_domain.hierarchy import EventSeq
    from wanxiang_domain.ids import ComponentId, EntityId
    from wanxiang_runtime.authority import CommitAuthority, CommitRequest
    from wanxiang_runtime.ports import InMemoryEventStore

    instance = WorldInstanceId("wld_g14b")
    branch = BranchId("br_g14b")
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RuntimeVersion(1), SchemaVersion(1))
    state = InMemoryCanonicalState(
        instance_id=instance,
        branch_id=branch,
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )
    delta = ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId("alice"),
                entity_type="person",
                components=(
                    ComponentData(
                        component_id=ComponentId("res"),
                        component_type="resource",
                        schema_version=SchemaVersion(1),
                        fields={"count": 1},
                    ),
                ),
            ),
        )
    )
    request = CommitRequest(
        command_id=CommandId("cmd_crash"),
        instance_id=instance,
        branch_id=branch,
        expected_revision=BranchRevision(0),
        delta=delta,
        world_time=WorldTime(1),
        rule_version=RuntimeVersion(1),
    )

    store.fail_append = True
    with pytest.raises(PersistenceError):
        authority.commit(state, request)
    store.fail_append = False

    # No half state: no event committed.
    assert store.load(instance, branch) == ()
    # Retry after recovery commits exactly once.
    result = authority.commit(state, request)
    assert result.event.event_seq == EventSeq(1)
    assert len(store.load(instance, branch)) == 1
    # Duplicate command retries never duplicate world effects: the append
    # boundary rejects a second event for the same command id even with a
    # valid next sequence number.
    from dataclasses import replace

    from wanxiang_domain.errors import DuplicateCommandConflict
    from wanxiang_domain.hierarchy import EventSeq
    from wanxiang_domain.ids import EventId

    retry_event = replace(result.event, event_seq=EventSeq(2), event_id=EventId("evt_retry_g14b"))
    with pytest.raises(DuplicateCommandConflict):
        store.append(retry_event)


def test_crash_after_append_recovers_from_authoritative_history(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_r1"))
    runtime.submit_command(_cmd(iid, branch, 1, "bob", command_id="cmd_r2"))
    expected = runtime.current_state(iid, branch).semantic_hash()

    # Simulated crash/restart: fresh runtime over the same database.
    restarted = make_world_runtime(persist_db_path)
    state = restarted.current_state(iid, branch)
    assert state.semantic_hash() == expected
    assert state.revision.value == 2
    events = restarted.persistence.event_store.load(iid, branch)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == expected


def test_checkpoint_does_not_break_recovery(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    for i in range(3):
        runtime.submit_command(_cmd(iid, branch, i, f"ent_{i}", command_id=f"cp_{i}"))
    meta = runtime.create_checkpoint(iid, branch)
    assert meta.revision.value == 3

    restarted = make_world_runtime(persist_db_path)
    restored = restarted.restore_and_replay(iid, branch)
    assert restored.used_snapshot is True
    assert restored.state.revision.value == 3
    assert restored.state.semantic_hash() == runtime.current_state(iid, branch).semantic_hash()


def test_retry_classification_after_restart(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    first = runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_known"))
    known_event_id = first.event.event_id.value

    restarted = make_world_runtime(persist_db_path)
    # Acknowledged command retry -> duplicate with the same event.
    dup = restarted.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_known"))
    assert dup.duplicate is True and dup.event is not None
    assert dup.event.event_id.value == known_event_id
    # Unknown command -> fresh commit.
    fresh = restarted.submit_command(_cmd(iid, branch, 1, "bob", command_id="cmd_new"))
    assert fresh.duplicate is False
    assert len(restarted.persistence.event_store.load(iid, branch)) == 2


def test_lifecycle_transition_survives_restart(persist_db_path: pathlib.Path) -> None:
    from wanxiang_runtime.resolver import ResolverRegistry
    from wanxiang_substrate.lifecycle.resolver import register_lifecycle_resolvers
    from wanxiang_substrate.lifecycle.service import LifecycleService
    from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

    def register(registry: ResolverRegistry) -> None:
        register_temporal_resolvers(registry)
        register_lifecycle_resolvers(registry)
        registry.register(
            "life.instantiate",
            lambda command, state: _instantiate_lifecycle(),
        )

    runtime = make_world_runtime(persist_db_path, extra_resolvers=register)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("life_init"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="life.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    service = LifecycleService(runtime, iid, branch)
    service.set_mode("PAUSED", tick=5)

    restarted = make_world_runtime(persist_db_path, extra_resolvers=register)
    service2 = LifecycleService(restarted, iid, branch)
    assert service2.current().mode == "PAUSED"
    assert service2.current().tick == 5


def _instantiate_lifecycle() -> ProposedWorldDelta:
    from wanxiang_domain.delta import EntityCreate
    from wanxiang_domain.entity import ComponentData
    from wanxiang_domain.ids import ComponentId, EntityId

    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(
                    ComponentData(
                        component_id=ComponentId("clock"),
                        component_type="temporal.clock",
                        schema_version=SchemaVersion(1),
                        fields={"ticks": 0, "paused": False},
                    ),
                ),
            ),
            EntityCreate(
                entity_id=EntityId("life_entity"),
                entity_type="lifecycle.entity",
                components=(),
            ),
        )
    )
