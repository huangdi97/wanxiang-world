"""Player worldline fork route (structural branch creation over the Kernel)."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Header, HTTPException, Request
from wanxiang_substrate.playable import PlayableService

router = APIRouter(prefix="/experience/player")


def _viewer(value: str | None) -> str:
    return value or "anonymous"


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
