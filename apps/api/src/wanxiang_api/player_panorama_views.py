"""Owner-safe capability view for synchronous T2 panorama upgrades."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import Request
from wanxiang_substrate.assets.book_scene_panorama_budget import _PanoramaBudgetLedger
from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider
from wanxiang_substrate.playable import PlayableService


def panorama_generation_view(
    request: Request,
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
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
    ledger = cast(_PanoramaBudgetLedger, request.app.state.panorama_budget_ledger)
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

    plan = _plan_book_scene_assets(package, max_preview_scenes=0)
    private_source = (
        package.draft.compiler_metadata.get("visual_private_source_v1", "true") == "true"
    )
    if provider.requires_network and not bool(request.app.state.panorama_asset_allow_network):
        generation["reason"] = "network_not_allowed"
    elif provider.requires_network and not plan.external_processing_allowed:
        generation["reason"] = "source_external_processing_not_allowed"
    elif private_source and not provider.private_safe:
        generation["reason"] = "private_source_provider_not_safe"
    elif provider.cost_units_per_asset < 0 or usage.remaining < provider.cost_units_per_asset:
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
