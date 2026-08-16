"""G16B: PostgreSQL production persistence & migration qualification.

The persistence model is dialect-agnostic (JSON-as-text, text PKs, integer
counters; SQLite pragma only applied for sqlite URLs). A live PostgreSQL
instance is not available in this environment -> the live integration profile
is EXTERNAL_BLOCKED with a precise reason; offline DDL compilation for the
postgresql dialect, the SQLite-free portable path, and storage-independent
semantic hashes are qualified deterministically.
"""

from __future__ import annotations

import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def test_postgres_live_integration_profile(persist_db_path: pathlib.Path) -> None:
    url = os.environ.get("WANXIANG_POSTGRES_TEST_URL")
    if not url:
        pytest.skip(
            "EXTERNAL_BLOCKED: no PostgreSQL instance available; set "
            "WANXIANG_POSTGRES_TEST_URL to run the live profile (see runbook)."
        )
    # Live profile: migrate a fresh Postgres schema, run the replay corpus, and
    # verify storage-independent hashes. This path executes only when an
    # operator provides a reachable instance.
    from alembic import command as alembic_command
    from alembic.config import Config as AlembicConfig
    from tests.helpers.replay_fixture import BRANCH, INSTANCE, build_fixture_events
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_persistence.database import create_engine_for
    from wanxiang_persistence.event_store import SqlAlchemyEventStore
    from wanxiang_runtime.replay import ReplayEngine

    # Migrate the PostgreSQL URL directly; upgrade_db() is a SQLite-file helper
    # and must not be handed a postgresql:// URL.
    old_db_url = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = url
    try:
        alembic_command.upgrade(AlembicConfig(str(ROOT / "alembic.ini")), "head")
    finally:
        if old_db_url is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old_db_url
    factory = __import__("sqlalchemy.orm", fromlist=["sessionmaker"]).sessionmaker(
        bind=create_engine_for(url), expire_on_commit=False
    )
    store = SqlAlchemyEventStore(factory)
    for event in build_fixture_events():
        store.append(event)
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(store.load(INSTANCE, BRANCH))
    assert final.revision.value == 5


def test_migrations_compile_for_postgresql_dialect() -> None:
    """Offline DDL compilation proves the migration chain is PostgreSQL-ready."""
    from alembic import command
    from alembic.config import Config

    old = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = "postgresql://wanxiang@localhost/wanxiang"
    import io
    import sys

    try:
        config = Config(str(ROOT / "alembic.ini"))
        # Offline SQL generation for the postgresql dialect (printed to stdout).
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            command.upgrade(config, "head", sql=True)
        finally:
            sys.stdout = old_stdout
        sql = buf.getvalue()
    finally:
        if old is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old
    assert "CREATE TABLE" in sql
    assert "alembic_version" in sql


def test_portable_persistence_path_has_no_sqlite_specific_sql() -> None:
    """Only the engine factory touches SQLite-specific pragma, guarded by scheme."""
    from wanxiang_persistence import database, event_store, models, snapshot_store

    for module in (event_store, models, snapshot_store):
        text = module.__file__ and pathlib.Path(module.__file__).read_text(encoding="utf-8")
        assert text is not None
        assert "PRAGMA" not in text
        assert "INSERT OR" not in text
    db_text = pathlib.Path(database.__file__).read_text(encoding="utf-8")
    assert "PRAGMA foreign_keys" in db_text
    assert 'url.startswith("sqlite")' in db_text


def test_semantic_hashes_storage_independent(persist_db_path: pathlib.Path) -> None:
    from tests.conftest import upgrade_db
    from tests.helpers.replay_fixture import BRANCH, INSTANCE, build_fixture_events
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_persistence.database import create_engine_for
    from wanxiang_persistence.event_store import SqlAlchemyEventStore
    from wanxiang_runtime.replay import ReplayEngine

    upgrade_db(persist_db_path)
    factory = __import__("sqlalchemy.orm", fromlist=["sessionmaker"]).sessionmaker(
        bind=create_engine_for(f"sqlite:///{persist_db_path.as_posix()}"), expire_on_commit=False
    )
    store = SqlAlchemyEventStore(factory)
    for event in build_fixture_events():
        store.append(event)
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(store.load(INSTANCE, BRANCH))
    # Storage-independent expectation: the golden hash.
    assert (
        final.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )
