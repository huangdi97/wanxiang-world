"""Owner-safe capability view for synchronous T2 panorama upgrades."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import Request
from wanxiang_substrate.assets.book_scene_panorama_budget import PanoramaBudgetLedger
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.spatial import plan_book_scene_assets


def panorama_generation_view(
    request: Request,
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
    place_name: str = "",
) -> dict[str, object]:
    """Describe T2 generation without calling a provider or changing world state."""
    package = service.packages.get(profile_id)
    if package is None:
        return {
            "generation": {
                "available": False,
                "reason": "package_not_found",
                "cost_units": 0,
                "budget_total": 0,
            },
            "ready_places": [],
        }

    ready_places = sorted(
        {
            asset.place_name
            for asset in service.visual_assets(profile_id, viewer_id=viewer_id)
            if asset.presentation_kind == "panorama"
        }
    )
    provider = cast(SceneImageProvider | None, request.app.state.panorama_asset_provider)
    budget = int(request.app.state.panorama_asset_max_cost_units)
    ledger = cast(PanoramaBudgetLedger, request.app.state.panorama_budget_ledger)
    try:
        usage = ledger.usage(profile_id, budget)
    except ValueError:
        usage = None
    generation: dict[str, object] = {
        "available": False,
        "reason": "",
        "cost_units": 0,
        "budget_total": budget,
        "budget_reserved": usage.reserved if usage is not None else budget,
        "budget_remaining": usage.remaining if usage is not None else 0,
        "reservation_count": usage.reservations if usage is not None else 0,
    }
    if usage is None:
        generation["reason"] = "budget_ledger_unavailable"
        return {"generation": generation, "ready_places": ready_places}
    if provider is None:
        generation["reason"] = "provider_not_configured"
        return {"generation": generation, "ready_places": ready_places}

    generation["cost_units"] = provider.cost_units_per_asset
    if provider.presentation_kind != "panorama":
        generation["reason"] = "provider_not_panorama"
        return {"generation": generation, "ready_places": ready_places}

    plan = plan_book_scene_assets(package, max_preview_scenes=0)
    resume_reserved = False
    requested_place = place_name.strip()
    if provider.generation_is_idempotent and requested_place in package.draft.places:
        requested_plan = plan_book_scene_assets(
            package,
            max_preview_scenes=1,
            preferred_places=(requested_place,),
        )
        if requested_plan.scene_requests and requested_plan.scene_requests[0].place_name == requested_place:
            scene_request = requested_plan.scene_requests[0]
            reservation_key = (
                f"{scene_request.cache_key}:t2-panorama-v1:"
                f"{provider.provider_id}@{provider.provider_version}"
            )
            resume_reserved = (
                ledger.reservation_cost(profile_id, reservation_key)
                == provider.cost_units_per_asset
            )
    generation["resume_reserved"] = resume_reserved
    private_source = (
        package.draft.compiler_metadata.get("visual_private_source_v1", "true") == "true"
    )
    if provider.requires_network and not bool(request.app.state.panorama_asset_allow_network):
        generation["reason"] = "network_not_allowed"
    elif provider.requires_network and not plan.external_processing_allowed:
        generation["reason"] = "source_external_processing_not_allowed"
    elif private_source and not provider.private_safe:
        generation["reason"] = "private_source_provider_not_safe"
    elif provider.cost_units_per_asset < 0:
        generation["reason"] = "budget_insufficient"
    elif usage.remaining < provider.cost_units_per_asset and not resume_reserved:
        generation["reason"] = "budget_insufficient"
    else:
        generation.update(
            {
                "available": True,
                "provider": {
                    "id": provider.provider_id,
                    "version": provider.provider_version,
                },
            }
        )
    return {"generation": generation, "ready_places": ready_places}
