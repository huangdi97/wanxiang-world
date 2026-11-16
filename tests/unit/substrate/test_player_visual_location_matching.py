"""Player scene matching reuses source-equivalent visual place labels."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib

from wanxiang_substrate.assets.book_scene_types import _SceneVisualAsset
from wanxiang_substrate.playable.player_projection import _visual_asset_at_location


def _asset(place: str) -> _SceneVisualAsset:
    content = f"premium:{place}".encode()
    return _SceneVisualAsset(
        scene_key=f"scene-{place}",
        place_name=place,
        provider_id="provider:premium",
        media_type="image/webp",
        content=content,
        content_sha256=hashlib.sha256(content).hexdigest(),
        cache_key=f"cache-{place}",
        provider_version="2026-10",
    )


def test_existing_premium_scene_survives_case_and_whitespace_location_variants() -> None:
    garden = _asset("Garden")
    assert _visual_asset_at_location((garden,), "  garden  ") is garden


def test_scene_matching_uses_same_unicode_identity_as_source_place_planning() -> None:
    cafe = _asset("Café")
    assert _visual_asset_at_location((cafe,), "Cafe\u0301") is cafe


def test_scene_matching_never_fuzzy_merges_distinct_places() -> None:
    garden = _asset("Garden")
    assert _visual_asset_at_location((garden,), "Garden Annex") is None
