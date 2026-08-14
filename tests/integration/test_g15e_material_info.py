"""G15E: material custody, information propagation & social continuity.

- An object never exists in two exclusive containers simultaneously.
- An unread actor cannot act on hidden message content (custody != knowledge);
  knowledge requires a causal path (receiving custody, then reading).
- Branch outcomes diverge causally and replay to stable distinct hashes.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.material.errors import NotCustodian, PayloadAlreadyRead
from wanxiang_substrate.material.fixture import (
    INSTANCE,
    LETTER,
    MESSENGER,
    RECIPIENT,
    WRITER,
    build_package_fixture_commands,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.resolver import (
    ACTION_CREATE_CONTAINER,
    ACTION_MOVE_INTO,
    ACTION_READ,
    ACTION_TRANSFER,
    register_material_resolvers,
)


def _cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: dict[str, FieldValue],
    command_id: str,
    instance: WorldInstanceId = INSTANCE,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=instance,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


def _material_runtime(path: pathlib.Path) -> WorldRuntime:
    return make_world_runtime(path, extra_resolvers=register_material_resolvers)


def _instantiate(runtime: WorldRuntime, w: CreateWorldResult) -> int:
    for command in build_package_fixture_commands(w.root_branch_id):
        runtime.submit_command(command)
    return runtime.current_state(w.instance_id, w.root_branch_id).revision.value


def test_object_never_in_two_exclusive_containers(persist_db_path: pathlib.Path) -> None:
    runtime = _material_runtime(persist_db_path)
    w = runtime.create_world(instance_id=INSTANCE)
    rev = _instantiate(runtime, w)
    branch = w.root_branch_id
    runtime.submit_command(
        _cmd(
            branch,
            rev,
            ACTION_CREATE_CONTAINER,
            {"container_id": "box_a", "capacity": 5, "accepts": "letter"},
            "c_a",
        )
    )
    rev += 1
    runtime.submit_command(
        _cmd(
            branch,
            rev,
            ACTION_CREATE_CONTAINER,
            {"container_id": "box_b", "capacity": 5, "accepts": "letter"},
            "c_b",
        )
    )
    rev += 1
    runtime.submit_command(
        _cmd(
            branch, rev, ACTION_MOVE_INTO, {"item_id": LETTER.value, "container_id": "box_a"}, "m_a"
        )
    )
    rev += 1
    runtime.submit_command(
        _cmd(
            branch, rev, ACTION_MOVE_INTO, {"item_id": LETTER.value, "container_id": "box_b"}, "m_b"
        )
    )
    rev += 1
    from wanxiang_domain.ids import EntityId

    state = runtime.current_state(INSTANCE, branch)
    query = MaterialQuery(state)
    assert query.container_of(LETTER) == EntityId("box_b")
    assert "letter_1" not in [e.value for e in query.contents(EntityId("box_a"))]
    assert LETTER.value in [e.value for e in query.contents(EntityId("box_b"))]


def test_unread_actor_cannot_act_on_hidden_payload(persist_db_path: pathlib.Path) -> None:
    runtime = _material_runtime(persist_db_path)
    w = runtime.create_world(instance_id=INSTANCE)
    rev = _instantiate(runtime, w)
    branch = w.root_branch_id
    state = runtime.current_state(INSTANCE, branch)
    info = MaterialQuery(state).payload(LETTER)
    assert info is not None and info.state == "sealed" and info.readers == ()
    # The messenger holds custody but the payload is sealed; the owner (writer)
    # cannot read while not the custodian (custody != knowledge).
    with pytest.raises(NotCustodian):
        runtime.submit_command(
            _cmd(
                branch,
                rev,
                ACTION_READ,
                {"item_id": LETTER.value, "reader_id": WRITER.value},
                "bad_read",
            )
        )
    # Knowledge requires a causal path: receive custody, then read.
    runtime.submit_command(
        _cmd(
            branch,
            rev,
            ACTION_TRANSFER,
            {
                "item_id": LETTER.value,
                "from_custodian": MESSENGER.value,
                "to_custodian": RECIPIENT.value,
            },
            "xfer",
        )
    )
    rev += 1
    runtime.submit_command(
        _cmd(
            branch,
            rev,
            ACTION_READ,
            {"item_id": LETTER.value, "reader_id": RECIPIENT.value},
            "read",
        )
    )
    rev += 1
    state = runtime.current_state(INSTANCE, branch)
    info = MaterialQuery(state).payload(LETTER)
    assert info is not None and info.state == "read"
    assert RECIPIENT in info.readers
    # Reading twice is rejected (no silent re-propagation).
    with pytest.raises(PayloadAlreadyRead):
        runtime.submit_command(
            _cmd(
                branch,
                rev,
                ACTION_READ,
                {"item_id": LETTER.value, "reader_id": RECIPIENT.value},
                "read2",
            )
        )


def test_branch_outcomes_diverge_causally_and_replay(persist_db_path: pathlib.Path) -> None:
    runtime = _material_runtime(persist_db_path)
    w = runtime.create_world(instance_id=INSTANCE)
    rev = _instantiate(runtime, w)
    branch = w.root_branch_id
    # Fork after instantiation.
    child = runtime.create_branch(INSTANCE, branch)
    # Child: deliver the letter to the recipient.
    runtime.submit_command(
        _cmd(
            child.branch_id,
            rev,
            ACTION_TRANSFER,
            {
                "item_id": LETTER.value,
                "from_custodian": MESSENGER.value,
                "to_custodian": RECIPIENT.value,
            },
            "xfer_child",
        )
    )
    # Parent: no delivery.
    parent_state = runtime.current_state(INSTANCE, branch)
    child_state = runtime.current_state(INSTANCE, child.branch_id)
    assert MaterialQuery(parent_state).custodian(LETTER) == MESSENGER
    assert MaterialQuery(child_state).custodian(LETTER) == RECIPIENT
    assert parent_state.semantic_hash() != child_state.semantic_hash()
    # Both branches replay to stable, distinct hashes.
    engine = ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
    parent_replay = engine.replay(runtime.persistence.event_store.load(INSTANCE, branch))
    child_events = runtime.persistence.event_store.load(INSTANCE, child.branch_id)
    child_replay = engine.replay(child_events, baseline=parent_state, start_seq=1)
    assert parent_replay.semantic_hash() == parent_state.semantic_hash()
    assert child_replay.semantic_hash() == child_state.semantic_hash()
    assert parent_replay.semantic_hash() != child_replay.semantic_hash()
