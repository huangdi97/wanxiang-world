"""Governed Player routes for on-demand source-derived visuals."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field
from wanxiang_substrate.assets.book_scene_panorama_budget import PanoramaBudgetLedger
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.player_service import player_world
from wanxiang_substrate.spatial import plan_book_scene_assets

from wanxiang_api.player_panorama_views import panorama_generation_view

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
        max_deferred_generations=int(request.app.state.visual_asset_max_deferred_generations),
    )
    return {
        "locale": locale,
        "provider_calls": result.provider_calls,
        "cache_hits": result.cache_hits,
        "cost_units": result.cost_units,
        "fallback_from_provider": result.fallback_from_provider,
        "fallback_reason": result.fallback_reason,
        "world": player_world(
            service,
            profile_id,
            viewer_id=viewer,
            locale=locale,
            include_visual=True,
        ),
    }


@router.get("/worlds/{profile_id}/panoramas")
def player_panorama_generation_status(
    profile_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = x_wanxiang_user or "anonymous"
    service = _service(request)
    profile = service.plaza.require_access(profile_id, viewer)
    if not profile.owner_id or profile.owner_id != viewer:
        raise HTTPException(status_code=403, detail="only the world owner may generate panoramas")
    return panorama_generation_view(request, service, profile_id, viewer_id=viewer)


@router.post("/worlds/{profile_id}/panoramas")
def player_upgrade_visual_place_to_panorama(
    profile_id: str,
    payload: VisualPlaceRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = x_wanxiang_user or "anonymous"
    locale = _locale(x_wanxiang_locale)
    service = _service(request)
    profile = service.plaza.require_access(profile_id, viewer)
    if not profile.owner_id or profile.owner_id != viewer:
        raise HTTPException(status_code=403, detail="only the world owner may generate panoramas")
    provider = cast(SceneImageProvider | None, request.app.state.panorama_asset_provider)
    if provider is None:
        raise HTTPException(status_code=503, detail="panorama provider is not configured")
    if provider.presentation_kind != "panorama":
        raise HTTPException(
            status_code=409,
            detail="configured provider is not a panorama provider",
        )

    package = service.packages.get(profile_id)
    if package is None:
        raise HTTPException(status_code=404, detail="playable package not found")
    place = payload.place_name.strip()
    if place not in package.draft.places:
        raise HTTPException(status_code=404, detail="source-grounded place not found")
    plan = plan_book_scene_assets(
        package,
        max_preview_scenes=1,
        preferred_places=(place,),
    )
    if not plan.scene_requests or plan.scene_requests[0].place_name != place:
        raise HTTPException(status_code=409, detail="panorama scene is not eligible for generation")

    capability = panorama_generation_view(
        request,
        service,
        profile_id,
        viewer_id=viewer,
    )
    ready_places = cast(list[str], capability.get("ready_places", []))
    generation = cast(dict[str, object], capability["generation"])
    if place not in ready_places and generation.get("available") is not True:
        raise HTTPException(
            status_code=409,
            detail=str(generation.get("reason") or "panorama generation unavailable"),
        )

    ledger = cast(PanoramaBudgetLedger, request.app.state.panorama_budget_ledger)
    budget = int(request.app.state.panorama_asset_max_cost_units)
    scene_request = plan.scene_requests[0]
    reservation_key = (
        f"{scene_request.cache_key}:t2-panorama-v1:"
        f"{provider.provider_id}@{provider.provider_version}"
    )
    if place not in ready_places:
        try:
            ledger.reserve(
                profile_id,
                reservation_key,
                provider.cost_units_per_asset,
                budget,
            )
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    try:
        result = service.materialize_visual_place(
            profile_id,
            place,
            viewer_id=viewer,
            provider=provider,
            allow_network=bool(request.app.state.panorama_asset_allow_network),
            max_cost_units=budget,
            fallback_to_t0=False,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    non_panorama = any(asset.presentation_kind != "panorama" for asset in result.assets)
    if not result.assets or non_panorama:
        raise HTTPException(
            status_code=409,
            detail="panorama provider returned a non-panorama asset",
        )
    return {
        "locale": locale,
        "tier": "T2",
        "provider_calls": result.provider_calls,
        "cache_hits": result.cache_hits,
        "cost_units": result.cost_units,
        "budget": ledger.usage(profile_id, budget).to_dict(),
        "world": player_world(
            service,
            profile_id,
            viewer_id=viewer,
            locale=locale,
            include_visual=True,
        ),
    }
