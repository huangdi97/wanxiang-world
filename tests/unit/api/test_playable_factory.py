"""Default Player catalog derivation for the API composition root."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.playable_factory import _configured_store_path, build_playable_service
from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.playable.local_store import LocalJsonPlayableStore


def test_explicit_store_path_wins(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    explicit = tmp_path / "explicit.json"
    monkeypatch.setenv("WANXIANG_PLAYABLE_STORE_PATH", str(explicit))
    monkeypatch.setenv("WANXIANG_DATABASE_URL", "sqlite:///./db.sqlite")
    assert _configured_store_path() == explicit


def test_sqlite_database_derives_a_player_store(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    monkeypatch.delenv("WANXIANG_PLAYABLE_STORE_PATH", raising=False)
    database = tmp_path / "world.db"
    monkeypatch.setenv("WANXIANG_DATABASE_URL", f"sqlite:///{database.as_posix()}")
    assert _configured_store_path() == tmp_path / "world.db.playable.json"

    service = build_playable_service(
        build_reference_runtime(),
        visual_cache=VisualAssetCache(),
    )
    assert isinstance(service.store, LocalJsonPlayableStore)
    assert service.store.path == tmp_path / "world.db.playable.json"
    assert not service.store.path.exists()


def test_memory_and_non_sqlite_urls_do_not_derive_a_store(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("WANXIANG_PLAYABLE_STORE_PATH", raising=False)
    monkeypatch.setenv("WANXIANG_DATABASE_URL", "postgresql://wanxiang@localhost/wanxiang")
    assert _configured_store_path() is None
    monkeypatch.setenv("WANXIANG_DATABASE_URL", "sqlite:///:memory:")
    assert _configured_store_path() is None


def test_injected_store_bypasses_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    injected = LocalJsonPlayableStore(tmp_path / "injected.json")
    monkeypatch.setenv("WANXIANG_PLAYABLE_STORE_PATH", "ignored.json")
    service = build_playable_service(
        build_reference_runtime(),
        visual_cache=VisualAssetCache(),
        playable_store=injected,
    )
    assert service.store is injected
