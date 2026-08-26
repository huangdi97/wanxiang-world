"""v5.2 minimality budget: code minimality as a continuous acceptance metric.

Reuses the deterministic v5.1 metrics + forensics scanners and the architecture
guard cycle check, then records a per-milestone incremental budget (M27-M92).
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


# Per-milestone incremental budget notes (M26 baseline -> M92).
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
    "M54": {
        "note": (
            "Distillation & Candidate Fabric: unified CandidateEnvelope, distiller "
            "DAG + registry, reference passes (identity/event/relation/character/"
            "object), candidate clustering. Candidates propose only; no Canon."
        ),
        "new_abstractions_allowance": 14,
        "hard_constraints": ("1 commit path", "no Canon from candidates", "no second envelope"),
    },
    "M55": {
        "note": (
            "Evidence/Rights/Review/Completion core: evidence bindings, conflict "
            "ledger, rights gate, review ledger, E0-E5 completion + planner, review "
            "API routes. All decisions append-only/reversible; no Canon promotion."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": ("1 commit path", "no last-write-wins", "no auto canon"),
    },
    "M56": {
        "note": (
            "Domain Matching & WorldDraft: domain capability registry + recommender "
            "+ resolver, WorldDraft v1 + store, coverage, scenario mining, genesis "
            "draft. Drafts are compile intermediates, never runtime state."
        ),
        "new_abstractions_allowance": 9,
        "hard_constraints": (
            "1 commit path",
            "no second runtime state",
            "no per-world domain fork",
        ),
    },
    "M57": {
        "note": (
            "World compiler/package/preview: revision-pinned compiler boundary, "
            "formal package manifest wrapper, deterministic rebuild plan, and an "
            "isolated preview scope over the existing runtime port."
        ),
        "new_abstractions_allowance": 10,
        "hard_constraints": (
            "1 commit path",
            "no second runtime state",
            "preview never mutates published registry",
        ),
    },
    "M58": {
        "note": (
            "Studio/API/CLI surfaces reuse one AuthoringService, existing JobStore, "
            "review ledger, and package/preview boundaries."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "one backend for API and CLI",
            "no transport-owned state",
            "no second commit path",
        ),
    },
    "M59": {
        "note": (
            "Cross-source reference E2E hardening: bounded chunks, hashes, "
            "resume/idempotency and security evidence over the existing Forge path."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "single source registry",
            "no source bytes in Git",
            "resume is idempotent",
        ),
    },
    "M60": {
        "note": (
            "Semantic world views add typed candidate projections for identity, "
            "events, relations, knowledge, topology and object continuity."
        ),
        "new_abstractions_allowance": 10,
        "hard_constraints": (
            "semantic views remain Forge data",
            "no E0 promotion",
            "deterministic no-API path",
        ),
    },
    "M61": {
        "note": (
            "Source-family alignment and fusion preserve provenance, dissent, "
            "rights decisions and incremental recomputation."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "no last-write-wins",
            "source identity stays explicit",
            "rights gate is scope-aware",
        ),
    },
    "M62": {
        "note": (
            "Multimodal and external-source additions are ports/capability "
            "descriptors only; missing providers remain typed failures."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "connectors propose only",
            "no network in reference path",
            "OCR_REQUIRED is explicit",
        ),
    },
    "M63": {
        "note": (
            "Domain fingerprint/composition and gap packs remain draft-scoped "
            "and reuse the single capability registry."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "no per-world domain fork",
            "gap packs are proposals",
            "no OS sandbox claim",
        ),
    },
    "M64": {
        "note": (
            "Completion and consistency add constraint-backed evidence views "
            "without changing the canonical completion boundary."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "E1-E5 cannot enter E0 implicitly",
            "unknowns stay explicit",
            "no auto canon",
        ),
    },
    "M65": {
        "note": (
            "Scenario/genesis authoring adds bounded Forge engines and immutable "
            "candidate snapshots; runtime activation reuses existing ports."
        ),
        "new_abstractions_allowance": 10,
        "hard_constraints": (
            "engines are Forge-scoped",
            "snapshot is not runtime state",
            "activation uses existing Commit Authority",
        ),
    },
    "M66": {
        "note": (
            "Worldness validation is a bounded simulation/repair proposal loop "
            "over WorldDraft and never writes Canonical World State."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "repair is candidate-only",
            "bounded simulation",
            "single commit path",
        ),
    },
    "M67": {
        "note": (
            "Authoring orchestration composes existing stages, providers and job "
            "checkpoints without a transport-owned pipeline."
        ),
        "new_abstractions_allowance": 8,
        "hard_constraints": (
            "provider routing is proposal-only",
            "checkpoint is metadata",
            "no second orchestrator",
        ),
    },
    "M68": {
        "note": (
            "Review inbox/impact policy reuses the append-only review ledger and "
            "keeps defer/unknown outside Canon."
        ),
        "new_abstractions_allowance": 6,
        "hard_constraints": (
            "review is not commit authority",
            "decisions append-only",
            "unknown is not E0",
        ),
    },
    "M69": {
        "note": (
            "One-click profiles are a facade over the unified authoring service, "
            "package validator, preview registry and existing runtime."
        ),
        "new_abstractions_allowance": 6,
        "hard_constraints": (
            "API and CLI share one service",
            "publish updates Forge job metadata only",
            "incomplete packages remain blocked",
        ),
    },
    "M70": {
        "note": (
            "Production hardening is evidence, compatibility, documentation and "
            "delivery work; no new Kernel authority or runtime state is allowed."
        ),
        "new_abstractions_allowance": 0,
        "hard_constraints": (
            "no new authority",
            "no source/private artifact publication",
            "stop after final certification",
        ),
    },
    "M71": {
        "note": (
            "Real-book semantic distillation adds a bounded provider port and "
            "typed progress without allowing providers to mutate Canon."
        ),
        "new_abstractions_allowance": 5,
        "hard_constraints": (
            "private bytes remain outside Git",
            "provider output is candidate-only",
            "zero coverage is typed",
        ),
    },
    "M72": {
        "note": (
            "Rights and schema diagnostics make the Source -> Candidate boundary "
            "explicit while preserving the existing SourceRegistry."
        ),
        "new_abstractions_allowance": 4,
        "hard_constraints": (
            "rights gates remain independent",
            "no source rewriting",
            "no hidden provider fallback",
        ),
    },
    "M73": {
        "note": (
            "CLI/API/Studio lifecycle additions reuse AuthoringService and expose "
            "the same typed state transitions."
        ),
        "new_abstractions_allowance": 4,
        "hard_constraints": (
            "one authoring backend",
            "transport owns no state",
            "no second commit path",
        ),
    },
    "M74": {
        "note": (
            "Worldness dimensions carry measurements and evidence, with bounded "
            "repair proposals over the draft only."
        ),
        "new_abstractions_allowance": 4,
        "hard_constraints": (
            "worldness cannot commit canon",
            "no hardcoded coverage",
            "failure evidence is retained",
        ),
    },
    "M75": {
        "note": (
            "Living Instance evaluation proves commit/replay and branch isolation "
            "through the existing Commit Authority runtime port."
        ),
        "new_abstractions_allowance": 5,
        "hard_constraints": (
            "only Commit Authority mutates canon",
            "replay must match",
            "parent branch remains unchanged",
        ),
    },
    "M76": {
        "note": (
            "Browser Studio and random-socket smoke evidence complete the product "
            "surface without introducing a separate runtime."
        ),
        "new_abstractions_allowance": 3,
        "hard_constraints": (
            "same API use cases",
            "socket allocation is bounded",
            "no browser-only success path",
        ),
    },
    "M77": {
        "note": "Real private-source acceptance and regression evidence only.",
        "new_abstractions_allowance": 0,
        "hard_constraints": (
            "same source bytes",
            "all required evidence present",
            "NOT_ACCEPTED remains honest",
        ),
    },
    "M78": {
        "note": "Final feature-branch delivery and Actions verification only.",
        "new_abstractions_allowance": 0,
        "hard_constraints": (
            "no v5.5",
            "no model training",
            "stop after delivery",
        ),
    },
    "M88": {
        "note": (
            "PressureProfile, Opportunity lifecycle, Director modes, canon "
            "attractor, intervention, Quest projection and deterministic "
            "benchmark records reuse the existing reality/runtime branch ports."
        ),
        "new_abstractions_allowance": 25,
        "hard_constraints": (
            "one runtime and branch system",
            "Director/Quest/intervention remain proposal or projection only",
            "no pressure-specific Kernel types",
        ),
    },
    "M89": {
        "note": (
            "Long-horizon scheduler, detached background execution, cursor-only "
            "checkpoint/recovery, reference compaction, SimulationLOD, cost "
            "budget, and qualification value objects reuse the existing runtime."
        ),
        "new_abstractions_allowance": 39,
        "hard_constraints": (
            "one runtime/event store/branch system",
            "scheduler/LOD/budget/compaction remain proposal or reference-only",
            "no giant manager and no world-specific Kernel types",
        ),
    },
    "M90": {
        "note": (
            "Thirty-day actor/relationship/organization qualification compares "
            "typed projection snapshots over the existing Commit Authority and "
            "replay path; no new runtime state is introduced."
        ),
        "new_abstractions_allowance": 2,
        "hard_constraints": (
            "same source and package bytes",
            "append-only canonical history and replay equality",
            "all three projection planes change without projection commits",
        ),
    },
    "M91": {
        "note": (
            "Pattern observations, repeated-pattern detection, and the bounded "
            "habit/norm/institution/culture-ontology candidate layers consume "
            "immutable derived views over committed history without creating a "
            "second history."
        ),
        "new_abstractions_allowance": 15,
        "hard_constraints": (
            "derived cache only",
            "event refs and rebuild determinism",
            "no automatic Candidate or canonical mutation",
        ),
    },
    "M92": {
        "note": (
            "World laboratory evidence contracts add a sanitized RunArtifact, "
            "versioned experiment metadata, isolated fork/intervention evidence, "
            "bounded batch worldlines, provider assignment and trajectory/validation "
            "reports over the existing runtime and Commit Authority."
        ),
        "new_abstractions_allowance": 24,
        "hard_constraints": (
            "one runtime/event store/branch system",
            "artifacts contain refs and hashes, never private source bytes",
            "provider output remains proposal-only",
            "unknown validation is not pass",
        ),
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
        "milestone": "M92 (v5.5 G95C)",
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
        "## Current snapshot — M92 / v5.5 G95C",
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
        "## Historical incremental budgets M26-M92",
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
