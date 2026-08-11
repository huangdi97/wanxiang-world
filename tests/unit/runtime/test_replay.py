"""GOAL_01D: replay engine semantics."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import RULES, SCHEMA, build_fixture_events
from wanxiang_domain.entity import EntityId
from wanxiang_domain.errors import CorruptEventStream, IncompatibleVersion
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine


def _engine(rule: RuntimeVersion = RULES, schema: SchemaVersion = SCHEMA) -> ReplayEngine:
    return ReplayEngine(rule, schema)


@pytest.mark.unit
def test_full_replay_from_baseline() -> None:
    events = build_fixture_events()
    final = _engine().replay(events)
    assert final.revision == BranchRevision(5)
    assert final.entity(EntityId("alice")) is not None
    assert (
        final.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )


@pytest.mark.unit
def test_replay_from_snapshot_baseline_matches_full_replay() -> None:
    events = build_fixture_events()
    engine = _engine()
    full = engine.replay(events)
    baseline = engine.replay(events[:2])
    restored = engine.replay(events[2:], baseline=baseline)
    assert restored.semantic_hash() == full.semantic_hash()


@pytest.mark.unit
def test_replay_rejects_gap_in_event_seq() -> None:
    events = list(build_fixture_events())
    events[2] = CommittedEvent(
        event_id=events[2].event_id,
        instance_id=events[2].instance_id,
        branch_id=events[2].branch_id,
        event_seq=EventSeq(9),
        revision=events[2].revision,
        schema_version=events[2].schema_version,
        command_id=events[2].command_id,
        delta=events[2].delta,
        world_time=events[2].world_time,
        rule_version=events[2].rule_version,
    )
    with pytest.raises(CorruptEventStream):
        _engine().replay(tuple(events))


@pytest.mark.unit
def test_replay_rejects_incompatible_schema_version() -> None:
    events = list(build_fixture_events())
    events[0] = CommittedEvent(
        event_id=events[0].event_id,
        instance_id=events[0].instance_id,
        branch_id=events[0].branch_id,
        event_seq=events[0].event_seq,
        revision=events[0].revision,
        schema_version=SchemaVersion(2),
        command_id=events[0].command_id,
        delta=events[0].delta,
        world_time=events[0].world_time,
        rule_version=events[0].rule_version,
    )
    with pytest.raises(IncompatibleVersion):
        _engine().replay(tuple(events))


@pytest.mark.unit
def test_replay_rejects_mismatched_rule_version() -> None:
    events = build_fixture_events()
    with pytest.raises(IncompatibleVersion):
        _engine(rule=RuntimeVersion(2)).replay(events)


@pytest.mark.unit
def test_replay_rejects_event_from_another_branch() -> None:
    events = list(build_fixture_events())
    events[0] = CommittedEvent(
        event_id=events[0].event_id,
        instance_id=WorldInstanceId("wld_other"),
        branch_id=events[0].branch_id,
        event_seq=events[0].event_seq,
        revision=events[0].revision,
        schema_version=events[0].schema_version,
        command_id=events[0].command_id,
        delta=events[0].delta,
        world_time=events[0].world_time,
        rule_version=events[0].rule_version,
    )
    with pytest.raises(CorruptEventStream):
        _engine().replay(tuple(events))


@pytest.mark.unit
def test_empty_replay_without_baseline_is_corrupt() -> None:
    with pytest.raises(CorruptEventStream):
        _engine().replay(())
