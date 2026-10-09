"""Governed Player routes for on-demand source-derived visuals."""

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.player_service import player_world

router = APIRouter(prefix="/experience/player")


class VisualPlaceRequest(BaseModel):
    place_name: str = Field(min_length=1, max_length=200)


def _locale(value: str | None) -> str:
    normalized = (value or "").strip().replace("_", "-").casefold()
    return "en-US" if normalized == "en" or normalized.startswith("en-") else "zh-CN"


def _service(request: Request) -> PlayableService:
    service = request.app.state.playable
    if service is None:
        raise HTTPException(status_code=503, detail="playable runtime is not configured")
    return cast(PlayableService, service)


@router.post("/worlds/{profile_id}/visuals")
def player_materialize_visual_place(
    profile_id: str,
    payload: VisualPlaceRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = x_wanxiang_user or "anonymous"
    locale = _locale(x_wanxiang_locale)
    service = _service(request)
    provider = cast(SceneImageProvider | None, request.app.state.visual_asset_provider)
    result = service.materialize_visual_place(
        profile_id,
        payload.place_name,
        viewer_id=viewer,
        provider=provider,
        allow_network=bool(request.app.state.visual_asset_allow_network),
        max_cost_units=int(request.app.state.visual_asset_max_cost_units),
    )
    return {
        "locale": locale,
        "provider_calls": result.provider_calls,
        "cache_hits": result.cache_hits,
        "cost_units": result.cost_units,
        "world": player_world(
            service,
            profile_id,
            viewer_id=viewer,
            locale=locale,
            include_visual=True,
        ),
    }
