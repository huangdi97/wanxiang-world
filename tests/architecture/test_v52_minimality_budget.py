"""G29G: v5.2 minimality budget reproducibility.

The budget script must run deterministically, hold the hard invariants (0
cycles, exactly 1 commit path, no manager-named classes), and document the
incremental M27-M34 budget table.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from typing import cast

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "v52_minimality_budget.py"
JSON_OUT = ROOT / "reports" / "v52_minimality_budget.json"


def _run() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def _load() -> dict[str, object]:
    return json.loads(JSON_OUT.read_text(encoding="utf-8"))


@pytest.mark.architecture
def test_budget_script_runs_and_hard_invariants_hold() -> None:
    _run()
    budget = _load()
    assert budget["hard_invariants_ok"] is True
    assert budget["import_cycles"] == 0
    assert budget["commit_paths"] == 1
    assert budget["manager_classes"] == 0


@pytest.mark.architecture
def test_budget_counts_are_stable() -> None:
    _run()
    budget = _load()
    # M26 baseline anchors (verified by G29A/G29B/G29C/G29E):
    # 10 at M26 + PresenceRegistry (M28) = 11
    assert budget["registry_classes"] == 13  # + AdapterRegistry (M52) + DistillerRegistry (M54)
    # 16 at M51-M52 + StructureParser/IncrementalParser/ParseCheckpointService (M53) = 17
    assert budget["service_classes"] == 17
    assert budget["engine_classes"] == 2
    # 23 at M26 + RealityRootContract Protocol (M27) = 24; + SourceAdapter (M52) = 25;
    # + Distiller Protocol (M54) = 26
    assert budget["ports"] == 26
    loc = budget["production_loc"]
    files = budget["production_files"]
    assert isinstance(loc, int) and loc > 0
    assert isinstance(files, int) and files > 0


@pytest.mark.architecture
def test_budget_documents_every_milestone() -> None:
    _run()
    budget = _load()
    raw_milestones = budget["milestone_budgets"]
    assert isinstance(raw_milestones, dict)
    milestones = cast(dict[str, dict[str, object]], raw_milestones)
    assert set(milestones) == {f"M{n}" for n in range(26, 35)} | {"M51", "M52", "M53", "M54"}
    for ms in (
        "M26", "M27", "M28", "M29", "M30", "M31", "M32", "M33", "M34",
        "M51", "M52", "M53", "M54"
    ):
        spec = milestones[ms]
        allowance = spec["new_abstractions_allowance"]
        assert isinstance(allowance, int) and allowance >= 0
        assert spec["note"]
        assert spec["hard_constraints"]
