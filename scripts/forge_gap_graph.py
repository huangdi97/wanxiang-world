"""G54C: Source->Living World capability/gap graph generator (M51).

Probes the CURRENT tree (not prior claims) for each pipeline stage's key
capability symbols and produces an honest existence/gap/closure graph:
status = EXISTS (all probes present) / PARTIAL (some) / MISSING (none).
Every non-EXISTS stage must map to at least one M51-M70 closure goal.

No domain content; pure introspection + goal index validation.
"""

from __future__ import annotations

import importlib
import json
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PIPELINE_STAGES: tuple[dict[str, Any], ...] = (
    {
        "stage": 1,
        "name": "SOURCE",
        "probes": [("wanxiang_substrate.sources.model", "SourceRecord")],
    },
    {
        "stage": 2,
        "name": "SourceRegistry + Rights + Version + Checksum",
        "probes": [
            ("wanxiang_substrate.sources.registry", "SourceRegistry"),
            ("wanxiang_substrate.sources.model", "RightsEnvelope"),
        ],
    },
    {
        "stage": 3,
        "name": "SourceAdapter (TXT/MD/EPUB/DOCX/text-PDF/JSON/YAML/CSV/GEDCOM/Asset)",
        "probes": [
            ("wanxiang_substrate.compiler.readers", "read_source"),
            ("wanxiang_substrate.compiler.readers", "read_epub"),
            ("wanxiang_substrate.compiler.readers", "read_docx"),
            ("wanxiang_substrate.compiler.readers", "read_pdf_text"),
            ("wanxiang_substrate.compiler.readers", "read_csv"),
            ("wanxiang_substrate.genealogy.gedcom", "parse_gedcom"),
        ],
    },
    {
        "stage": 4,
        "name": "ParsedDocument / StructuredRecords / AssetReferences",
        "probes": [
            ("wanxiang_substrate.compiler.model", "CandidateObject"),
            ("wanxiang_substrate.parsing.model", "ParsedDocument"),
        ],
    },
    {
        "stage": 5,
        "name": "Segment + StableLocator",
        "probes": [("wanxiang_substrate.sources.locator", "segment_source")],
    },
    {
        "stage": 6,
        "name": "Multi-pass Distillation",
        "probes": [
            ("wanxiang_substrate.sources.identity", "IdentityDistiller"),
            ("wanxiang_substrate.sources.entity_distill", "EntityDistiller"),
            ("wanxiang_substrate.distill.passes", "EventTimeSpacePass"),
            ("wanxiang_substrate.distill.passes", "RelationOrganizationPass"),
        ],
    },
    {
        "stage": 7,
        "name": "CandidateEnvelope / Claim / Evidence",
        "probes": [
            ("wanxiang_substrate.sources.model", "ClaimCandidate"),
            ("wanxiang_substrate.sources.model", "EvidenceLink"),
            ("wanxiang_substrate.candidates.envelope", "CandidateEnvelope"),
        ],
    },
    {
        "stage": 8,
        "name": "Identity Resolution + Cross-source Alignment",
        "probes": [
            ("wanxiang_substrate.sources.identity", "IdentityCandidate"),
            ("wanxiang_substrate.fusion.alignment", "CrossSourceAligner"),
        ],
    },
    {
        "stage": 9,
        "name": "Conflict Preservation + Review Decisions",
        "probes": [
            ("wanxiang_substrate.sources.fixture", "conflicting_claims"),
            ("wanxiang_substrate.sources.entity_distill", "EntityReviewGate"),
            ("wanxiang_substrate.conflict.workbench", "ConflictWorkbench"),
        ],
    },
    {"stage": 10, "name": "Domain Inference / Dependency Resolution", "probes": []},
    {
        "stage": 11,
        "name": "WorldDraft",
        "probes": [("wanxiang_substrate.draft.model", "WorldDraft")],
    },
    {
        "stage": 12,
        "name": "Missingness Graph / Completion Plan",
        "probes": [
            ("wanxiang_substrate.completion.missingness", "MissingnessGraph"),
            ("wanxiang_substrate.completion.planner", "CompletionPlanner"),
        ],
    },
    {
        "stage": 13,
        "name": "Completion Candidate E0-E5",
        "probes": [
            ("wanxiang_substrate.ledger.ledger", "CompletionLedger"),
            ("wanxiang_substrate.completion.candidates", "CompletionCandidate"),
        ],
    },
    {
        "stage": 14,
        "name": "Consistency / Constraint Validation",
        "probes": [("wanxiang_substrate.completion.consistency", "ConsistencySolver")],
    },
    {
        "stage": 15,
        "name": "Scenario Candidate / Genesis Plan",
        "probes": [
            ("wanxiang_substrate.sources.canon", "ScenarioPoint"),
            ("wanxiang_substrate.genesis.plan", "GenesisPlan"),
        ],
    },
    {
        "stage": 16,
        "name": "WorldPackageDraft",
        "probes": [
            ("wanxiang_substrate.packages.model", "PackageManifest"),
            ("wanxiang_substrate.draft.package", "WorldPackageDraft"),
        ],
    },
    {
        "stage": 17,
        "name": "Preview Instance",
        "probes": [
            ("wanxiang_substrate.living.runtime", "instantiate_scenarios"),
            ("wanxiang_substrate.preview.scope", "PreviewScope"),
        ],
    },
    {
        "stage": 18,
        "name": "Worldness Evaluation",
        "probes": [
            ("wanxiang_substrate.living.runtime", "WORLDNESS_CLASSES"),
            ("wanxiang_substrate.worldness.evaluator", "WorldnessEvaluator"),
        ],
    },
    {
        "stage": 19,
        "name": "Repair Proposal / Completion Loop",
        "probes": [
            ("wanxiang_substrate.worldness.repair", "RepairProposal"),
            ("wanxiang_substrate.worldness.repair", "RecompileLoop"),
        ],
    },
    {
        "stage": 20,
        "name": "Publishable WorldPackage",
        "probes": [
            ("wanxiang_substrate.release.readiness", "ReleaseGates"),
            ("wanxiang_substrate.worldpack.assembler", "GenesisSpec"),
        ],
    },
    {
        "stage": 21,
        "name": "Living World Instance",
        "probes": [
            ("wanxiang_application.world_runtime", "WorldRuntime"),
            ("wanxiang_substrate.living.runtime", "ScenarioInstance"),
        ],
    },
)
CLOSURE_GOALS: dict[int, tuple[str, ...]] = {
    3: ("G55D", "G55E", "G55F", "G55G"),
    4: ("G56A", "G56B"),
    5: ("G56C", "G56D"),
    6: ("G57A", "G57B", "G57C", "G57D", "G57E", "G57F", "G57G", "G57H"),
    7: ("G57A", "G58A"),
    8: ("G63A", "G64B", "G57C"),
    9: ("G58B", "G58D", "G64C", "G64E"),
    10: ("G59A", "G59B", "G59C", "G66A", "G66B", "G66C"),
    11: ("G59D", "G59E"),
    12: ("G59E", "G67A", "G67B"),
    13: ("G58E", "G58F"),
    14: ("G67F", "G67G"),
    15: ("G59F", "G68A", "G68F"),
    16: ("G60B", "G60C"),
    17: ("G60E", "G60F", "G60G"),
    18: ("G69A", "G69B"),
    19: ("G69C", "G69D", "G69E", "G69F"),
    20: ("G60C", "G73G"),
    21: ("G72E",),
}


