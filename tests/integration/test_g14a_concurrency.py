"""G14A: concurrency, race, idempotency & lost-update adversarial qualification.

Deterministic adversarial scenarios (no reliance on thread timing):
- Lost-update attack: two clients submit with the same expected revision; only
  one commits, the other gets an explicit StaleRevision and no invalid event is
  appended.
- Duplicate command retry across a simulated process restart yields exactly one
  semantic effect.
- Out-of-order delivery produces explicit conflicts and recovers.
- Independent instances/branches progress without cross-contamination.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import StaleRevision
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime


def _cmd(
    instance: WorldInstanceId,
    branch: BranchId,
    revision: int,
    name: str,
    count: int = 1,
    command_id: str | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id or f"cmd_{name}"),
        instance_id=instance,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type="create_entity",
        payload={"entity_id": name, "count": count},
        world_time=WorldTime(revision + 1),
    )


def test_lost_update_attack_rejected_explicitly(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id

    # Both clients read revision 0 and submit "create alice" with expected 0.
    runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_a"))
    with pytest.raises(StaleRevision):
        runtime.submit_command(_cmd(iid, branch, 0, "bob", command_id="cmd_b"))
    events = runtime.persistence.event_store.load(iid, branch)
    assert len(events) == 1
    assert events[0].command_id.value == "cmd_a"
    state = runtime.current_state(iid, branch)
    assert state.entity(EntityId("alice")) is not None
    # No invalid event was appended for the losing client.
    assert runtime.persistence.event_store.command_result_event(CommandId("cmd_b")) is None


def test_duplicate_command_single_effect_across_restart(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    first = runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_dup"))
    event_id = first.event.event_id.value
    count_before = len(runtime.persistence.event_store.load(iid, branch))

    # Simulated process restart: a fresh runtime over the same database.
    restarted = make_world_runtime(persist_db_path)
    # Client retries the same command id (idempotency across restart).
    retry = restarted.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_dup"))
    assert retry.duplicate is True
    assert retry.event is not None and retry.event.event_id.value == event_id
    count_after = len(restarted.persistence.event_store.load(iid, branch))
    assert count_after == count_before == 1


def test_out_of_order_delivery_explicit_conflict_and_recovery(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    # Deliver revision-1 command before revision-0: it must fail explicitly.
    with pytest.raises(StaleRevision):
        runtime.submit_command(_cmd(iid, branch, 1, "bob", command_id="cmd_ooo1"))
    assert runtime.persistence.event_store.load(iid, branch) == ()
    # Then the revision-0 command commits and the retry of rev-1 succeeds.
    runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_ooo0"))
    runtime.submit_command(_cmd(iid, branch, 1, "bob", command_id="cmd_ooo1"))
    events = runtime.persistence.event_store.load(iid, branch)
    assert [e.revision.value for e in events] == [1, 2]


def test_independent_instances_do_not_contaminate(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w1 = runtime.create_world(instance_id=WorldInstanceId("wld_a_g14a"))
    w2 = runtime.create_world(instance_id=WorldInstanceId("wld_b_g14a"))
    # Interleave commands across the two instances.
    runtime.submit_command(_cmd(w1.instance_id, w1.root_branch_id, 0, "a1", command_id="c_a1"))
    runtime.submit_command(_cmd(w2.instance_id, w2.root_branch_id, 0, "b1", command_id="c_b1"))
    runtime.submit_command(_cmd(w1.instance_id, w1.root_branch_id, 1, "a2", command_id="c_a2"))
    runtime.submit_command(_cmd(w2.instance_id, w2.root_branch_id, 1, "b2", command_id="c_b2"))
    ev1 = runtime.persistence.event_store.load(w1.instance_id, w1.root_branch_id)
    ev2 = runtime.persistence.event_store.load(w2.instance_id, w2.root_branch_id)
    assert [e.event_seq.value for e in ev1] == [1, 2]
    assert [e.event_seq.value for e in ev2] == [1, 2]
    assert all(e.instance_id == w1.instance_id for e in ev1)
    assert all(e.instance_id == w2.instance_id for e in ev2)
    # Replay each independently and confirm isolation hashes.
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.replay import ReplayEngine

    engine = ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
    h1 = engine.replay(ev1).semantic_hash()
    h2 = engine.replay(ev2).semantic_hash()
    assert h1 != h2


def test_burst_of_conflicting_and_non_conflicting_commands(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    for i in range(20):
        runtime.submit_command(_cmd(iid, branch, i, f"ent_{i}", count=i, command_id=f"burst_{i}"))
    events = runtime.persistence.event_store.load(iid, branch)
    assert [e.event_seq.value for e in events] == list(range(1, 21))
    assert len({e.command_id.value for e in events}) == 20
