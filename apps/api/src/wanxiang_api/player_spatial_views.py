"""Safe Player projection of asynchronous T3 job and generation capability."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import Request
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.spatial import (
    SpatialGenerationProvider,
    SpatialGenerationTicket,
    SpatialJobStore,
    plan_book_scene_assets,
    source_scene_key,
)


def spatial_ticket_view(ticket: SpatialGenerationTicket) -> dict[str, object]:
    view: dict[str, object] = {
        "submission_id": ticket.submission_id,
        "state": ticket.state,
        "provider": {"id": ticket.provider_id, "version": ticket.provider_version},
        "reserved_cost_units": ticket.reserved_cost_units,
        "asset_count": len(ticket.asset_refs),
        "attempt": ticket.attempt,
        "media_types": sorted({ref.content_type for ref in ticket.asset_refs}),
    }
    if ticket.provider_usage_units is not None:
        view["provider_usage_units"] = ticket.provider_usage_units
    return view


def spatial_generation_view(
    request: Request,
    package: WorldPackageDraft,
    scope_key: str,
) -> dict[str, object]:
    provider = cast(SpatialGenerationProvider | None, request.app.state.spatial_asset_provider)
    allow_network = bool(request.app.state.spatial_asset_allow_network)
    budget = int(request.app.state.spatial_asset_max_cost_units)
    jobs = cast(SpatialJobStore, request.app.state.spatial_asset_jobs)
    reserved = sum(ticket.reserved_cost_units for ticket in jobs.list_scope(scope_key))
    remaining = max(0, budget - reserved)
    if provider is None:
        return {
            "available": False,
            "reason": "provider_not_configured",
            "cost_units": 0,
            "budget_total": budget,
            "budget_reserved": reserved,
            "budget_remaining": remaining,
        }
    if provider.cost_units_per_job < 0:
        return {
            "available": False,
            "reason": "budget_insufficient",
            "cost_units": 0,
            "budget_total": budget,
            "budget_reserved": reserved,
            "budget_remaining": remaining,
        }
    plan = plan_book_scene_assets(package, max_preview_scenes=0)
    private_source = (
        package.draft.compiler_metadata.get("visual_private_source_v1", "true") == "true"
    )
    if provider.requires_network and not allow_network:
        return {
            "available": False,
            "reason": "network_not_allowed",
            "cost_units": 0,
            "budget_total": budget,
            "budget_reserved": reserved,
            "budget_remaining": remaining,
        }
    if provider.requires_network and not plan.external_processing_allowed:
        return {
            "available": False,
            "reason": "source_external_processing_not_allowed",
            "cost_units": 0,
            "budget_total": budget,
            "budget_reserved": reserved,
            "budget_remaining": remaining,
        }
    if private_source and not provider.private_safe:
        return {
            "available": False,
            "reason": "private_source_provider_not_safe",
            "cost_units": 0,
            "budget_total": budget,
            "budget_reserved": reserved,
            "budget_remaining": remaining,
        }
    if provider.cost_units_per_job > remaining:
        return {
            "available": False,
            "reason": "budget_insufficient",
            "cost_units": provider.cost_units_per_job,
            "budget_total": budget,
            "budget_reserved": reserved,
            "budget_remaining": remaining,
        }
    return {
        "available": True,
        "reason": "",
        "cost_units": provider.cost_units_per_job,
        "budget_total": budget,
        "budget_reserved": reserved,
        "budget_remaining": remaining,
        "provider": {"id": provider.provider_id, "version": provider.provider_version},
    }


def spatial_ticket_views_for_world(
    package: WorldPackageDraft,
    tickets: tuple[SpatialGenerationTicket, ...],
) -> list[dict[str, object]]:
    plan = plan_book_scene_assets(package, max_preview_scenes=0)
    place_by_scene = {
        source_scene_key(plan.source_digest, place): place for place in package.draft.places
    }
    rows: list[dict[str, object]] = []
    for ticket in sorted(tickets, key=lambda row: (row.scene_key, row.attempt, row.submission_id)):
        place = place_by_scene.get(ticket.scene_key)
        if place is None:
            continue
        row = spatial_ticket_view(ticket)
        row["place_name"] = place
        rows.append(row)
    return rows
