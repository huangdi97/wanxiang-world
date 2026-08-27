"""G97A: the v5.5 certification matrix is explicit and threshold-frozen."""

from __future__ import annotations

import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MATRIX = ROOT / "reports" / "V55_ACCEPTANCE_MATRIX.md"
_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*[^|]+\|\s*([^|]+)\|\s*([^|]+)\|$")


@pytest.mark.architecture
def test_v55_matrix_has_frozen_gate_rows_and_release_lock() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    rows = [_ROW.match(line) for line in text.splitlines()]
    parsed = [match for match in rows if match is not None]
    assert [int(match.group(1)) for match in parsed] == list(range(1, 61))
    assert all(
        match.group(2).strip() in {"ACCEPTED", "ACCEPTED-INHERITED", "PENDING", "LOCKED"}
        for match in parsed
    )
    assert "thresholds may not be lowered" in text
    assert "Gates 1-59 must be ACCEPTED" in text
    assert "| 60 | Release gate / rc1 only if all ACCEPTED | LOCKED |" in text
    assert "Status at G97I: **IN_PROGRESS / NOT_ACCEPTED**" in text


@pytest.mark.architecture
def test_g97a_matrix_keeps_known_unaccepted_boundaries_explicit() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    for gate in ("90-day selected-world run", "Source/canon immutability"):
        assert f"| {24 if '90-day' in gate else 32} |" in text
        assert gate in text
    for phrase in (
        "Four or more parallel worldlines",
        "Browser Experience/Studio E2E",
        "Security/private-source/UGC scan",
        "Remote SHA equals local HEAD",
        "Required GitHub Actions",
        "Evidence boundary separation",
    ):
        assert phrase in text
    assert "v5.5.0-rc1" in text
