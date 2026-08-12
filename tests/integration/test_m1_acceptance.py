"""GOAL_01F: M1 acceptance scenarios A1-A10 (application/runtime + SQLite)."""

from __future__ import annotations

import pytest
from sqlalchemy import update
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from tests.helpers.replay_fixture import BRANCH as GOLDEN_BRANCH
from tests.helpers.replay_fixture import INSTANCE as GOLDEN_INSTANCE
from tests.helpers.replay_fixture import build_fixture_events
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import StaleRevision, ValidationRejected, WanxiangError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_persistence.models import EventRecord
from wanxiang_runtime.replay import ReplayEngine

GOLDEN_HASH = "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"


def create_cmd(
    branch: BranchId,
    revision: int,
    name: str,
    count: int = 5,
    command_id: str | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id or f"cmd_{name}"),
        instance_id=WorldInstanceId("wld_m1"),
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type="create_entity",
        payload={"entity_id": name, "count": count},
        world_time=WorldTime(revision + 1),
    )


def transfer_cmd(
    branch: BranchId,
    revision: int,
    source: str,
    target: str,
    amount: int,
    command_id: str | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id or f"cmd_xfer_{revision}"),
        instance_id=WorldInstanceId("wld_m1"),
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type="transfer_resource",
        payload={"source_id": source, "target_id": target, "amount": amount},
        world_time=WorldTime(revision + 1),
    )


def setup_two_entities(runtime: WorldRuntime, world: object, branch: BranchId) -> None:
    runtime.submit_command(create_cmd(branch, 0, "alice", 10))
    runtime.submit_command(create_cmd(branch, 1, "bob", 0))


def _hash(runtime: WorldRuntime, instance: WorldInstanceId, branch: BranchId) -> str:
    return runtime.current_state(instance, branch).semantic_hash()


