"""G13B: traceability matrix validator.

Loads scripts.traceability (data + rules) and checks the invariants the
matrix must satisfy: unique requirement ids, valid statuses, all 16 kernels
covered, every VERIFIED row has implementation and test ownership, and every
G00A-G12H goal maps to existing requirement ids.
"""

from __future__ import annotations

import json
from pathlib import Path

from scripts.traceability import (
    ALLOWED_STATUSES,
    GOALS,
    KERNELS,
    REQUIREMENTS,
    validate,
)

ROOT = Path(__file__).resolve().parent.parent.parent
JSON_PATH = ROOT / "reports" / "design_implementation_traceability.json"


def test_requirement_ids_unique() -> None:
    ids = [r["id"] for r in REQUIREMENTS]
    assert len(ids) == len(set(ids)), "requirement ids must be unique"
    assert ids, "requirement list must not be empty"


def test_all_statuses_valid() -> None:
    for r in REQUIREMENTS:
        assert r["status"] in ALLOWED_STATUSES, f"{r['id']} has invalid status"


def test_all_sixteen_kernels_covered() -> None:
    assert len(KERNELS) == 16, "the spec defines 16 logical kernels"
    covered = {r["kernel"] for r in REQUIREMENTS}
    assert set(KERNELS) == covered, "every kernel must have at least one row"


def test_verified_rows_have_implementation_and_test() -> None:
    for r in REQUIREMENTS:
        if r["status"] == "VERIFIED":
            assert r["implementation"], f"{r['id']} VERIFIED but no implementation owner"
            assert r["test"], f"{r['id']} VERIFIED but no test pointer"


def test_every_goal_has_valid_mapping() -> None:
    ids = {r["id"] for r in REQUIREMENTS}
    assert GOALS, "goal mapping must not be empty"
    for goal, reqs in GOALS.items():
        assert goal.startswith("G"), f"goal id {goal} malformed"
        assert reqs, f"goal {goal} has no requirement mapping"
        for req in reqs:
            assert req in ids, f"goal {goal} references unknown requirement {req}"


def test_validate_returns_no_errors() -> None:
    assert validate() == []


def test_generated_json_is_valid_and_current() -> None:
    assert JSON_PATH.exists(), "run scripts/traceability.py to regenerate the JSON"
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert payload["traceability"]["requirements"] == REQUIREMENTS
    assert payload["traceability"]["goals"] == GOALS
    assert len(payload["coverage"]["kernels"]) == 16
