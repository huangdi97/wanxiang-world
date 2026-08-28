"""Evidence-derived predicates used by the M100 Stable gate aggregate."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from m98_burn_in_summary_checks import (
    burn_gate,
    capacity_gate,
    emergence_gate,
    matrix_shape,
    scale_gate,
)

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_ROOT = ROOT / "artifacts" / "v55_stable"
LEDGER = ROOT / "reports" / "V55_STABLE_ACCEPTANCE_MATRIX.md"


def load(relative: str) -> dict[str, Any]:
    return json.loads((EVIDENCE_ROOT / relative).read_text(encoding="utf-8"))


def _all_true(values: dict[str, Any]) -> bool:
    return all(bool(value) for value in values.values())


def gate61(baseline: dict[str, Any]) -> dict[str, Any]:
    lineage = baseline["lineage"]
    checks_ok = all(item["status"] == "PASS" for item in baseline["checks"])
    predicate = (
        baseline["conclusion"] == "PASS"
        and baseline["gate"] == "61"
        and lineage["final_closure"]["is_ancestor"] is True
        and lineage["rc1_peeled"]["is_ancestor"] is True
        and lineage["v54_peeled"]["is_ancestor"] is True
        and lineage["rc1"]["status"] == "PASS"
        and lineage["v54"]["status"] == "PASS"
        and baseline["scope_scan"]["status"] == "PASS"
        and checks_ok
    )
    return {
        "status": "PASS" if predicate else "FAIL",
        "evidence": ["artifacts/v55_stable/baseline.json"],
        "checks": {
            "baseline_conclusion": baseline["conclusion"] == "PASS",
            "tag_objects": lineage["rc1"]["status"] == "PASS"
            and lineage["v54"]["status"] == "PASS",
            "closure_and_tag_ancestry": lineage["final_closure"]["is_ancestor"]
            and lineage["rc1_peeled"]["is_ancestor"]
            and lineage["v54_peeled"]["is_ancestor"],
            "local_check_set": checks_ok,
            "scope_scan": baseline["scope_scan"]["status"] == "PASS",
        },
    }


def human_gates(player: dict[str, Any]) -> dict[str, dict[str, Any]]:
    status = "USER_INPUT_REQUIRED" if player["conclusion"] == "USER_INPUT_REQUIRED" else "FAIL"
    return {
        str(gate): {
            "status": status,
            "evidence": ["artifacts/v55_stable/m95/player_acceptance.json"],
            "human_required": player["human_required"],
            "human_fields_present": all(
                player[field] is not None
                for field in ("human_actions", "ratings", "free_text_notes")
            ),
            "automated_route_conclusion": player["automated_route_conclusion"],
        }
        for gate in range(62, 67)
    }


def quality_gates(
    artifact: dict[str, Any], evidence: str, gates: tuple[str, ...]
) -> dict[str, dict[str, Any]]:
    checks_ok = _all_true(artifact["checks"])
    return {
        gate: {
            "status": (
                "PASS"
                if artifact["conclusion"] == "PASS"
                and artifact["gates"][gate] == "PASS"
                and checks_ok
                else "FAIL"
            ),
            "evidence": [evidence],
            "checks": checks_ok,
            "artifact_gate": artifact["gates"][gate],
            "build_sha": artifact["build_sha"],
        }
        for gate in gates
    }


def m98_gates(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    matrix = load("m98/run_matrix.json")
    burn_30d = load("m98/30d_burn_in.json")
    burn_90d = load("m98/90d_burn_in.json")
    emergence = load("m98/emergence_controls.json")
    scale = load("m98/scale_curve.json")
    capacity = load("m98/capacity_curve.json")
    matrix_hash = matrix["content_hash"]
    matrix_ok = matrix_shape(matrix)["status"] == "PASS"
    derived = {
        "73": burn_gate(burn_30d, 12, matrix_hash),
        "74": burn_gate(burn_90d, 6, matrix_hash),
        "75": emergence_gate(emergence),
        "76": scale_gate(scale),
        "77": capacity_gate(capacity),
    }
    result: dict[str, dict[str, Any]] = {}
    evidence = [
        f"artifacts/v55_stable/m98/{name}"
        for name in (
            "run_matrix.json",
            "30d_burn_in.json",
            "90d_burn_in.json",
            "emergence_controls.json",
            "scale_curve.json",
            "capacity_curve.json",
        )
    ]
    for gate, check in derived.items():
        same_as_summary = summary["gates"][gate]["status"] == check["status"]
        predicate = check["status"] == "PASS" and matrix_ok and same_as_summary
        result[gate] = {
            "status": "PASS" if predicate else "FAIL",
            "evidence": evidence,
            "derived_check": check,
            "summary_status_matches": same_as_summary,
            "matrix_shape": matrix_ok,
        }
    return result


def gate78(godot: dict[str, Any]) -> dict[str, Any]:
    checks = godot["checks"]
    predicate = (
        godot["conclusion"] == "EXTERNAL_BLOCKED"
        and godot["gate_78"] == "EXTERNAL_BLOCKED"
        and checks["godot_executable_found"] is False
        and checks["godot4_executable_found"] is False
        and checks["real_engine_e2e"] is False
        and checks["reference_abi_not_relabelled_as_godot"] is True
    )
    return {
        "status": "EXTERNAL_BLOCKED" if predicate else "FAIL",
        "evidence": ["artifacts/v55_stable/m99/godot_integration.json"],
        "checks": checks,
        "reason": godot["external_block_reason"],
    }


def ledger_statuses() -> dict[str, str]:
    text = LEDGER.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^\|\s*(6[1-9]|7[0-9]|80)\s*\|[^|]*\|\s*([^|]+?)\s*\|",
        re.MULTILINE,
    )
    return {match.group(1): match.group(2).strip() for match in pattern.finditer(text)}


__all__ = [
    "gate61",
    "gate78",
    "human_gates",
    "ledger_statuses",
    "load",
    "m98_gates",
    "quality_gates",
]
