"""FastAPI application factory for the Wanxiang world API."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
from wanxiang_substrate.authoring import AuthoringService, LocalSemanticProvider
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.lineage import LineageGraph
from wanxiang_substrate.preview import register_preview_resolvers

from wanxiang_api.authoring_routes import router as authoring_router
from wanxiang_api.constitution_routes import router as constitution_router
from wanxiang_api.errors import install_error_handler
from wanxiang_api.limits import PayloadTooLarge
from wanxiang_api.lineage_routes import router as lineage_router
from wanxiang_api.living_world_routes import router as living_world_router
from wanxiang_api.one_click_routes import router as one_click_router
from wanxiang_api.promotion_routes import router as promotion_router
from wanxiang_api.review_routes import router as review_router
from wanxiang_api.routes import router
from wanxiang_api.studio_ui_routes import router as studio_ui_router

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
    register_preview_resolvers(registry)
    return WorldRuntime(
        persistence,
        RuntimeVersion(rule_version),
        schema_version=SchemaVersion(schema_version),
        resolvers=registry,
    )


def create_app(
    runtime: WorldRuntime | None = None,
    lineage_graph: LineageGraph | None = None,
) -> FastAPI:
    app = FastAPI(title=API_TITLE, version=API_VERSION)
    app.state.runtime = runtime
    app.state.lineage_graph = lineage_graph or LineageGraph()
    app.state.studio_admin = False
    app.state.promotion_candidates = ()
    from wanxiang_substrate.completion.planner import CompletionPlanner
    from wanxiang_substrate.evidence.binding import EvidenceBindings
    from wanxiang_substrate.evidence.conflict import ConflictLedger
    from wanxiang_substrate.review.decisions import ReviewLedger

    app.state.review_ledger = ReviewLedger()
    app.state.conflict_ledger = ConflictLedger()
    app.state.evidence_bindings = EvidenceBindings()
    app.state.completion_planner = CompletionPlanner()
    # The local provider is available as an explicit capability. Jobs still
    # require the caller to opt in via semantic_provider; omitted means the
    # no-key deterministic baseline and can return SEMANTIC_PROVIDER_REQUIRED.
    app.state.authoring = AuthoringService(providers=ProviderRouter((LocalSemanticProvider(),)))
    install_error_handler(app)

    @app.exception_handler(PayloadTooLarge)
    async def _payload_too_large(request: Request, exc: PayloadTooLarge) -> JSONResponse:  # pyright: ignore[reportUnusedFunction]
        _ = request
        return JSONResponse(
            status_code=413,
            content={
                "code": "payload_too_large",
                "message": f"payload {exc.size} bytes exceeds limit {exc.limit}",
                "details": {},
            },
        )

    app.include_router(router)
    app.include_router(review_router)
    app.include_router(lineage_router)
    app.include_router(promotion_router)
    app.include_router(constitution_router)
    app.include_router(authoring_router)
    app.include_router(one_click_router)
    app.include_router(living_world_router)
    app.include_router(studio_ui_router)
    return app
