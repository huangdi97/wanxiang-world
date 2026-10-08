"""Kernel v1 change guard (G38C).

Scans the Kernel packages (domain/runtime) for:
1. Forbidden domain proper nouns (Red Chamber etc.) - domain names must never
   enter Kernel.
2. New direct mutation paths: canonical-state mutation (.apply / apply_delta)
   in production code outside the runtime state internals and CommitAuthority.
3. ABI drift: the committed kernel v1 ABI golden must match the current ABI.

Returns exit code 0 when clean; prints violations otherwise.
"""

from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent
KERNEL_ROOTS = (ROOT / "packages/domain", ROOT / "packages/runtime")
SUBSTRATE_ROOT = ROOT / "packages/substrate"
FORBIDDEN_DOMAIN_NAMES = (
    "林黛玉",
    "贾宝玉",
    "潇湘馆",
    "怡红院",
    "红楼梦",
    "贾府",
    "太虚幻境",
    "荣国府",
    "red_chamber",
)
MUTATION_ALIASES = ("apply_delta",)
MUTATION_METHODS = (".apply(", ".with_revision(")
# Runtime state internals that legitimately implement mutation.
ALLOWED_MUTATION_FILES = (
    "packages/runtime/src/wanxiang_runtime/state.py",
    "packages/runtime/src/wanxiang_runtime/invariants.py",
    "packages/runtime/src/wanxiang_runtime/authority.py",
)
# Vetted pure dry-run / policy applications on the IMMUTABLE canonical state
# (InMemoryCanonicalState.apply derives a new state; never mutates in place).
# New mutation-looking calls outside this list are flagged for review.
# resolution/service.py: dry-run delta validation before commit.
# capability/resolver.py: LearningPolicy.apply(delta, current) policy application.
ALLOWED_PURE_APPLY = (
    "packages/substrate/src/wanxiang_substrate/resolution/service.py",
    "packages/substrate/src/wanxiang_substrate/capability/resolver.py",
    # ActorGoalStack and RelationshipGraph are immutable projection replay
    # records; they never hold or mutate canonical runtime state.
    "packages/substrate/src/wanxiang_substrate/actor_continuity/goal_stack.py",
    "packages/substrate/src/wanxiang_substrate/actor_continuity/relationship_graph.py",
)


@dataclass(frozen=True, slots=True)
class GuardViolation:
    kind: str
    path: str
    line: int
    detail: str


def scan_domain_names(
    roots: tuple[pathlib.Path, ...] = KERNEL_ROOTS, *, root: pathlib.Path = ROOT
) -> tuple[GuardViolation, ...]:
    violations: list[GuardViolation] = []
    for base in roots:
        for py in base.rglob("*.py"):
            text = py.read_text(encoding="utf-8")
            for index, line in enumerate(text.splitlines(), start=1):
                for name in FORBIDDEN_DOMAIN_NAMES:
                    if name in line:
                        violations.append(
                            GuardViolation(
                                "domain_name_in_kernel",
                                str(py.relative_to(root)),
                                index,
                                f"forbidden domain name {name!r}",
                            )
                        )
    return tuple(violations)


def scan_direct_mutation(
    root: pathlib.Path = SUBSTRATE_ROOT, *, workspace_root: pathlib.Path = ROOT
) -> tuple[GuardViolation, ...]:
    violations: list[GuardViolation] = []
    for py in root.rglob("*.py"):
        rel = str(py.relative_to(workspace_root)).replace("\\", "/")
        if any(rel.startswith(prefix) for prefix in ALLOWED_MUTATION_FILES):
            continue
        if rel in ALLOWED_PURE_APPLY:
            continue
        text = py.read_text(encoding="utf-8")
        for index, line in enumerate(text.splitlines(), start=1):
            lowered = line.strip()
            if lowered.startswith(("#", '"""', "//")):
                continue
            if "def " in line or "class " in line:
                continue
            if any(alias in line for alias in MUTATION_ALIASES):
                violations.append(
                    GuardViolation(
                        "direct_mutation_path",
                        rel,
                        index,
                        "canonical-state mutation alias outside authority",
                    )
                )
            if any(method in line for method in MUTATION_METHODS):
                violations.append(
                    GuardViolation(
                        "direct_mutation_path",
                        rel,
                        index,
                        "state mutation call outside CommitAuthority",
                    )
                )
    return tuple(violations)


def scan_abi_drift() -> tuple[GuardViolation, ...]:
    golden_path = ROOT / "reports" / "kernel_v1_abi_golden.json"
    if not golden_path.exists():
        return (
            GuardViolation("abi_drift", "reports/kernel_v1_abi_golden.json", 1, "golden missing"),
        )
    try:
        from wanxiang_substrate.kernel.abi import abi_golden
    except Exception as exc:  # noqa: BLE001
        return (GuardViolation("abi_drift", "kernel/abi", 1, str(exc)),)
    committed = json.loads(golden_path.read_text(encoding="utf-8"))
    current = abi_golden()
    if committed != current:
        return (
            GuardViolation(
                "abi_drift",
                "kernel/abi",
                1,
                "kernel v1 ABI drifted from committed golden; review required",
            ),
        )
    return ()


def run() -> tuple[GuardViolation, ...]:
    return scan_domain_names() + scan_direct_mutation() + scan_abi_drift()


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    violations = run()
    for violation in violations:
        print(f"{violation.kind}: {violation.path}:{violation.line} - {violation.detail}")
    print(f"kernel guard: {len(violations)} violation(s)")
    sys.exit(1 if violations else 0)
