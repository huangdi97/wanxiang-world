"""G34A: Kernel/Runtime/Forge/Experiences responsibility boundary conformance."""

from __future__ import annotations

import ast
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOUNDARY_DOC = ROOT / "docs" / "architecture" / "V5_2_KERNEL_RUNTIME_FORGE_EXPERIENCES.md"

# The ONLY production classes/functions with "Engine" in the name.
ALLOWED_ENGINE_NAMES = {
    "ReplayEngine",
    "PlannerEngine",
    "create_engine_for",
}


def _prod_py() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for base in (ROOT / "packages", ROOT / "apps"):
        for py in base.rglob("*.py"):
            if "__pycache__" in py.parts:
                continue
            files.append(py)
    return files


@pytest.mark.architecture
def test_boundary_doc_exists_and_import_rules_documented() -> None:
    text = BOUNDARY_DOC.read_text(encoding="utf-8")
    for keyword in ("Kernel", "Runtime", "Forge", "Experiences", "No-God-Engine"):
        assert keyword in text


@pytest.mark.architecture
def test_no_new_god_engine() -> None:
    found: set[str] = set()
    for py in _prod_py():
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if "Engine" in node.name:
                    found.add(node.name)
            elif isinstance(node, ast.FunctionDef) and "engine" in node.name.lower():
                found.add(node.name)
    assert found == ALLOWED_ENGINE_NAMES, (
        f"unexpected engine-named abstractions: {found - ALLOWED_ENGINE_NAMES}"
    )  # noqa: E501


@pytest.mark.architecture
def test_kernel_does_not_import_runtime_forge_web_orm() -> None:
    import re

    kernel_dirs = ("packages/domain/src", "packages/runtime/src")
    for py in _prod_py():
        rel = py.as_posix()
        if not any(rel.startswith(d) for d in kernel_dirs):
            continue
        text = py.read_text(encoding="utf-8")
        imports = chr(10).join(
            ln for ln in text.splitlines() if ln.strip().startswith(("import ", "from "))
        )
        for forbidden in (
            "wanxiang_application",
            "wanxiang_api",
            "fastapi",
            "sqlalchemy",
            "wanxiang_persistence",
            "wanxiang_substrate",
        ):
            assert not re.search(rf"\b{forbidden}\b", imports), (
                f"Kernel must not import {forbidden}: {rel}"
            )
