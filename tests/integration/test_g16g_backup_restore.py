"""G16G: backup, restore, PITR-like recovery & disaster game day.

- Restored canonical worlds match expected semantic hashes to the recovery point.
- Backup includes DB + event counts + schema version + integrity hash.
- Disaster game day: accidental deletion of the live DB is recovered from backup.
- Advanced PITR (PostgreSQL WAL) is accurately named as not implemented in this profile.
"""

from __future__ import annotations

import json
import os
import pathlib
import uuid
from collections.abc import Iterator

import pytest
from scripts.backup_restore import backup, restore
from tests.conftest import fresh_db_path
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
BACKUP_ROOT = ROOT / "tests" / "_arch_tmp"


@pytest.fixture
def backup_dir() -> Iterator[pathlib.Path]:
    d = BACKUP_ROOT / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield d
    for p in d.rglob("*"):
        if p.is_file():
            try:  # noqa: SIM105
                p.unlink()
            except OSError:
                pass
    try:  # noqa: SIM105
        d.rmdir()
    except OSError:
        pass


def _populate(db_path: pathlib.Path) -> tuple[str, WorldInstanceId, BranchId]:
    """Build a world over a disposable engine so the file can be deleted on Windows."""
    from sqlalchemy.orm import sessionmaker
    from tests.conftest import upgrade_db
    from wanxiang_application.ports import PersistenceBundle
    from wanxiang_application.synthetic_microworld import register_synthetic_resolvers
    from wanxiang_application.world_runtime import WorldRuntime
    from wanxiang_persistence.audit_repository import AuditTraceRepository
    from wanxiang_persistence.branch_repository import SqlAlchemyBranchRepository
    from wanxiang_persistence.database import create_engine_for
    from wanxiang_persistence.event_store import SqlAlchemyEventStore
    from wanxiang_persistence.instance_repository import WorldInstanceRepository
    from wanxiang_persistence.snapshot_store import SqlAlchemySnapshotStore
    from wanxiang_runtime.resolver import ResolverRegistry

    upgrade_db(db_path)
    engine = create_engine_for(f"sqlite:///{db_path.as_posix()}")
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    persistence = PersistenceBundle(
        event_store=SqlAlchemyEventStore(factory),
        snapshot_store=SqlAlchemySnapshotStore(factory),
        branches=SqlAlchemyBranchRepository(factory),
        instances=WorldInstanceRepository(factory),
        audit=AuditTraceRepository(factory),
    )
    registry = ResolverRegistry()
    register_synthetic_resolvers(registry)
    runtime = WorldRuntime(persistence, RuntimeVersion(1), resolvers=registry)
    w = runtime.create_world()
    for i in range(3):
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"dr_{i}"),
                instance_id=w.instance_id,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(i),
                action_type="create_entity",
                payload={"entity_id": f"e{i}", "count": i},
                world_time=WorldTime(i + 1),
            )
        )
    result = (
        runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash(),
        w.instance_id,
        w.root_branch_id,
    )
    engine.dispose()
    return result


def _replay_hashes(db_path: pathlib.Path) -> set[str]:
    from sqlalchemy import text
    from sqlalchemy.orm import sessionmaker
    from wanxiang_persistence.database import create_engine_for
    from wanxiang_persistence.event_store import SqlAlchemyEventStore

    engine = create_engine_for(f"sqlite:///{db_path.as_posix()}")
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    store = SqlAlchemyEventStore(factory)
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT DISTINCT instance_id, branch_id FROM events")).fetchall()
    hashes: set[str] = set()
    for iid_s, bid_s in rows:
        events = store.load(WorldInstanceId(iid_s), BranchId(bid_s))
        hashes.add(ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events).semantic_hash())
    engine.dispose()
    return hashes


def test_restore_matches_recovery_point(backup_dir: pathlib.Path) -> None:
    live = fresh_db_path()
    expected_hash, _iid, _branch = _populate(live)
    manifest = backup(live, backup_dir)
    assert manifest["schema_version"] == 1
    assert manifest["event_counts"]
    restored_db = fresh_db_path()
    restore(backup_dir, restored_db)
    assert expected_hash in _replay_hashes(restored_db)


def test_disaster_game_day_accidental_deletion(backup_dir: pathlib.Path) -> None:
    live = fresh_db_path()
    expected_hash, _iid, _branch = _populate(live)
    backup(live, backup_dir)
    # Disaster: the live DB is accidentally deleted.
    os.remove(live)
    assert not live.exists()
    # Recovery from the backup into a fresh path (no manual DB repair).
    recovered = fresh_db_path()
    restore(backup_dir, recovered)
    assert expected_hash in _replay_hashes(recovered)


def test_backup_includes_metadata(backup_dir: pathlib.Path) -> None:
    live = fresh_db_path()
    _populate(live)
    backup(live, backup_dir)
    assert (backup_dir / "wanxiang.db").exists()
    assert (backup_dir / "backup_manifest.json").exists()
    manifest = json.loads((backup_dir / "backup_manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["db_sha256"]
