"""G38C: kernel v1 change guard (mechanism)."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.kernel_guard as guard


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.mark.unit
def test_guard_passes_on_current_tree() -> None:
    violations = guard.run()
    assert violations == ()


@pytest.mark.unit
def test_guard_catches_domain_name_in_kernel(workspace_tmp_path: Path) -> None:
    tmp_path = workspace_tmp_path
    _write(
        tmp_path / "packages/domain/src/wanxiang_domain/bad.py",
        'NAME = "林黛玉"\n',
    )
    roots = (tmp_path / "packages/domain", tmp_path / "packages/runtime")
    violations = guard.scan_domain_names(roots, root=tmp_path)
    kinds = [v.kind for v in violations]
    assert "domain_name_in_kernel" in kinds


@pytest.mark.unit
def test_guard_catches_new_direct_mutation_path(workspace_tmp_path: Path) -> None:
    tmp_path = workspace_tmp_path
    _write(
        tmp_path / "packages/substrate/src/wanxiang_substrate/x.py",
        "state.apply(delta)\n",
    )
    violations = guard.scan_direct_mutation(
        tmp_path / "packages/substrate", workspace_root=tmp_path
    )
    kinds = [v.kind for v in violations]
    assert "direct_mutation_path" in kinds
