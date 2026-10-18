"""Backups must carry the Player catalog sidecar with the SQLite database."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib
import shutil
import sqlite3
from dataclasses import replace

import pytest
from scripts.backup_restore import PLAYER_STORE_COPY, backup, restore
from tests.conftest import make_world_runtime
from wanxiang_substrate.assets.book_scene_cache import (
    LocalJsonVisualCacheIndex,
    VisualAssetCache,
)
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_render import _ProceduralSvgSceneProvider
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider, _SceneVisualAsset
from wanxiang_substrate.assets.storage import LocalObjectStore
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.local_store import LocalJsonPlayableStore
from wanxiang_substrate.playable.restore import restore_playable_service
from wanxiang_substrate.preview import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Chapter\nCharacter: Alice\nAlice arrived in Beijing in 1985.\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id="backup_player_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://backup_player_source",
        stage="E3",
        rights=RightsEnvelope(owner="test", usage="test", approved=True),
        payload=content,
        provenance="synthetic:backup-player",
        access="private",
    )


def test_backup_and_restore_keep_the_player_catalog(tmp_path: pathlib.Path) -> None:
    db_path = tmp_path / "world.db"
    sidecar = db_path.with_name(db_path.name + ".playable.json")
    runtime = make_world_runtime(db_path, extra_resolvers=register_preview_resolvers)
    authored = OneClickAuthoring().run("job_backup_world", (_source(),), profile="book")
    service = PlayableService(
        runtime,
        store=LocalJsonPlayableStore(sidecar),
    )
    profile = service.register_package(
        authored.package,
        owner_id="alice",
        visibility="public",
        display_name="备份世界",
    )
    assert sidecar.exists()

    backup_dir = tmp_path / "backup"
    manifest = backup(db_path, backup_dir)
    assert manifest["player_store"] is not None
    assert (backup_dir / PLAYER_STORE_COPY).exists()

    db_path.unlink()
    sidecar.unlink()
    restored_db = tmp_path / "restored.db"
    restore(backup_dir, restored_db)
    restored_sidecar = restored_db.with_name(restored_db.name + ".playable.json")
    assert restored_sidecar.exists()

    restored_runtime = make_world_runtime(
        restored_db,
        extra_resolvers=register_preview_resolvers,
    )
    restored = PlayableService(
        restored_runtime,
        store=LocalJsonPlayableStore(restored_sidecar),
    )
    assert restore_playable_service(restored) == 1
    assert [card.profile_id for card in restored.plaza.explore_worlds("alice")] == [
        profile.profile_id
    ]


def test_backup_captures_uncheckpointed_wal_data(tmp_path: pathlib.Path) -> None:
    db_path = tmp_path / "wal-world.db"
    make_world_runtime(db_path, extra_resolvers=register_preview_resolvers)
    writer = sqlite3.connect(db_path)
    try:
        writer.execute("PRAGMA journal_mode=WAL")
        writer.execute("CREATE TABLE wal_probe (value TEXT)")
        writer.execute("INSERT INTO wal_probe VALUES ('visible-after-restore')")
        writer.commit()

        backup_dir = tmp_path / "wal-backup"
        backup(db_path, backup_dir)
    finally:
        writer.close()

    restored_db = tmp_path / "wal-restored.db"
    restore(backup_dir, restored_db)
    restored = sqlite3.connect(restored_db)
    try:
        assert restored.execute("SELECT value FROM wal_probe").fetchone() == (
            "visible-after-restore",
        )
    finally:
        restored.close()


def test_backup_without_a_player_catalog_still_restores_the_database(
    tmp_path: pathlib.Path,
) -> None:
    db_path = tmp_path / "plain.db"
    make_world_runtime(db_path, extra_resolvers=register_preview_resolvers)
    backup_dir = tmp_path / "plain-backup"
    manifest = backup(db_path, backup_dir)
    assert manifest["player_store"] is None

    restored_db = tmp_path / "plain-restored.db"
    restore(backup_dir, restored_db)
    assert restored_db.exists()
    assert not restored_db.with_name(restored_db.name + ".playable.json").exists()


def test_backup_and_restore_keep_the_visual_and_spatial_cache(tmp_path: pathlib.Path) -> None:
    db_path = tmp_path / "cache-world.db"
    make_world_runtime(db_path, extra_resolvers=register_preview_resolvers)
    visual = tmp_path / "visual-cache"
    (visual / "blobs").mkdir(parents=True)
    (visual / "blobs" / "aa").write_bytes(b"\x89PNG\r\n\x1a\npayload")
    (visual / "index.json").write_text("{}", encoding="utf-8")
    (visual / "spatial-jobs.json").write_text('{"ticket": {}}', encoding="utf-8")

    backup_dir = tmp_path / "cache-backup"
    manifest = backup(db_path, backup_dir, visual_cache_dir=visual)
    assert manifest["visual_cache"]["file_count"] == 3

    restored_visual = tmp_path / "restored-visual"
    restore(
        backup_dir,
        tmp_path / "cache-restored.db",
        visual_cache_dir=restored_visual,
    )
    assert (restored_visual / "blobs" / "aa").read_bytes() == b"\x89PNG\r\n\x1a\npayload"
    assert (restored_visual / "spatial-jobs.json").read_text(encoding="utf-8") == '{"ticket": {}}'

    (backup_dir / "visual-cache" / "blobs" / "aa").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="visual cache integrity"):
        restore(
            backup_dir,
            tmp_path / "cache2.db",
            visual_cache_dir=tmp_path / "visual2",
        )


class _BackupProvider(SceneImageProvider):
    provider_id = "provider:backup-cache"
    provider_version = "1.0"
    cost_units_per_asset = 1
    private_safe = True

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        produced = _ProceduralSvgSceneProvider().produce(request)
        return replace(
            produced,
            provider_id=self.provider_id,
            provider_version=self.provider_version,
            cache_key=f"{request.cache_key}:{self.provider_id}@{self.provider_version}",
        )


def test_backup_restore_keeps_t1_cache_hits_free(tmp_path: pathlib.Path) -> None:
    db_path = tmp_path / "t1-world.db"
    sidecar = db_path.with_name(db_path.name + ".playable.json")
    visual = tmp_path / "visual-cache"
    runtime = make_world_runtime(db_path, extra_resolvers=register_preview_resolvers)
    cache = VisualAssetCache(
        LocalObjectStore(visual / "blobs"),
        LocalJsonVisualCacheIndex(visual / "index.json"),
    )
    authored = OneClickAuthoring().run("job_backup_t1", (_source(),), profile="book")
    assert authored.visual_plan is not None
    place = authored.visual_plan.place_names[0]
    service = PlayableService(
        runtime,
        store=LocalJsonPlayableStore(sidecar),
        visual_cache=cache,
    )
    profile = service.register_package(authored.package, owner_id="alice", visibility="public")
    provider = _BackupProvider()
    generated = service.materialize_visual_place(
        profile.profile_id,
        place,
        viewer_id="alice",
        provider=provider,
        max_cost_units=5,
        max_deferred_generations=5,
    )
    assert generated.provider_calls == 1

    backup_dir = tmp_path / "t1-backup"
    backup(db_path, backup_dir, visual_cache_dir=visual)
    db_path.unlink()
    sidecar.unlink()
    shutil.rmtree(visual)
    restored_db = tmp_path / "t1-restored.db"
    restored_visual = tmp_path / "t1-restored-visual"
    restore(backup_dir, restored_db, visual_cache_dir=restored_visual)

    restored_runtime = make_world_runtime(
        restored_db,
        extra_resolvers=register_preview_resolvers,
    )
    restored = PlayableService(
        restored_runtime,
        store=LocalJsonPlayableStore(restored_db.with_name(restored_db.name + ".playable.json")),
        visual_cache=VisualAssetCache(
            LocalObjectStore(restored_visual / "blobs"),
            LocalJsonVisualCacheIndex(restored_visual / "index.json"),
        ),
    )
    assert restore_playable_service(restored) == 1
    assets = restored.visual_assets(profile.profile_id, viewer_id="alice")
    assert provider.provider_id in {asset.provider_id for asset in assets}
    reused = restored.materialize_visual_place(
        profile.profile_id,
        place,
        viewer_id="alice",
        provider=provider,
        max_cost_units=5,
        max_deferred_generations=5,
    )
    assert reused.provider_calls == 0
    assert reused.cache_hits == 1
