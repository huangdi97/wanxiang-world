"""GOAL_01D: snapshot store round trips and rebuild-from-snapshot."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA, build_fixture_events
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.snapshot import InMemorySnapshotStore, create_snapshot_metadata


@pytest.mark.unit
def test_snapshot_round_trip_preserves_hash() -> None:
    events = build_fixture_events()
    engine = ReplayEngine(RULES, SCHEMA)
    final = engine.replay(events)
    store = InMemorySnapshotStore()
    metadata = create_snapshot_metadata(final, EventSeq(5))
    store.save(metadata, final)
    stored = store.load(INSTANCE, BRANCH, BranchRevision(5))
    assert stored is not None
    assert stored.metadata == metadata
    assert stored.state.semantic_hash() == final.semantic_hash()


@pytest.mark.unit
def test_snapshot_plus_remaining_events_rebuilds_final_state() -> None:
    events = build_fixture_events()
    engine = ReplayEngine(RULES, SCHEMA)
    full = engine.replay(events)
    intermediate = engine.replay(events[:2])
    store = InMemorySnapshotStore()
    metadata = create_snapshot_metadata(intermediate, EventSeq(2))
    store.save(metadata, intermediate)

    stored = store.latest(INSTANCE, BRANCH, at_or_before_revision=BranchRevision(5))
    assert stored is not None
    rebuilt = engine.replay(events[2:], baseline=stored.state)
    assert rebuilt.semantic_hash() == full.semantic_hash()


@pytest.mark.unit
def test_latest_respects_at_or_before_revision() -> None:
    events = build_fixture_events()
    engine = ReplayEngine(RULES, SCHEMA)
    store = InMemorySnapshotStore()
    for count in (2, 4):
        state = engine.replay(events[:count])
        store.save(create_snapshot_metadata(state, EventSeq(count)), state)
    at_3 = store.latest(INSTANCE, BRANCH, at_or_before_revision=BranchRevision(3))
    assert at_3 is not None and at_3.metadata.revision == BranchRevision(2)
