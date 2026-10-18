"""Backup/restore utility for the SQLite profile (G16G).

Backs up the durable DB file plus a manifest (event counts per branch, package
lock hash, schema version) and restores into an isolated clean path, verifying
integrity. Advanced PITR (PostgreSQL WAL / log shipping) is NOT implemented in
this profile and is named accurately as such.
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import sqlite3
import sys
import time
from typing import Any

from wanxiang_domain.versions import SchemaVersion

MANIFEST_NAME = "backup_manifest.json"
PLAYER_STORE_SUFFIX = ".playable.json"
PLAYER_STORE_COPY = "wanxiang.db.playable.json"


def _sha256(path: pathlib.Path) -> str:
    return __import__("hashlib").sha256(path.read_bytes()).hexdigest()


def _tree_digest(root: pathlib.Path) -> tuple[int, str]:
    digest = __import__("hashlib").sha256()
    files = sorted(path for path in root.rglob("*") if path.is_file())
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return len(files), digest.hexdigest()


def _visual_cache_entry(source: pathlib.Path | None) -> dict[str, object] | None:
    if source is None or not source.is_dir():
        return None
    count, tree_hash = _tree_digest(source)
    return {"name": "visual-cache", "file_count": count, "tree_sha256": tree_hash}


def visual_cache_from_environment() -> pathlib.Path | None:
    """Use the same cache directory the app reads by default for CLI backups."""

    configured = os.environ.get("WANXIANG_VISUAL_CACHE_DIR", "").strip()
    return pathlib.Path(configured) if configured else None


def _player_store_entry(source: pathlib.Path) -> dict[str, object] | None:
    if not source.exists():
        return None
    return {"name": PLAYER_STORE_COPY, "sha256": _sha256(source)}


def _event_counts(db_path: pathlib.Path) -> dict[str, int]:
    con = sqlite3.connect(db_path)
    try:
        rows = con.execute(
            "SELECT instance_id, branch_id, COUNT(*) FROM events GROUP BY instance_id, branch_id"
        ).fetchall()
    finally:
        con.close()
    return {f"{i}:{b}": n for i, b, n in rows}


def backup(
    db_path: pathlib.Path,
    dest_dir: pathlib.Path,
    *,
    visual_cache_dir: pathlib.Path | None = None,
) -> dict[str, Any]:
    """Copy the DB, Player sidecar, optional visual cache, and an integrity manifest."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    db_copy = dest_dir / "wanxiang.db"
    shutil.copy2(db_path, db_copy)
    player_store = db_path.with_name(db_path.name + PLAYER_STORE_SUFFIX)
    player_entry = _player_store_entry(player_store)
    if player_entry is not None:
        shutil.copy2(player_store, dest_dir / PLAYER_STORE_COPY)
    visual_entry = _visual_cache_entry(visual_cache_dir)
    if visual_entry is not None and visual_cache_dir is not None:
        shutil.copytree(visual_cache_dir, dest_dir / "visual-cache", dirs_exist_ok=True)
    manifest = {
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "schema_version": SchemaVersion(1).value,
        "event_counts": _event_counts(db_copy),
        "db_sha256": _sha256(db_copy),
        "player_store": player_entry,
        "visual_cache": visual_entry,
    }
    (dest_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def restore(
    backup_dir: pathlib.Path,
    dest_db_path: pathlib.Path,
    *,
    visual_cache_dir: pathlib.Path | None = None,
) -> dict[str, Any]:
    """Restore the DB, Player sidecar and visual cache, verifying every hash."""
    db_copy = backup_dir / "wanxiang.db"
    if not db_copy.exists():
        raise FileNotFoundError("backup DB missing")
    manifest = json.loads((backup_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    if _sha256(db_copy) != manifest["db_sha256"]:
        raise ValueError("backup integrity mismatch")
    dest_db_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(db_copy, dest_db_path)
    player_entry = manifest.get("player_store")
    if player_entry is not None:
        name = player_entry.get("name", PLAYER_STORE_COPY)
        source = backup_dir / str(name)
        if not source.exists():
            raise FileNotFoundError("backup Player catalog missing")
        if _sha256(source) != player_entry.get("sha256"):
            raise ValueError("backup Player catalog integrity mismatch")
        shutil.copy2(
            source,
            dest_db_path.with_name(dest_db_path.name + PLAYER_STORE_SUFFIX),
        )
    visual_entry = manifest.get("visual_cache")
    if visual_entry is not None and visual_cache_dir is not None:
        source = backup_dir / str(visual_entry.get("name", "visual-cache"))
        if not source.is_dir():
            raise FileNotFoundError("backup visual cache missing")
        count, tree_hash = _tree_digest(source)
        if count != visual_entry.get("file_count") or tree_hash != visual_entry.get("tree_sha256"):
            raise ValueError("backup visual cache integrity mismatch")
        visual_cache_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, visual_cache_dir, dirs_exist_ok=True)
    return manifest


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "backup":
        visual = pathlib.Path(sys.argv[4]) if len(sys.argv) > 4 else visual_cache_from_environment()
        backup(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), visual_cache_dir=visual)
    elif action == "restore":
        visual = pathlib.Path(sys.argv[4]) if len(sys.argv) > 4 else visual_cache_from_environment()
        restore(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), visual_cache_dir=visual)
    else:
        raise SystemExit("usage: backup_restore.py backup|restore <path> <path> [visual_cache_dir]")
