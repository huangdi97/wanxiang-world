"""Player worldline fork route (structural branch creation over the Kernel)."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Header, HTTPException, Query, Request
from wanxiang_substrate.playable import PlayableService

router = APIRouter(prefix="/experience/player")


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


@router.get("/instances/{instance_id}/worldlines")
def player_list_worldlines(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    """List the viewer's playable worldlines of this runtime instance."""
    viewer = _viewer(x_wanxiang_user)
    return _service(request).worldlines(instance_id, viewer_id=viewer)


@router.get("/instances/{instance_id}/compare")
def player_compare_worldlines(
    instance_id: str,
    request: Request,
    with_instance: str = Query(alias="with"),
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    """Compare two owned worldlines: shared history point and divergent heads."""
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    try:
        result = _service(request).compare_worldlines(
            instance_id,
            other_instance_id=with_instance,
            viewer_id=viewer,
            locale=locale,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "locale": locale,
        "instance_id": instance_id,
        "with": with_instance,
        **result,
    }


@router.post("/instances/{instance_id}/fork")
def player_fork_worldline(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    """Fork the owned branch at its current head as a new Player worldline."""
    viewer = _viewer(x_wanxiang_user)
    worldline = _service(request).fork_worldline(instance_id, viewer_id=viewer)
    return {"instance_id": instance_id, "worldline": worldline}
