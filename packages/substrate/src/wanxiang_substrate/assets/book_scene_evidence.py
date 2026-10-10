"""Untrusted evidence field validation and visual cache-only locator identity.

Canonical Source Refs stay intact; only equivalent one-source re-imports use
content-pinned locators to avoid unnecessary image generation charges.
"""

from __future__ import annotations

import math
from typing import cast


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


def _cache_evidence_ref(
    ref: str, *, single_source: tuple[str, str] | None
) -> str:
    """Replace a known source ID by its verified fingerprint *only for caching*."""
    if single_source is None:
        return ref
    scheme, separator, remainder = ref.partition("://")
    source_id, marker, locator = remainder.partition("#")
    if not scheme or not separator or not marker or not locator:
        return ref
    if source_id != single_source[0]:
        return ref
    return f"{scheme}://content-sha256:{single_source[1]}#{locator}"
