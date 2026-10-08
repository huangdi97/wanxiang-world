"""Qualify G101G/M98 from the persisted burn-in evidence artifacts."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from m98_burn_in_summary_checks import (
    burn_gate,
    capacity_gate,
    emergence_gate,
    matrix_shape,
    scale_gate,
)
from m98_burn_in_support import write_json

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_ROOT = ROOT / "artifacts" / "v55_stable" / "m98"
SUMMARY_ARTIFACT = ARTIFACT_ROOT / "burn_in_summary.json"
SUMMARY_REPORT = ROOT / "reports" / "M98_EMERGENCE_MULTI_RUN_SCALE_BURN_IN.md"
ARTIFACT_NAMES = (
    "run_matrix.json",
    "30d_burn_in.json",
    "90d_burn_in.json",
    "emergence_controls.json",
    "scale_curve.json",
    "capacity_curve.json",
)


def _load(name: str) -> dict[str, Any]:
    return json.loads((ARTIFACT_ROOT / name).read_text(encoding="utf-8"))


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _source_records(artifacts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        name: {
            "path": f"artifacts/v55_stable/m98/{name}",
            "schema": artifact["schema"],
            "conclusion": artifact.get("conclusion", "DECLARATION"),
            "build_sha": artifact.get("build_sha"),
        }
        for name, artifact in artifacts.items()
    }


def qualify() -> dict[str, Any]:
    artifacts = {name: _load(name) for name in ARTIFACT_NAMES}
    matrix = artifacts["run_matrix.json"]
    matrix_hash = matrix["content_hash"]
    gates = {
        "73": burn_gate(artifacts["30d_burn_in.json"], 12, matrix_hash),
        "74": burn_gate(artifacts["90d_burn_in.json"], 6, matrix_hash),
        "75": emergence_gate(artifacts["emergence_controls.json"]),
        "76": scale_gate(artifacts["scale_curve.json"]),
        "77": capacity_gate(artifacts["capacity_curve.json"]),
    }
    all_pass = all(item["status"] == "PASS" for item in gates.values())
    summary: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m98.burn-in-summary.v1",
        "conclusion": "PASS" if all_pass else "FAIL",
        "generated_build_sha": _head(),
        "reproducible_command": "uv run python scripts/m98_burn_in_summary.py",
        "matrix": {
            "matrix_id": matrix["matrix_id"],
            "content_hash": matrix_hash,
            "shape": matrix_shape(matrix),
        },
        "gates": gates,
        "source_artifacts": _source_records(artifacts),
        "run_refs": {
            "30d": gates["73"]["run_refs"],
            "90d": gates["74"]["run_refs"],
            "scale": gates["76"]["run_refs"],
            "emergence_positive": [
                gates["75"]["positive_world_ref"],
                gates["75"]["positive_branch_ref"],
            ],
            "emergence_null": [
                gates["75"]["null_world_ref"],
                gates["75"]["null_branch_ref"],
            ],
        },
        "boundaries": {
            "implemented": [
                "versioned 30d/90d multi-run burn-in",
                "bounded emergence and null-control qualification",
                "10/50/100/500/1000 SimulationLOD scale curve",
                "capacity/degradation metric aggregation",
            ],
            "validated": [
                "Gates 73-77 from complete persisted evidence",
                "real local SQLite/Commit Authority/replay/recovery paths",
            ],
            "experimental": [
                "bounded long-horizon interpretation",
                "bounded emergence interpretation",
                "local capacity/degradation interpretation",
            ],
            "not_proven": [
                "universal emergence",
                "scientific causality",
                "production or live-customer capacity",
                "10k/100k actor capacity",
            ],
            "external_blocked": [
                "live PostgreSQL",
                "heavy physical/visual E2E",
                "live external-provider monetary cost",
            ],
        },
        "stable_release_boundary": {
            "gate_80": "LOCKED",
            "reason": [
                "M95 genuine human-player evidence remains USER_INPUT_REQUIRED",
                "Gates 78-79 are not yet accepted",
            ],
        },
    }
    write_json(SUMMARY_ARTIFACT, summary)
    gate_lines = "\n".join(f"- Gate {gate}: {result['status']}" for gate, result in gates.items())
    SUMMARY_REPORT.write_text(
        f"""# M98 Emergence, Multi-run, Scale, and Burn-in Qualification

Conclusion: {summary["conclusion"]}. G101G re-verified the persisted M98
artifacts and accepted Gates 73-77 only when their complete machine predicates
were true:

{gate_lines}

The 30d and 90d matrices are complete and replay/recovery/branch/provider
checks are true for every persisted row. The bounded emergence artifact has a
separate qualified positive recurrence and unqualified null control; candidate
derivation did not invoke a canonical promotion boundary. The scale ladder has
three repetitions at 10, 50, 100, 500, and 1000 actors, with active L0/L1
counts kept separate from full-policy population counts. The capacity artifact
records the measured degradation knee at
{gates["77"]["observed_knee"]} and forbids 10k/100k extrapolation.

This is creator-owned synthetic, local SQLite/reference-provider engineering
evidence. Prompt Genesis, bounded long-horizon/World Lab, and emergence remain
EXPERIMENTAL/BOUNDED. Production capacity, scientific causality, universal
emergence, live PostgreSQL, heavy physical/visual E2E, and live-provider
monetary cost remain NOT_PROVEN or EXTERNAL_BLOCKED. Gate 80 remains LOCKED
because M95 human evidence is USER_INPUT_REQUIRED and Gates 78-79 are pending.

Machine-readable evidence: artifacts/v55_stable/m98/burn_in_summary.json
Source artifacts are listed in the summary with build SHAs, hashes, and run
references. Reproduce with: uv run python scripts/m98_burn_in_summary.py
""",
        encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    result = qualify()
    print(
        json.dumps(
            {
                "conclusion": result["conclusion"],
                "generated_build_sha": result["generated_build_sha"],
                "gates": {gate: item["status"] for gate, item in result["gates"].items()},
                "gate_80": result["stable_release_boundary"]["gate_80"],
            },
            indent=2,
        )
    )
    raise SystemExit(0 if result["conclusion"] == "PASS" else 1)
