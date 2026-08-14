"""G29D: State/Event/Audit derivation invariants.

Committed history is the only authority. CurrentState is a materialized
projection (rebuildable from events after dropping derived state), audit rows
reference the committed event instead of duplicating its payload, and the
replay hash is stable regardless of derived state or audit retention.
"""

from __future__ import annotations

import pytest
from tests.conftest import (
    cleanup_db_file,
    fresh_db_path,
    make_sqlite_engine_and_factory,
    make_world_runtime,
)
from wanxiang_application.world_runtime import SubmitCommandResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

INSTANCE = WorldInstanceId("wld_g29d")


def _submit(
    runtime: WorldRuntime,
    instance_id: WorldInstanceId,
    branch: BranchId,
    action: str,
    payload: dict[str, FieldValue],
    revision: int,
    *,
    actor_id: str | None = None,
) -> SubmitCommandResult:
    from wanxiang_domain.ids import ActorId

    return runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(f"cmd_g29d_{action}_{revision}"),
            instance_id=instance_id,
            branch_id=branch,
            expected_revision=BranchRevision(revision),
            action_type=action,
            payload=payload,
            world_time=WorldTime(revision + 1),
            actor_id=ActorId(actor_id) if actor_id else None,
        )
    )


@pytest.mark.integration
def test_current_state_is_rebuildable_materialized_projection() -> None:
    path = fresh_db_path()
    try:
        runtime = make_world_runtime(path)
        created = runtime.create_world()
        instance_id = created.instance_id
        branch = created.root_branch_id
        _submit(
            runtime, instance_id, branch, "create_entity", {"entity_id": "alice", "count": 10}, 0
        )
        _submit(runtime, instance_id, branch, "create_entity", {"entity_id": "bob", "count": 0}, 1)
        _submit(
            runtime,
            instance_id,
            branch,
            "transfer_resource",
            {"source_id": "alice", "target_id": "bob", "amount": 3},
            2,
        )
        expected = runtime.current_state(instance_id, branch).semantic_hash()

        # Materialize derived state (snapshot) then delete ALL of it: snapshot
        # rows + the in-memory read cache. History must rebuild the same state.
        runtime.create_checkpoint(instance_id, branch)
        _engine, factory = make_sqlite_engine_and_factory(path)
        from wanxiang_persistence.database import session_scope
        from wanxiang_persistence.models import SnapshotRecord

        with session_scope(factory) as session:
            deleted = session.query(SnapshotRecord).delete()
        assert deleted >= 1, "expected at least one snapshot row to drop"
        runtime.invalidate_state_cache()

        rebuilt = runtime.current_state(instance_id, branch)
        assert rebuilt.semantic_hash() == expected
        restored = runtime.restore_and_replay(instance_id, branch)
        assert restored.used_snapshot is False
        assert restored.state.semantic_hash() == expected

        # Replay hash invariant: committed history alone reproduces the state.
        events = runtime.persistence.event_store.load(instance_id, branch)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        assert replayed.semantic_hash() == expected
    finally:
        cleanup_db_file(path)


@pytest.mark.integration
def test_audit_rows_reference_events_and_are_not_authoritative() -> None:
    path = fresh_db_path()
    try:
        runtime = make_world_runtime(path)
        created = runtime.create_world()
        instance_id = created.instance_id
        branch = created.root_branch_id
        result = _submit(
            runtime,
            instance_id,
            branch,
            "create_entity",
            {"entity_id": "alice", "count": 10},
            0,
            actor_id="lin_daiyu",
        )
        event = result.event
        assert result.audit is not None

        _engine, factory = make_sqlite_engine_and_factory(path)
        from wanxiang_persistence.database import session_scope
        from wanxiang_persistence.models import AuditTraceRecord

        with session_scope(factory) as session:
            rows = list(session.query(AuditTraceRecord).all())
        assert len(rows) == 1
        row = rows[0]
        # Audit is a reference view: it points at the committed event and carries
        # no duplicate delta payload.
        assert row.event_id == event.event_id.value
        assert row.trace_id == result.audit.trace_id.value
        assert row.command_id == event.command_id.value
        assert row.actor_id == "lin_daiyu"
        assert not hasattr(row, "delta_json")

        # Clearing the audit view never changes canonical replay.
        with session_scope(factory) as session:
            session.query(AuditTraceRecord).delete()
        events = runtime.persistence.event_store.load(instance_id, branch)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        assert (
            replayed.semantic_hash() == runtime.current_state(instance_id, branch).semantic_hash()
        )
    finally:
        cleanup_db_file(path)
