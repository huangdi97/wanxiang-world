"""G17B: package authoring CLI, scaffolder & schema validation.

- A generated package passes baseline schema/conformance without manual repair.
- Invalid manifests produce actionable errors.
- The scaffold has no dependency on Wanxiang internal modules (public SDK only).
"""

from __future__ import annotations

import pathlib
import uuid
from collections.abc import Iterator

import pytest
from scripts.wxpack import dry_run_build, scaffold, validate

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
TMP = ROOT / "tests" / "_arch_tmp"


@pytest.fixture
def workdir() -> Iterator[pathlib.Path]:
    d = TMP / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield d
    for p in d.rglob("*"):
        if p.is_file():
            try:  # noqa: SIM105
                p.unlink()
            except OSError:
                pass
    try:  # noqa: SIM105
        d.rmdir()
    except OSError:
        pass


def test_generated_package_passes_conformance_without_manual_repair(
    workdir: pathlib.Path,
) -> None:
    pkg_dir = scaffold(workdir, "demo-domain", "domain", "Demo Domain")
    assert pkg_dir.exists()
    # Validate: no actionable errors.
    assert validate(workdir, "demo-domain") == []
    # Dry-run build through the public installer.
    result = dry_run_build(workdir, "demo-domain")
    assert result["lock_hash"]
    # The generated test passes (baseline conformance).
    import subprocess

    env = dict(__import__("os").environ)
    env["UV_CACHE_DIR"] = str(ROOT / ".uv-cache")
    proc = subprocess.run(
        ["uv", "run", "pytest", "-q", "test_package.py"],
        cwd=pkg_dir,
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_invalid_manifest_produces_actionable_errors(workdir: pathlib.Path) -> None:
    pkg_dir = scaffold(workdir, "demo-domain", "domain", "Demo Domain")
    # Corrupt the generated module: package_id mismatch.
    module = pkg_dir / "demo_domain.py"
    text = module.read_text(encoding="utf-8")
    module.write_text(
        text.replace("package_id='demo-domain'", "package_id='other-domain'"), encoding="utf-8"
    )
    errors = validate(workdir, "demo-domain")
    assert any("package_id" in e for e in errors)


def test_scaffold_has_no_internal_dependency(workdir: pathlib.Path) -> None:
    import ast

    pkg_dir = scaffold(workdir, "demo-domain", "domain", "Demo Domain")
    tree = ast.parse((pkg_dir / "demo_domain.py").read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    for mod in imported:
        if mod.startswith("wanxiang_"):
            assert mod in {
                "wanxiang_domain",
                "wanxiang_substrate",
            }, f"scaffold must not import internal module {mod}"
