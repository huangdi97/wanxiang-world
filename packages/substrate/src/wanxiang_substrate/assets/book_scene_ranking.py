"""Deterministic source-evidence ranking for book scenes.

Ranking is a projection over source evidence only: no coordinates, chapter
order geography, or invented place relations.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import cast

from wanxiang_substrate.assets.book_scene_evidence import _bounded_confidence, _string_list

_PlaceStats = tuple[set[str], float, int]


def _place_stats(matching: list[dict[str, object]]) -> _PlaceStats:
    refs = {ref for row in matching for ref in _string_list(row.get("source_refs", []))}
    confidence = max(
        (_bounded_confidence(row.get("confidence", 0.0)) for row in matching),
        default=0.0,
    )
    context_count = sum(
        len(cast(list[object], raw_context))
        for row in matching
        if isinstance((raw_context := row.get("cooccurring_candidates", [])), list)
    )
    return refs, confidence, context_count


def _rank_places(
    distinct_places: tuple[str, ...],
    evidence_by_place: dict[str, list[dict[str, object]]],
) -> tuple[tuple[str, ...], dict[str, _PlaceStats]]:
    """Order places by source support; mention order is the final tie-break."""
    positions = {place: index for index, place in enumerate(distinct_places)}
    stats = {place: _place_stats(evidence_by_place.get(place, [])) for place in distinct_places}

    def rank(place: str) -> tuple[int, float, int, int, str, int]:
        refs, confidence, context_count = stats[place]
        return (
            -len(refs),
            -confidence,
            -context_count,
            0 if refs else 1,
            min(refs, default=""),
            positions[place],
        )

    return tuple(sorted(distinct_places, key=rank)), stats
