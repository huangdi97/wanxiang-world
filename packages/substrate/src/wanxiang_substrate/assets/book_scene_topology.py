"""Source-grounded narrative topology relations for visual plans.

Only explicit, locator-backed place relations become Atlas edges. Repeated
evidence for the same edge is merged so the Atlas does not render duplicate
relations while provenance and confidence are preserved.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_substrate.assets.book_scene_evidence import (
    _bounded_confidence,
    _json_list,
    _object_dict,
    _string_list,
)


@dataclass(frozen=True, slots=True)
class _SourceTopologyRelation:
    """An explicit, source-grounded relation between named places."""

    source_place: str
    target_place: str
    relation_type: str
    source_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    conflicting: bool = False


def _normalize_relation_type(value: str) -> str:
    """Collapse lexical formatting without merging genuinely different types."""
    return "_".join(value.strip().lower().replace("-", " ").split())


def _topology_relations(
    raw_topology: str,
    known_places: set[str],
) -> tuple[_SourceTopologyRelation, ...]:
    merged: dict[tuple[str, str, str], _SourceTopologyRelation] = {}
    for raw_row in _json_list(raw_topology):
        row = _object_dict(raw_row)
        if row is None:
            continue
        source_place = row.get("source_place")
        target_place = row.get("target_place")
        relation_type = row.get("relation_type")
        if isinstance(source_place, str):
            source_place = source_place.strip()
        if isinstance(target_place, str):
            target_place = target_place.strip()
        if (
            not isinstance(source_place, str)
            or not isinstance(target_place, str)
            or not isinstance(relation_type, str)
            or not source_place
            or not target_place
            or source_place == target_place
            or source_place not in known_places
            or target_place not in known_places
        ):
            continue
        normalized_type = _normalize_relation_type(relation_type)
        source_refs = _string_list(row.get("source_refs", []))
        confidence = _bounded_confidence(row.get("confidence", 0.0))
        if not source_refs or not normalized_type or confidence <= 0.0:
            continue
        key = (source_place, target_place, normalized_type)
        existing = merged.get(key)
        if existing is None:
            merged[key] = _SourceTopologyRelation(
                source_place=source_place,
                target_place=target_place,
                relation_type=normalized_type,
                source_refs=source_refs,
                confidence=confidence,
            )
            continue
        merged[key] = replace(
            existing,
            source_refs=tuple(sorted({*existing.source_refs, *source_refs})),
            confidence=max(existing.confidence, confidence),
        )
    groups: dict[tuple[str, str], list[tuple[str, str, str]]] = {}
    for key in merged:
        pair = (key[0], key[1]) if key[0] <= key[1] else (key[1], key[0])
        groups.setdefault(pair, []).append(key)
    for keys in groups.values():
        if len(keys) <= 1:
            continue
        directions = {key[:2] for key in keys}
        types = {key[2] for key in keys}
        if len(directions) > 1 or len(types) > 1:
            for key in keys:
                merged[key] = replace(merged[key], conflicting=True)
    return tuple(merged.values())
