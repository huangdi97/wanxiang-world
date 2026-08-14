"""Architecture conformance guard for the Wanxiang monorepo.

Stable command from repository root::

    uv run python scripts/architecture_check.py

Checks (all enforced by `scripts/quality.py`):

1. Forbidden-import boundaries per physical package (domain must stay
   framework-free; ORM/web/LLM leakage is detected).
2. Import cycles between workspace packages (AST-based, on the physical tree).
3. Production file-size report (default target <= 300 lines; generated files
   marked with a header comment are exempt and only reported).
4. Secret scan over tracked code/config (no credentials committed).
5. Placeholder scan over required production paths (TODO/FIXME/placeholder/
   NotImplemented/stub/mock-only markers are rejected there, while docs/tests
   may discuss these words freely).

The module is importable so tests can exercise each rule directly.
"""

from __future__ import annotations

import ast
import dataclasses
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

PRODUCTION_SRC_DIRS = ("packages", "apps")
MAX_PRODUCTION_FILE_LINES = 300

# package dir -> top-level modules a package must never import.
FORBIDDEN_IMPORTS: dict[str, tuple[str, ...]] = {
    "packages/domain": (
        "fastapi",
        "sqlalchemy",
        "alembic",
        "wanxiang_api",
        "httpx",
        "requests",
        "openai",
        "pydantic",
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

SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r'(?i)(password|passwd|secret|api[_-]?key|token)\s*[=:]\s*"[^"]{6,}"'),
    re.compile(r"(?i)(password|passwd|secret|api[_-]?key|token)\s*[=:]\s*'[^']{6,}'"),
)

PLACEHOLDER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bTODO\b"),
    re.compile(r"\bFIXME\b"),
    re.compile(r"\bXXX\b"),
    re.compile(r"\bNotImplemented\b"),
    re.compile(r"\bplaceholder\b", re.IGNORECASE),
    re.compile(r"\bstub\b", re.IGNORECASE),
    re.compile(r"\bmock[- ]only\b", re.IGNORECASE),
)

GENERATED_MARKERS = ("# generated", "@generated", r"\[generated\]")

SECRET_SCAN_EXTENSIONS = {".py", ".toml", ".yaml", ".yml", ".json", ".env", ".example"}
SKIP_DIRS = {".git", ".venv", ".uv-cache", "node_modules", "dist", ".pytest_cache", "reports"}


@dataclasses.dataclass(frozen=True, slots=True)
class Violation:
    kind: str
    path: str
    line: int | None
    message: str

    def format(self) -> str:
        location = f"{self.path}:{self.line}" if self.line is not None else self.path
        return f"[{self.kind}] {location}: {self.message}"


def _package_src_dirs(root: pathlib.Path) -> list[pathlib.Path]:
    """Collect production source directories: packages/*/src and apps/*/src."""
    dirs: list[pathlib.Path] = []
    for parent_name in PRODUCTION_SRC_DIRS:
        parent = root / parent_name
        if not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            src = child / "src"
            if src.is_dir():
                dirs.append(src)
    return dirs


def _iter_python_files(src_dirs: list[pathlib.Path]) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for src in src_dirs:
        files.extend(sorted(src.rglob("*.py")))
    return files


