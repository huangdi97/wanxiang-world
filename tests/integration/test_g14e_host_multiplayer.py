"""G14E: world host, multiplayer, reconnect, ordering & backpressure chaos.

- Reconnect resyncs from server history (client cache never authoritative).
- Many clients through the command queue preserve total order + idempotency.
- Slow clients cannot block the canonical world: queue backpressure is bounded
  and observable (QueueFull), and the world still advances.
- Embodiment lease ownership remains unique; disconnect recovery works.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import StaleRevision
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.queue.errors import DuplicateQueuedCommand, QueueFull
from wanxiang_substrate.queue.queue import CommandQueue


def _cmd(
    instance: WorldInstanceId,
    branch: BranchId,
    revision: int,
    name: str,
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=instance,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type="create_entity",
        payload={"entity_id": name, "count": 1},
        world_time=WorldTime(revision + 1),
    )


def test_reconnect_resyncs_from_server_history(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(_cmd(iid, branch, 0, "alice", "c_a"))
    runtime.submit_command(_cmd(iid, branch, 1, "bob", "c_b"))

    # A disconnected client reconnects with a stale revision: rejected, and its
    # cache can never become authoritative.
    with pytest.raises(StaleRevision):
        runtime.submit_command(_cmd(iid, branch, 1, "eve", "c_stale"))
    # It resyncs from the server's authoritative history...
    state = runtime.current_state(iid, branch)
    assert state.revision.value == 2
    # ...and only then submits with the correct revision.
    runtime.submit_command(_cmd(iid, branch, state.revision.value, "eve", "c_eve"))
    events = runtime.persistence.event_store.load(iid, branch)
    assert [e.revision.value for e in events] == [1, 2, 3]
    assert len(runtime.persistence.event_store.load(iid, branch)) == 3


def test_many_clients_queue_preserves_order_and_idempotency(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    queue = CommandQueue(capacity=128, runtime=runtime)
    envelopes = tuple(_cmd(iid, branch, i, f"client_{i}", f"multi_{i}") for i in range(30))
    queue.enqueue_all(envelopes)
    results = queue.drain()
    assert len(results) == 30
    events = runtime.persistence.event_store.load(iid, branch)
    assert [e.event_seq.value for e in events] == list(range(1, 31))
    assert len({e.command_id.value for e in events}) == 30
    # Duplicate command id through the queue is rejected (idempotent dedup).
    with pytest.raises(DuplicateQueuedCommand):
        queue.enqueue(_cmd(iid, branch, 30, "client_0", "multi_0"))


def test_slow_client_backpressure_is_bounded_and_world_advances(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    queue = CommandQueue(capacity=3, runtime=runtime)
    queue.enqueue(_cmd(iid, branch, 0, "n0", "q0"))
    queue.enqueue(_cmd(iid, branch, 1, "n1", "q1"))
    queue.enqueue(_cmd(iid, branch, 2, "n2", "q2"))
    # A slow consumer (un-drained queue) cannot accept more: backpressure is
    # observable and explicit, not an unbounded queue.
    with pytest.raises(QueueFull):
        queue.enqueue(_cmd(iid, branch, 3, "n3", "q3"))
    assert queue.pending_count() == 3
    # The canonical world still advances independently of the slow client:
    # a direct command at the current revision commits even while the queue is
    # full (backpressure applies to the client queue, never to the world).
    runtime.submit_command(_cmd(iid, branch, 0, "direct", "direct_1"))
    assert runtime.current_state(iid, branch).revision.value == 1
    # Draining later rejects the now-stale queued command explicitly (conflict),
    # never silently misapplying it.
    results = queue.drain()
    assert len(results) == 3
    assert any(r.status == "conflict" for r in results)


def test_lease_ownership_remains_unique_and_recoverable() -> None:
    from wanxiang_substrate.session.errors import LeaseConflict
    from wanxiang_substrate.session.model import Session
    from wanxiang_substrate.session.service import LeaseService

    service = LeaseService()
    session = Session(
        session_id="s1",
        controller="c1",
        instance_id=WorldInstanceId("w_lease"),
        mode="embody",
        created_seq=1,
    )
    lease = service.acquire(session, "alice", "lease_1", acquired_seq=1, expires_seq=100)
    assert service.primary_controller("alice") == "s1"
    assert lease.active
    # A second controller for the same actor is rejected: ownership is unique.
    other = Session(
        session_id="s2",
        controller="c2",
        instance_id=WorldInstanceId("w_lease"),
        mode="embody",
        created_seq=2,
    )
    with pytest.raises(LeaseConflict):
        service.acquire(other, "alice", "lease_2", acquired_seq=2, expires_seq=200)
    # Disconnect: expire the lease, then a new session can acquire.
    service.expire("lease_1")
    service.acquire(other, "alice", "lease_2", acquired_seq=3, expires_seq=200)
    assert service.primary_controller("alice") == "s2"
