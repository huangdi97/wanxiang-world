"""GOAL_00B: architecture guard rule tests.

Positive tests verify the current tree is clean; negative tests feed synthetic
sources to the guard rules to prove forbidden imports, cycles, secrets and
placeholders are actually detected.
"""

from __future__ import annotations

import pathlib
import shutil
import uuid
from collections.abc import Iterator

import pytest
from scripts.architecture_check import (
    ROOT,
    detect_import_cycles,
    scan_file_sizes,
    scan_forbidden_imports,
    scan_placeholders,
    scan_secrets,
)


@pytest.mark.architecture
def test_current_tree_has_no_forbidden_imports() -> None:
    assert scan_forbidden_imports(ROOT) == []


@pytest.mark.architecture
def test_current_tree_has_no_import_cycles() -> None:
    assert detect_import_cycles(ROOT) == []


@pytest.mark.architecture
def test_current_tree_files_within_size_target() -> None:
    assert scan_file_sizes(ROOT) == []


@pytest.mark.architecture
def test_current_tree_has_no_committed_secrets() -> None:
    assert scan_secrets(ROOT) == []


@pytest.mark.architecture
def test_current_tree_has_no_production_placeholders() -> None:
    assert scan_placeholders(ROOT) == []


ROOT_FOR_TMP = pathlib.Path(__file__).resolve().parents[2]
_ARCH_TMP = ROOT_FOR_TMP / "tests" / "_arch_tmp"


def _write_tree(files: dict[str, str]) -> pathlib.Path:
    """Create a synthetic source tree under a workspace-local tmp dir.

    Workspace-local (default ACLs) instead of pytest's system-temp basetemp,
    because sandboxed Windows ACLs on mode-0700 dirs are not re-listable.
    """
    tmp = _ARCH_TMP / uuid.uuid4().hex
    tmp.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        target = tmp / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return tmp


@pytest.fixture(autouse=True)
def _clean_arch_tmp() -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    yield
    if _ARCH_TMP.is_dir():
        for child in _ARCH_TMP.iterdir():
            shutil.rmtree(child, ignore_errors=True)


@pytest.mark.architecture
def test_forbidden_import_rule_detects_fastapi_in_domain() -> None:
    tree = _write_tree(
        {
            "packages/domain/src/wanxiang_domain/__init__.py": "",
            "packages/domain/src/wanxiang_domain/model.py": "from fastapi import APIRouter\n",
        },
    )
    violations = scan_forbidden_imports(tree)
    assert any(v.kind == "forbidden-import" and "fastapi" in v.message for v in violations)


@pytest.mark.architecture
def test_forbidden_import_rule_detects_sqlalchemy_in_runtime() -> None:
    tree = _write_tree(
        {
            "packages/runtime/src/wanxiang_runtime/__init__.py": "",
            "packages/runtime/src/wanxiang_runtime/commit.py": "import sqlalchemy  # noqa\n",
        },
    )
    violations = scan_forbidden_imports(tree)
    assert any(v.kind == "forbidden-import" and "sqlalchemy" in v.message for v in violations)


@pytest.mark.architecture
def test_substrate_forbidden_import_rule() -> None:
    tree = _write_tree(
        {
            "packages/substrate/src/wanxiang_substrate/__init__.py": "",
            "packages/substrate/src/wanxiang_substrate/evil.py": "import sqlalchemy  # noqa\n",
        },
    )
    violations = scan_forbidden_imports(tree)
    assert any(v.kind == "forbidden-import" and "sqlalchemy" in v.message for v in violations)


@pytest.mark.architecture
def test_import_cycle_detection() -> None:
    tree = _write_tree(
        {
            "packages/domain/src/wanxiang_domain/__init__.py": "import wanxiang_application\n",
            "packages/application/src/wanxiang_application/__init__.py": "import wanxiang_domain\n",
        },
    )
    violations = detect_import_cycles(tree)
    assert any(v.kind == "import-cycle" for v in violations)


@pytest.mark.architecture
def test_secret_scan_detects_api_key() -> None:
    # The fake key is assembled at runtime so the repository-wide CI secret
    # grep does not flag this intentional secret-detection fixture. The temp
    # file read by scan_secrets still contains the full contiguous fake key,
    # so the guard behavior under test is unchanged.
    fake_key = "sk-" + "0123456789abcdef" + "0123456789abcdef"
    tree = _write_tree(
        {
            "packages/domain/src/wanxiang_domain/__init__.py": "",
            "packages/domain/src/wanxiang_domain/config.py": (f'API_KEY = "{fake_key}"\n'),
        },
    )
    violations = scan_secrets(tree)
    assert any(v.kind == "secret" for v in violations)


@pytest.mark.architecture
def test_placeholder_scan_detects_todo_in_production() -> None:
    tree = _write_tree(
        {
            "packages/domain/src/wanxiang_domain/__init__.py": "",
            "packages/domain/src/wanxiang_domain/thing.py": (
                "# TODO: implement later\ndef f() -> int:\n    return 1\n"
            ),
        },
    )
    violations = scan_placeholders(tree)
    assert any(v.kind == "placeholder" and "TODO" in v.message for v in violations)


@pytest.mark.architecture
def test_file_size_scan_detects_oversized_file() -> None:
    lines = "\n".join(f"x{i} = {i}" for i in range(400))
    tree = _write_tree(
        {
            "packages/domain/src/wanxiang_domain/__init__.py": "",
            "packages/domain/src/wanxiang_domain/big.py": lines + "\n",
        },
    )
    violations = scan_file_sizes(tree)
    assert any(v.kind == "file-size" for v in violations)


@pytest.mark.architecture
def test_placeholder_scan_allows_notimplementederror() -> None:
    tree = _write_tree(
        {
            "packages/domain/src/wanxiang_domain/__init__.py": "",
            "packages/domain/src/wanxiang_domain/base.py": (
                "class Base:\n    def f(self) -> int:\n        raise NotImplementedError\n"
            ),
        },
    )
    assert scan_placeholders(tree) == []
