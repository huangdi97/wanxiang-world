"""Opaque, derived asset revision for renderer refresh.

A player-facing asset token exists so a renderer can tell when a visual asset
changed. It is deliberately not a canonical digest and never a source, world,
branch or history revision: the browser must not be handed canonical internals.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations


def _asset_revision(digest: str) -> str:
    """Return an opaque revision token derived from one rendered asset digest."""

    cleaned = str(digest).strip()
    if not cleaned:
        return "rev-unknown"
    return f"rev-{cleaned[:12]}"
