"""Player-safe projection of derived T3 spatial attachment capability."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_substrate.assets.storage import AssetRef

SpatialAssetMap = Mapping[str, tuple[AssetRef, ...]]


def _spatial_capability(
    scene_key: str,
    spatial_assets: SpatialAssetMap | None,
) -> dict[str, object]:
    """Expose renderer capability without leaking storage identity or provenance."""
    refs = tuple((spatial_assets or {}).get(scene_key, ()))
    media_types = tuple(dict.fromkeys(ref.content_type for ref in refs))
    return {
        "ready": bool(refs),
        "asset_count": len(refs),
        "media_types": list(media_types),
    }
