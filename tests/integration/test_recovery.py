"""G06C: crash recovery, checkpoint validation and resource budgets."""

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
from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget
from wanxiang_substrate.recovery.checkpoint import (
    CheckpointMeta,
    CheckpointService,
    InMemorySnapshotStore,
)
from wanxiang_substrate.recovery.errors import BudgetExceeded, CorruptSnapshot, NoSnapshot
from wanxiang_substrate.recovery.recovery import RecoveryService
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_rec")
TOWN = EntityId("town")


def make_rec_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        registry.register("rec.instantiate", _instantiate)

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
def test_kill_restart_preserves_canonical_hash() -> None:
    path = fresh_db_path()
    try:
        runtime = make_rec_runtime(path)
        w = runtime.create_world(instance_id=INSTANCE)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId("cmd_rec_instantiate"),
                instance_id=INSTANCE,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(0),
                action_type="rec.instantiate",
                payload={},
                world_time=WorldTime(1),
            )
        )
        revision = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
        runtime.submit_command(
            _cmd(
                w.root_branch_id,
                revision,
                "create_entity",
                {"entity_id": "a", "entity_type": "thing"},
                "cmd_a",
            )
        )
        before_hash = runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash()
        # "Restart" on the same DB: replay reproduces the identical hash.
        runtime2 = make_rec_runtime(path)
        events = runtime2.events(INSTANCE, w.root_branch_id)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        assert replayed.semantic_hash() == before_hash
    finally:
        cleanup_db_file(path)


@pytest.mark.unit
def test_checkpoint_roundtrip_and_corruption_policy() -> None:
    store = InMemorySnapshotStore()
    checkpoint = CheckpointService(store)
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta

    base = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BranchId("br1"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )
    state = apply_delta(
        base,
        ProposedWorldDelta(
            operations=(EntityCreate(entity_id=TOWN, entity_type="spatial.place", components=()),)
        ),
    )
    meta = checkpoint.save(INSTANCE.value, "br1", state.revision.value, state, "snap_1")
    assert isinstance(meta, CheckpointMeta)
    restored = checkpoint.restore(INSTANCE.value)
    assert restored.semantic_hash() == state.semantic_hash()
    with pytest.raises(NoSnapshot):
        checkpoint.restore(WorldInstanceId("wld_missing").value)
    # Revision mismatch is a corrupt checkpoint.
    with pytest.raises(CorruptSnapshot):
        checkpoint.save(INSTANCE.value, "br1", state.revision.value + 1, state, "snap_bad")


@pytest.mark.unit
def test_recovery_falls_back_to_event_replay() -> None:
    store = InMemorySnapshotStore()
    checkpoint = CheckpointService(store)
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta

    state = apply_delta(
        InMemoryCanonicalState(
            instance_id=INSTANCE,
            branch_id=BranchId("br1"),
            revision=BranchRevision(0),
            schema_version=SchemaVersion(1),
            rule_version=RuntimeVersion(1),
        ),
        ProposedWorldDelta(
            operations=(EntityCreate(entity_id=TOWN, entity_type="spatial.place", components=()),)
        ),
    )
    report = RecoveryService(checkpoint).recover(INSTANCE.value, state)
    assert report.restored_from == "event_replay"
    assert report.semantic_hash == state.semantic_hash()


@pytest.mark.unit
def test_runaway_actor_cannot_monopolize_loop() -> None:
    tracker = BudgetTracker(ResourceBudget(max_commands=3, max_ticks=10_000))
    for _ in range(3):
        tracker.consume(commands=1)
    with pytest.raises(BudgetExceeded):
        tracker.consume(commands=1)
    tracker.reset()
    assert tracker.remaining()["commands"] == 3
