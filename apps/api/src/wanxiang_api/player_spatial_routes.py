"""Owner-governed asynchronous T3 spatial generation for source-grounded Player places."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Header, HTTPException, Request, Response
from pydantic import BaseModel, Field
from wanxiang_substrate.assets.errors import AssetCorrupt, AssetNotFound
from wanxiang_substrate.assets.storage import AssetRef, ObjectStore
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.player_service import player_world
from wanxiang_substrate.spatial import (
    DerivedSpatialAttachments,
    SpatialGenerationCoordinator,
    SpatialGenerationProvider,
    SpatialJobStore,
    plan_book_scene_assets,
    source_scene_key_allowed,
)

from wanxiang_api.player_spatial_recovery import rehydrate_spatial_attachments
from wanxiang_api.player_spatial_views import (
    spatial_generation_view,
    spatial_ticket_view,
    spatial_ticket_views_for_world,
)

router = APIRouter(prefix="/experience/player")


class SpatialPlaceRequest(BaseModel):
    place_name: str = Field(min_length=1, max_length=200)


def _viewer(value: str | None) -> str:
    return value or "anonymous"


def _locale(value: str | None) -> str:
    normalized = (value or "").strip().replace("_", "-").casefold()
    return "en-US" if normalized == "en" or normalized.startswith("en-") else "zh-CN"


def _service(request: Request) -> PlayableService:
    service = request.app.state.playable
    if service is None:
        raise HTTPException(status_code=503, detail="playable runtime is not configured")
    return cast(PlayableService, service)


def _owner_service(request: Request, profile_id: str, viewer: str) -> PlayableService:
    service = _service(request)
    profile = service.plaza.require_access(profile_id, viewer)
    if not profile.owner_id or profile.owner_id != viewer:
        raise HTTPException(
            status_code=403,
            detail="only the world owner may generate spatial assets",
        )
    return service


def _provider(request: Request) -> SpatialGenerationProvider:
    provider = cast(
        SpatialGenerationProvider | None,
        request.app.state.spatial_asset_provider,
    )
    if provider is None:
        raise HTTPException(status_code=503, detail="spatial provider is not configured")
    return provider


def _jobs(request: Request) -> SpatialJobStore:
    return cast(SpatialJobStore, request.app.state.spatial_asset_jobs)


def _coordinator(request: Request) -> SpatialGenerationCoordinator:
    return SpatialGenerationCoordinator(
        _provider(request),
        jobs=_jobs(request),
        objects=cast(ObjectStore, request.app.state.spatial_asset_objects),
    )


def _profile_package(service: PlayableService, profile_id: str):
    package = service.packages.get(profile_id)
    if package is None:
        raise HTTPException(status_code=404, detail="playable package not found")
    return package


@router.get("/worlds/{profile_id}/spatial")
def player_list_spatial_places(
    profile_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    service = _owner_service(request, profile_id, viewer)
    package = _profile_package(service, profile_id)
    tickets = tuple(
        ticket
        for ticket in _jobs(request).list_scope(profile_id)
        if source_scene_key_allowed(package, ticket.scene_key)
    )
    rehydrated, unavailable = rehydrate_spatial_attachments(
        request,
        service,
        profile_id,
        viewer_id=viewer,
    )
    return {
        "spatial_jobs": spatial_ticket_views_for_world(package, tickets),
        "generation": spatial_generation_view(request, package, profile_id),
        "rehydrated_attachments": rehydrated,
        "unavailable_attachments": unavailable,
    }


@router.post("/worlds/{profile_id}/spatial", status_code=202)
def player_submit_spatial_place(
    profile_id: str,
    payload: SpatialPlaceRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    service = _owner_service(request, profile_id, viewer)
    package = _profile_package(service, profile_id)
    place = payload.place_name.strip()
    if place not in package.draft.places:
        raise HTTPException(status_code=404, detail="source-grounded place not found")
    plan = plan_book_scene_assets(
        package,
        max_preview_scenes=1,
        preferred_places=(place,),
    )
    if not plan.scene_requests or plan.scene_requests[0].place_name != place:
        raise HTTPException(status_code=409, detail="spatial scene is not eligible for generation")
    try:
        ticket = _coordinator(request).submit(
            plan.scene_requests[0],
            allow_network=bool(request.app.state.spatial_asset_allow_network),
            external_processing_allowed=plan.external_processing_allowed,
            private_source=(
                package.draft.compiler_metadata.get("visual_private_source_v1", "true") == "true"
            ),
            max_cost_units=int(request.app.state.spatial_asset_max_cost_units),
            delivery_rights=plan.delivery_rights,
            scope_key=profile_id,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail="spatial provider temporarily unavailable",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"spatial": spatial_ticket_view(ticket)}


@router.get("/worlds/{profile_id}/spatial-assets/{asset_index}")
def player_spatial_asset(
    profile_id: str,
    asset_index: int,
    place_name: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> Response:
    viewer = _viewer(x_wanxiang_user)
    service = _service(request)
    rehydrate_spatial_attachments(request, service, profile_id, viewer_id=viewer)
    package = _profile_package(service, profile_id)
    place = place_name.strip()
    if place not in package.draft.places:
        raise HTTPException(status_code=404, detail="spatial asset not found")
    plan = plan_book_scene_assets(
        package,
        max_preview_scenes=1,
        preferred_places=(place,),
    )
    if not plan.scene_requests or plan.scene_requests[0].place_name != place:
        raise HTTPException(status_code=404, detail="spatial asset not found")
    scene_key = plan.scene_requests[0].stable_key
    refs = service.spatial_assets(profile_id, viewer_id=viewer).get(scene_key, ())
    if asset_index < 0 or asset_index >= len(refs):
        raise HTTPException(status_code=404, detail="spatial asset not found")
    ref = refs[asset_index]
    try:
        content = cast(ObjectStore, request.app.state.spatial_asset_objects).get(ref)
    except (AssetNotFound, AssetCorrupt) as exc:
        raise HTTPException(status_code=404, detail="spatial asset not found") from exc
    return Response(
        content=content,
        media_type=ref.content_type,
        headers={
            "cache-control": "private, no-store",
            "x-content-type-options": "nosniff",
        },
    )


@router.get("/worlds/{profile_id}/spatial/{submission_id}")
def player_poll_spatial_place(
    profile_id: str,
    submission_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    service = _owner_service(request, profile_id, viewer)
    package = _profile_package(service, profile_id)
    jobs = _jobs(request)
    ticket = jobs.get(submission_id)
    if (
        ticket is None
        or ticket.scope_key != profile_id
        or not source_scene_key_allowed(package, ticket.scene_key)
    ):
        raise HTTPException(status_code=404, detail="spatial generation ticket not found")

    if ticket.state in {"submitted", "queued", "running"}:
        try:
            ticket = _coordinator(request).poll(submission_id)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=503,
                detail="spatial provider temporarily unavailable",
            ) from exc
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    if ticket.state in {"verified", "attached"}:
        if not ticket.asset_refs:
            raise HTTPException(status_code=409, detail="verified spatial ticket has no assets")
        catalog = cast(DerivedSpatialAttachments, request.app.state.spatial_asset_catalog)
        current_rights = plan_book_scene_assets(
            package,
            max_preview_scenes=0,
        ).delivery_rights
        try:
            ticket = _coordinator(request).attach(
                submission_id,
                catalog,
                expected_delivery_rights=current_rights,
            )
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        service.attach_spatial_assets(
            profile_id,
            ticket.scene_key,
            ticket.asset_refs,
            projection_frame=ticket.projection_frame,
        )

    locale = _locale(x_wanxiang_locale)
    return {
        "locale": locale,
        "spatial": spatial_ticket_view(ticket),
        "world": player_world(
            service,
            profile_id,
            viewer_id=viewer,
            locale=locale,
            include_visual=True,
        ),
    }
