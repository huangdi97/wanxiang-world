"""V5.1 code-minimality metrics.

Computes coarse metrics for the minimal-core ledger:
- production LOC by top-level package (packages/*/src + apps/api/src)
- public class/function names per package
- names matching registry/manager/service/engine (potential consolidation targets)
- total files
Deterministic and reusable across Goals; results are recorded manually in
reports/V5_1_CODE_MINIMALITY_LEDGER.md and consumed by
scripts/v52_minimality_budget.py.
"""

from __future__ import annotations

import ast
import pathlib
from typing import TypedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent


class PkgStats(TypedDict):
    files: int
    loc: int
    classes: int
    functions: int
    public_names: list[str]
    flag_names: list[str]


class Metrics(TypedDict):
    per_pkg: dict[str, PkgStats]
    rows: list[tuple[str, int, int, int, int, int, int]]
    total: dict[str, int]
    flag_rows: list[tuple[str, str]]


def package_label(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) >= 3 and parts[0] == "packages":
        return f"packages/{parts[1]}"
    if len(parts) >= 2 and parts[0] == "apps":
        return f"apps/{parts[1]}"
    return str(rel)


def _empty_stats() -> PkgStats:
    return PkgStats(
        files=0,
        loc=0,
        classes=0,
        functions=0,
        public_names=[],
        flag_names=[],
    )


def compute_metrics(root: pathlib.Path) -> Metrics:
    """Compute the deterministic code-minimality metrics (reusable)."""
    per_pkg: dict[str, PkgStats] = {}
    for base in (root / "packages", root / "apps"):
        if not base.exists():
            continue
        for py in sorted(base.rglob("*.py")):
            if "__pycache__" in py.parts:
                continue
            label = package_label(py)
            pkg = per_pkg.setdefault(label, _empty_stats())
            pkg["files"] += 1
            try:
                text = py.read_text(encoding="utf-8")
                tree = ast.parse(text)
            except (OSError, SyntaxError):
                continue
            pkg["loc"] += len(text.splitlines())
            for node in tree.body:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = node.name
                    if name.startswith("_"):
                        continue
                    if isinstance(node, ast.ClassDef):
                        pkg["classes"] += 1
                    else:
                        pkg["functions"] += 1
                    pkg["public_names"].append(name)
                    low = name.lower()
                    if any(k in low for k in ("registry", "manager", "service", "engine")):
                        pkg["flag_names"].append(name)

    total: dict[str, int] = {"files": 0, "loc": 0, "classes": 0, "functions": 0}
    rows: list[tuple[str, int, int, int, int, int, int]] = []
    for label in sorted(per_pkg):
        pkg = per_pkg[label]
        total["files"] += pkg["files"]
        total["loc"] += pkg["loc"]
        total["classes"] += pkg["classes"]
        total["functions"] += pkg["functions"]
        rows.append(
            (
                label,
                pkg["files"],
                pkg["loc"],
                pkg["classes"],
                pkg["functions"],
                len(pkg["public_names"]),
                len(pkg["flag_names"]),
            )
        )
    flag_rows = [(label, name) for label, pkg in per_pkg.items() for name in pkg["flag_names"]]
    return {"per_pkg": per_pkg, "rows": rows, "total": total, "flag_rows": flag_rows}


def main() -> int:
    metrics = compute_metrics(ROOT)
    rows = metrics["rows"]
    total = metrics["total"]
    flag_rows = metrics["flag_rows"]
    header = (
        f"{'package':<20} {'files':>4} {'loc':>5} "
        f"{'classes':>6} {'funcs':>5} {'pub':>4} {'flags':>4}"
    )
    print(header)
    row_fmt = "{:<20} {:>4} {:>5} {:>6} {:>5} {:>4} {:>4}"
    for r in rows:
        print(row_fmt.format(*r))
    tot_line = (
        f"{'TOTAL':<20} {total['files']:>4} {total['loc']:>5} "
        f"{total['classes']:>6} {total['functions']:>5}"
    )
    print(tot_line)
    print("\nFlagged names (registry/manager/service/engine):")
    for label, name in sorted(flag_rows):
        print(f"  {label}: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
