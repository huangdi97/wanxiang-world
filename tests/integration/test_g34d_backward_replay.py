"""G34D: backward replay of old Event/Snapshot/Branch against M26 golden samples."""

from __future__ import annotations

import json
import pathlib
from typing import cast

import pytest
from tests.helpers.replay_fixture import RULES, SCHEMA
from wanxiang_domain.serialization_history import event_from_primitive
from wanxiang_domain.version_context import legacy_version_context
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import state_from_primitive

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASELINE = ROOT / "tests" / "fixtures" / "v5_2_baseline"


def _load(name: str) -> dict[str, object]:
    return json.loads((BASELINE / name).read_text(encoding="utf-8"))


def _events(data: dict[str, object]) -> list[dict[str, object]]:
    raw = data["events"]
    assert isinstance(raw, list)
    return [cast(dict[str, object], e) for e in cast(list[object], raw)]


@pytest.mark.integration
def test_replay_old_events_matches_baseline_hash() -> None:
    data = _load("events.json")
    events = [event_from_primitive(e) for e in _events(data)]
    state = ReplayEngine(RULES, SCHEMA).replay(events)
    # Semantic hash identical to the M26 baseline golden.
    assert state.semantic_hash() == data["expected_semantic_hash"]
    assert state.revision.value == data["final_revision"]


@pytest.mark.integration
def test_restore_old_snapshot_matches_baseline_hash() -> None:
    data = _load("snapshot.json")
    state = state_from_primitive(cast(dict[str, object], data["state"]))
    assert state.semantic_hash() == data["expected_semantic_hash"]
    # The restored snapshot state equals the event replay (no data-clearing).
    events = [event_from_primitive(e) for e in _events(_load("events.json"))]
    assert state.semantic_hash() == ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash()


@pytest.mark.integration
def test_fork_old_branch_under_v52() -> None:
    data = _load("branch.json")
    parent_events = [
        event_from_primitive(cast(dict[str, object], e))
        for e in cast(list[object], data["parent_events"])
    ]
    parent_state = ReplayEngine(RULES, SCHEMA).replay(parent_events)
    assert parent_state.semantic_hash() == data["parent_expected_semantic_hash"]
    # The recorded child fork still replays and preserves the parent.
    child_events = [
        event_from_primitive(cast(dict[str, object], e))
        for e in cast(list[object], data["child_events"])
    ]
    child_state = ReplayEngine(RULES, SCHEMA).replay(child_events, parent_state, start_seq=1)
    assert child_state.semantic_hash() == data["child_expected_semantic_hash"]
    assert parent_state.semantic_hash() == data["parent_expected_semantic_hash"]


@pytest.mark.integration
def test_new_fields_arrive_via_legacy_defaults() -> None:
    """Old events carry no v5.2 context; legacy defaults keep them interpretable."""
    data = _load("events.json")
    events = [event_from_primitive(e) for e in _events(data)]
    # v5.2 commit/context semantics default to legacy for old history.
    legacy = legacy_version_context(RULES.value, SCHEMA.value)
    assert legacy.constitution_version == 1
    assert legacy.law_set_version == 0
    # Old events replay deterministically under the current engine (no v5.2 field required).
    assert (
        ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash() == data["expected_semantic_hash"]
    )
