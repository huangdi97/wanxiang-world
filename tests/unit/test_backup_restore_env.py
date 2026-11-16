"""CLI backup/restore reuses the app's visual cache directory by default."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib

import pytest
from scripts.backup_restore import visual_cache_from_environment


def test_visual_cache_directory_comes_from_the_app_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    monkeypatch.setenv("WANXIANG_VISUAL_CACHE_DIR", str(tmp_path / "visual"))
    assert visual_cache_from_environment() == tmp_path / "visual"


def test_missing_or_blank_visual_cache_directory_is_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("WANXIANG_VISUAL_CACHE_DIR", raising=False)
    assert visual_cache_from_environment() is None
    monkeypatch.setenv("WANXIANG_VISUAL_CACHE_DIR", "  ")
    assert visual_cache_from_environment() is None
