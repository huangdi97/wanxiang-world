"""G13B: traceability matrix validator.

Loads scripts/traceability.py (data + rules) and checks the invariants the
matrix must satisfy: unique requirement ids, valid statuses, all 16 kernels
covered, every VERIFIED row has implementation and test ownership, and every
G00A-G12H goal maps to existing requirement ids.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = ROOT / "scripts" / "traceability.py"
JSON_PATH = ROOT / "reports" / "design_implementation_traceability.json"


@pytest.fixture(scope="module")
def trace() -> object:
    spec = importlib.util.spec_from_file_location("traceability", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_requirement_ids_unique(trace: object) -> None:
    ids = [r["id"] for r in trace.REQUIREMENTS]
    assert len(ids) == len(set(ids)), "requirement ids must be unique"
    assert ids, "requirement list must not be empty"


def test_all_statuses_valid(trace: object) -> None:
    for r in trace.REQUIREMENTS:
        assert r["status"] in trace.ALLOWED_STATUSES, f"{r['id']} has invalid status"


def test_all_sixteen_kernels_covered(trace: object) -> None:
    assert len(trace.KERNELS) == 16, "the spec defines 16 logical kernels"
    covered = {r["kernel"] for r in trace.REQUIREMENTS}
    assert set(trace.KERNELS) == covered, "every kernel must have at least one row"


def test_verified_rows_have_implementation_and_test(trace: object) -> None:
    for r in trace.REQUIREMENTS:
        if r["status"] == "VERIFIED":
            assert r["implementation"], f"{r['id']} VERIFIED but no implementation owner"
            assert r["test"], f"{r['id']} VERIFIED but no test pointer"


def test_every_goal_has_valid_mapping(trace: object) -> None:
    ids = {r["id"] for r in trace.REQUIREMENTS}
    assert trace.GOALS, "goal mapping must not be empty"
    for goal, reqs in trace.GOALS.items():
        assert goal.startswith("G"), f"goal id {goal} malformed"
        assert reqs, f"goal {goal} has no requirement mapping"
        for req in reqs:
            assert req in ids, f"goal {goal} references unknown requirement {req}"


def test_validate_returns_no_errors(trace: object) -> None:
    assert trace.validate() == []


def test_generated_json_is_valid_and_current(trace: object) -> None:
    assert JSON_PATH.exists(), "run scripts/traceability.py to regenerate the JSON"
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert payload["traceability"]["requirements"] == trace.REQUIREMENTS
    assert payload["traceability"]["goals"] == trace.GOALS
    assert len(payload["coverage"]["kernels"]) == 16
