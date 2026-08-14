"""G29A: v5.2 compatibility golden baseline reproducibility.

Reloads every frozen fixture under tests/fixtures/v5_2_baseline/ and verifies
that the recorded semantic hashes are reproducible, so later v5.2 goals can
regress against them (event replay, snapshot restore, branch isolation,
worldpack manifest hashing, and the API contract shape).
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import cast

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASELINE = ROOT / "tests" / "fixtures" / "v5_2_baseline"

from tests.helpers.replay_fixture import RULES, SCHEMA  # noqa: E402
from wanxiang_domain.serialization_history import (  # noqa: E402
    event_from_primitive,
    snapshot_from_primitive,
)
from wanxiang_runtime.replay import ReplayEngine  # noqa: E402
from wanxiang_runtime.state import state_from_primitive  # noqa: E402


def _load(name: str) -> dict[str, object]:
    data = json.loads((BASELINE / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return cast(dict[str, object], data)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.mark.architecture
def test_manifest_combined_hash_reproducible() -> None:
    manifest = _load("manifest.json")
    raw_files = manifest["files"]
    assert isinstance(raw_files, dict)
    files = cast(dict[str, str], raw_files)
    assert set(files) == {
        "events.json",
        "snapshot.json",
        "branch.json",
        "worldpack.json",
        "api.json",
    }
    for name, expected in files.items():
        assert _sha256((BASELINE / name).read_bytes()) == expected
    combined = _sha256("\n".join(f"{name}:{files[name]}" for name in sorted(files)).encode("utf-8"))
    assert combined == manifest["combined_semantic_hash"]


@pytest.mark.architecture
def test_events_fixture_replays_to_same_hash() -> None:
    data = _load("events.json")
    raw_events = cast(list[object], data["events"])
    events = [event_from_primitive(cast(dict[str, object], event)) for event in raw_events]
    state = ReplayEngine(RULES, SCHEMA).replay(events)
    assert state.semantic_hash() == data["expected_semantic_hash"]
    assert state.revision.value == data["final_revision"]


@pytest.mark.architecture
def test_snapshot_fixture_restores_same_state() -> None:
    data = _load("snapshot.json")
    metadata = snapshot_from_primitive(cast(dict[str, object], data["metadata"]))
    state = state_from_primitive(cast(dict[str, object], data["state"]))
    assert state.semantic_hash() == data["expected_semantic_hash"]
    assert metadata.snapshot_id.value == "snap_golden_v52"


@pytest.mark.architecture
def test_branch_fixture_preserves_parent_and_child() -> None:
    data = _load("branch.json")
    raw_parent = cast(list[object], data["parent_events"])
    raw_child = cast(list[object], data["child_events"])
    parent_events = [event_from_primitive(cast(dict[str, object], event)) for event in raw_parent]
    parent_state = ReplayEngine(RULES, SCHEMA).replay(parent_events)
    assert parent_state.semantic_hash() == data["parent_expected_semantic_hash"]
    child_events = [event_from_primitive(cast(dict[str, object], event)) for event in raw_child]
    child_state = ReplayEngine(RULES, SCHEMA).replay(child_events, parent_state, start_seq=1)
    assert child_state.semantic_hash() == data["child_expected_semantic_hash"]
    raw_ancestry = data["child_ancestry"]
    assert isinstance(raw_ancestry, dict)
    ancestry = cast(dict[str, object], raw_ancestry)
    assert ancestry["parent_branch_id"] == data["parent_branch_id"]
    assert ancestry["fork_revision"] == 5


@pytest.mark.architecture
def test_worldpack_manifest_hashes_reproducible() -> None:
    data = _load("worldpack.json")
    raw_expected = data["expected_hashes"]
    raw_manifests = cast(list[object], data["manifests"])
    assert isinstance(raw_expected, dict)
    expected = cast(dict[str, str], raw_expected)
    for raw in raw_manifests:
        assert isinstance(raw, dict)
        manifest = cast(dict[str, object], raw)
        package_id = manifest["package_id"]
        assert isinstance(package_id, str)
        payload = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
        assert _sha256(payload) == expected[package_id]


@pytest.mark.architecture
def test_api_fixture_is_well_formed() -> None:
    data = _load("api.json")
    assert data["openapi"]
    raw_paths = data["paths"]
    assert isinstance(raw_paths, dict) and raw_paths
    for raw_item in cast(dict[str, object], raw_paths).values():
        assert isinstance(raw_item, dict)
        for raw_op in cast(dict[str, object], raw_item).values():
            assert isinstance(raw_op, dict)
            assert raw_op["operationId"]
