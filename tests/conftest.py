"""Shared test configuration (deterministic profile + SQLite persistence fixtures)."""

from __future__ import annotations

import os
import pathlib
import shutil
import uuid
from collections.abc import Callable, Iterator

import pytest
from alembic import command
from alembic.config import Config
from hypothesis import settings
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

ROOT = pathlib.Path(__file__).resolve().parents[1]
# Windows ACLs can make the conventional pytest temp root unusable. Keep the
# fixture workspace-local and ignored, while allowing CI/desktop runners to
# select an explicitly writable directory without changing product behavior.
_PERSIST_TMP = pathlib.Path(
    os.environ.get("WANXIANG_TEST_TMP", str(ROOT / ".pytest-tmp" / "persist"))
)

from wanxiang_application.world_runtime import WorldRuntime  # noqa: E402
from wanxiang_persistence.database import create_engine_for  # noqa: E402
from wanxiang_runtime.resolver import ResolverRegistry  # noqa: E402

settings.register_profile("wanxiang-deterministic", derandomize=True, deadline=None)
settings.load_profile("wanxiang-deterministic")


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


def make_world_runtime(
    path: pathlib.Path,
    extra_resolvers: Callable[[ResolverRegistry], None] | None = None,
) -> WorldRuntime:
    """Build the authoritative application runtime over a fresh upgraded SQLite DB.

    `extra_resolvers` is an optional callable(ResolverRegistry) registering
    additional deterministic resolvers (e.g. substrate actions).
    """
    from wanxiang_application.ports import PersistenceBundle
    from wanxiang_application.synthetic_microworld import register_synthetic_resolvers
    from wanxiang_application.world_runtime import WorldRuntime
    from wanxiang_domain.versions import RuntimeVersion
    from wanxiang_persistence.audit_repository import AuditTraceRepository
    from wanxiang_persistence.branch_repository import SqlAlchemyBranchRepository
    from wanxiang_persistence.event_store import SqlAlchemyEventStore
    from wanxiang_persistence.instance_repository import WorldInstanceRepository
    from wanxiang_persistence.snapshot_store import SqlAlchemySnapshotStore

    _engine, factory = make_sqlite_engine_and_factory(path)
    persistence = PersistenceBundle(
        event_store=SqlAlchemyEventStore(factory),
        snapshot_store=SqlAlchemySnapshotStore(factory),
        branches=SqlAlchemyBranchRepository(factory),
        instances=WorldInstanceRepository(factory),
        audit=AuditTraceRepository(factory),
    )
    registry = ResolverRegistry()
    register_synthetic_resolvers(registry)
    if extra_resolvers is not None:
        extra_resolvers(registry)
    return WorldRuntime(persistence, RuntimeVersion(1), resolvers=registry)


def fresh_db_path() -> pathlib.Path:
    _PERSIST_TMP.mkdir(parents=True, exist_ok=True)
    return _PERSIST_TMP / f"{uuid.uuid4().hex}.db"


@pytest.fixture
def workspace_tmp_path() -> Iterator[pathlib.Path]:
    """Writable repository-local scratch path for ACL-hostile Windows runners."""
    root = ROOT / "tests" / "_arch_tmp" / "pytest_workspace"
    root.mkdir(parents=True, exist_ok=True)
    path = root / uuid.uuid4().hex
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


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


@pytest.fixture
def world_runtime(persist_db_path: pathlib.Path):
    return make_world_runtime(persist_db_path)
