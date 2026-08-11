"""GOAL_01D: minimal state diff."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import RULES, SCHEMA, build_fixture_events
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.diff import diff_states
from wanxiang_runtime.replay import ReplayEngine


@pytest.mark.unit
def test_diff_detects_added_and_updated_entities() -> None:
    events = build_fixture_events()
    engine = ReplayEngine(RULES, SCHEMA)
    before = engine.replay(events[:1])
    after = engine.replay(events[:3])
    diff = diff_states(before, after)
    assert EntityId("bob") in diff.added_entities
    assert EntityId("alice") in diff.updated_entities


@pytest.mark.unit
def test_diff_is_empty_for_equal_states() -> None:
    events = build_fixture_events()
    engine = ReplayEngine(RULES, SCHEMA)
    state = engine.replay(events)
    assert diff_states(state, state).is_empty()