def _probe(module_name: str, symbol: str) -> bool:
    try:
        module = importlib.import_module(module_name)
    except Exception:  # noqa: BLE001
        return False
    return hasattr(module, symbol)


@dataclass(frozen=True, slots=True)
class StageStatus:
    stage: int
    name: str
    status: str
    present: tuple[str, ...]
    missing: tuple[str, ...]
    closure_goals: tuple[str, ...]


def build_graph() -> tuple[StageStatus, ...]:
    results: list[StageStatus] = []
    for spec in PIPELINE_STAGES:
        present: list[str] = []
        missing: list[str] = []
        for module_name, symbol in spec["probes"]:
            if _probe(module_name, symbol):
                present.append(f"{module_name}.{symbol}")
            else:
                missing.append(f"{module_name}.{symbol}")
        if present and not missing:
            status = "EXISTS"
        elif present:
            status = "PARTIAL"
        else:
            status = "MISSING"
        results.append(
            StageStatus(
                stage=int(spec["stage"]),
                name=str(spec["name"]),
                status=status,
                present=tuple(present),
                missing=tuple(missing),
                closure_goals=CLOSURE_GOALS.get(int(spec["stage"]), ()),
            )
        )
    return tuple(results)


def collect_goal_ids() -> set[str]:
    pattern = re.compile(r"^G(\d+)([A-Z])_")
    ids: set[str] = set()
    for path in (ROOT / "goals").glob("*.md"):
        match = pattern.match(path.name)
        if match and 54 <= int(match.group(1)) <= 73:
            ids.add(f"G{int(match.group(1))}{match.group(2)}")
    return ids


def validate(graph: tuple[StageStatus, ...], goal_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for status in graph:
        if status.status != "EXISTS" and not status.closure_goals:
            errors.append(f"stage {status.stage} ({status.name}) has no closure goals")
        for goal in status.closure_goals:
            if goal not in goal_ids:
                errors.append(f"stage {status.stage} references unknown goal {goal}")
    return errors


def stage_payload(status: StageStatus) -> dict[str, object]:
    """JSON-safe stage payload (tuples -> lists)."""
    return {
        "stage": status.stage,
        "name": status.name,
        "status": status.status,
        "present": list(status.present),
        "missing": list(status.missing),
        "closure_goals": list(status.closure_goals),
    }


def main() -> int:
    graph = build_graph()
    goal_ids = collect_goal_ids()
    errors = validate(graph, goal_ids)
    payload = {
        "graph": "G54C Source->Living World capability/gap graph",
        "stages": [stage_payload(s) for s in graph],
        "closure_goal_count": len(goal_ids),
        "errors": errors,
        "verdict": "PASS" if not errors else "FAIL",
    }
    out = ROOT / "reports" / "forge_gap_graph.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
