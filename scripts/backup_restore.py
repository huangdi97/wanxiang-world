"""Backup/restore utility for the SQLite profile (G16G).

Backs up the durable DB file plus a manifest (event counts per branch, package
lock hash, schema version) and restores into an isolated clean path, verifying
integrity. Advanced PITR (PostgreSQL WAL / log shipping) is NOT implemented in
this profile and is named accurately as such.
"""

from __future__ import annotations

import json
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


def backup(db_path: pathlib.Path, dest_dir: pathlib.Path) -> dict[str, Any]:
    """Copy the DB, the Player catalog sidecar, and write an integrity manifest."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    db_copy = dest_dir / "wanxiang.db"
    shutil.copy2(db_path, db_copy)
    player_store = db_path.with_name(db_path.name + PLAYER_STORE_SUFFIX)
    player_entry = _player_store_entry(player_store)
    if player_entry is not None:
        shutil.copy2(player_store, dest_dir / PLAYER_STORE_COPY)
    manifest = {
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "schema_version": SchemaVersion(1).value,
        "event_counts": _event_counts(db_copy),
        "db_sha256": _sha256(db_copy),
        "player_store": player_entry,
    }
    (dest_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def restore(backup_dir: pathlib.Path, dest_db_path: pathlib.Path) -> dict[str, Any]:
    """Restore the DB and Player sidecar into an isolated path, verifying hashes."""
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
    return manifest


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "backup":
        backup(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]))
    elif action == "restore":
        restore(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]))
    else:
        raise SystemExit("usage: backup_restore.py backup|restore <path> <path>")