@pytest.mark.integration
def test_a1_valid_commit_changes_state_exactly_once(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    result = world_runtime.submit_command(create_cmd(world.root_branch_id, 0, "alice", 10))
    assert result.state.revision == BranchRevision(1)
    assert result.state.entity(EntityId("alice")) is not None
    assert len(world_runtime.events(world.instance_id, world.root_branch_id)) == 1
    assert (
        _hash(world_runtime, world.instance_id, world.root_branch_id)
        == result.state.semantic_hash()
    )


@pytest.mark.integration
def test_a2_invalid_command_does_not_mutate(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    setup_two_entities(world_runtime, world, world.root_branch_id)
    before = _hash(world_runtime, world.instance_id, world.root_branch_id)
    with pytest.raises(ValidationRejected):
        world_runtime.submit_command(transfer_cmd(world.root_branch_id, 2, "alice", "ghost", 1))
    assert _hash(world_runtime, world.instance_id, world.root_branch_id) == before
    assert len(world_runtime.events(world.instance_id, world.root_branch_id)) == 2


@pytest.mark.integration
def test_a3_duplicate_command_is_idempotent(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    first = world_runtime.submit_command(
        create_cmd(world.root_branch_id, 0, "alice", 10, "cmd_dup")
    )
    second = world_runtime.submit_command(
        create_cmd(world.root_branch_id, 1, "alice", 10, "cmd_dup")
    )
    assert second.duplicate is True
    assert second.event.event_id == first.event.event_id
    assert len(world_runtime.events(world.instance_id, world.root_branch_id)) == 1


@pytest.mark.integration
def test_a4_stale_revision_is_rejected(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    setup_two_entities(world_runtime, world, world.root_branch_id)
    with pytest.raises(StaleRevision):
        world_runtime.submit_command(create_cmd(world.root_branch_id, 0, "carol", 1, "cmd_stale"))
    state = world_runtime.current_state(world.instance_id, world.root_branch_id)
    assert state.revision == BranchRevision(2)
    assert state.entity(EntityId("carol")) is None


@pytest.mark.integration
def test_a5_snapshot_plus_remaining_replay(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    setup_two_entities(world_runtime, world, world.root_branch_id)
    world_runtime.create_checkpoint(world.instance_id, world.root_branch_id)
    world_runtime.submit_command(transfer_cmd(world.root_branch_id, 2, "alice", "bob", 3, "cmd_t1"))
    current_hash = _hash(world_runtime, world.instance_id, world.root_branch_id)
    restored = world_runtime.restore_and_replay(world.instance_id, world.root_branch_id)
    assert restored.used_snapshot is True
    assert restored.state.semantic_hash() == current_hash


@pytest.mark.integration
def test_a6_full_replay_from_initial_baseline(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    setup_two_entities(world_runtime, world, world.root_branch_id)
    world_runtime.submit_command(transfer_cmd(world.root_branch_id, 2, "alice", "bob", 3, "cmd_t1"))
    current_hash = _hash(world_runtime, world.instance_id, world.root_branch_id)
    # No snapshot exists here, so restore_and_replay replays the full stream.
    restored = world_runtime.restore_and_replay(world.instance_id, world.root_branch_id)
    assert restored.used_snapshot is False
    assert restored.state.semantic_hash() == current_hash


@pytest.mark.integration
def test_a7_branch_isolation(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    setup_two_entities(world_runtime, world, world.root_branch_id)
    parent_hash = _hash(world_runtime, world.instance_id, world.root_branch_id)
    child = world_runtime.create_branch(world.instance_id, world.root_branch_id)
    child_state = world_runtime.current_state(world.instance_id, child.branch_id)
    assert child_state.revision == BranchRevision(2)
    child_result = world_runtime.submit_command(
        create_cmd(child.branch_id, 2, "carol", 7, "cmd_child")
    )
    assert child_result.state.revision == BranchRevision(3)
    parent_after = world_runtime.current_state(world.instance_id, world.root_branch_id)
    assert parent_after.semantic_hash() == parent_hash
    assert parent_after.entity(EntityId("carol")) is None
    assert child.ancestry.parent_branch_id == world.root_branch_id


@pytest.mark.integration
def test_a8_deterministic_reproduction(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    setup_two_entities(world_runtime, world, world.root_branch_id)
    world_runtime.submit_command(transfer_cmd(world.root_branch_id, 2, "alice", "bob", 3, "cmd_t1"))
    first_hash = _hash(world_runtime, world.instance_id, world.root_branch_id)

    second_path = fresh_db_path()
    try:
        runtime2 = make_world_runtime(second_path)
        world2 = runtime2.create_world(instance_id=WorldInstanceId("wld_m1"))
        runtime2.submit_command(create_cmd(world2.root_branch_id, 0, "alice", 10, "cmd_alice"))
        runtime2.submit_command(create_cmd(world2.root_branch_id, 1, "bob", 0, "cmd_bob"))
        runtime2.submit_command(transfer_cmd(world2.root_branch_id, 2, "alice", "bob", 3, "cmd_t1"))
        second_hash = _hash(runtime2, world2.instance_id, world2.root_branch_id)
        assert first_hash == second_hash
    finally:
        cleanup_db_file(second_path)


@pytest.mark.integration
def test_a9_corrupt_stream_fails_explicitly(world_runtime: WorldRuntime) -> None:
    world = world_runtime.create_world(instance_id=WorldInstanceId("wld_m1"))
    setup_two_entities(world_runtime, world, world.root_branch_id)
    store = world_runtime.persistence.event_store
    assert isinstance(store, SqlAlchemyEventStore)
    with store.session_factory() as session:
        session.execute(
            update(EventRecord)
            .where(EventRecord.event_seq == 2)
            .values(delta_json='{"schema_version": 999}')
        )
        session.commit()
    world_runtime.invalidate_state_cache()
    with pytest.raises(WanxiangError):
        world_runtime.current_state(world.instance_id, world.root_branch_id)


@pytest.mark.integration
def test_a10_durable_replay_matches_golden(world_runtime: WorldRuntime) -> None:
    store = world_runtime.persistence.event_store
    for event in build_fixture_events():
        store.append(event)
    engine = ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
    final = engine.replay(store.load(GOLDEN_INSTANCE, GOLDEN_BRANCH))
    assert final.semantic_hash() == GOLDEN_HASH
