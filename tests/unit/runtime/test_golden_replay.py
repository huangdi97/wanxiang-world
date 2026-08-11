"""GOAL_01D: committed golden replay fixture regression."""

from __future__ import annotations

import json
import pathlib
from typing import cast

import pytest
from wanxiang_domain.errors import ReplayError
from wanxiang_domain.serialization_history import event_from_primitive
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

FIXTURE = pathlib.Path(__file__).resolve().parents[2] / "fixtures" / "golden_replay_v1.json"


def _load_fixture() -> dict[str, object]:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return cast(dict[str, object], data)


@pytest.mark.unit
def test_golden_fixture_replays_to_expected_hash() -> None:
    data = _load_fixture()
    raw_events = cast(list[object], data["events"])
    events = tuple(event_from_primitive(cast(dict[str, object], event)) for event in raw_events)
    expected_hash = data["expected_semantic_hash"]
    assert isinstance(expected_hash, str)
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert final.semantic_hash() == expected_hash


@pytest.mark.unit
def test_corrupt_fixture_event_fails_explicitly() -> None:
    data = _load_fixture()
    raw_events = cast(list[object], data["events"])
    events = [event_from_primitive(cast(dict[str, object], event)) for event in raw_events]
    primitive = dict(cast(dict[str, object], raw_events[0]))
    primitive["event_seq"] = 99
    events[0] = event_from_primitive(primitive)
    with pytest.raises(ReplayError):
        ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(tuple(events))
