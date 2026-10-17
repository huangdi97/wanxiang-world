"""FastAPI application factory for the Wanxiang world API."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
import pathlib
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
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
from wanxiang_substrate.assets.book_scene_cache import (
    LocalJsonVisualCacheIndex,
    VisualAssetCache,
)
from wanxiang_substrate.assets.book_scene_panorama_budget import (
    LocalJsonPanoramaBudgetLedger,
    PanoramaBudgetLedger,
)
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider
from wanxiang_substrate.assets.storage import InMemoryObjectStore, LocalObjectStore
from wanxiang_substrate.authoring import AuthoringService, LocalSemanticProvider
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.lineage import LineageGraph
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview import register_preview_resolvers
from wanxiang_substrate.spatial import (
    DerivedSpatialAttachments,
    InMemorySpatialJobStore,
    LocalJsonSpatialJobStore,
    SpatialGenerationProvider,
)
from wanxiang_substrate.workshop import LocalPromptGenesisProvider, WorkshopService

from wanxiang_api.authoring_routes import router as authoring_router
from wanxiang_api.constitution_routes import router as constitution_router
from wanxiang_api.errors import install_error_handler
from wanxiang_api.limits import PayloadTooLarge
from wanxiang_api.lineage_routes import router as lineage_router
from wanxiang_api.living_world_routes import router as living_world_router
from wanxiang_api.one_click_routes import router as one_click_router
from wanxiang_api.panorama_tokenhub_runtime import panorama_tokenhub_runtime_from_env
from wanxiang_api.playable_routes import router as playable_router
from wanxiang_api.player_history_routes import router as player_history_router
from wanxiang_api.player_routes import router as player_router
from wanxiang_api.player_spatial_routes import router as player_spatial_router
from wanxiang_api.player_ui_routes import router as player_ui_router
from wanxiang_api.player_visual_routes import router as player_visual_router
from wanxiang_api.player_worldline_routes import router as player_worldline_router
from wanxiang_api.promotion_routes import router as promotion_router
from wanxiang_api.review_routes import router as review_router
from wanxiang_api.routes import router
from wanxiang_api.spatial_http_gateway import spatial_http_runtime_from_env
from wanxiang_api.spatial_tokenhub_runtime import spatial_tokenhub_runtime_from_env
from wanxiang_api.studio_ui_routes import router as studio_ui_router
from wanxiang_api.visual_http_gateway import visual_http_runtime_from_env
from wanxiang_api.workshop_routes import router as workshop_router

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
    *,
    visual_cache: VisualAssetCache | None = None,
    visual_provider: SceneImageProvider | None = None,
    visual_allow_network: bool = False,
    visual_max_cost_units: int = 0,
    panorama_provider: SceneImageProvider | None = None,
    panorama_allow_network: bool = False,
    panorama_max_cost_units: int = 0,
    spatial_provider: SpatialGenerationProvider | None = None,
    spatial_allow_network: bool = False,
    spatial_max_cost_units: int = 0,
) -> FastAPI:
    if visual_max_cost_units < 0:
        raise ValueError("visual_max_cost_units must be non-negative")
    if panorama_max_cost_units < 0:
        raise ValueError("panorama_max_cost_units must be non-negative")
    if spatial_max_cost_units < 0:
        raise ValueError("spatial_max_cost_units must be non-negative")
    if visual_provider is None:
        http_visual = visual_http_runtime_from_env()
        visual_provider = http_visual.provider
        visual_allow_network = visual_allow_network or http_visual.allow_network
        if visual_max_cost_units == 0:
            visual_max_cost_units = http_visual.max_cost_units
    if visual_allow_network and visual_provider is None:
        raise ValueError("visual_allow_network requires an injected visual_provider")
    if panorama_provider is None:
        tokenhub_panorama = panorama_tokenhub_runtime_from_env()
        panorama_provider = tokenhub_panorama.provider
        panorama_allow_network = panorama_allow_network or tokenhub_panorama.allow_network
        if panorama_max_cost_units == 0:
            panorama_max_cost_units = tokenhub_panorama.max_cost_units
    if panorama_allow_network and panorama_provider is None:
        raise ValueError("panorama_allow_network requires a configured panorama provider")
    if spatial_provider is None:
        tokenhub_spatial = spatial_tokenhub_runtime_from_env()
        if tokenhub_spatial.provider is not None:
            spatial_provider = tokenhub_spatial.provider
            spatial_allow_network = spatial_allow_network or tokenhub_spatial.allow_network
            if spatial_max_cost_units == 0:
                spatial_max_cost_units = tokenhub_spatial.max_cost_units
        else:
            http_spatial = spatial_http_runtime_from_env()
            spatial_provider = http_spatial.provider
            spatial_allow_network = spatial_allow_network or http_spatial.allow_network
            if spatial_max_cost_units == 0:
                spatial_max_cost_units = http_spatial.max_cost_units
    if spatial_allow_network and spatial_provider is None:
        raise ValueError("spatial_allow_network requires an injected spatial_provider")
    app = FastAPI(title=API_TITLE, version=API_VERSION)
    identity_mode = os.environ.get("WANXIANG_IDENTITY_MODE", "local-demo").strip()
    if identity_mode not in {"local-demo", "trusted"}:
        raise ValueError("WANXIANG_IDENTITY_MODE must be local-demo or trusted")

    if identity_mode == "trusted":
        # A trusted outer ASGI authenticator must populate these scope values.
        # Never treat a caller-supplied HTTP header as proof of identity.
        async def _trusted_identity_boundary(
            request: Request,
            call_next: Callable[[Request], Awaitable[Response]],
        ) -> Response:
            principal = request.scope.get("wanxiang_authenticated_user")
            if not isinstance(principal, str) or not principal.strip():
                return JSONResponse(
                    status_code=401,
                    content={"code": "trusted_identity_required"},
                )
            roles = request.scope.get("wanxiang_authenticated_roles", ())
            if request.url.path.startswith("/studio") and (
                not isinstance(roles, (tuple, list, set, frozenset)) or "creator" not in roles
            ):
                return JSONResponse(
                    status_code=403,
                    content={"code": "studio_creator_role_required"},
                )
            headers = [
                (key, value)
                for key, value in request.scope.get("headers", [])
                if key.lower() != b"x-wanxiang-user"
            ]
            headers.append((b"x-wanxiang-user", principal.encode("utf-8")))
            request.scope["headers"] = headers
            return await call_next(request)

        app.middleware("http")(_trusted_identity_boundary)

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
    providers = ProviderRouter((LocalSemanticProvider(), LocalPromptGenesisProvider()))
    app.state.authoring = AuthoringService(providers=providers)
    visual_cache_root = os.environ.get("WANXIANG_VISUAL_CACHE_DIR", "").strip()
    visual_cache_path = pathlib.Path(visual_cache_root) if visual_cache_root else None
    if visual_cache is not None:
        app.state.visual_asset_cache = visual_cache
    elif visual_cache_path is not None:
        app.state.visual_asset_cache = VisualAssetCache(
            LocalObjectStore(visual_cache_path / "blobs"),
            LocalJsonVisualCacheIndex(visual_cache_path / "index.json"),
        )
    else:
        app.state.visual_asset_cache = VisualAssetCache()
    app.state.visual_asset_provider = visual_provider
    app.state.visual_asset_allow_network = visual_allow_network
    app.state.visual_asset_max_cost_units = visual_max_cost_units
    app.state.visual_asset_max_deferred_generations = max(
        0,
        int(os.environ.get("WANXIANG_VISUAL_MAX_DEFERRED_GENERATIONS", "24") or 24),
    )
    app.state.panorama_asset_provider = panorama_provider
    app.state.panorama_asset_allow_network = panorama_allow_network
    app.state.panorama_asset_max_cost_units = panorama_max_cost_units
    app.state.panorama_budget_ledger = (
        LocalJsonPanoramaBudgetLedger(visual_cache_path / "panorama-budget.json")
        if visual_cache_path is not None
        else PanoramaBudgetLedger()
    )
    if visual_cache_path is not None:
        app.state.spatial_asset_jobs = LocalJsonSpatialJobStore(
            visual_cache_path / "spatial-jobs.json"
        )
        app.state.spatial_asset_objects = LocalObjectStore(visual_cache_path / "spatial-blobs")
    else:
        app.state.spatial_asset_jobs = InMemorySpatialJobStore()
        app.state.spatial_asset_objects = InMemoryObjectStore()
    app.state.spatial_asset_catalog = DerivedSpatialAttachments()
    app.state.spatial_asset_provider = spatial_provider
    app.state.spatial_asset_allow_network = spatial_allow_network
    app.state.spatial_asset_max_cost_units = spatial_max_cost_units
    app.state.workshop = WorkshopService(app.state.authoring, providers=providers)
    app.state.playable = (
        PlayableService(runtime, visual_cache=app.state.visual_asset_cache)
        if runtime is not None
        else None
    )
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
    app.include_router(workshop_router)
    app.include_router(playable_router)
    app.include_router(player_router)
    app.include_router(player_history_router)
    app.include_router(player_worldline_router)
    app.include_router(player_spatial_router)
    app.include_router(player_visual_router)
    app.include_router(player_ui_router)
    return app
