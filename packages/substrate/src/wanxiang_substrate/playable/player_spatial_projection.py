"""Player-safe projection of derived T3 spatial attachment capability."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import hashlib
from collections.abc import Mapping

from wanxiang_substrate.assets.book_spatial_types import _SpatialProjectionFrame
from wanxiang_substrate.assets.storage import AssetRef

_SpatialAssetMap = Mapping[str, tuple[AssetRef, ...]]
_SpatialProjectionFrameMap = Mapping[str, _SpatialProjectionFrame]


def _spatial_capability(
    scene_key: str,
    spatial_assets: _SpatialAssetMap | None,
    spatial_frames: _SpatialProjectionFrameMap | None = None,
) -> dict[str, object]:
    """Expose renderer capability without leaking storage identity or provenance."""
    refs = tuple((spatial_assets or {}).get(scene_key, ()))
    media_types = tuple(dict.fromkeys(ref.content_type for ref in refs))
    capability: dict[str, object] = {
        "ready": bool(refs),
        "projection_only": True,
        "asset_count": len(refs),
        "media_types": list(media_types),
    }
    if refs:
        revision_payload = "|".join(
            f"{ref.content_hash}:{ref.content_type}:{ref.size}" for ref in refs
        )
        capability["asset_revision"] = hashlib.sha256(
            revision_payload.encode("utf-8")
        ).hexdigest()[:20]
    frame = (spatial_frames or {}).get(scene_key)
    if refs and frame is not None:
        capability["projection_frame"] = {
            "up": list(frame.up),
            "forward": list(frame.forward),
            "center": list(frame.center),
            "scale": frame.scale,
            "convention": frame.convention,
        }
    return capability
