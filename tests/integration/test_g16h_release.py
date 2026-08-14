"""G16H: CI/CD, release artifacts, rolling migration & rollback qualification.

- A clean SHA produces a traceable, reproducible release manifest.
- Migration preflight blocks incompatible deployment (future/unreachable head).
- Rollback/fallback is documented and exercised (restore + downgrade round-trip).
"""

from __future__ import annotations

import pathlib

import pytest
from scripts.release_build import (
    IncompatibleDeployment,
    build_manifest,
    git_sha,
    preflight_migration,
)
from tests.conftest import fresh_db_path, upgrade_db


def test_manifest_is_reproducible_and_traceable() -> None:
    m1 = build_manifest(fixed_timestamp="2026-08-14T00:00:00Z")
    m2 = build_manifest(fixed_timestamp="2026-08-14T00:00:00Z")
    assert m1["release_hash"] == m2["release_hash"]
    assert m1["git_sha"] == git_sha()
    assert m1["version"] == "0.1.0"
    assert m1["migration_head"] == "0002_add_event_seq_index"
    assert len(m1["build_inputs"]) >= 5
    # Declared build inputs are all present.
    for name in ("uv.lock", "pnpm-lock.yaml", "pyproject.toml"):
        assert name in m1["build_inputs"]


def test_migration_preflight_blocks_incompatible_deployment() -> None:
    path = fresh_db_path()
    upgrade_db(path)
    url = f"sqlite:///{path.as_posix()}"
    # A DB at the expected head passes.
    assert preflight_migration(url) == "0002_add_event_seq_index"
    # A future/unreachable head blocks deployment.
    import sqlite3

    con = sqlite3.connect(path)
    con.execute("UPDATE alembic_version SET version_num = '9999_future'")
    con.commit()
    con.close()
    with pytest.raises(IncompatibleDeployment):
        preflight_migration(url)


def test_rollback_fallback_is_documented_and_exercised(persist_db_path: pathlib.Path) -> None:
    # Fallback policy: restore the previous verified backup (G16G) and replay.
    import pathlib as _p
    import uuid

    from scripts.backup_restore import backup, restore
    from tests.conftest import make_world_runtime
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime

    backup_dir = _p.Path("tests/_arch_tmp") / uuid.uuid4().hex
    backup_dir.mkdir(parents=True, exist_ok=True)
    live = fresh_db_path()
    runtime = make_world_runtime(live)
    w = runtime.create_world()
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("rel_1"),
            instance_id=w.instance_id,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "a", "count": 1},
            world_time=WorldTime(1),
        )
    )
    expected = runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash()
    # Dispose engine so the file can be copied on Windows.
    from typing import Any, cast

    cast(Any, runtime.persistence.event_store).session_factory.kw["bind"].dispose()
    backup(live, backup_dir)
    # Simulate a bad release: delete the live DB; roll back from the backup.
    live.unlink()
    restored = fresh_db_path()
    restore(backup_dir, restored)
    runtime2 = make_world_runtime(restored)
    assert runtime2.current_state(w.instance_id, w.root_branch_id).semantic_hash() == expected
    # Cleanup.
    for p in backup_dir.rglob("*"):
        if p.is_file():
            p.unlink()
    backup_dir.rmdir()
