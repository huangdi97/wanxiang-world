"""Runtime validation for dynamically injected visual provider pricing."""

from __future__ import annotations

from typing import cast

from wanxiang_substrate.assets.book_scene_types import SceneImageProvider


def provider_cost_units(provider: SceneImageProvider) -> int | None:
    """Return a usable Wanxiang budget cost or fail closed for malformed adapters."""
    raw = cast(object, provider.cost_units_per_asset)
    if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
        return None
    return raw
