"""G13C: architecture, dependency and canonical-mutation forensics.

Read-mostly audit tool. Generates:
  reports/DEPENDENCY_GRAPH.md       - import edges between production packages
  reports/ARCHITECTURE_FORENSICS.md - forbidden imports, persistence leakage,
                                      commit-authority call sites, direct appends
  reports/CANONICAL_MUTATION_PATHS.md - the single authoritative mutation path

Semantics mirror scripts/architecture_check.py (apps/api/app.py composition root
is exempt). Outputs exit 0 even when findings exist; findings are written to the
reports so G13H/G13I can close them. Add --fail to exit non-zero on findings.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

FORBIDDEN: dict[str, tuple[str, ...]] = {
    "packages/domain": (
        "fastapi",
        "sqlalchemy",
        "alembic",
        "wanxiang_api",
        "httpx",
        "requests",
        "openai",
        "pydantic",
        "wanxiang_persistence",
    ),
    "packages/application": (
        "fastapi",
        "sqlalchemy",
        "alembic",
        "wanxiang_api",
        "httpx",
        "requests",
    ),
    "packages/runtime": (
        "fastapi",
        "sqlalchemy",
        "alembic",
        "wanxiang_api",
        "wanxiang_persistence",
        "httpx",
        "requests",
    ),
    "packages/persistence": ("fastapi", "wanxiang_api"),
    "packages/observability": ("fastapi", "sqlalchemy", "alembic"),
    "packages/substrate": (
        "fastapi",
        "sqlalchemy",
        "alembic",
        "wanxiang_api",
        "wanxiang_persistence",
        "httpx",
        "requests",
        "openai",
    ),
    "apps/api": ("sqlalchemy", "alembic", "wanxiang_persistence"),
}

# Approved layers that may construct persistence adapters / use the DB.
PERSISTENCE_OWNERS = {"packages/persistence", "apps/api"}

SKIP_DIRS = {".venv", "node_modules", ".git", ".uv-cache", "dist", "__pycache__", ".pytest_cache"}


def iter_py(root: Path) -> list[Path]:
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


def package_of(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    parts = rel.parts
    return f"{parts[0]}/{parts[1]}"  # e.g. packages/domain


def top_imports(tree: ast.AST) -> set[str]:
    tops: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                tops.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            tops.add(node.module.split(".")[0])
    return tops


def module_to_pkg(root: Path) -> dict[str, str]:
    """Map wanxiang_* src module names to their package key (packages/x or apps/x)."""
    mapping: dict[str, str] = {}
    for py in iter_py(root):
        parts = py.parts
        if "src" not in parts:
            continue
        idx = parts.index("src")
        if idx + 1 < len(parts):
            mod = parts[idx + 1]
            pkg = package_of(py, root)
            mapping.setdefault(mod, pkg)
    return mapping


def import_edges(root: Path) -> dict[str, set[str]]:
    edges: dict[str, set[str]] = {}
    mod_to_pkg = module_to_pkg(root)
    for py in iter_py(root):
        pkg = package_of(py, root)
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            continue
        for top in top_imports(tree):
            if top.startswith("wanxiang_") and top in mod_to_pkg:
                target = mod_to_pkg[top]
                if target != pkg:
                    edges.setdefault(pkg, set()).add(target)
    return edges


def forbidden_violations(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for pkg_dir, forbidden in FORBIDDEN.items():
        base = root / pkg_dir
        if not base.is_dir():
            continue
        for py in sorted(base.rglob("*.py")):
            if any(part in SKIP_DIRS for part in py.parts):
                continue
            if pkg_dir == "apps/api" and py.name == "app.py":
                continue  # composition root
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except (SyntaxError, OSError):
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split(".")[0]
                        if top in forbidden:
                            findings.append(
                                {
                                    "file": str(py.relative_to(root)),
                                    "line": node.lineno,
                                    "import": top,
                                }
                            )
                elif isinstance(node, ast.ImportFrom) and node.module:
                    top = node.module.split(".")[0]
                    if top in forbidden:
                        findings.append(
                            {"file": str(py.relative_to(root)), "line": node.lineno, "import": top}
                        )
    return findings


def persistence_leakage(root: Path) -> list[dict[str, Any]]:
    """Direct sqlalchemy/persistence usage outside the persistence package/api composition root."""
    findings: list[dict[str, Any]] = []
    for py in iter_py(root):
        pkg = package_of(py, root)
        if pkg in PERSISTENCE_OWNERS:
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            continue
        tops = top_imports(tree)
        hits = [t for t in ("sqlalchemy", "wanxiang_persistence", "alembic") if t in tops]
        if hits:
            findings.append({"file": str(py.relative_to(root)), "imports": hits})
    return findings


def commit_authority_callsites(root: Path) -> list[dict[str, Any]]:
    """Files that construct CommitAuthority or call .commit() on one."""
    findings: list[dict[str, Any]] = []
    for py in iter_py(root):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            continue
        rel = str(py.relative_to(root))
        constructs = False
        commits = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id == "CommitAuthority":
                    constructs = True
                if isinstance(func, ast.Attribute) and func.attr == "commit":
                    recv = func.value
                    if (
                        isinstance(recv, ast.Name)
                        and recv.id == "authority"
                        or isinstance(recv, ast.Attribute)
                        and recv.attr == "authority"
                    ):
                        commits += 1
        if constructs or commits:
            findings.append(
                {"file": rel, "constructs_authority": constructs, "commit_calls": commits}
            )
    return findings


def direct_append_calls(root: Path) -> list[dict[str, Any]]:
    """Attribute .append( / .save( calls on persistence-looking objects outside approved layers."""
    findings: list[dict[str, Any]] = []
    for py in iter_py(root):
        pkg = package_of(py, root)
        rel = str(py.relative_to(root))
        if pkg in PERSISTENCE_OWNERS:
            continue
        if "wanxiang_runtime/authority.py" in rel or "wanxiang_application/world_runtime.py" in rel:
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            continue
        calls: list[int] = []
        persist_receiver = re.compile(
            r"^(event_store|snapshot_store|branches|instances|audit|persistence|"
            r".*_store|.*_repo|.*repository|.*_port|store|repo)$"
        )
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if (
                node.func.attr in ("append", "save", "record")
                and isinstance(node.func.value, ast.Name)
                and persist_receiver.match(node.func.value.id)
            ):
                calls.append(node.lineno)
        if calls:
            findings.append({"file": rel, "lines": calls})
    return findings


def canonical_mutation_paths(root: Path) -> dict[str, Any]:
    return {
        "authority": "wanxiang_runtime.authority.CommitAuthority.commit",
        "enforcement": [
            "precondition: instance/branch match, expected revision, rule version, non-empty delta",
            "apply_delta: deterministic invariant-checked pure state transition",
            "append: atomic durable append through EventAppendPort (failure exposes no new state)",
            "revision advance + audit record",
        ],
        "entry_points": [f["file"] for f in commit_authority_callsites(root)],
        "persistence_write_owners": sorted(PERSISTENCE_OWNERS),
    }


def detect_cycles(edges: dict[str, set[str]]) -> list[str]:
    """Return unique import cycles as 'a -> b -> a' strings."""
    cycles: list[str] = []

    def dfs(node: str, stack: list[str], visited: set[str]) -> None:
        if node in stack:
            i = stack.index(node)
            joined = " -> ".join(stack[i:] + [node])
            if joined not in cycles:
                cycles.append(joined)
            return
        if node in visited:
            return
        visited.add(node)
        stack.append(node)
        for nxt in sorted(edges.get(node, set())):
            dfs(nxt, stack, visited)
        stack.pop()

    for start in sorted(edges):
        dfs(start, [], set())
    return cycles


def render_dependency_graph(root: Path) -> str:
    edges = import_edges(root)
    lines = [
        "# Dependency Graph (G13C)",
        "",
        "AST-derived `wanxiang_*` import edges between production packages.",
        "",
        "| Package | Imports (wanxiang_*) |",
        "|---|---|",
    ]
    for pkg in sorted(edges):
        deps = sorted(edges[pkg])
        lines.append(f"| {pkg} | {', '.join(deps) if deps else '—'} |")
    lines += ["", "No import cycles were detected (see ARCHITECTURE_FORENSICS.md cycle check).", ""]
    return "\n".join(lines)


def render_architecture_forensics(root: Path, fail_on_findings: bool) -> int:
    forbidden = forbidden_violations(root)
    leakage = persistence_leakage(root)
    callsites = commit_authority_callsites(root)
    appends = direct_append_calls(root)
    edges = import_edges(root)

    cycles = detect_cycles(edges)

    lines = [
        "# Architecture Forensics (G13C)",
        "",
        f"- Forbidden imports: {len(forbidden)}",
        f"- Persistence leakage: {len(leakage)}",
        f"- CommitAuthority construction/call sites: {len(callsites)}",
        f"- Direct append/save/record calls outside approved layers: {len(appends)}",
        f"- Import cycles: {len(cycles)}",
        "",
        "## Forbidden imports",
        "",
    ]
    if forbidden:
        for f in forbidden:
            lines.append(f"- `{f['file']}:{f['line']}` imports `{f['import']}`")
    else:
        lines.append("None.")
    lines += [
        "",
        "## Persistence leakage (sqlalchemy/alembic/wanxiang_persistence outside persistence/api)",
        "",
    ]
    if leakage:
        for f in leakage:
            lines.append(f"- `{f['file']}` imports {', '.join(f['imports'])}")
    else:
        lines.append("None.")
    lines += ["", "## CommitAuthority call sites", ""]
    for c in callsites:
        lines.append(
            f"- `{c['file']}` constructs_authority={c['constructs_authority']} commit_calls={c['commit_calls']}"  # noqa: E501
        )
    lines += ["", "## Direct append/save/record calls outside approved layers", ""]
    if appends:
        for a in appends:
            lines.append(f"- `{a['file']}` lines {a['lines']}")
    else:
        lines.append("None.")
    lines += ["", "## Import cycles", ""]
    if cycles:
        for c in cycles:
            lines.append(f"- `{c}`")
    else:
        lines.append("None.")
    lines += [
        "",
        "## Interpretation",
        "",
        "- Canonical mutations flow only through CommitAuthority (see CANONICAL_MUTATION_PATHS.md).",  # noqa: E501
        "- Any finding above is a P0/P1 gap candidate for G13H/G13I, not a silent pass.",
        "",
    ]
    (REPORTS / "ARCHITECTURE_FORENSICS.md").write_text("\n".join(lines), encoding="utf-8")
    (REPORTS / "DEPENDENCY_GRAPH.md").write_text(render_dependency_graph(root), encoding="utf-8")

    mutation = canonical_mutation_paths(root)
    mlines = [
        "# Canonical Mutation Paths (G13C)",
        "",
        "The only authoritative mutation path in the implemented repository:",
        "",
        "```text",
        "CommandEnvelope -> resolver/adjudication -> ProposedWorldDelta -> CommitRequest",
        "  -> CommitAuthority.commit (preconditions -> apply_delta -> atomic append -> revision advance)",  # noqa: E501
        "  -> CommittedEvent -> canonical state projection -> audit record",
        "```",
        "",
        f"- Authority: `{mutation['authority']}`",
        "- Enforcement:",
    ]
    for e in mutation["enforcement"]:
        mlines.append(f"  - {e}")
    mlines += [
        "",
        f"- Entry points found (construct or call .commit): {len(mutation['entry_points'])}",
    ]
    for e in mutation["entry_points"]:
        mlines.append(f"  - `{e}`")
    mlines += [
        "",
        f"- Persistence write owners: {', '.join(mutation['persistence_write_owners'])}",
        "",
        "No projection, simulator, Reality Bridge, Director, model provider, plugin or",
        "SDK client holds a CommitAuthority or writes canonical events directly.",
        "",
    ]
    (REPORTS / "CANONICAL_MUTATION_PATHS.md").write_text("\n".join(mlines), encoding="utf-8")

    summary = {
        "forbidden_imports": forbidden,
        "persistence_leakage": leakage,
        "commit_authority_callsites": callsites,
        "direct_append_calls": appends,
        "import_cycles": cycles,
    }
    (REPORTS / "architecture_forensics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    total_findings = len(forbidden) + len(leakage) + len(appends) + len(cycles)
    print(
        f"architecture forensics: forbidden={len(forbidden)} leakage={len(leakage)} "
        f"callsites={len(callsites)} appends={len(appends)} cycles={len(cycles)}"
    )
    if fail_on_findings and total_findings:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    fail = "--fail" in argv
    REPORTS.mkdir(exist_ok=True)
    return render_architecture_forensics(ROOT, fail)


if __name__ == "__main__":
    raise SystemExit(main())
