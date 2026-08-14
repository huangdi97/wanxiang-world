"""G14C: database/storage/network/dependency fault injection.

A test-only FaultyEventStore wraps the durable store and injects
append/load failures (disconnect/timeout/disk-full-like). Verifies:
- persistence failure never produces a success for an uncommitted command;
- retry storms are bounded and each retry is idempotent;
- service recovers without manual DB mutation;
- API returns a structured error (5xx), never a fake success, during faults.
"""

from __future__ import annotations

import pathlib
from typing import Any

import pytest
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import PersistenceError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.ports import EventStore


class FaultyEventStore:
    """EventStore-compatible wrapper that injects deterministic faults."""

    def __init__(self, inner: EventStore) -> None:
        self._inner = inner
        self.fail_append = False
        self.fail_load = False
        self.append_attempts = 0
        self.load_attempts = 0

    def append(self, event: CommittedEvent) -> None:
        self.append_attempts += 1
        if self.fail_append:
            raise PersistenceError("simulated persistence outage")
        self._inner.append(event)

    def load(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        from_seq: int | None = None,
        to_seq: int | None = None,
    ) -> tuple[CommittedEvent, ...]:
        self.load_attempts += 1
        if self.fail_load:
            raise PersistenceError("simulated storage unavailability")
        return self._inner.load(instance_id, branch_id, from_seq=from_seq, to_seq=to_seq)

    def last_event_seq(self, instance_id: WorldInstanceId, branch_id: BranchId) -> EventSeq:
        return self._inner.last_event_seq(instance_id, branch_id)

    def command_result_event(self, command_id: CommandId) -> CommittedEvent | None:
        return self._inner.command_result_event(command_id)

    def has_command(self, command_id: CommandId) -> bool:
        return self._inner.has_command(command_id)

    def integrity_check(self, instance_id: WorldInstanceId, branch_id: BranchId) -> None:
        self._inner.integrity_check(instance_id, branch_id)


def _cmd(
    instance: WorldInstanceId, branch: BranchId, revision: int, name: str, command_id: str
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


def _wrap(runtime: Any) -> FaultyEventStore:
    faulty = FaultyEventStore(runtime.persistence.event_store)
    runtime.persistence.event_store = faulty
    return faulty


def test_append_failure_never_reports_success(persist_db_path: pathlib.Path) -> None:
    from tests.conftest import make_world_runtime

    runtime = make_world_runtime(persist_db_path)
    faulty = _wrap(runtime)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id

    faulty.fail_append = True
    with pytest.raises(PersistenceError):
        runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_f1"))
    assert runtime.persistence.event_store.load(iid, branch) == ()

    faulty.fail_append = False
    result = runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_f1"))
    assert result.duplicate is False
    assert len(runtime.persistence.event_store.load(iid, branch)) == 1


def test_load_failure_surfaces_error_and_recovers(persist_db_path: pathlib.Path) -> None:
    from tests.conftest import make_world_runtime

    runtime = make_world_runtime(persist_db_path)
    faulty = _wrap(runtime)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_l1"))

    runtime.invalidate_state_cache()  # force a real load from the store
    faulty.fail_load = True
    with pytest.raises(PersistenceError):
        runtime.current_state(iid, branch)
    faulty.fail_load = False
    # Recovery without manual DB mutation.
    assert runtime.current_state(iid, branch).revision.value == 1


def test_retry_storm_is_bounded_and_idempotent(persist_db_path: pathlib.Path) -> None:
    from tests.conftest import make_world_runtime

    runtime = make_world_runtime(persist_db_path)
    faulty = _wrap(runtime)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id

    faulty.fail_append = True
    attempts = 5
    for _ in range(attempts):
        with pytest.raises(PersistenceError):
            runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_storm"))
    assert faulty.append_attempts == attempts
    assert runtime.persistence.event_store.load(iid, branch) == ()

    faulty.fail_append = False
    runtime.submit_command(_cmd(iid, branch, 0, "alice", command_id="cmd_storm"))
    # The retry storm was bounded to the attempt count and produced one effect.
    assert len(runtime.persistence.event_store.load(iid, branch)) == 1


def test_api_returns_error_not_success_during_fault(persist_db_path: pathlib.Path) -> None:
    from fastapi.testclient import TestClient
    from tests.conftest import upgrade_db
    from wanxiang_api.app import build_runtime, create_app

    upgrade_db(persist_db_path)
    runtime = build_runtime(f"sqlite:///{persist_db_path.as_posix()}")
    faulty = _wrap(runtime)
    app = create_app(runtime)
    client: Any = TestClient(app)
    with client:
        world: dict[str, Any] = client.post("/worlds", json={"instance_id": "wld_fault"}).json()
        instance: str = world["instance_id"]
        branch: str = world["root_branch_id"]
        faulty.fail_append = True
        resp: Any = client.post(
            f"/worlds/{instance}/actions",
            json={
                "branch_id": branch,
                "expected_revision": 0,
                "action_type": "create_entity",
                "payload": {"entity_id": "alice", "count": 1},
            },
        )
        assert resp.status_code == 500
        assert resp.json()["code"] == "persistence_error"
        faulty.fail_append = False
        ok: Any = client.post(
            f"/worlds/{instance}/actions",
            json={
                "branch_id": branch,
                "expected_revision": 0,
                "action_type": "create_entity",
                "payload": {"entity_id": "alice", "count": 1},
            },
        )
        assert ok.status_code == 200
        # Health endpoint still answers (operator-visible), while the write failed closed.
        assert client.get("/healthz").json() == {"status": "ok"}
