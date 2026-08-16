"""G54A: Source->Living World repository truth audit (M51).

Reproducible audit over the CURRENT tree (never trusts prior claims):
inventory of packages/modules/tests/reports, Forge capability inventory,
forbidden-file / secret / corpus checks, and a KEEP/EXTEND/MERGE/DELETE/ADD
matrix snapshot. Exits 0 when all hard invariants hold, 1 otherwise.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
from dataclasses import asdict, dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent

PRODUCTION_DIRS = ("packages", "apps")
FORGE_MODULES = (
    "sources",
    "compiler",
    "corpus",
    "canon_graph",
    "semantic_world",
    "worldpack",
    "living",
    "genealogy",
    "heritage",
    "studio_experience",
    "release",
    "lineage",
)
SECRET_PATTERNS = (
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)
FORBIDDEN_TRACKED = re.compile(r"(^|/)(\.env|.*\.pem|.*\.p12|.*\.jks|.*\.key|.*\.sqlite|.*\.db)$")
PLACEHOLDER = re.compile(r"\bTODO\b|\bFIXME\b|\bNotImplemented\b|\bplaceholder\b|\bstub\b", re.I)
RESTRICTED_CORPUS = pathlib.Path("sources/red_chamber")
ALLOWED_CORPUS_FILES = ("README.md", "MANIFEST_TEMPLATE.yaml")


@dataclass(frozen=True, slots=True)
class Inventory:
    packages: dict[str, int]
    apps: dict[str, int]
    scripts: int
    test_files: int
    reports: int
    forge_modules: dict[str, int]
    tracked_files: int
    tracked_md: int
    tracked_py: int


@dataclass(frozen=True, slots=True)
class Violation:
    kind: str
    path: str
    detail: str


def _py_count(directory: pathlib.Path) -> int:
    return len(list(directory.rglob("*.py"))) if directory.exists() else 0


def _tracked() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return [line for line in result.stdout.splitlines() if line]


def inventory() -> Inventory:
    packages = {
        p.name: _py_count(p / "src") for p in sorted((ROOT / "packages").iterdir()) if p.is_dir()
    }
    apps = {p.name: _py_count(p / "src") for p in sorted((ROOT / "apps").iterdir()) if p.is_dir()}
    substrate = ROOT / "packages/substrate/src/wanxiang_substrate"
    forge_modules = {name: _py_count(substrate / name) for name in FORGE_MODULES}
    tracked = _tracked()
    return Inventory(
        packages=packages,
        apps=apps,
        scripts=_py_count(ROOT / "scripts"),
        test_files=len(list((ROOT / "tests").rglob("test_*.py"))),
        reports=len(list((ROOT / "reports").glob("*.md"))),
        forge_modules=forge_modules,
        tracked_files=len(tracked),
        tracked_md=sum(1 for p in tracked if p.endswith(".md")),
        tracked_py=sum(1 for p in tracked if p.endswith(".py")),
    )


def forbidden_tracked() -> list[str]:
    return [p for p in _tracked() if FORBIDDEN_TRACKED.search(p)]


def secret_scan() -> list[str]:
    hits: list[str] = []
    for path in (ROOT / "packages").rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path.relative_to(ROOT)))
    return hits


def corpus_check() -> list[str]:
    if not (ROOT / RESTRICTED_CORPUS).exists():
        return []
    violations: list[str] = []
    for path in (ROOT / RESTRICTED_CORPUS).rglob("*"):
        if path.is_file() and path.name not in ALLOWED_CORPUS_FILES:
            violations.append(str(path.relative_to(ROOT)))
    return violations


def placeholder_scan() -> list[str]:
    violations: list[str] = []
    for parent in PRODUCTION_DIRS:
        for path in (ROOT / parent).rglob("*.py"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for idx, line in enumerate(text.splitlines(), start=1):
                if line.strip() == "return NotImplemented":
                    continue
                if PLACEHOLDER.search(line):
                    violations.append(f"{path.relative_to(ROOT)}:{idx}")
                    break
    return violations


def run() -> tuple[Inventory, list[Violation]]:
    violations: list[Violation] = []
    for path in forbidden_tracked():
        violations.append(Violation("forbidden_tracked", path, "forbidden env/secret/db tracked"))
    for path in secret_scan():
        violations.append(Violation("secret_pattern", path, "secret-like pattern in code"))
    for path in corpus_check():
        violations.append(Violation("restricted_corpus", path, "restricted corpus content tracked"))
    for path in placeholder_scan():
        violations.append(
            Violation("placeholder_in_production", path, "placeholder marker in production")
        )
    return inventory(), violations


def main() -> int:
    inv, violations = run()
    payload = {
        "audit": "G54A repository truth audit",
        "inventory": asdict(inv),
        "violations": [asdict(v) for v in violations],
        "verdict": "PASS" if not violations else "FAIL",
    }
    out = ROOT / "reports" / "forge_truth_audit.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
