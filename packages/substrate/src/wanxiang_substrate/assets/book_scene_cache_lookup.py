"""Read-only visual cache lookup used when reattaching projections.

Kept outside `book_scene_cache` so the cache stays under the size target. This
never generates, never spends budget, and still verifies bytes and rights.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_types import _SceneVisualAsset
from wanxiang_substrate.assets.storage import AssetRef


def cached_visual_for(
    cache: VisualAssetCache,
    request: _SourceSceneRequest,
    *,
    rights: str = "public",
) -> tuple[_SceneVisualAsset, AssetRef] | None:
    """Find a previously cached non-offline asset for one scene request."""

    prefix = f"{request.cache_key}:"
    candidates = [
        record
        for record in cache.index.list()
        if record.cache_key.startswith(prefix)
        and record.scene_key == request.stable_key
        and record.place_name == request.place_name
        and record.provider_id != "procedural-svg"
    ]
    # Restore the richest durable projection for a scene. Cache-key order
    # is not a fidelity signal and must never downgrade a previously generated
    # panorama to a still image after process restart.
    ordered = sorted(
        candidates,
        key=lambda item: (item.presentation_kind != "panorama", item.cache_key),
    )
    for record in ordered:
        found = cache.get(record.cache_key, rights=rights)
        if found is not None:
            return found
    return None
