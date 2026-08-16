"""G54D: duplicate abstraction scan (M51).

Scans production source for duplicate class names across modules and reports
them. A small, documented allowlist captures intentional same-name types that
serve distinct pipeline concerns (verified by call sites); any NEW duplicate
name outside the allowlist fails the scan so the program never accretes a
second registry/job/candidate/review/package abstraction.

No domain content; pure AST introspection.
"""

from __future__ import annotations

import ast
import json
import pathlib
import sys
from dataclasses import asdict, dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRODUCTION_DIRS = ("packages", "apps")

# Intentional same-name classes that are NOT duplicates (distinct concerns,
# verified by field shapes + call sites; see reports/G54D_REPORT.md).
ALLOWED_DUPLICATE_NAMES: dict[str, tuple[str, ...]] = {
    "AssetGenerator": (
        "packages/research/src/wanxiang_research/generative_assets.py",
        "packages/substrate/src/wanxiang_substrate/assets/foundry.py",
    ),
    "CandidateEnvelope": (
        "packages/substrate/src/wanxiang_substrate/candidates/envelope.py",
        "packages/substrate/src/wanxiang_substrate/evolution/distillation.py",
    ),
    "CanonClaim": (
        "packages/substrate/src/wanxiang_substrate/canon_graph/timeline_canon.py",
        "packages/substrate/src/wanxiang_substrate/sources/canon.py",
    ),
    "CoverageReport": (
        "packages/substrate/src/wanxiang_substrate/canon_graph/timeline_canon.py",
        "packages/substrate/src/wanxiang_substrate/draft/coverage.py",
    ),
    "DeterministicPolicy": (
        "packages/substrate/src/wanxiang_substrate/agency/policy.py",
        "packages/substrate/src/wanxiang_substrate/population/policy.py",
    ),
    "EvidenceLink": (
        "packages/substrate/src/wanxiang_substrate/evidence/binding.py",
        "packages/substrate/src/wanxiang_substrate/sources/model.py",
    ),
    "ReviewDecision": (
        "packages/substrate/src/wanxiang_substrate/ledger/model.py",
        "packages/substrate/src/wanxiang_substrate/review/decisions.py",
    ),
    "Observation": (
        "packages/substrate/src/wanxiang_substrate/observation/model.py",
        "packages/substrate/src/wanxiang_substrate/research/adapters.py",
    ),
    "ObservationFusion": (
        "packages/research/src/wanxiang_research/reality_stream.py",
        "packages/substrate/src/wanxiang_substrate/reality/fusion.py",
    ),
    "Order": (
        "packages/substrate/src/wanxiang_substrate/agency/model.py",
        "packages/substrate/src/wanxiang_substrate/cosim/campaign.py",
    ),
    "RightsDenied": (
        "packages/domain/src/wanxiang_domain/errors.py",
        "packages/substrate/src/wanxiang_substrate/sources/errors.py",
    ),
    "RightsEnvelope": (
        "packages/domain/src/wanxiang_domain/rights.py",
        "packages/substrate/src/wanxiang_substrate/sources/model.py",
    ),
    "ValidityEnvelope": (
        "packages/research/src/wanxiang_research/sim_federation.py",
        "packages/substrate/src/wanxiang_substrate/reality/experiment.py",
    ),
}


@dataclass(frozen=True, slots=True)
class DuplicateName:
    name: str
    modules: tuple[str, ...]
    allowed: bool


def scan(root: pathlib.Path = ROOT) -> tuple[DuplicateName, ...]:
    class_names: dict[str, list[str]] = {}
    for parent in PRODUCTION_DIRS:
        for py in (root / parent).rglob("*.py"):
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            rel = str(py.relative_to(root)).replace("\\", "/")
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_names.setdefault(node.name, []).append(rel)
    duplicates: list[DuplicateName] = []
    for name, modules in sorted(class_names.items()):
        if len(modules) < 2:
            continue
        allowed = tuple(modules) == ALLOWED_DUPLICATE_NAMES.get(name)
        if not allowed and name in ALLOWED_DUPLICATE_NAMES:
            allowed = tuple(modules) == ALLOWED_DUPLICATE_NAMES[name]
        duplicates.append(DuplicateName(name=name, modules=tuple(modules), allowed=allowed))
    return tuple(duplicates)


def main() -> int:
    duplicates = scan()
    payload = {
        "scan": "G54D duplicate abstraction scan",
        "duplicates": [asdict(d) for d in duplicates],
        "unallowed": [d.name for d in duplicates if not d.allowed],
        "verdict": "PASS" if all(d.allowed for d in duplicates) else "FAIL",
    }
    out = ROOT / "reports" / "duplicate_abstraction_scan.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if any(not d.allowed for d in duplicates) else 0


if __name__ == "__main__":
    sys.exit(main())
