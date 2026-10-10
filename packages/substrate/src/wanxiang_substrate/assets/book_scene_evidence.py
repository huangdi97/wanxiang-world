"""Untrusted evidence field validation and visual cache-only locator identity.

Canonical Source Refs stay intact; only equivalent one-source re-imports use
content-pinned locators to avoid unnecessary image generation charges.
"""

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


def _cache_evidence_ref(ref: str, *, single_source: tuple[str, str] | None) -> str:
    """Replace a known source ID by its verified fingerprint *only for caching*."""
    if single_source is None:
        return ref
    source_name, fingerprint = single_source
    if ref == source_name:
        return f"content-sha256:{fingerprint}"
    if ref.startswith(f"{source_name}#"):
        return f"content-sha256:{fingerprint}#{ref.partition('#')[2]}"
    scheme, separator, remainder = ref.partition("://")
    source_id, marker, locator = remainder.partition("#")
    if not scheme or not separator or source_id != source_name:
        return ref
    suffix = f"#{locator}" if marker and locator else ""
    return f"{scheme}://content-sha256:{fingerprint}{suffix}"
