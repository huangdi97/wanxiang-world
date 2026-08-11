"""FastAPI application factory for the Wanxiang world API."""

from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.synthetic_microworld import register_synthetic_resolvers
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_persistence.audit_repository import AuditTraceRepository
from wanxiang_persistence.branch_repository import SqlAlchemyBranchRepository
from wanxiang_persistence.database import create_engine_for
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_persistence.instance_repository import WorldInstanceRepository
from wanxiang_persistence.snapshot_store import SqlAlchemySnapshotStore
from wanxiang_runtime.resolver import ResolverRegistry

from wanxiang_api.errors import install_error_handler
from wanxiang_api.routes import router

API_TITLE = "Wanxiang World API"
API_VERSION = "0.1.0"


def build_runtime(
    database_url: str,
    *,
    rule_version: int = 1,
    schema_version: int = 1,
) -> WorldRuntime:
    """Wire the authoritative vertical slice over SQLite persistence."""
    engine = create_engine_for(database_url)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    persistence = PersistenceBundle(
        event_store=SqlAlchemyEventStore(session_factory),
        snapshot_store=SqlAlchemySnapshotStore(session_factory),
        branches=SqlAlchemyBranchRepository(session_factory),
        instances=WorldInstanceRepository(session_factory),
        audit=AuditTraceRepository(session_factory),
    )
    registry = ResolverRegistry()
    register_synthetic_resolvers(registry)
    return WorldRuntime(
        persistence,
        RuntimeVersion(rule_version),
        schema_version=SchemaVersion(schema_version),
        resolvers=registry,
    )


def create_app(runtime: WorldRuntime | None = None) -> FastAPI:
    app = FastAPI(title=API_TITLE, version=API_VERSION)
    app.state.runtime = runtime
    install_error_handler(app)
    app.include_router(router)
    return app
