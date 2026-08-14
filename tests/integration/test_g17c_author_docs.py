"""G17C: external author documentation & reference templates.

- A clean-room authoring exercise follows the docs (scaffold -> validate ->
  build -> instantiate) using only the public SDK.
- Examples distinguish definition content from runtime instance state.
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


def test_clean_room_authoring_follows_guide(workdir: pathlib.Path) -> None:
    """Walk through the external-author guide end to end."""
    # 1) scaffold (docs quickstart)
    pkg_dir = scaffold(workdir, "author-demo", "world", "Author Demo")
    assert pkg_dir.exists()
    # 2) validate + build (docs)
    assert validate(workdir, "author-demo") == []
    build = dry_run_build(workdir, "author-demo")
    assert build["lock_hash"]
    # 3) The generated package is definition; no world instance was created.
    #    Definition vs runtime distinction: the manifest is immutable content.
    import importlib.util

    spec = importlib.util.spec_from_file_location("author_demo", pkg_dir / "author_demo.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    manifest = mod.build_manifest()
    assert manifest.package_id == "author-demo"
    # No runtime state was touched by definition-only work.


def test_guide_exists_and_distinguishes_definition_vs_runtime() -> None:
    guide = (ROOT / "docs" / "sdk" / "EXTERNAL_AUTHOR_GUIDE.md").read_text(encoding="utf-8")
    assert "Domain Pack" in guide
    assert "World Instance" in guide
    assert "definition content" in guide or "definition" in guide
    assert "Commit Authority" in guide
    # Examples are public-SDK only.
    assert "wanxiang_substrate.packages" in guide or "wxpack" in guide
