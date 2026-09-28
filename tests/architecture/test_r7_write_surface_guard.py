"""R7 Gate C: static write-surface guard.

Facts enforced here so a new module cannot quietly join a credential-bearing set:

- only `apps/api` (composition root) and the persistence adapters import
  `wanxiang_persistence`;
- only the authority mint pathway references `mint_canonical_write_lease`;
- the modules that reference `CommitAuthority` are a frozen golden set;
- packages that must never hold a canonical write handle reference neither
  `wanxiang_persistence`, `mint_canonical_write_lease` nor `mintCapability`;
- the runtime write-surface inventory script returns `PASS` on this tree.

Every set is asserted exactly (drift fails), not merely bounded.
"""

from __future__ import annotations

import ast
import pathlib
from collections.abc import Callable

import pytest
from scripts.r7_write_surface_inventory import build

ROOT = pathlib.Path(__file__).resolve().parents[2]

_SKIP_DIRS = {
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

# Golden set: production modules importing `wanxiang_persistence`.
PERSISTENCE_IMPORTERS = (
    "apps/api/src/wanxiang_api/app.py",
    "packages/persistence/src/wanxiang_persistence/__init__.py",
    "packages/persistence/src/wanxiang_persistence/audit_repository.py",
    "packages/persistence/src/wanxiang_persistence/branch_repository.py",
    "packages/persistence/src/wanxiang_persistence/event_store.py",
    "packages/persistence/src/wanxiang_persistence/instance_repository.py",
    "packages/persistence/src/wanxiang_persistence/lineage_repository.py",
    "packages/persistence/src/wanxiang_persistence/snapshot_store.py",
)

# Golden set: production modules referencing `CommitAuthority` (imports, calls or
# the class definition itself), i.e. the documented authority wiring modules.
COMMIT_AUTHORITY_REFERENCES = (
    "packages/application/src/wanxiang_application/world_runtime.py",
    "packages/runtime/src/wanxiang_runtime/__init__.py",
    "packages/runtime/src/wanxiang_runtime/authority.py",
    "packages/runtime/src/wanxiang_runtime/isa_pipeline.py",
    "packages/substrate/src/wanxiang_substrate/evolution/institution_promotion.py",
    "packages/substrate/src/wanxiang_substrate/rc001/chaos.py",
    "packages/substrate/src/wanxiang_substrate/rc001/instantiate.py",
)

# Golden set: the mint/brand core. `authority.py` is the sole production caller of
# the minter, `canonical_write.py` defines it, `lease_core.py` is the brand core.
MINT_ALLOWED = (
    "packages/runtime/src/wanxiang_runtime/authority.py",
    "packages/runtime/src/wanxiang_runtime/canonical_write.py",
    "packages/runtime/src/wanxiang_runtime/internal/lease_core.py",
)

# Packages (and the R7 harness modules) that may never hold a write handle.
FORBIDDEN_PREFIXES = (
    "packages/foundry/",
    "packages/execution/",
    "packages/reality/",
    "packages/substrate/",
    "packages/application/",
    "packages/observability/",
    "packages/research/",
)
FORBIDDEN_RUNTIME_MODULES = (
    "packages/runtime/src/wanxiang_runtime/r7_agent_harness.py",
    "packages/runtime/src/wanxiang_runtime/r7_agent_harness_contract.py",
)


def _production_python_modules() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for parent in ("packages", "apps"):
        base = ROOT / parent
        if base.is_dir():
            files.extend(
                p for p in base.rglob("*.py") if not any(part in _SKIP_DIRS for part in p.parts)
            )
    return sorted(files)


def _parse(path: pathlib.Path) -> ast.Module | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return None


def _imported_modules(tree: ast.Module) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _referenced_names(tree: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.ImportFrom):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
    return names


def _rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _modules_where(predicate: Callable[[ast.Module], bool]) -> set[str]:
    result: set[str] = set()
    for path in _production_python_modules():
        tree = _parse(path)
        if tree is not None and predicate(tree):
            result.add(_rel(path))
    return result


@pytest.mark.architecture
def test_persistence_package_is_imported_only_by_adapters_and_composition_root() -> None:
    importers = _modules_where(
        lambda tree: any(m.split(".")[0] == "wanxiang_persistence" for m in _imported_modules(tree))
    )
    assert importers == set(PERSISTENCE_IMPORTERS)
    assert all(
        rel.startswith("apps/api/") or rel.startswith("packages/persistence/") for rel in importers
    )


@pytest.mark.architecture
def test_only_the_authority_mint_path_references_the_minter() -> None:
    mint_references = _modules_where(
        lambda tree: "mint_canonical_write_lease" in _referenced_names(tree)
    )
    lease_core_importers = _modules_where(
        lambda tree: "wanxiang_runtime.internal.lease_core" in _imported_modules(tree)
    )
    assert mint_references | lease_core_importers | {MINT_ALLOWED[2]} == set(MINT_ALLOWED)
    assert mint_references == {MINT_ALLOWED[0], MINT_ALLOWED[1]}


@pytest.mark.architecture
def test_commit_authority_references_are_a_frozen_golden_set() -> None:
    references = _modules_where(lambda tree: "CommitAuthority" in _referenced_names(tree))
    assert references == set(COMMIT_AUTHORITY_REFERENCES)


@pytest.mark.architecture
def test_guarded_packages_hold_no_canonical_write_credential() -> None:
    guarded = [
        path
        for path in _production_python_modules()
        if _rel(path).startswith(FORBIDDEN_PREFIXES) or _rel(path) in FORBIDDEN_RUNTIME_MODULES
    ]
    assert guarded
    for path in guarded:
        rel = _rel(path)
        tree = _parse(path)
        assert tree is not None
        assert not any(
            module.split(".")[0] == "wanxiang_persistence" for module in _imported_modules(tree)
        ), f"{rel} imports wanxiang_persistence"
        names = _referenced_names(tree)
        assert "mint_canonical_write_lease" not in names, f"{rel} references the minter"
        assert "mintCapability" not in names, f"{rel} references mintCapability"


@pytest.mark.architecture
def test_write_surface_inventory_passes() -> None:
    report = build()
    assert report["schema"] == "wanxiang.r7.security.write-surface-inventory.v1"
    assert report["verdict"] == "PASS"
