"""G54D: duplicate abstraction guard (M51)."""

from __future__ import annotations

import json
import pathlib

import pytest
import scripts.duplicate_abstraction_scan as dup

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCAN = ROOT / "reports" / "duplicate_abstraction_scan.json"


@pytest.mark.architecture
def test_no_unallowed_duplicate_abstractions() -> None:
    duplicates = dup.scan()
    assert all(d.allowed for d in duplicates), [d.name for d in duplicates if not d.allowed]


@pytest.mark.architecture
def test_every_allowed_name_is_documented() -> None:
    duplicates = dup.scan()
    by_name = {d.name: d.modules for d in duplicates}
    for name, modules in dup.ALLOWED_DUPLICATE_NAMES.items():
        assert name in by_name, f"allowlisted name {name} not found in scan"
        assert by_name[name] == modules


@pytest.mark.architecture
def test_committed_scan_matches_current() -> None:
    data = json.loads(SCAN.read_text(encoding="utf-8"))
    assert data["verdict"] == "PASS"
    assert data["unallowed"] == []
