"""G16C: background execution, work queue & scheduler reliability.

Uses the in-process CommandQueue (no Redis/Celery without evidence) with a
command_id idempotency key. Verifies:
- at-least-once delivery cannot duplicate semantic effects;
- failed jobs are diagnosable and retryable;
- queue pressure cannot corrupt the world.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.queue.errors import QueueFull
from wanxiang_substrate.queue.queue import CommandQueue


def _job(
    instance: WorldInstanceId,
    branch: BranchId,
    revision: int,
    action: str,
    payload: dict[str, FieldValue],
    command_id: str,
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


def test_at_least_once_delivery_no_duplicate_effects(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    queue = CommandQueue(capacity=8, runtime=runtime)
    job = _job(iid, branch, 0, "create_entity", {"entity_id": "alice", "count": 1}, "job_deliver")
    queue.enqueue(job)
    queue.drain()
    assert len(runtime.persistence.event_store.load(iid, branch)) == 1
    # Redelivery (at-least-once) of the same job id is rejected at intake, so it
    # can never duplicate semantic effects.
    from wanxiang_substrate.queue.errors import DuplicateQueuedCommand

    with pytest.raises(DuplicateQueuedCommand):
        queue.enqueue(job)
    # The canonical stream still has exactly one event for this job.
    events = runtime.persistence.event_store.load(iid, branch)
    assert len(events) == 1
    assert ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events).revision.value == 1


def test_failed_job_diagnosable_and_retryable(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    queue = CommandQueue(capacity=8, runtime=runtime)
    bad = _job(iid, branch, 0, "no_such_action", {}, "job_bad")
    queue.enqueue(bad)
    results = queue.drain()
    assert len(results) == 1
    assert results[0].status in ("rejected", "conflict")
    assert results[0].message  # diagnosable
    # Retry with a corrected job (new idempotency key) succeeds.
    ok = _job(iid, branch, 0, "create_entity", {"entity_id": "alice", "count": 1}, "job_ok")
    queue.enqueue(ok)
    queue.drain()
    assert len(runtime.persistence.event_store.load(iid, branch)) == 1


def test_queue_pressure_cannot_corrupt_world(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    queue = CommandQueue(capacity=2, runtime=runtime)
    queue.enqueue(_job(iid, branch, 0, "create_entity", {"entity_id": "a", "count": 1}, "p0"))
    queue.enqueue(_job(iid, branch, 1, "create_entity", {"entity_id": "b", "count": 1}, "p1"))
    with pytest.raises(QueueFull):
        queue.enqueue(_job(iid, branch, 2, "create_entity", {"entity_id": "c", "count": 1}, "p2"))
    # The world still advances directly; then the queued jobs drain with valid
    # revisions (conflicts are reported, never silent corruption).
    runtime.submit_command(
        _job(iid, branch, 0, "create_entity", {"entity_id": "x", "count": 1}, "direct")
    )
    results = queue.drain()
    assert len(results) == 2
    events = runtime.persistence.event_store.load(iid, branch)
    assert [e.event_seq.value for e in events] == list(range(1, len(events) + 1))
    ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
