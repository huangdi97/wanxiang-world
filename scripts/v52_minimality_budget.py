"""v5.2 minimality budget: code minimality as a continuous acceptance metric.

Reuses the deterministic v5.1 metrics + forensics scanners and the architecture
guard cycle check, then records a per-milestone incremental budget (M27-M34).
No arbitrary absolute LOC cap: budgets are per-stage *increment* allowances on
new abstractions (with mandatory justification in V5_2_CODE_MINIMALITY_LEDGER.md)
and hard invariants (0 cycles, exactly 1 commit path, no second Event/Branch/
Registry/State system).

Outputs:
  reports/V5_2_MINIMALITY_BUDGET.md
  reports/v52_minimality_budget.json

Run from the repository root:
    uv run python scripts/v52_minimality_budget.py
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections.abc import Mapping, Sequence
from typing import TypedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.architecture_check import detect_import_cycles  # noqa: E402
from scripts.v51_forensics import collect  # noqa: E402
from scripts.v51_metrics import compute_metrics  # noqa: E402


class MilestoneBudget(TypedDict):
    note: str
    new_abstractions_allowance: int
    hard_constraints: tuple[str, ...]


class Budget(TypedDict):
    milestone: str
    production_files: int
    production_loc: int
    public_classes: int
    public_functions: int
    registry_classes: int
    manager_classes: int
    service_classes: int
    engine_classes: int
    ports: int
    store_classes: int
    state_schema_models: int
    import_cycles: int
    commit_paths: int
    oversized_modules: int
    hard_invariants_ok: bool
    milestone_budgets: dict[str, MilestoneBudget]


# Per-milestone incremental budget notes (M26 baseline -> M34).
# key: milestone; value: allowed new production abstractions (types/protocols/
# classes/services) with justification, plus hard constraints.
MILESTONE_BUDGETS: dict[str, MilestoneBudget] = {
    "M26": {
        "note": "Baseline freeze + convergence; no net new abstractions (dedupe only).",
        "new_abstractions_allowance": 0,
        "hard_constraints": ("0 cycles", "1 commit path", "no second Event/Branch/Registry/State"),
    },
    "M27": {
        "note": (
            "Reality Root / Constitution / ISA are thin semantic layers over "
            "existing contracts; allow minimal value types + ISA verbs mapped to "
            "the existing pipeline."
        ),
        "new_abstractions_allowance": 3,
        "hard_constraints": (
            "no RealityRootEngine/SemanticISAEngine god objects",
            "no second commit pipeline",
        ),
    },
    "M28": {
        "note": (
            "Worldline / Lineage Graph / Hypervisor; lineage must reuse branch history semantics."
        ),
        "new_abstractions_allowance": 4,
        "hard_constraints": ("no second branch system", "no WorldLineageManager god object"),
    },
    "M29": {
        "note": (
            "Evolution Policy Stack as configuration over one runtime; "
            "scheduler + distillations are functions."
        ),
        "new_abstractions_allowance": 3,
        "hard_constraints": ("no third runtime for canon modes", "no per-distiller pipeline"),
    },
    "M30": {
        "note": (
            "Promotion pipeline + cross-world distillation reuse Candidate/Invariant machinery."
        ),
        "new_abstractions_allowance": 3,
        "hard_constraints": ("no World Merge as git-merge", "no auto platform promotion"),
    },
    "M31": {
        "note": "Compatibility migrations + thin API extensions only.",
        "new_abstractions_allowance": 2,
        "hard_constraints": ("migrations have rollback/compat", "no new API namespace copy"),
    },
    "M32": {
        "note": "Red Chamber content (World/Domain/Experience) must NOT add Core abstractions.",
        "new_abstractions_allowance": 1,
        "hard_constraints": ("no Core special-casing for red_chamber", "no model-memory Canon"),
    },
    "M33": {
        "note": "Red Chamber instance runtime; reuse Living World substrate.",
        "new_abstractions_allowance": 1,
        "hard_constraints": ("no second Runtime", "no Core hack for RC-001"),
    },
    "M34": {
        "note": "Final acceptance: verification + evidence only; no new abstractions.",
        "new_abstractions_allowance": 0,
        "hard_constraints": ("working tree clean or explained", "no failed-test skips"),
    },
    "M51": {
        "note": (
            "Source->LivingWorld Forge baseline: unified Job/JobCheckpoint/JobStore/"
            "JobService + typed job errors; reuses single commit path (jobs never mutate canon)."
        ),
        "new_abstractions_allowance": 5,
        "hard_constraints": ("1 commit path", "no second source registry", "jobs propose only"),
    },
    "M52": {
        "note": (
            "Source Registry & Adapter Foundation: convergence fields, blob refs, "
            "SourceAdapter ABI + AdapterRegistry, book/structured/asset adapters, "
            "ingestion security gate. All adapters propose only; single SourceRegistry."
        ),
        "new_abstractions_allowance": 12,
        "hard_constraints": ("1 commit path", "single source registry", "no fake extraction"),
    },
    "M53": {
        "note": (
            "Parse/Segment/Stable Locator: ParsedDocument IR, StructureParser, "
            "segment model + format locators, incremental cache, parse checkpoint, "
            "diagnostics API. All propose only; single locator/source-registry."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": ("1 commit path", "single source registry", "no fake extraction"),
    },
}


def _count_kind(found: Mapping[str, Sequence[object]], key: str) -> int:
    return len(found.get(key, []))


def build_budget() -> Budget:
    metrics = compute_metrics(ROOT)
    total = metrics["total"]
    flag_rows = metrics["flag_rows"]
    found, oversized = collect()
    cycles = detect_import_cycles(ROOT)
    registry_classes = _count_kind(found, "registry_classes")
    engine_classes = _count_kind(found, "engine_classes")
    ports = _count_kind(found, "ports")
    store_classes = _count_kind(found, "store_classes")
    state_classes = _count_kind(found, "state_classes")
    service_classes = _count_kind(found, "service_classes")
    commit_paths = _count_kind(found, "commit_paths")

    # Hard invariants must hold at every milestone.
    hard_ok = len(cycles) == 0 and commit_paths == 1
    # No manager-named production classes exist (by construction).
    managers = sum(1 for _label, name in flag_rows if "manager" in name.lower())

    payload: Budget = {
        "milestone": "M26",
        "production_files": total["files"],
        "production_loc": total["loc"],
        "public_classes": total["classes"],
        "public_functions": total["functions"],
        "registry_classes": registry_classes,
        "manager_classes": managers,
        "service_classes": service_classes,
        "engine_classes": engine_classes,
        "ports": ports,
        "store_classes": store_classes,
        "state_schema_models": state_classes,
        "import_cycles": len(cycles),
        "commit_paths": commit_paths,
        "oversized_modules": len(oversized),
        "hard_invariants_ok": hard_ok,
        "milestone_budgets": MILESTONE_BUDGETS,
    }
    return payload


def render(budget: Budget) -> str:
    lines = [
        "# V5.2 Minimality Budget (G29G)",
        "",
        "Code minimality is a continuous acceptance metric. No arbitrary absolute",
        "LOC cap: per-milestone *incremental* allowances on new abstractions (each",
        "with mandatory justification in `V5_2_CODE_MINIMALITY_LEDGER.md`) plus",
        "hard invariants that must hold at every milestone.",
        "",
        "## M26 baseline snapshot",
        "",
        "| Metric | Count |",
        "|---|---|",
        f"| Production files | {budget['production_files']} |",
        f"| Production LOC | {budget['production_loc']} |",
        f"| Public classes | {budget['public_classes']} |",
        f"| Public functions | {budget['public_functions']} |",
        f"| Registries | {budget['registry_classes']} |",
        f"| Managers | {budget['manager_classes']} |",
        f"| Services | {budget['service_classes']} |",
        f"| Engines | {budget['engine_classes']} |",
        f"| Ports | {budget['ports']} |",
        f"| Stores | {budget['store_classes']} |",
        f"| State/schema models | {budget['state_schema_models']} |",
        f"| Import cycles | {budget['import_cycles']} |",
        f"| Commit paths | {budget['commit_paths']} |",
        f"| Oversized modules (>300 lines) | {budget['oversized_modules']} |",
        "",
        f"Hard invariants hold: **{budget['hard_invariants_ok']}** (0 cycles, 1 commit path).",
        "",
        "## Incremental budgets M27-M34",
        "",
        "| Milestone | New-abstraction allowance | Note | Hard constraints |",
        "|---|---|---|---|",
    ]
    for ms, spec in MILESTONE_BUDGETS.items():
        lines.append(
            f"| {ms} | {spec['new_abstractions_allowance']} | "
            f"{spec['note']} | {'; '.join(spec['hard_constraints'])} |"
        )
    lines += [
        "",
        "Every new abstraction must answer the four questions in",
        "`reports/V5_2_CODE_MINIMALITY_LEDGER.md`; otherwise it is not added.",
        "",
    ]
    return chr(10).join(lines)


def main() -> int:
    budget = build_budget()
    (ROOT / "reports" / "V5_2_MINIMALITY_BUDGET.md").write_text(render(budget), encoding="utf-8")
    (ROOT / "reports" / "v52_minimality_budget.json").write_text(
        json.dumps(budget, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        "minimality budget: loc="
        f"{budget['production_loc']} files={budget['production_files']} "
        f"registries={budget['registry_classes']} managers={budget['manager_classes']} "
        f"services={budget['service_classes']} engines={budget['engine_classes']} "
        f"ports={budget['ports']} cycles={budget['import_cycles']} "
        f"commit_paths={budget['commit_paths']} hard_ok={budget['hard_invariants_ok']}"
    )
    return 0 if budget["hard_invariants_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
