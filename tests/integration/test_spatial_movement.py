"""G02A: spatial movement through the M1 Commit Authority path."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, SubmitCommandResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.spatial.errors import (
    PlaceAtCapacity,
    PortalClosed,
    PortalLocked,
)
from wanxiang_substrate.spatial.fixture import INSTANCE, build_house_fixture_commands
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.spatial.resolver import (
    ACTION_MOVE,
    ACTION_SET_PORTAL_STATE,
    register_spatial_resolvers,
)


def make_house_runtime(path: pathlib.Path) -> WorldRuntime:
    return make_world_runtime(path, extra_resolvers=register_spatial_resolvers)


def move(
    runtime: WorldRuntime,
    branch: BranchId,
    revision: int,
    entity: str,
    target: str,
    command_id: str,
    actor_id: str | None = None,
) -> SubmitCommandResult:
    return runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=INSTANCE,
            branch_id=branch,
            expected_revision=BranchRevision(revision),
            action_type=ACTION_MOVE,
            payload={"entity_id": entity, "target_place_id": target},
            actor_id=ActorId(actor_id) if actor_id else None,
            world_time=WorldTime(revision + 1),
        )
    )


def set_portal(
    runtime: WorldRuntime, branch: BranchId, revision: int, portal: str, state: str, command_id: str
) -> SubmitCommandResult:
    return runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=INSTANCE,
            branch_id=branch,
            expected_revision=BranchRevision(revision),
            action_type=ACTION_SET_PORTAL_STATE,
            payload={"portal_id": portal, "new_state": state},
            world_time=WorldTime(revision + 1),
        )
    )


@pytest.fixture
def house() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_house_runtime(path)
    world = runtime.create_world(instance_id=INSTANCE)
    for command in build_house_fixture_commands(world.root_branch_id):
        runtime.submit_command(command)
    yield runtime, world
    cleanup_db_file(path)


@pytest.mark.integration
def test_move_through_open_door(house: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, world = house
    result = move(runtime, world.root_branch_id, 1, "alice", "kitchen", "cmd_m1")
    assert result.state.revision == BranchRevision(2)
    assert SpatialQuery(result.state).location(EntityId("alice")) == EntityId("kitchen")


@pytest.mark.integration
def test_locked_portal_rejects_without_key_no_mutation(
    house: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, world = house
    before = runtime.current_state(world.instance_id, world.root_branch_id).semantic_hash()
    with pytest.raises(PortalLocked):
        move(runtime, world.root_branch_id, 1, "alice", "garden", "cmd_locked")
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert after.semantic_hash() == before
    assert SpatialQuery(after).location(EntityId("alice")) == EntityId("hall")


@pytest.mark.integration
def test_locked_portal_allows_key_holder(house: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, world = house
    result = move(runtime, world.root_branch_id, 1, "bob", "garden", "cmd_bob", actor_id="bob")
    assert SpatialQuery(result.state).location(EntityId("bob")) == EntityId("garden")


@pytest.mark.integration
def test_closed_portal_rejects_movement(house: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, world = house
    set_portal(runtime, world.root_branch_id, 1, "door_hall_kitchen", "closed", "cmd_close")
    with pytest.raises(PortalClosed):
        move(runtime, world.root_branch_id, 2, "alice", "kitchen", "cmd_closed")
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    assert SpatialQuery(state).location(EntityId("alice")) == EntityId("hall")


@pytest.mark.integration
def test_capacity_rejects_overflow(house: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, world = house
    move(runtime, world.root_branch_id, 1, "alice", "kitchen", "cmd_a")
    move(runtime, world.root_branch_id, 2, "bob", "hall", "cmd_b")
    move(runtime, world.root_branch_id, 3, "bob", "kitchen", "cmd_c")
    with pytest.raises(PlaceAtCapacity):
        move(runtime, world.root_branch_id, 4, "no_key", "kitchen", "cmd_d")
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    assert SpatialQuery(state).location(EntityId("no_key")) == EntityId("hall")


@pytest.mark.integration
def test_spatial_replay_is_deterministic(house: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, world = house
    move(runtime, world.root_branch_id, 1, "alice", "kitchen", "cmd_a")
    move(runtime, world.root_branch_id, 2, "bob", "hall", "cmd_b")
    move(runtime, world.root_branch_id, 3, "bob", "garden", "cmd_c", actor_id="bob")
    current = runtime.current_state(world.instance_id, world.root_branch_id)
    events = runtime.events(world.instance_id, world.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == current.semantic_hash()
    assert SpatialQuery(replayed).location(EntityId("alice")) == EntityId("kitchen")
    assert SpatialQuery(replayed).location(EntityId("bob")) == EntityId("garden")


@pytest.mark.integration
def test_m1_golden_replay_unaffected(world_runtime: WorldRuntime) -> None:
    from tests.helpers.replay_fixture import BRANCH as GB
    from tests.helpers.replay_fixture import INSTANCE as GI
    from tests.helpers.replay_fixture import build_fixture_events

    for event in build_fixture_events():
        world_runtime.persistence.event_store.append(event)
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(
        world_runtime.persistence.event_store.load(GI, GB)
    )
    assert (
        final.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )


@pytest.mark.integration
def test_pre_g02_db_upgrades_cleanly_and_m1_fixture_still_replays() -> None:
    """G02A adds no persisted schema (spatial rides on versioned components).

    Prove: a pre-G02 database (M1 head 0002) still upgrades to head, the M1
    golden fixture replays, and spatial events replay on top without breaking it.
    """

    from sqlalchemy import text
    from tests.conftest import upgrade_db
    from tests.helpers.replay_fixture import build_fixture_events

    path = fresh_db_path()
    try:
        upgrade_db(path)  # M1 head (0002)
        # Verify the alembic head is still the M1 schema (no G02A migration).
        from wanxiang_persistence.database import create_engine_for

        engine = create_engine_for(f"sqlite:///{path.as_posix()}")
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
        assert version == "0004_add_world_metadata"
        engine.dispose()

        # M1 golden fixture + spatial events on the same DB.
        runtime = make_house_runtime(path)
        world = runtime.create_world(instance_id=INSTANCE)
        for event in build_fixture_events():
            runtime.persistence.event_store.append(event)
        for command in build_house_fixture_commands(world.root_branch_id):
            runtime.submit_command(command)
        move(runtime, world.root_branch_id, 1, "alice", "kitchen", "cmd_pre_g02")
        events = runtime.events(world.instance_id, world.root_branch_id)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        assert SpatialQuery(replayed).location(EntityId("alice")) == EntityId("kitchen")
        assert (
            replayed.semantic_hash()
            == runtime.current_state(world.instance_id, world.root_branch_id).semantic_hash()
        )
    finally:
        cleanup_db_file(path)
