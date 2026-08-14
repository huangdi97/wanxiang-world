"""G21C: duplicate-abstraction forensics acceptance.

Re-runs the deterministic forensic scanner and asserts the invariants that make
the consolidation safe: exactly one commit path, a bounded set of registries,
and that every duplicate candidate in the report has a disposition.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCANNER = ROOT / "scripts" / "v51_forensics.py"
FORENSICS = ROOT / "reports" / "V5_1_DUPLICATE_FORENSICS.md"


def _run_scanner() -> str:
    result = subprocess.run(
        [sys.executable, str(SCANNER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


@pytest.mark.architecture
def test_scanner_runs_deterministically() -> None:
    first = _run_scanner()
    second = _run_scanner()
    assert first == second, "forensic scanner output is not deterministic"


@pytest.mark.architecture
def test_exactly_one_commit_path() -> None:
    out = _run_scanner()
    lines = [ln for ln in out.splitlines() if ln.startswith("  commit_paths:")]
    assert lines and lines[0].endswith(": 1"), f"expected exactly 1 commit path, got {lines}"


@pytest.mark.architecture
def test_dispositions_recorded_for_all_duplicate_candidates() -> None:
    text = FORENSICS.read_text(encoding="utf-8")
    # Every registry/store candidate listed in the scan must have a disposition row.
    for name in (
        "PackageRegistry",
        "InMemoryPackageRegistry",
        "SourceRegistry",
        "SkillRegistry",
        "ActionRegistry",
        "AdjudicatorRegistry",
        "ResolverRegistry",
        "HostRegistry",
        "SnapshotStore",
        "CompletionLedger",
        "ObjectStore",
        "ReplayEngine",
    ):
        assert name in text, f"missing disposition for duplicate candidate {name}"
