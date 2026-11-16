"""Owner-only best-effort cancellation for derived T3 generation tasks."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request
from wanxiang_substrate.spatial import (
    request_spatial_cancellation,
    source_scene_key_allowed,
)

from wanxiang_api.player_spatial_routes import (
    _jobs,
    _owner_service,
    _profile_package,
    _provider,
    _viewer,
)
from wanxiang_api.player_spatial_views import spatial_ticket_view

router = APIRouter(prefix="/experience/player")


@router.post("/worlds/{profile_id}/spatial/{submission_id}/cancel", status_code=202)
def player_cancel_spatial_place(
    profile_id: str,
    submission_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
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
    try:
        updated = request_spatial_cancellation(_provider(request), jobs, submission_id)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail="spatial provider temporarily unavailable",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"spatial": spatial_ticket_view(updated)}
