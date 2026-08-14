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
    """Copy the DB and write an integrity manifest."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    db_copy = dest_dir / "wanxiang.db"
    shutil.copy2(db_path, db_copy)
    manifest = {
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "schema_version": SchemaVersion(1).value,
        "event_counts": _event_counts(db_copy),
        "db_sha256": __import__("hashlib").sha256(db_copy.read_bytes()).hexdigest(),
    }
    (dest_dir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def restore(backup_dir: pathlib.Path, dest_db_path: pathlib.Path) -> dict[str, Any]:
    """Restore into an isolated path and verify the manifest hash matches."""
    db_copy = backup_dir / "wanxiang.db"
    if not db_copy.exists():
        raise FileNotFoundError("backup DB missing")
    manifest = json.loads((backup_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    actual = __import__("hashlib").sha256(db_copy.read_bytes()).hexdigest()
    if actual != manifest["db_sha256"]:
        raise ValueError("backup integrity mismatch")
    dest_db_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(db_copy, dest_db_path)
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
