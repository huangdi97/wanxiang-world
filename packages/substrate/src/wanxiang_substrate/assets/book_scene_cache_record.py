"""Visual cache record schema and JSON codec.

Kept separate from cache locking/storage so provenance growth does not turn the
cache coordinator into an oversized mixed-responsibility module.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from dataclasses import dataclass
from typing import cast


@dataclass(frozen=True, slots=True)
class _VisualCacheRecord:
    cache_key: str
    scene_key: str
    place_name: str
    provider_id: str
    provider_version: str
    media_type: str
    content_sha256: str
    asset_id: str
    size: int
    illustrative: bool
    style_key: str
    presentation_kind: str = "still"
    provider_usage_units: int | None = None
    provider_request_id: str = ""
    provider_operation_id: str = ""


def _safe_provider_id(value: object) -> str | None:
    if (
        not isinstance(value, str)
        or len(value) > 1024
        or "\r" in value
        or "\n" in value
    ):
        return None
    return value


def _decode_visual_cache_record(raw: dict[str, object]) -> _VisualCacheRecord | None:
    required_strings = (
        "cache_key",
        "scene_key",
        "place_name",
        "provider_id",
        "provider_version",
        "media_type",
        "content_sha256",
        "asset_id",
        "style_key",
    )
    if not all(isinstance(raw.get(name), str) for name in required_strings):
        return None
    size = raw.get("size")
    illustrative = raw.get("illustrative")
    usage = raw.get("provider_usage_units")
    request_id = _safe_provider_id(raw.get("provider_request_id", ""))
    operation_id = _safe_provider_id(raw.get("provider_operation_id", ""))
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        return None
    if not isinstance(illustrative, bool):
        return None
    if usage is not None and (
        isinstance(usage, bool) or not isinstance(usage, int) or usage < 0
    ):
        return None
    if request_id is None or operation_id is None:
        return None
    presentation = raw.get("presentation_kind")
    return _VisualCacheRecord(
        cache_key=cast(str, raw["cache_key"]),
        scene_key=cast(str, raw["scene_key"]),
        place_name=cast(str, raw["place_name"]),
        provider_id=cast(str, raw["provider_id"]),
        provider_version=cast(str, raw["provider_version"]),
        media_type=cast(str, raw["media_type"]),
        content_sha256=cast(str, raw["content_sha256"]),
        asset_id=cast(str, raw["asset_id"]),
        size=size,
        illustrative=illustrative,
        style_key=cast(str, raw["style_key"]),
        presentation_kind=presentation if isinstance(presentation, str) else "still",
        provider_usage_units=usage,
        provider_request_id=request_id,
        provider_operation_id=operation_id,
    )


def _encode_visual_cache_record(record: _VisualCacheRecord) -> dict[str, object]:
    return {
        "cache_key": record.cache_key,
        "scene_key": record.scene_key,
        "place_name": record.place_name,
        "provider_id": record.provider_id,
        "provider_version": record.provider_version,
        "media_type": record.media_type,
        "content_sha256": record.content_sha256,
        "asset_id": record.asset_id,
        "size": record.size,
        "illustrative": record.illustrative,
        "style_key": record.style_key,
        "presentation_kind": record.presentation_kind,
        "provider_usage_units": record.provider_usage_units,
        "provider_request_id": record.provider_request_id,
        "provider_operation_id": record.provider_operation_id,
    }
