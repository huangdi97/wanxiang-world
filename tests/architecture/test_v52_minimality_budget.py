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
    # Current v5.5 G92H/M89 snapshot anchors; the M26-M89 history remains in
    # the ledger and these counts include the accepted v5.5 projection/product
    # additions.
    assert budget["registry_classes"] == 16
    assert budget["service_classes"] == 25
    assert budget["engine_classes"] == 5
    assert budget["ports"] == 41
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
    assert set(milestones) == (
        {f"M{n}" for n in range(26, 35)} | {f"M{n}" for n in range(51, 79)} | {"M88", "M89"}
    )
    for ms in (
        "M26",
        "M27",
        "M28",
        "M29",
        "M30",
        "M31",
        "M32",
        "M33",
        "M34",
        *[f"M{n}" for n in range(51, 79)],
        "M89",
    ):
        spec = milestones[ms]
        allowance = spec["new_abstractions_allowance"]
        assert isinstance(allowance, int) and allowance >= 0
        assert spec["note"]
        assert spec["hard_constraints"]
