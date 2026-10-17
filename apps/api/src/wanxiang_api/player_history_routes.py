"""Player history and replay routes (read-only over committed events)."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Header, HTTPException, Request
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


@router.get("/instances/{instance_id}/replay")
def player_replay_instance(
    instance_id: str,
    at_ticks: int,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    """Return a read-only projection of the instance at a past world tick."""
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    try:
        view = _service(request).replay_at(
            instance_id,
            viewer_id=viewer,
            at_ticks=at_ticks,
            locale=locale,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "locale": locale,
        "instance_id": instance_id,
        "replay": view.get("replay"),
        "view": view,
    }


@router.get("/instances/{instance_id}/history")
def player_instance_history(
    instance_id: str,
    request: Request,
    limit: int = 200,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    """Return the player-safe chronicle, newest first, for an owned instance."""
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    try:
        history = _service(request).history(
            instance_id,
            viewer_id=viewer,
            limit=limit,
            locale=locale,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"locale": locale, "instance_id": instance_id, **history}
