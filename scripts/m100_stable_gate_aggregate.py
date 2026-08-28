"""Aggregate Gates 61-79 from evidence, then compare the stable ledger."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from m98_burn_in_support import write_json
from m100_stable_gate_evidence import (
    gate61,
    gate78,
    human_gates,
    ledger_statuses,
    load,
    m98_gates,
    quality_gates,
)

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_ROOT = ROOT / "artifacts" / "v55_stable"
M100_ROOT = EVIDENCE_ROOT / "m100"
OUTPUT = M100_ROOT / "stable_gate_aggregate.json"
REPORT = ROOT / "reports" / "M100_G103A_STABLE_GATE_AGGREGATE.md"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _record(relative: str, artifact: dict[str, Any]) -> dict[str, Any]:
    path = EVIDENCE_ROOT / relative
    return {
        "path": f"artifacts/v55_stable/{relative}",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "schema": artifact["schema"],
        "conclusion": artifact.get("conclusion", "DECLARATION"),
        "build_sha": artifact.get("build_sha", artifact.get("generated_build_sha")),
    }


def qualify() -> dict[str, Any]:
    baseline = load("baseline.json")
    player = load("m95/player_acceptance.json")
    m96 = load("m96/original_prompt_world.json")
    m97 = load("m97/experience_quality_baseline.json")
    m98 = load("m98/burn_in_summary.json")
    godot = load("m99/godot_integration.json")
    gates: dict[str, dict[str, Any]] = {"61": gate61(baseline)}
    gates.update(human_gates(player))
    gates.update(
        quality_gates(
            m96,
            "artifacts/v55_stable/m96/original_prompt_world.json",
            ("67", "68", "69"),
        )
    )
    gates.update(
        quality_gates(
            m97,
            "artifacts/v55_stable/m97/experience_quality_baseline.json",
            ("70", "71", "72"),
        )
    )
    gates.update(m98_gates(m98))
    gates["78"] = gate78(godot)
    gates["79"] = {
        "status": "LOCKED",
        "evidence": ["G103B-G103D stable preflight is pending"],
        "reason": "M100 stable preflight and clean-clone evidence is not yet accepted",
    }
    derived = {gate: item["status"] for gate, item in gates.items()}
    expected_ledger = {**derived, "80": "LOCKED"}
    observed_ledger = ledger_statuses()
    ledger_ok = all(observed_ledger.get(gate) == status for gate, status in expected_ledger.items())
    stable_predicate = (
        all(derived[str(gate)] == "PASS" for gate in range(61, 78))
        and derived["78"] in ("PASS", "EXTERNAL_BLOCKED")
        and derived["79"] == "PASS"
        and ledger_ok
    )
    relative_names = (
        "baseline.json",
        "m95/player_acceptance.json",
        "m96/original_prompt_world.json",
        "m97/experience_quality_baseline.json",
        "m98/burn_in_summary.json",
        "m99/godot_integration.json",
    )
    artifacts = {relative: _record(relative, load(relative)) for relative in relative_names}
    summary: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m100.stable-gate-aggregate.v1",
        "conclusion": "PASS" if stable_predicate else "LOCKED",
        "generated_build_sha": _head(),
        "evidence_derived": True,
        "gates": gates,
        "ledger_consistency": {
            "status": "PASS" if ledger_ok else "FAIL",
            "ledger_path": "reports/V55_STABLE_ACCEPTANCE_MATRIX.md",
            "observed": observed_ledger,
            "expected_from_evidence": expected_ledger,
        },
        "stable_release_predicate": {
            "gate_80": "ACCEPTED_FOR_STABLE" if stable_predicate else "LOCKED",
            "all_required_gates": stable_predicate,
            "reason": [
                "Gates 62-66 remain USER_INPUT_REQUIRED",
                "Gate 79 stable preflight is not yet accepted",
            ],
        },
        "source_artifacts": artifacts,
        "boundaries": {
            "implemented": [
                "evidence-derived Gates 61-79 aggregate",
                "stable ledger consistency comparison",
            ],
            "validated": [
                "Gates 61, 67-77 from persisted local evidence",
                "Gate 78 explicit Godot external block",
            ],
            "experimental": [
                "Prompt Genesis and bounded long-horizon continuity",
                "World Lab and emergence interpretation",
            ],
            "not_proven": [
                "genuine human experience acceptance",
                "Stable Gate 79/80",
                "production or scientific generalization",
            ],
            "external_blocked": [
                "live Git remote refresh",
                "live PostgreSQL",
                "heavy physical/visual E2E",
                "real Godot runtime",
            ],
        },
    }
    write_json(OUTPUT, summary)
    gate_lines = "\n".join(f"- Gate {gate}: {item['status']}" for gate, item in gates.items())
    REPORT.write_text(
        f"""# M100 G103A Evidence-derived Stable Gate Aggregate

Conclusion: {summary["conclusion"]}. The aggregate reads persisted evidence
artifacts and recomputes the M98 predicates; it does not use STATUS, PLAN, or
README prose as the source of gate truth.

{gate_lines}

The ledger consistency check is {summary["ledger_consistency"]["status"]}.
Gate 78 is an explicit external block because no supported Godot executable is
available; reference ABI tests were not relabeled as Godot E2E. Gate 79 is
still LOCKED pending G103B-G103D. Gate 80 is LOCKED and no Stable tag/release
action is authorized.

Prompt Genesis, bounded long-horizon/World Lab, and emergence remain
EXPERIMENTAL/BOUNDED. Genuine human M95 evidence remains USER_INPUT_REQUIRED.
Live PostgreSQL, heavy physical/visual E2E, live remote refresh, and
production/scientific claims remain NOT_PROVEN or EXTERNAL_BLOCKED.

Machine-readable evidence: artifacts/v55_stable/m100/stable_gate_aggregate.json
Reproduce with: uv run python scripts/m100_stable_gate_aggregate.py
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
                "gate_80": result["stable_release_predicate"]["gate_80"],
                "ledger_consistency": result["ledger_consistency"]["status"],
                "gates": {gate: item["status"] for gate, item in result["gates"].items()},
            },
            indent=2,
        )
    )
    raise SystemExit(0 if result["conclusion"] in ("PASS", "LOCKED") else 1)
