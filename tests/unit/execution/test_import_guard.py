"""No commit path from the execution fabric: import guard over the package."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "packages" / "execution" / "src" / "wanxiang_execution"
)
FORBIDDEN_MODULE_PREFIXES = ("wanxiang_runtime", "wanxiang_substrate", "wanxiang_persistence")
FORBIDDEN_IMPORT_NAME_PARTS = ("commit", "authority")


def _source_files() -> list[Path]:
    return sorted(PACKAGE_ROOT.rglob("*.py"))


def _imported_module_names(source: str) -> list[str]:
    names: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names.append(node.module)
    return names


def test_execution_package_has_no_commit_or_state_imports() -> None:
    files = _source_files()
    assert files, f"no package sources found at {PACKAGE_ROOT}"

    for path in files:
        text = path.read_text(encoding="utf-8")
        for prefix in FORBIDDEN_MODULE_PREFIXES:
            assert prefix not in text, f"{path.name} references {prefix}"
        for imported in _imported_module_names(text):
            lowered = imported.lower()
            assert not any(part in lowered for part in FORBIDDEN_IMPORT_NAME_PARTS), (
                f"{path.name} imports {imported!r}"
            )


def test_execution_package_only_imports_stdlib_and_itself() -> None:
    for path in _source_files():
        for imported in _imported_module_names(path.read_text(encoding="utf-8")):
            top_level = imported.split(".")[0]
            assert top_level in sys.stdlib_module_names or top_level == "wanxiang_execution", (
                f"{path.name} imports non-stdlib module {imported!r}"
            )
