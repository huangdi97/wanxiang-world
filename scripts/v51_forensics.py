"""V5.1 duplicate-abstraction forensics scanner (G21C).

Deterministic inventory of architecture duplication candidates:
- registries / catalogs
- state models (canonical/current/read)
- append/audit stores
- managers/services/engines
- ports (Protocol) vs implementations
- oversized modules (>300 lines)
- canonical mutation paths (CommitAuthority usage)

Output is written to reports/V5_1_DUPLICATE_FORENSICS.md and printed to stdout.
"""

from __future__ import annotations

import ast
import pathlib
import re
from typing import TypedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCAN_DIRS = [ROOT / "packages", ROOT / "apps"]
OUT = ROOT / "reports" / "V5_1_DUPLICATE_FORENSICS.md"
SIZE_LIMIT = 300


class Item(TypedDict):
    path: str
    name: str
    line: int


class Oversized(TypedDict):
    path: str
    loc: int
    limit: int


KIND_PATTERNS: dict[str, re.Pattern[str]] = {
    "registry": re.compile(r"^(.*)(registry|catalog)$", re.IGNORECASE),
    "state": re.compile(r"^(.*)(state|snapshot|readmodel|read_model|projection)$", re.IGNORECASE),
    "store": re.compile(r"^(.*)(store|ledger|eventlog|event_log|stream|journal)$", re.IGNORECASE),
    "service": re.compile(r"^(.*)(service|manager)$", re.IGNORECASE),
    "engine": re.compile(r"^(.*)engine$", re.IGNORECASE),
}


def kind_of(name: str) -> str | None:
    for kind, pat in KIND_PATTERNS.items():
        if pat.match(name):
            return kind
    return None


def collect() -> tuple[dict[str, list[Item]], list[Oversized]]:
    found: dict[str, list[Item]] = {}
    oversized: list[Oversized] = []
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for py in sorted(base.rglob("*.py")):
            if "__pycache__" in py.parts:
                continue
            rel = py.relative_to(ROOT).as_posix()
            try:
                src = py.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            tree = ast.parse(src)
            loc = len(src.splitlines())
            if loc > SIZE_LIMIT:
                oversized.append(Oversized(path=rel, loc=loc, limit=SIZE_LIMIT))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    kind = kind_of(node.name)
                    if kind:
                        found.setdefault(f"{kind}_classes", []).append(
                            Item(path=rel, name=node.name, line=node.lineno)
                        )
                if (
                    isinstance(node, ast.FunctionDef)
                    and node.name == "commit"
                    and ("authority" in rel.lower() or "authority" in node.name.lower())
                ):
                    found.setdefault("commit_paths", []).append(
                        Item(path=rel, name=node.name, line=node.lineno)
                    )
                if isinstance(node, ast.ClassDef):
                    bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                    if "Protocol" in bases or "ABC" in bases:
                        found.setdefault("ports", []).append(
                            Item(path=rel, name=node.name, line=node.lineno)
                        )
    return found, oversized


def render(found: dict[str, list[Item]], oversized: list[Oversized]) -> str:
    lines = ["# V5.1 Duplicate-Abstraction Forensics (G21C)", ""]
    lines.append("> Deterministic AST scan. Groups: registry/catalog, state models, stores,")
    lines.append("> services/managers, engines, ports, oversized modules, commit paths.")
    order = [
        "registry_classes",
        "state_classes",
        "store_classes",
        "service_classes",
        "engine_classes",
        "ports",
        "oversized_modules",
        "commit_paths",
    ]
    for key in order:
        if key == "oversized_modules":
            lines.append(f"## oversized_modules ({len(oversized)})")
            lines.append("")
            if not oversized:
                lines.append("(none)")
            else:
                lines.append("| path | loc | limit |")
                lines.append("|---|---|---|")
                for o in oversized:
                    lines.append(f"| {o['path']} | {o['loc']} | {o['limit']} |")
            lines.append("")
            continue
        items = found.get(key, [])
        lines.append(f"## {key} ({len(items)})")
        lines.append("")
        if not items:
            lines.append("(none)")
            lines.append("")
            continue
        lines.append("| path | name | line |")
        lines.append("|---|---|---|")
        for it in items:
            lines.append(f"| {it['path']} | {it['name']} | {it['line']} |")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    found, oversized = collect()
    OUT.write_text(render(found, oversized), encoding="utf-8")
    print(OUT.relative_to(ROOT))
    for key in sorted(found):
        print(f"  {key}: {len(found[key])}")
    print(f"  oversized_modules: {len(oversized)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
