"""G34C: DB & Ledger compatibility migration (v5.2 metadata + backup/restore)."""

from __future__ import annotations

import os
import pathlib

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from tests.conftest import cleanup_db_file, fresh_db_path, upgrade_db
from tests.helpers.replay_fixture import BRANCH, INSTANCE, build_fixture_events
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_persistence.database import create_engine_for
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_runtime.replay import ReplayEngine

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _config() -> Config:
    return Config(str(ROOT / "alembic.ini"))


@pytest.mark.migration
def test_old_db_copy_upgrade_keeps_event_count_and_hash() -> None:
    """Upgrade to 0001, insert a world + events, upgrade to head: no loss."""
    path = fresh_db_path()
    os.environ["WANXIANG_DATABASE_URL"] = f"sqlite:///{path.as_posix()}"
    try:
        command.upgrade(_config(), "0001_initial")
        factory = sessionmaker(
            bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
        )
        store = SqlAlchemyEventStore(factory)
        for event in build_fixture_events():
            store.append(event)
        command.upgrade(_config(), "head")
    finally:
        os.environ.pop("WANXIANG_DATABASE_URL", None)

    factory2 = sessionmaker(
        bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
    )
    store2 = SqlAlchemyEventStore(factory2)
    events = store2.load(INSTANCE, BRANCH)
    assert len(events) == 5  # event count unchanged
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert final.revision.value == 5
    assert (
        final.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )

    # New v5.2 metadata columns exist (nullable).
    engine = factory2.kw["bind"]
    cols = {c["name"] for c in inspect(engine).get_columns("world_instances")}
    assert {"definition_ref", "constitution_ref", "evolution_policy_ref"} <= cols
    engine.dispose()
    cleanup_db_file(path)


@pytest.mark.migration
def test_downgrade_from_0004_to_0003_restores_old_schema() -> None:
    path = fresh_db_path()
    upgrade_db(path)
    os.environ["WANXIANG_DATABASE_URL"] = f"sqlite:///{path.as_posix()}"
    try:
        command.downgrade(_config(), "0003_add_lineage")
    finally:
        os.environ.pop("WANXIANG_DATABASE_URL", None)
    engine = create_engine_for(f"sqlite:///{path.as_posix()}")
    cols = {c["name"] for c in inspect(engine).get_columns("world_instances")}
    assert "constitution_ref" not in cols
    assert "events" in set(inspect(engine).get_table_names())
    engine.dispose()
    cleanup_db_file(path)


@pytest.mark.migration
def test_backup_restore_path_preserves_history() -> None:

    from scripts.backup_restore import backup, restore

    path = fresh_db_path()
    upgrade_db(path)
    factory = sessionmaker(
        bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
    )
    store = SqlAlchemyEventStore(factory)
    for event in build_fixture_events():
        store.append(event)
    factory.kw["bind"].dispose()

    backup_dir = ROOT / "tests" / "_persist_tmp" / "g34c_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    manifest = backup(pathlib.Path(path), backup_dir)
    assert manifest["event_counts"] == {f"{INSTANCE.value}:{BRANCH.value}": 5}

    restored_path = fresh_db_path()
    restore(backup_dir, pathlib.Path(restored_path))
    factory2 = sessionmaker(
        bind=create_engine_for(f"sqlite:///{restored_path.as_posix()}"), expire_on_commit=False
    )
    store2 = SqlAlchemyEventStore(factory2)
    events = store2.load(INSTANCE, BRANCH)
    assert len(events) == 5
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert (
        final.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )
    factory2.kw["bind"].dispose()
    cleanup_db_file(path)
    cleanup_db_file(restored_path)