def _is_skipped(path: pathlib.Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def scan_forbidden_imports(root: pathlib.Path = ROOT) -> list[Violation]:
    violations: list[Violation] = []
    for package_dir, forbidden in FORBIDDEN_IMPORTS.items():
        base = root / package_dir
        if not base.is_dir():
            continue
        for py in sorted(base.rglob("*.py")):
            if _is_skipped(py):
                continue
            if package_dir == "apps/api" and py.name == "app.py":
                # app.py is the composition root: it legitimately wires adapters.
                continue
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split(".")[0]
                        if top in forbidden:
                            violations.append(
                                Violation(
                                    "forbidden-import",
                                    str(py.relative_to(root)),
                                    node.lineno,
                                    f"{top} forbidden in {package_dir}",
                                )
                            )
                elif isinstance(node, ast.ImportFrom) and node.module:
                    top = node.module.split(".")[0]
                    if top in forbidden:
                        violations.append(
                            Violation(
                                "forbidden-import",
                                str(py.relative_to(root)),
                                node.lineno,
                                f"{top} forbidden in {package_dir}",
                            )
                        )
    return violations


def _import_edges(root: pathlib.Path, src_dirs: list[pathlib.Path]) -> dict[str, set[str]]:
    """Map package distribution name -> set of package names it imports."""
    edges: dict[str, set[str]] = {}
    for src in src_dirs:
        package_name = f"wanxiang_{src.parent.name}"
        edges.setdefault(package_name, set())
        for py in src.rglob("*.py"):
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split(".")[0]
                        if top.startswith("wanxiang_") and top != package_name:
                            edges[package_name].add(top)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    top = node.module.split(".")[0]
                    if top.startswith("wanxiang_") and top != package_name:
                        edges[package_name].add(top)
    return edges


def detect_import_cycles(root: pathlib.Path = ROOT) -> list[Violation]:
    src_dirs = _package_src_dirs(root)
    edges = _import_edges(root, src_dirs)
    violations: list[Violation] = []

    def visit(start: str, path: list[str]) -> None:
        for nxt in sorted(edges.get(start, set())):
            if nxt in path:
                cycle = path[path.index(nxt) :] + [nxt]
                violations.append(Violation("import-cycle", start, None, " -> ".join(cycle)))
                continue
            visit(nxt, path + [nxt])

    for start in sorted(edges):
        visit(start, [start])

    seen: set[str] = set()
    unique: list[Violation] = []
    for v in violations:
        if v.message not in seen:
            seen.add(v.message)
            unique.append(v)
    return unique


def scan_file_sizes(
    root: pathlib.Path = ROOT, max_lines: int = MAX_PRODUCTION_FILE_LINES
) -> list[Violation]:
    violations: list[Violation] = []
    src_dirs = _package_src_dirs(root)
    for py in _iter_python_files(src_dirs):
        text = py.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) <= max_lines:
            continue
        if any(marker in text for marker in GENERATED_MARKERS):
            continue
        violations.append(
            Violation(
                "file-size",
                str(py.relative_to(root)),
                None,
                f"{len(lines)} lines exceeds target {max_lines}",
            )
        )
    return violations


def _tracked_code_files(root: pathlib.Path) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for parent_name in PRODUCTION_SRC_DIRS:
        parent = root / parent_name
        if not parent.is_dir():
            continue
        for py in parent.rglob("*.py"):
            if not _is_skipped(py):
                files.append(py)
    config_names = (
        "pyproject.toml",
        ".env.example",
        "docker-compose.yml",
        ".github/workflows/ci.yml",
    )
    for name in config_names:
        p = root / name
        if p.is_file():
            files.append(p)
    return files


def scan_secrets(root: pathlib.Path = ROOT) -> list[Violation]:
    violations: list[Violation] = []
    for path in _tracked_code_files(root):
        if path.suffix not in SECRET_SCAN_EXTENSIONS and path.name != ".env.example":
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for idx, line in enumerate(lines, start=1):
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                violations.append(
                    Violation("secret", str(path.relative_to(root)), idx, "possible secret value")
                )
    return violations


def scan_placeholders(root: pathlib.Path = ROOT) -> list[Violation]:
    violations: list[Violation] = []
    src_dirs = _package_src_dirs(root)
    for py in _iter_python_files(src_dirs):
        text = py.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            # `return NotImplemented` is the standard rich-comparison idiom
            # (__lt__/__le__/__gt__/__ge__ signalling "not comparable") and is
            # not a placeholder; everything else is scanned across ALL marker
            # patterns (first non-None match), not only the first pattern.
            if line.strip() == "return NotImplemented":
                continue
            matched = next(
                (
                    m
                    for pattern in PLACEHOLDER_PATTERNS
                    for m in [pattern.search(line)]
                    if m is not None
                ),
                None,
            )
            if matched is not None:
                violations.append(
                    Violation(
                        "placeholder",
                        str(py.relative_to(root)),
                        idx,
                        f"placeholder marker {matched.group(0)!r} in production path",
                    )
                )
    return violations


def run_all(root: pathlib.Path = ROOT) -> list[Violation]:
    checks = (
        scan_forbidden_imports(root),
        detect_import_cycles(root),
        scan_file_sizes(root),
        scan_secrets(root),
        scan_placeholders(root),
    )
    return [violation for check in checks for violation in check]


def main(argv: list[str] | None = None) -> int:
    _ = argv
    violations = run_all(ROOT)
    if not violations:
        print("Architecture conformance: PASS")
        return 0
    for violation in violations:
        print(violation.format())
    print(f"Architecture conformance: FAIL ({len(violations)} violation(s))")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
