"""V5.1 code-minimality metrics.

Computes coarse metrics for the minimal-core ledger:
- production LOC by top-level package (packages/*/src + apps/api/src)
- public class/function names per package
- names matching registry/manager/service/engine (potential consolidation targets)
- total files
Deterministic and reusable across Goals; results are recorded manually in
reports/V5_1_CODE_MINIMALITY_LEDGER.md.
"""

from __future__ import annotations

import ast
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCAN_DIRS = [ROOT / "packages", ROOT / "apps"]


def package_label(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) >= 3 and parts[0] == "packages":
        return f"packages/{parts[1]}"
    if len(parts) >= 2 and parts[0] == "apps":
        return f"apps/{parts[1]}"
    return str(rel)


def main() -> int:
    per_pkg: dict[str, dict] = {}
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for py in sorted(base.rglob("*.py")):
            if "__pycache__" in py.parts:
                continue
            label = package_label(py)
            pkg = per_pkg.setdefault(
                label,
                {
                    "files": 0,
                    "loc": 0,
                    "classes": 0,
                    "functions": 0,
                    "public_names": [],
                    "flag_names": [],
                },
            )
            pkg["files"] += 1
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            pkg["loc"] += len(py.read_text(encoding="utf-8").splitlines())
            for node in tree.body:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = node.name
                    if name.startswith("_"):
                        continue
                    pkg["classes" if isinstance(node, ast.ClassDef) else "functions"] += 1
                    pkg["public_names"].append(name)
                    low = name.lower()
                    if any(k in low for k in ("registry", "manager", "service", "engine")):
                        pkg["flag_names"].append(name)

    total = {"files": 0, "loc": 0, "classes": 0, "functions": 0}
    rows = []
    for label in sorted(per_pkg):
        p = per_pkg[label]
        for k in total:
            total[k] += p[k]
        rows.append(
            (
                label,
                p["files"],
                p["loc"],
                p["classes"],
                p["functions"],
                len(p["public_names"]),
                len(p["flag_names"]),
            )
        )
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
    flag_rows = [(label, n) for label, p in per_pkg.items() for n in p["flag_names"]]
    print("\nFlagged names (registry/manager/service/engine):")
    for label, n in sorted(flag_rows):
        print(f"  {label}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
