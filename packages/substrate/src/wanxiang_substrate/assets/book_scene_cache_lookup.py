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
    for record in sorted(candidates, key=lambda item: item.cache_key):
        found = cache.get(record.cache_key, rights=rights)
        if found is not None:
            return found
    return None
