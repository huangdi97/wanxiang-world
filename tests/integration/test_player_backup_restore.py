"""Backups must carry the Player catalog sidecar with the SQLite database."""

from __future__ import annotations

import pathlib

import pytest
from scripts.backup_restore import PLAYER_STORE_COPY, backup, restore
from tests.conftest import make_world_runtime
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
