"""SQLite persistence fixtures (workspace-local temp DBs with default ACLs)."""

from __future__ import annotations

import os
import pathlib
import uuid
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

ROOT = pathlib.Path(__file__).resolve().parents[2]
_PERSIST_TMP = ROOT / "tests" / "_persist_tmp"

from wanxiang_persistence.database import create_engine_for  # noqa: E402


def upgrade_db(path: pathlib.Path) -> None:
    old = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = f"sqlite:///{path.as_posix()}"
    try:
        command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    finally:
        if old is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old


def make_sqlite_engine_and_factory(
    path: pathlib.Path,
) -> tuple[Engine, sessionmaker[Session]]:
    upgrade_db(path)
    engine = create_engine_for(f"sqlite:///{path.as_posix()}")
    return engine, sessionmaker(bind=engine, expire_on_commit=False)


def sqlite_event_store_fixture():
    """Fresh upgraded SQLite DB + event store (used by the shared contract suite)."""
    from wanxiang_persistence.event_store import SqlAlchemyEventStore

    path = fresh_db_path()
    _engine, factory = make_sqlite_engine_and_factory(path)
    return SqlAlchemyEventStore(factory)


def fresh_db_path() -> pathlib.Path:
    _PERSIST_TMP.mkdir(parents=True, exist_ok=True)
    return _PERSIST_TMP / f"{uuid.uuid4().hex}.db"


def cleanup_db_file(path: pathlib.Path) -> None:
    """Best-effort removal; sandboxed Windows may hold SQLite files open."""
    try:
        if path.exists():
            path.unlink()
    except OSError:
        pass


@pytest.fixture
def persist_db_path() -> Iterator[pathlib.Path]:
    path = fresh_db_path()
    yield path
    cleanup_db_file(path)


@pytest.fixture
def session_factory(persist_db_path: pathlib.Path) -> Iterator[sessionmaker[Session]]:
    engine, factory = make_sqlite_engine_and_factory(persist_db_path)
    yield factory
    engine.dispose()
