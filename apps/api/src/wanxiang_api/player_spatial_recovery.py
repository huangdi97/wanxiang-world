"""Read-path restoration of verified T3 attachments after process restart.

The durable ticket/object stores remain derived infrastructure. Rehydration only
repopulates Player projection state and never writes Canon or History.
"""

from __future__ import annotations

from typing import cast

from fastapi import Request
from wanxiang_substrate.assets.errors import AssetCorrupt, AssetNotFound
from wanxiang_substrate.assets.storage import ObjectStore
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.spatial import SpatialJobStore, source_scene_key_allowed


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
    restored = 0
    unavailable = 0
    for ticket in jobs.list_scope(profile_id):
        if (
            ticket.state != "attached"
            or not ticket.asset_refs
            or not source_scene_key_allowed(package, ticket.scene_key)
        ):
            continue
        try:
            if not all(len(objects.get(ref)) == ref.size for ref in ticket.asset_refs):
                unavailable += 1
                continue
        except (AssetNotFound, AssetCorrupt):
            unavailable += 1
            continue
        service.attach_spatial_assets(profile_id, ticket.scene_key, ticket.asset_refs)
        restored += 1
    return (restored, unavailable)
