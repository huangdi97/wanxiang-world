"""The local Player server persists its catalog next to the SQLite database."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
import pathlib

import pytest
from scripts.m95_player_server import ROOT, _configure_playable_store, _sqlite_path


def test_sqlite_server_derives_a_durable_player_store(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("WANXIANG_PLAYABLE_STORE_PATH", raising=False)
    _configure_playable_store("sqlite:///.pytest-tmp/m95/wanxiang.db")

    configured = pathlib.Path(os.environ["WANXIANG_PLAYABLE_STORE_PATH"])
    assert configured == ROOT / ".pytest-tmp/m95/wanxiang.db.playable.json"


def test_explicit_store_path_wins(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WANXIANG_PLAYABLE_STORE_PATH", "/tmp/explicit.json")
    _configure_playable_store("sqlite:///other.db")
    assert os.environ["WANXIANG_PLAYABLE_STORE_PATH"] == "/tmp/explicit.json"


def test_non_sqlite_and_memory_urls_do_not_configure_a_store(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("WANXIANG_PLAYABLE_STORE_PATH", raising=False)
    _configure_playable_store("postgresql://wanxiang@localhost/wanxiang")
    assert "WANXIANG_PLAYABLE_STORE_PATH" not in os.environ
    assert _sqlite_path("sqlite:///:memory:") is None
    assert _sqlite_path("sqlite://") is None
