"""Keep the v5.5 acceptance matrix consistent with its current evidence."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parents[2]
MATRIX = ROOT / "reports" / "V55_ACCEPTANCE_MATRIX.md"
LEDGER = ROOT / "reports" / "G97I_FINAL_EVIDENCE.json"
HISTORICAL_REPORT = ROOT / "reports" / "REAL_BOOK_LIVING_WORLD_ACCEPTANCE_2026-08-25.md"
LINEAGE_REPORT = ROOT / "reports" / "V55_REAL_BOOK_EVIDENCE_LINEAGE.md"


def _matrix_rows() -> dict[int, tuple[str, str]]:
    rows: dict[int, tuple[str, str]] = {}
    pattern = re.compile(r"^\|\s*(\d+)\s*\|.*?\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|$")
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            rows[int(match.group(1))] = (match.group(2), match.group(3))
    return rows


def test_acceptance_matrix_and_final_ledger_converge() -> None:
    rows = _matrix_rows()
    assert set(range(1, 61)).issubset(rows)
    assert rows[1][0] == "ACCEPTED"
    assert rows[32][0] == "ACCEPTED"
    assert rows[59][0] == "ACCEPTED"
    assert (ROOT / "reports" / "V55_GATE1_RECONCILIATION.md").exists()
    assert (ROOT / "reports" / "V55_SOURCE_CANON_IMMUTABILITY_QUALIFICATION.md").exists()
    assert (ROOT / "reports" / "V55_GATE59_RECONCILIATION.md").exists()
    assert (ROOT / "reports" / "V55_FINAL_RELEASE_REPORT.md").exists()

    artifact = json.loads(
        (ROOT / "artifacts" / "v55" / "source_canon_immutability.json").read_text(encoding="utf-8")
    )
    assert artifact["status"] == "ACCEPTED"

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    lineage = ledger["qualification_lineage"]
    latest = max(lineage["records"], key=lambda item: item["qualified_at"])
    assert latest["id"] == lineage["latest_authoritative_qualification"]
    assert latest["status"] == "ACCEPTED"
    assert latest["authority_role"] == "latest_authoritative_qualification"
    assert any(
        item["id"] == "historical_pre_repair" and item["status"] == "NOT_ACCEPTED"
        for item in lineage["records"]
    )
    assert "latest_authoritative_qualification" in LINEAGE_REPORT.read_text(encoding="utf-8")
    all_prior_gates_accepted = all(rows[index][0] == "ACCEPTED" for index in range(1, 60))
    if all_prior_gates_accepted:
        assert rows[60][0] in {"UNLOCKED", "ACCEPTED_FOR_RC", "ACCEPTED"}
        assert ledger["release_gate"] != "LOCKED"
        if ledger["release_status"] == "ACCEPTED":
            assert ledger["release_artifacts"]["v5.5.0-rc1_tag_created"] is True
            assert ledger["release_artifacts"]["github_prerelease_created"] is True
    else:
        assert rows[60][0] == "LOCKED"
        assert ledger["release_status"] == "NOT_ACCEPTED"
        assert ledger["release_gate"] == "LOCKED"

    historical_hash = hashlib.sha256(HISTORICAL_REPORT.read_bytes()).hexdigest().upper()
    assert historical_hash == "8E976B210E96EA1369A05E3D5EA6410DBEB6F39F8E55A4460197365818FA7B73"
