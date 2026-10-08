"""R7 Gate C: repository-wide canonical write-surface inventory (Python + TS).

Deterministic AST scan (regex is used only to match imports / TS text, never to
guess Python structure) that classifies every module able to reach a canonical
write implementation, so a new writer cannot join the surface unnoticed.

Roles:
- TEST            test code (excluded from violations but still listed)
- COMPOSITION_ROOT `apps/api` wiring root
- INFRASTRUCTURE  the persistence adapters themselves
- TRANSPORT       presents/carries a credential but cannot mint one
- AUTHORITY       may hold the credential (references the mint or CommitAuthority)
- VIOLATION       a guarded package that reaches a DIRECT write handle

Referencing `CommitAuthority` is the sanctioned path (the authority is where a
canonical mutation is supposed to happen), so it is classified AUTHORITY rather
than VIOLATION; VIOLATION is reserved for a module that can write canonical rows
without going through the authority (persistence import, raw SQLAlchemy session
write, or minting a lease).
"""

from __future__ import annotations

import ast
import json
import pathlib
import re
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = "wanxiang.r7.security.write-surface-inventory.v1"
OUTPUT = ROOT / "artifacts" / "r7" / "security" / "write_surface_inventory.json"

SKIP_DIRS = {
    ".venv",
    "node_modules",
    ".git",
    ".uv-cache",
    "dist",
    "__pycache__",
    ".pytest_cache",
    "reports",
    "artifacts",
}

GUARDED_PACKAGES = (
    "packages/foundry",
    "packages/execution",
    "packages/reality",
    "packages/substrate",
    "packages/application",
    "packages/observability",
    "packages/research",
)

_TS_TRANSPORT = ("packages/cordis_host/src/bridge.ts",)
_PY_TRANSPORT = ("packages/reality/src/wanxiang_reality/rpc.py",)
_APPEND_RECEIVERS = frozenset({"event_store", "event_port", "_event_port", "_store", "store"})
_SESSION_RECEIVERS = frozenset({"session", "_session"})
_TS_MARKERS = ("mintCapability", "commitThroughAuthority", "HistoryService", "RpcHistoryProvider")
_TS_APPEND = re.compile(r"\.append\(")


@dataclass(frozen=True, slots=True)
class Finding:
    path: str
    language: str
    role: str
    triggers: tuple[str, ...]


def _skipped(path: pathlib.Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def _iter_python() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for parent in ("packages", "apps", "tests", "scripts"):
        base = ROOT / parent
        if base.is_dir():
            files.extend(p for p in base.rglob("*.py") if not _skipped(p))
    return sorted(files)


def _iter_typescript() -> list[pathlib.Path]:
    base = ROOT / "packages" / "cordis_host" / "src"
    if not base.is_dir():
        return []
    return sorted(p for p in base.rglob("*.ts") if not _skipped(p))


def _python_triggers(path: pathlib.Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return set()
    triggers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                triggers |= _import_trigger(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            triggers |= _import_trigger(node.module.split(".")[0])
        elif isinstance(node, ast.Name):
            triggers |= _name_trigger(node.id)
        elif isinstance(node, ast.Attribute):
            triggers |= _attribute_trigger(node)
    return triggers


def _import_trigger(top: str) -> set[str]:
    if top == "wanxiang_persistence":
        return {"imports wanxiang_persistence"}
    if top == "sqlalchemy":
        return {"imports sqlalchemy"}
    return set()


def _name_trigger(name: str) -> set[str]:
    if name == "CommitAuthority":
        return {"references CommitAuthority"}
    if name == "mint_canonical_write_lease":
        return {"mints canonical write lease"}
    if name == "require_canonical_write_lease":
        return {"requires canonical write lease"}
    return set()


def _attribute_trigger(node: ast.Attribute) -> set[str]:
    receiver = node.value.id if isinstance(node.value, ast.Name) else None
    if node.attr in {"add", "commit"} and receiver in _SESSION_RECEIVERS:
        return {"sqlalchemy session write"}
    if node.attr == "append" and receiver in _APPEND_RECEIVERS:
        return {"appends to event store"}
    return set()


def _typescript_triggers(path: pathlib.Path) -> set[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return set()
    triggers = {f"mentions {marker}" for marker in _TS_MARKERS if marker in text}
    if _TS_APPEND.search(text):
        triggers.add("appends to a history provider")
    return triggers


def _is_test(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("tests/"):
        return True
    name = path.name
    return name.startswith("test_") or name.endswith("_test.py") or name.endswith(".test.ts")


def _in_guarded_package(rel: str) -> bool:
    if any(rel.startswith(pkg + "/") for pkg in GUARDED_PACKAGES):
        return True
    return rel.startswith("packages/runtime/src/wanxiang_runtime/r7_agent_harness")


def _direct_write(triggers: set[str]) -> bool:
    return bool(
        triggers
        & {
            "imports wanxiang_persistence",
            "sqlalchemy session write",
            "mints canonical write lease",
        }
    )


def _role(rel: str, triggers: set[str]) -> str:
    if _is_test(ROOT / rel):
        return "TEST"
    if rel.startswith("packages/persistence/"):
        return "INFRASTRUCTURE"
    if rel.startswith("apps/api/"):
        return "COMPOSITION_ROOT"
    if rel in _TS_TRANSPORT or rel in _PY_TRANSPORT:
        return "TRANSPORT"
    if triggers & {
        "references CommitAuthority",
        "mints canonical write lease",
        "requires canonical write lease",
    }:
        return "AUTHORITY"
    if _direct_write(triggers) and _in_guarded_package(rel):
        return "VIOLATION"
    return "AUTHORITY" if triggers else "NONE"


def scan() -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_python():
        triggers = _python_triggers(path)
        if not triggers:
            continue
        rel = path.relative_to(ROOT).as_posix()
        findings.append(Finding(rel, "python", _role(rel, triggers), tuple(sorted(triggers))))
    for path in _iter_typescript():
        triggers = _typescript_triggers(path)
        if not triggers:
            continue
        rel = path.relative_to(ROOT).as_posix()
        findings.append(Finding(rel, "typescript", _role(rel, triggers), tuple(sorted(triggers))))
    return sorted(findings, key=lambda f: (f.role, f.path))


def _summary(findings: list[Finding]) -> str:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.role] = counts.get(finding.role, 0) + 1
    roles = ", ".join(f"{role}={counts[role]}" for role in sorted(counts))
    return f"write-surface inventory: {len(findings)} module(s); {roles}"


def build() -> dict[str, object]:
    findings = scan()
    violations = [f for f in findings if f.role == "VIOLATION"]
    return {
        "schema": SCHEMA,
        "verdict": "VIOLATION" if violations else "PASS",
        "counts": {
            role: sum(1 for f in findings if f.role == role)
            for role in sorted({f.role for f in findings})
        },
        "modules": [
            {
                "path": f.path,
                "language": f.language,
                "role": f.role,
                "triggers": list(f.triggers),
            }
            for f in findings
        ],
    }


def main(argv: list[str] | None = None) -> int:
    _ = argv
    report = build()
    findings = scan()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(_summary(findings))
    print(f"artifact: {OUTPUT.relative_to(ROOT).as_posix()}")
    for finding in findings:
        if finding.role == "VIOLATION":
            print(f"  VIOLATION {finding.path}: {', '.join(finding.triggers)}")
    if report["verdict"] != "PASS":
        print("R7 write-surface inventory: FAIL")
        return 1
    print("R7 write-surface inventory: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
