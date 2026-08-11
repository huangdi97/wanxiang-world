"""GOAL_01E: durable SQLite persistence integration."""

from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA, build_fixture_events
from wanxiang_domain.errors import Conflict, DuplicateCommandConflict
from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata, BranchRevision, EventSeq
from wanxiang_domain.ids import (
    CommandId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_persistence.audit_repository import AuditTraceRepository
from wanxiang_persistence.branch_repository import SqlAlchemyBranchRepository
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_persistence.instance_repository import WorldInstanceRepository
from wanxiang_persistence.models import EventRecord
from wanxiang_persistence.snapshot_store import SqlAlchemySnapshotStore
from wanxiang_runtime.audit import AuditRecord
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.snapshot import create_snapshot_metadata


@pytest.mark.integration
def test_durable_commit_and_reload_replay(
    session_factory: sessionmaker[Session],
) -> None:
    events = build_fixture_events()
    store = SqlAlchemyEventStore(session_factory)
    for event in events:
        store.append(event)
    assert store.last_event_seq(INSTANCE, BRANCH) == EventSeq(5)

    # New store/session over the same file proves persistence across recreation.
    store2 = SqlAlchemyEventStore(session_factory)
    loaded = store2.load(INSTANCE, BRANCH)
    assert len(loaded) == 5
    final = ReplayEngine(RULES, SCHEMA).replay(loaded)
    assert (
        final.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )
    store2.integrity_check(INSTANCE, BRANCH)


@pytest.mark.integration
def test_duplicate_command_rejected_at_db_level(
    session_factory: sessionmaker[Session],
) -> None:
    store = SqlAlchemyEventStore(session_factory)
    events = build_fixture_events()
    store.append(events[0])
    with pytest.raises(DuplicateCommandConflict):
        store.append(events[0])
    assert store.last_event_seq(INSTANCE, BRANCH) == EventSeq(1)


@pytest.mark.integration
def test_out_of_order_append_rejected(
    session_factory: sessionmaker[Session],
) -> None:
    from wanxiang_domain.event import CommittedEvent
    from wanxiang_domain.hierarchy import EventSeq

    store = SqlAlchemyEventStore(session_factory)
    events = build_fixture_events()
    store.append(events[0])
    wrong = CommittedEvent(
        event_id=events[1].event_id,
        instance_id=events[1].instance_id,
        branch_id=events[1].branch_id,
        event_seq=EventSeq(9),
        revision=events[1].revision,
        schema_version=events[1].schema_version,
        command_id=events[1].command_id,
        delta=events[1].delta,
        world_time=events[1].world_time,
        rule_version=events[1].rule_version,
    )
    with pytest.raises(Conflict):
        store.append(wrong)
    assert store.load(INSTANCE, BRANCH) == (events[0],)


@pytest.mark.integration
def test_transaction_failure_leaves_no_partial_row(
    session_factory: sessionmaker[Session],
) -> None:
    store = SqlAlchemyEventStore(session_factory)
    events = build_fixture_events()
    store.append(events[0])
    with pytest.raises(DuplicateCommandConflict):
        store.append(events[0])
    with session_factory() as session:
        count = len(session.scalars(select(EventRecord)).all())
    assert count == 1


@pytest.mark.integration
def test_snapshot_save_and_load(
    session_factory: sessionmaker[Session],
) -> None:
    store = SqlAlchemyEventStore(session_factory)
    events = build_fixture_events()
    for event in events:
        store.append(event)
    final = ReplayEngine(RULES, SCHEMA).replay(store.load(INSTANCE, BRANCH))
    snapshot_store = SqlAlchemySnapshotStore(session_factory)
    metadata = create_snapshot_metadata(final, EventSeq(5))
    snapshot_store.save(metadata, final)
    stored = snapshot_store.load(INSTANCE, BRANCH, BranchRevision(5))
    assert stored is not None
    assert stored.state.semantic_hash() == final.semantic_hash()
    latest = snapshot_store.latest(INSTANCE, BRANCH)
    assert latest is not None and latest.metadata.revision == BranchRevision(5)


@pytest.mark.integration
def test_branch_and_instance_repositories(
    session_factory: sessionmaker[Session],
) -> None:
    instance_repo = WorldInstanceRepository(session_factory)
    instance_repo.create(INSTANCE, SCHEMA, RULES, WorldTime(0))
    schema, rule, created = instance_repo.get(INSTANCE)
    assert schema == SCHEMA and rule == RULES and created == WorldTime(0)

    branch_repo = SqlAlchemyBranchRepository(session_factory)
    metadata = BranchMetadata(
        branch_id=BRANCH,
        instance_id=INSTANCE,
        ancestry=BranchAncestry(),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    branch_repo.save(metadata)
    assert branch_repo.get(BRANCH) == metadata
    assert branch_repo.list(INSTANCE) == (metadata,)


@pytest.mark.integration
def test_audit_trace_recorded(
    session_factory: sessionmaker[Session],
) -> None:
    from wanxiang_domain.ids import EventId, TraceId

    audit = AuditRecord(
        trace_id=TraceId("trace_1"),
        command_id=CommandId("cmd_1"),
        event_id=EventId("evt_1"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(1),
        rule_version=RULES,
        world_time=WorldTime(1),
    )
    AuditTraceRepository(session_factory).record(audit)
