"""V5.1 package dependency graph report (G21D).

Deterministic AST-based scan of import edges between workspace packages.
Writes reports/V5_1_PACKAGE_DEPENDENCY_GRAPH.md and prints the edge list.
"""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "V5_1_PACKAGE_DEPENDENCY_GRAPH.md"

# physical package dir -> logical v5.1 target responsibility
TARGETS: dict[str, str] = {
    "packages/domain": "core",
    "packages/runtime": "core",
    "packages/application": "application (orchestration facade)",
    "packages/substrate": "definition+runtime+agency+experience (modular monolith substrate)",
    "packages/persistence": "infrastructure (persistence)",
    "packages/observability": "infrastructure (telemetry)",
    "packages/research": "EXPERIMENTAL (research namespace)",
    "apps/api": "infrastructure (API composition root)",
    "packages/sdk_ts": "infrastructure (TS SDK, generated contract)",
}

IMPORT_RE = re.compile(
    r"^\s*(?:from|import)\s+(wanxiang_[a-z_]+|wanxiang_api)(?:\s|\.|$)",
    re.MULTILINE,
)


def package_of(path: pathlib.Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    parts = rel.split("/")
    if len(parts) >= 2 and parts[0] in ("packages", "apps"):
        return f"{parts[0]}/{parts[1]}"
    return None


def collect_edges() -> dict[str, set[str]]:
    edges: dict[str, set[str]] = {}
    for base in (ROOT / "packages", ROOT / "apps"):
        if not base.exists():
            continue
        for child in sorted(base.iterdir()):
            src = child / "src"
            if not src.is_dir():
                continue
            pkg = package_of(src)
            if pkg is None:
                continue
            edges.setdefault(pkg, set())
            for py in sorted(src.rglob("*.py")):
                if "__pycache__" in py.parts:
                    continue
                text = py.read_text(encoding="utf-8")
                for m in IMPORT_RE.finditer(text):
                    imported = m.group(1)
                    target_pkg = None
                    for cand, _ in TARGETS.items():
                        ns = cand.split("/")[-1]
                        if imported == f"wanxiang_{ns}":
                            target_pkg = cand
                            break
                    if target_pkg and target_pkg != pkg:
                        edges[pkg].add(target_pkg)
    return edges


def render(edges: dict[str, set[str]]) -> str:
    lines = ["# V5.1 Package Dependency Graph (G21D)", ""]
    lines.append("> Deterministic AST edge scan (package -> imported package).")
    lines.append("")
    lines.append("| package | target responsibility | imports |")
    lines.append("|---|---|---|")
    for pkg in sorted(edges):
        targets = ", ".join(sorted(edges[pkg])) if edges[pkg] else "(none)"
        lines.append(f"| {pkg} | {TARGETS.get(pkg, '?')} | {targets} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    edges = collect_edges()
    OUT.write_text(render(edges), encoding="utf-8")
    print(OUT.relative_to(ROOT))
    for pkg in sorted(edges):
        print(f"  {pkg}: {', '.join(sorted(edges[pkg])) if edges[pkg] else '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
