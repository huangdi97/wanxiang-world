"""Untrusted evidence field validation and visual cache-only locator identity.

Canonical Source Refs stay intact; only equivalent one-source re-imports use
content-pinned locators to avoid unnecessary image generation charges.
"""

# pyright: reportUnusedFunction=false

from __future__ import annotations

import json
import math
from typing import cast


def _json_list(raw: str) -> list[object]:
    """Decode an untrusted metadata JSON array without leaking Unknown into strict typing."""
    try:
        decoded: object = json.loads(raw)
    except (TypeError, ValueError):
        return []
    return cast(list[object], decoded) if isinstance(decoded, list) else []


def _object_dict(value: object) -> dict[str, object] | None:
    return cast(dict[str, object], value) if isinstance(value, dict) else None


def _json_string_map(raw: str) -> dict[str, str]:
    try:
        decoded: object = json.loads(raw)
    except (TypeError, ValueError):
        return {}
    if not isinstance(decoded, dict):
        return {}
    return {
        key: value
        for key, value in cast(dict[object, object], decoded).items()
        if isinstance(key, str) and key and isinstance(value, str) and value
    }


def _string_list(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(
        sorted(
            item
            for raw in cast(list[object], value)
            if isinstance(raw, str) and (item := raw.strip())
        )
    )


def _bounded_confidence(value: object) -> float:
    """Prevent invalid/untrusted scores from changing ranking or map truth."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0.0
    score = float(value)
    return score if math.isfinite(score) and 0.0 <= score <= 1.0 else 0.0


def _cache_evidence_ref(ref: str, *, source_fingerprints: dict[str, str]) -> str:
    """Use content identity only for cache keys; preserve original refs elsewhere."""
    if not source_fingerprints:
        return ref
    scheme, separator, remainder = ref.partition("://")
    source_ref = remainder if separator else ref
    source_id, marker, locator = source_ref.partition("#")
    fingerprint = source_fingerprints.get(source_id)
    if fingerprint is None:
        return ref
    prefix = f"{scheme}://" if separator else ""
    suffix = f"#{locator}" if marker and locator else ""
    return f"{prefix}content-sha256:{fingerprint}{suffix}"
