"""Read-path restoration of verified T3 attachments after process restart.

The durable ticket/object stores remain derived infrastructure. Rehydration only
repopulates Player projection state and never writes Canon or History.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

from fastapi import Request
from wanxiang_substrate.assets.book_spatial_safety import _require_spatial_asset_refs
from wanxiang_substrate.assets.storage import ObjectStore
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.spatial import (
    SpatialJobStore,
    plan_book_scene_assets,
    source_scene_key_allowed,
)


def rehydrate_spatial_attachments(
    request: Request,
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
) -> tuple[int, int]:
    """Restore durable attached T3 assets before projecting an accessible world."""
    service.plaza.require_access(profile_id, viewer_id)
    package = service.packages.get(profile_id)
    if package is None:
        return (0, 0)

    jobs = cast(SpatialJobStore, request.app.state.spatial_asset_jobs)
    objects = cast(ObjectStore, request.app.state.spatial_asset_objects)
    current_rights = plan_book_scene_assets(
        package,
        max_preview_scenes=0,
    ).delivery_rights
    existing = service.spatial_assets(profile_id, viewer_id=viewer_id)
    existing_frames = service.spatial_projection_frames(profile_id, viewer_id=viewer_id)
    restored = 0
    unavailable = 0
    for ticket in jobs.list_scope(profile_id):
        if (
            ticket.state != "attached"
            or not ticket.asset_refs
            or not source_scene_key_allowed(package, ticket.scene_key)
        ):
            continue
        if (
            existing.get(ticket.scene_key) == ticket.asset_refs
            and existing_frames.get(ticket.scene_key) == ticket.projection_frame
        ):
            continue
        try:
            if ticket.delivery_rights != current_rights:
                raise ValueError(
                    "persisted spatial ticket rights do not match current source rights"
                )
            _require_spatial_asset_refs(
                objects,
                ticket.asset_refs,
                delivery_rights=current_rights,
            )
        except ValueError:
            unavailable += 1
            continue
        service.attach_spatial_assets(
            profile_id,
            ticket.scene_key,
            ticket.asset_refs,
            projection_frame=ticket.projection_frame,
        )
        restored += 1
    return (restored, unavailable)
