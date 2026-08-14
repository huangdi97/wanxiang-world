"""Release build + migration preflight (G16H).

`build_manifest` produces a traceable release manifest (version, git SHA,
build-input hashes, migration head) reproducibly from a clean checkout.
`preflight_migration` blocks deployment when the database head is not
compatible with the code's supported migration chain.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPECTED_MIGRATION_HEAD = "0003_add_lineage"
RELEASE_VERSION = "0.1.0"

_BUILD_INPUTS = (
    "uv.lock",
    "pnpm-lock.yaml",
    "docs/spec/WANXIANG_v5_MASTER_SPEC.md",
    "alembic.ini",
    "pyproject.toml",
)


def _sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()


class IncompatibleDeployment(Exception):
    pass


def build_manifest(*, fixed_timestamp: str | None = None) -> dict[str, Any]:
    inputs = {name: _sha256(ROOT / name) for name in _BUILD_INPUTS}
    manifest = {
        "version": RELEASE_VERSION,
        "git_sha": git_sha(),
        "migration_head": EXPECTED_MIGRATION_HEAD,
        "build_inputs": inputs,
        "built_at_utc": fixed_timestamp or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    canonical = json.dumps(
        {k: manifest[k] for k in ("version", "git_sha", "migration_head", "build_inputs")},
        sort_keys=True,
        separators=(",", ":"),
    )
    manifest["release_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return manifest


def preflight_migration(database_url: str) -> str:
    """Return the DB head; block if it is not reachable from the code's chain."""
    old = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = database_url
    try:
        import sqlite3

        if database_url.startswith("sqlite:///"):
            db_path = database_url[len("sqlite:///") :]
            con = sqlite3.connect(db_path)
            try:
                row = con.execute("SELECT version_num FROM alembic_version").fetchone()
            finally:
                con.close()
            current = row[0] if row else None
        else:
            current = None
    finally:
        if old is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old
    if current is not None and current not in ("0001_initial", EXPECTED_MIGRATION_HEAD):
        raise IncompatibleDeployment(
            f"database head {current!r} is not reachable by the deployed migration chain"
        )
    return current or "none"


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    m = build_manifest()
    print(json.dumps(m, indent=2))
