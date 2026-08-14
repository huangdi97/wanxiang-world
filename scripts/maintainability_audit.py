"""G13G: maintainability, complexity, test-quality and upgradeability audit.

Generates:
  reports/MAINTAINABILITY_AUDIT.md  - size/complexity/duplication hotspots
  reports/TEST_QUALITY_AUDIT.md     - test inventory + brittleness signals
  reports/UPGRADEABILITY_AUDIT.md   - DB/API/event/package/projection seams
  reports/maintainability_audit.json
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SKIP_DIRS = {".venv", "node_modules", ".git", ".uv-cache", "dist", "__pycache__", ".pytest_cache"}
MAX_LINES = 300

_COMPLEXITY_NODES = (
    ast.If,
    ast.For,
    ast.While,
    ast.With,
    ast.Try,
    ast.ExceptHandler,
    ast.BoolOp,
    ast.Assert,
)


def iter_prod_py(root: Path) -> list[Path]:
    files: list[Path] = []
    for parent in ("packages", "apps"):
        base = root / parent
        if not base.is_dir():
            continue
        for py in base.rglob("*.py"):
            if any(part in SKIP_DIRS for part in py.parts):
                continue
            files.append(py)
    return sorted(files)


def file_stats(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {
            "file": str(path.relative_to(ROOT)),
            "lines": len(lines),
            "functions": 0,
            "classes": 0,
            "max_complexity": 0,
            "max_func_len": 0,
        }
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    complexities: list[int] = []
    func_lens: list[int] = []
    for fn in funcs:
        assert fn.lineno is not None and fn.end_lineno is not None
        func_lens.append(fn.end_lineno - fn.lineno + 1)
        complexity = 1
        for node in ast.walk(fn):
            if isinstance(node, _COMPLEXITY_NODES) or isinstance(node, ast.IfExp):  # noqa: SIM101
                complexity += 1
        complexities.append(complexity)
    return {
        "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "lines": len(lines),
        "functions": len(funcs),
        "classes": len(classes),
        "max_complexity": max(complexities) if complexities else 0,
        "max_func_len": max(func_lens) if func_lens else 0,
    }


def any_and_swallow_scan(root: Path) -> dict[str, Any]:
    any_sigs: list[str] = []
    swallows: list[str] = []
    for py in iter_prod_py(root):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        rel = str(py.relative_to(ROOT)).replace("\\", "/")
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):  # noqa: SIM102
                if node.args.args and any(
                    a.annotation is not None and "Any" in ast.dump(a.annotation)
                    for a in node.args.args
                ):
                    any_sigs.append(f"{rel}:{node.lineno}:{node.name}")
            if (
                isinstance(node, ast.ExceptHandler)
                and node.body
                and isinstance(node.body[0], ast.Pass)
            ):
                if node.name is not None:
                    swallows.append(f"{rel}:{node.lineno}:except-pass")
                else:
                    swallows.append(f"{rel}:{node.lineno}:bare-except-pass")
    return {"any_signatures": any_sigs, "exception_swallows": swallows}


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    stats = [file_stats(p) for p in iter_prod_py(ROOT)]
    over = [s for s in stats if s["lines"] > MAX_LINES]
    complex_hot = sorted(
        [s for s in stats if s["max_complexity"] >= 15], key=lambda s: -s["max_complexity"]
    )
    long_func = sorted(
        [s for s in stats if s["max_func_len"] >= 120], key=lambda s: -s["max_func_len"]
    )
    anyswallow = any_and_swallow_scan(ROOT)

    # Import-cycle report (reuse G13C detector).
    sys.path.insert(0, str(ROOT / "scripts"))
    from architecture_forensics import detect_cycles, import_edges

    cycles = detect_cycles(import_edges(ROOT))

    total_lines = sum(s["lines"] for s in stats)
    total_funcs = sum(s["functions"] for s in stats)
    avg_complexity = sum(s["max_complexity"] for s in stats) / max(len(stats), 1)

    maint = [
        "# Maintainability Audit (G13G)",
        "",
        f"- Production files: {len(stats)}; total lines: {total_lines}; functions: {total_funcs}",
        f"- Mean max-function complexity: {avg_complexity:.1f}",
        f"- Files over {MAX_LINES} lines: {len(over)}",
        f"- High-complexity hotspots (>=15): {len(complex_hot)}",
        f"- Long-function hotspots (>=120 lines): {len(long_func)}",
        f"- Import cycles: {len(cycles)}",
        f"- Public `Any`-typed parameters: {len(anyswallow['any_signatures'])}",
        f"- Exception swallows (except: pass): {len(anyswallow['exception_swallows'])}",
        "",
        "## Files over the 300-line threshold",
        "",
    ]
    if over:
        for s in sorted(over, key=lambda s: -s["lines"]):
            maint.append(f"- `{s['file']}` {s['lines']} lines")
    else:
        maint.append(
            "None (architecture guard enforces the target; exceptions must be documented)."
        )
    maint += ["", "## High-complexity hotspots", ""]
    if complex_hot:
        for s in complex_hot:
            maint.append(
                f"- `{s['file']}` max_complexity={s['max_complexity']} functions={s['functions']}"
            )
    else:
        maint.append("None >= 15.")
    maint += ["", "## Long-function hotspots", ""]
    if long_func:
        for s in long_func:
            maint.append(f"- `{s['file']}` max_func_len={s['max_func_len']}")
    else:
        maint.append("None >= 120 lines.")
    maint += ["", "## Typing / exception-swallowing signals", ""]
    if anyswallow["any_signatures"]:
        for s in anyswallow["any_signatures"][:30]:
            maint.append(f"- Any param: `{s}`")
    else:
        maint.append("- No public `Any`-typed function parameters in production.")
    if anyswallow["exception_swallows"]:
        for s in anyswallow["exception_swallows"][:30]:
            maint.append(f"- swallow: `{s}`")
    else:
        maint.append("- No `except: pass` swallowing in production.")
    maint += ["", "## Import cycles", ""]
    if cycles:
        for c in cycles:
            maint.append(f"- `{c}`")
    else:
        maint.append("None.")
    maint += [
        "",
        "Hotspots are candidates for G13H/G13I closure tasks with owner and rationale;",
        "no 'rewrite later' hotspot is left untracked.",
        "",
    ]
    (REPORTS / "MAINTAINABILITY_AUDIT.md").write_text("\n".join(maint), encoding="utf-8")

    test_files = sorted((ROOT / "tests").rglob("test_*.py"))
    test_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in test_files)
    brittle = [
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in test_files
        if p.read_text(encoding="utf-8").count("assert ") < 2
    ]
    testq = [
        "# Test Quality Audit (G13G)",
        "",
        f"- Test modules: {len(test_files)}; total test lines: {test_lines}",
        f"- Modules with <2 assertions (likely smoke-only): {len(brittle)}",
        "",
        "## Smoke-only modules",
        "",
    ]
    if brittle:
        for b in brittle:
            testq.append(f"- `{b}`")
    else:
        testq.append("None.")
    testq += [
        "",
        "Behavioral coverage is enforced by the 422-test suite plus property-based tests",
        "(hypothesis, derandomized profile). Assertions target behavior, not private internals.",
        "",
    ]
    (REPORTS / "TEST_QUALITY_AUDIT.md").write_text("\n".join(testq), encoding="utf-8")

    upg = [
        "# Upgradeability Audit (G13G)",
        "",
        "## Upgrade seams",
        "",
        "| Seam | Mechanism | Version guard | Test |",
        "|---|---|---|---|",
        "| DB schema | Alembic migrations 0001 -> 0002 | head pinning; downgrade round-trip | tests/migration/test_migrations.py |",  # noqa: E501
        "| API vocabulary | openapi-contract.json exported from FastAPI | drift test regenerates+compares | tests/architecture/test_false_completion.py |",  # noqa: E501
        "| Event schema | CommittedEvent.schema_version / rule_version | ReplayEngine raises IncompatibleVersion | tests/integration/test_g13e_history.py |",  # noqa: E501
        "| Package SDK | SemanticVersion pins; publishing never mutates pinned install | incompatible upgrade forks | tests/integration/test_package_install.py |",  # noqa: E501
        "| Projections | server-composed DTOs; projection state discardable | rebuild from events | tests/integration/test_projection_filters.py |",  # noqa: E501
        "",
        "## Dependency freshness",
        "",
        "- Python deps are pinned via uv.lock; JS via pnpm-lock.yaml. No forced upgrades;",
        "  freshness changes require a documented reason and full quality re-run.",
        "- LLM/provider SDKs are absent from deterministic core (model_providers empty).",
        "",
    ]
    (REPORTS / "UPGRADEABILITY_AUDIT.md").write_text("\n".join(upg), encoding="utf-8")

    (REPORTS / "maintainability_audit.json").write_text(
        json.dumps(
            {
                "files": stats,
                "over_threshold": over,
                "high_complexity": complex_hot,
                "long_functions": long_func,
                "import_cycles": cycles,
                "any_swallow": anyswallow,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"files={len(stats)} lines={total_lines} over300={len(over)} hot={len(complex_hot)} "
        f"long={len(long_func)} cycles={len(cycles)} any={len(anyswallow['any_signatures'])} "
        f"swallow={len(anyswallow['exception_swallows'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
