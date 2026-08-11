"""GOAL_01E: Alembic migration harness tests."""

from __future__ import annotations

import os
import pathlib

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
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
def test_fresh_db_upgrade_to_head() -> None:
    path = fresh_db_path()
    upgrade_db(path)
    engine = create_engine_for(f"sqlite:///{path.as_posix()}")
    tables = set(inspect(engine).get_table_names())
    assert {
        "world_instances",
        "branches",
        "events",
        "snapshots",
        "audit_traces",
    } <= tables
    engine.dispose()
    cleanup_db_file(path)


@pytest.mark.migration
def test_pre_head_fixture_upgrade_keeps_data() -> None:
    """Upgrade to 0001, insert data, upgrade to head (0002): data intact."""
    from sqlalchemy.orm import sessionmaker

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

    # After upgrade to head, data is still readable and replayable.
    factory2 = sessionmaker(
        bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
    )
    store2 = SqlAlchemyEventStore(factory2)
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(store2.load(INSTANCE, BRANCH))
    assert final.revision.value == 5
    engine = factory2.kw["bind"]
    with engine.connect() as conn:
        indexes = {row[1] for row in conn.execute(text("PRAGMA index_list(events)")).fetchall()}
    assert "ix_events_stream_ordered" in indexes
    engine.dispose()
    cleanup_db_file(path)


@pytest.mark.migration
def test_downgrade_round_trip() -> None:
    path = fresh_db_path()
    upgrade_db(path)
    command.downgrade(_config(), "base")
    command.upgrade(_config(), "head")
    engine = create_engine_for(f"sqlite:///{path.as_posix()}")
    tables = set(inspect(engine).get_table_names())
    assert "events" in tables
    engine.dispose()
    cleanup_db_file(path)
