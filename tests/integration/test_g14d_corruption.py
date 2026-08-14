"""G14D: event/snapshot/branch/history corruption adversarial qualification.

- Every corruption type is detected with a precise error or diagnostic.
- Snapshot corruption is rejected at restore and falls back to authoritative
  event replay (no silent semantic drift).
- A valid history remains replayable after a read-only diagnostic scan.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import replace
from typing import Any

import pytest
from scripts.history_diagnostics import diagnose_stream
from tests.conftest import make_world_runtime
from tests.helpers.replay_fixture import build_fixture_events
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import CorruptEventStream, IncompatibleVersion
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)


def _corrupt(**changes: Any) -> tuple[CommittedEvent, ...]:
    events = build_fixture_events()
    return (replace(events[0], **changes),) + events[1:]


def test_sequence_gap_is_detected() -> None:
    events = _corrupt(event_seq=EventSeq(99))
    with pytest.raises(CorruptEventStream):
        ReplayEngine(RULES, SCHEMA).replay(events)
    findings = diagnose_stream(events, rule_version=RULES, schema_version=SCHEMA)
    assert any(f["kind"] == "sequence_gap_or_reorder" for f in findings)


def test_instance_branch_mismatch_is_detected() -> None:
    events = _corrupt(branch_id=BranchId("br_foreign"))
    with pytest.raises(CorruptEventStream):
        ReplayEngine(RULES, SCHEMA).replay(events)
    findings = diagnose_stream(events, rule_version=RULES, schema_version=SCHEMA)
    assert any(f["kind"] == "instance_branch_mismatch" for f in findings)


def test_revision_jump_is_detected() -> None:
    events = _corrupt(revision=BranchRevision(99))
    with pytest.raises(CorruptEventStream):
        ReplayEngine(RULES, SCHEMA).replay(events)
    findings = diagnose_stream(events, rule_version=RULES, schema_version=SCHEMA)
    assert any(f["kind"] == "revision_jump" for f in findings)


def test_unsupported_versions_are_detected() -> None:
    events = _corrupt(schema_version=SchemaVersion(99))
    with pytest.raises(IncompatibleVersion):
        ReplayEngine(RULES, SCHEMA).replay(events)
    findings = diagnose_stream(events, rule_version=RULES, schema_version=SCHEMA)
    assert any(f["kind"] == "unsupported_schema_version" for f in findings)

    events = _corrupt(rule_version=RuntimeVersion(99))
    with pytest.raises(IncompatibleVersion):
        ReplayEngine(RULES, SCHEMA).replay(events)
    findings = diagnose_stream(events, rule_version=RULES, schema_version=SCHEMA)
    assert any(f["kind"] == "unsupported_rule_version" for f in findings)


def test_valid_history_replayable_after_readonly_diagnostic() -> None:
    events = build_fixture_events()
    expected = ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash()
    assert diagnose_stream(events, rule_version=RULES, schema_version=SCHEMA) == []
    # Diagnostic is read-only: history still replays to the same hash.
    assert ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash() == expected


def test_snapshot_corruption_is_rejected_not_silently_used(persist_db_path: pathlib.Path) -> None:
    from sqlalchemy.orm import sessionmaker
    from wanxiang_persistence.database import create_engine_for
    from wanxiang_persistence.models import SnapshotRecord

    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    for i in range(3):
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"c_g14d_{i}"),
                instance_id=iid,
                branch_id=branch,
                expected_revision=BranchRevision(i),
                action_type="create_entity",
                payload={"entity_id": f"e{i}", "count": i},
                world_time=WorldTime(i + 1),
            )
        )
    runtime.create_checkpoint(iid, branch)

    engine = create_engine_for(f"sqlite:///{persist_db_path.as_posix()}")
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    session = factory()
    rec = session.query(SnapshotRecord).first()
    assert rec is not None
    state = json.loads(rec.state_json)
    state["revision"] = 0  # corrupt the snapshot baseline
    rec.state_json = json.dumps(state)
    session.commit()
    engine.dispose()

    restarted = make_world_runtime(persist_db_path)
    restored = restarted.restore_and_replay(iid, branch)
    truth = restarted.current_state(iid, branch)
    assert restored.used_snapshot is False
    assert restored.snapshot_rejected is True
    assert restored.state.semantic_hash() == truth.semantic_hash()


def test_snapshot_corruption_recovery_without_mutation(persist_db_path: pathlib.Path) -> None:
    """Recovery does not require manual DB repair; a fresh restore uses events."""
    from sqlalchemy.orm import sessionmaker
    from wanxiang_persistence.database import create_engine_for
    from wanxiang_persistence.models import SnapshotRecord

    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    for i in range(2):
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"c_g14d_r{i}"),
                instance_id=iid,
                branch_id=branch,
                expected_revision=BranchRevision(i),
                action_type="create_entity",
                payload={"entity_id": f"e{i}", "count": i},
                world_time=WorldTime(i + 1),
            )
        )
    runtime.create_checkpoint(iid, branch)

    engine = create_engine_for(f"sqlite:///{persist_db_path.as_posix()}")
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    session = factory()
    rec = session.query(SnapshotRecord).first()
    assert rec is not None
    rec.state_json = json.dumps({"revision": 0, "entities": {}, "relations": {}})
    session.commit()
    engine.dispose()

    restarted = make_world_runtime(persist_db_path)
    restored = restarted.restore_and_replay(iid, branch)
    # An unreadable snapshot never blocks recovery: events are authoritative.
    assert restored.used_snapshot is False
    assert restored.state.revision.value == 2
