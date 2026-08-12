"""G02C: material custody/transfer/container/payload through the M1 authority."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.material.errors import (
    ContainerFull,
    ContainmentCycle,
    InvalidMaterialState,
    NotCustodian,
    PayloadAlreadyRead,
)
from wanxiang_substrate.material.fixture import (
    INSTANCE,
    LETTER,
    RECIPIENT,
    build_package_fixture_commands,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.resolver import (
    ACTION_CREATE_CONTAINER,
    ACTION_CREATE_ITEM,
    ACTION_MOVE_INTO,
    ACTION_READ,
    ACTION_TRANSFER,
    register_material_resolvers,
)


def make_material_runtime(path: pathlib.Path) -> WorldRuntime:
    return make_world_runtime(path, extra_resolvers=register_material_resolvers)


def cmd(
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
        payload=dict(payload),
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_material_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    for command in build_package_fixture_commands(w.root_branch_id):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_transfer_requires_custodian(world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = world
    # Messenger holds the letter; writer is not the custodian.
    with pytest.raises(NotCustodian):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                1,
                ACTION_TRANSFER,
                {"item_id": LETTER.value, "from_custodian": "writer", "to_custodian": "recipient"},
                "cmd_bad",
            )
        )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            ACTION_TRANSFER,
            {"item_id": LETTER.value, "from_custodian": "messenger", "to_custodian": "recipient"},
            "cmd_ok",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert MaterialQuery(state).custodian(LETTER) == RECIPIENT


@pytest.mark.integration
def test_holding_sealed_letter_does_not_reveal_content(
    world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = world
    # Messenger holds the letter; payload stays sealed and unread: custody != knowledge.
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    info = MaterialQuery(state).payload(LETTER)
    assert info is not None and info.state == "sealed" and info.readers == ()
    # The writer (owner, not custodian) cannot read the sealed payload.
    with pytest.raises(NotCustodian):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                1,
                ACTION_READ,
                {"item_id": LETTER.value, "reader_id": "writer"},
                "cmd_writer_read",
            )
        )


@pytest.mark.integration
def test_recipient_reads_after_receiving(world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            ACTION_TRANSFER,
            {"item_id": LETTER.value, "from_custodian": "messenger", "to_custodian": "recipient"},
            "cmd_t",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_READ,
            {"item_id": LETTER.value, "reader_id": "recipient"},
            "cmd_read",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    info = MaterialQuery(state).payload(LETTER)
    assert info is not None and info.state == "read"
    assert EntityId("recipient") in info.readers
    with pytest.raises(PayloadAlreadyRead):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                3,
                ACTION_READ,
                {"item_id": LETTER.value, "reader_id": "recipient"},
                "cmd_read2",
            )
        )


@pytest.mark.integration
def test_container_full_and_cycle_rejected(world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            ACTION_CREATE_CONTAINER,
            {"container_id": "box", "capacity": 1, "accepts": "letter"},
            "cmd_box",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_MOVE_INTO,
            {"item_id": LETTER.value, "container_id": "box"},
            "cmd_in",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            3,
            ACTION_CREATE_ITEM,
            {"item_id": "note_2", "kind": "letter"},
            "cmd_note",
        )
    )
    with pytest.raises(ContainerFull):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                4,
                ACTION_MOVE_INTO,
                {"item_id": "note_2", "container_id": "box"},
                "cmd_full",
            )
        )

    # Nested containers: storage accepts containers; crate in storage, then
    # storage in crate is a containment cycle.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            4,
            ACTION_CREATE_CONTAINER,
            {"container_id": "storage", "capacity": 4, "accepts": "letter,container"},
            "cmd_storage",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            5,
            ACTION_CREATE_CONTAINER,
            {"container_id": "crate", "capacity": 4},
            "cmd_crate",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            6,
            ACTION_MOVE_INTO,
            {"item_id": "crate", "container_id": "storage"},
            "cmd_crate_in",
        )
    )
    with pytest.raises(ContainmentCycle):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                7,
                ACTION_MOVE_INTO,
                {"item_id": "storage", "container_id": "crate"},
                "cmd_cycle",
            )
        )


@pytest.mark.integration
def test_consume_and_damage_transitions(world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            ACTION_CREATE_ITEM,
            {"item_id": "apple", "kind": "food"},
            "cmd_apple",
        )
    )
    runtime.submit_command(
        cmd(w.root_branch_id, 2, "material.consume", {"item_id": "apple"}, "cmd_eat")
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert MaterialQuery(state).item(EntityId("apple")).state == "consumed"  # type: ignore[union-attr]
    with pytest.raises(InvalidMaterialState):
        runtime.submit_command(
            cmd(w.root_branch_id, 3, "material.damage", {"item_id": "apple"}, "cmd_bad")
        )


@pytest.mark.integration
def test_material_replay_and_branch(world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            ACTION_TRANSFER,
            {"item_id": LETTER.value, "from_custodian": "messenger", "to_custodian": "recipient"},
            "cmd_t",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_READ,
            {"item_id": LETTER.value, "reader_id": "recipient"},
            "cmd_read",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
    assert MaterialQuery(replayed).custodian(LETTER) == RECIPIENT

    # Branch: child commits a different custody without touching parent.
    parent_hash = state.semantic_hash()
    child = runtime.create_branch(w.instance_id, w.root_branch_id)
    child_state = runtime.current_state(w.instance_id, child.branch_id)
    assert child_state.semantic_hash() == parent_hash
    # child transfers letter back to messenger (base revision = parent head)
    parent_rev = state.revision.value
    runtime.submit_command(
        cmd(
            child.branch_id,
            parent_rev,
            ACTION_TRANSFER,
            {"item_id": LETTER.value, "from_custodian": "recipient", "to_custodian": "messenger"},
            "cmd_child",
        )
    )
    parent_after = runtime.current_state(w.instance_id, w.root_branch_id)
    assert parent_after.semantic_hash() == parent_hash
