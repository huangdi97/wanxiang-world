"""Budgeted source-driven visual scene requests over existing WorldDraft.

This is an Asset Foundry preparation step, NOT a renderer or a generated image.
No paid API calls, world-specific templates, canonical writes, or invented geography.
"""

# pyright: reportUnusedFunction=false

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import cast

from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.compile.assembler import WorldPackageDraft


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


@dataclass(frozen=True, slots=True)
class _SourceSceneRequest:
    """A book-derived visual candidate request, not a canonical scene."""

    place_name: str
    stable_key: str
    spec: SemanticSceneSpec
    cache_key: str
    source_refs: tuple[str, ...] = ()
    confidence: float = 0.0
    style_key: str = ""
    context_candidates: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class _SourceTopologyRelation:
    """An explicit, source-grounded relation between named places."""

    source_place: str
    target_place: str
    relation_type: str
    source_refs: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(frozen=True, slots=True)
class _SourceVisualPlan:
    """Explicit budget/rights result for the generic book-to-visual pipeline."""

    package_id: str
    source_digest: str
    status: str
    scene_requests: tuple[_SourceSceneRequest, ...]
    deferred_scene_count: int
    delivery_rights: str = "source-gated"
    external_processing_allowed: bool = False
    topology_relations: tuple[_SourceTopologyRelation, ...] = ()
    place_names: tuple[str, ...] = ()

    @property
    def image_provider_calls(self) -> int:
        """Planning never calls a billable image provider."""
        return 0


def _plan_book_scene_assets(
    package: WorldPackageDraft,
    *,
    max_preview_scenes: int = 3,
    preferred_places: tuple[str, ...] = (),
) -> _SourceVisualPlan:
    """Select a small reusable, source-pinned scene set for any book package.

    Places are declared source-derived *names*, not inferred spatial coordinates.
    Characters/objects from a book are not automatically assigned to a place:
    the current WorldDraft has no trustworthy place-to-entity mapping.

    Remote image generation requires a separate permission and a configured
    provider; this function creates no image, geometry or canonical history.
    """
    if not 0 <= max_preview_scenes <= 12:
        raise ValueError("max_preview_scenes must be within [0, 12]")

    raw_fingerprints = package.draft.compiler_metadata.get("source_fingerprints_v1", "[]")
    decoded_fingerprints = _json_list(raw_fingerprints)
    fingerprints = tuple(
        sorted(item for item in decoded_fingerprints if isinstance(item, str) and item)
    )
    source_identity = json.dumps(
        {
            "source_fingerprints": fingerprints,
            "source_versions": package.source_versions if not fingerprints else (),
            "draft_revision": package.draft_revision,
        },
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    source_digest = hashlib.sha256(source_identity.encode("utf-8")).hexdigest()

    if not package.rights_ok:
        return _SourceVisualPlan(package.package_id, source_digest, "RIGHTS_BLOCKED", (), 0)
    if not package.source_versions:
        return _SourceVisualPlan(package.package_id, source_digest, "SOURCE_PINS_MISSING", (), 0)

    # No invented map nodes: a sparse or unrecognized book stays honestly sparse.
    distinct_places = tuple(dict.fromkeys(p.strip() for p in package.draft.places if p.strip()))
    if not distinct_places:
        return _SourceVisualPlan(package.package_id, source_digest, "PLACES_NOT_EXTRACTED", (), 0)

    raw_topology = package.draft.compiler_metadata.get("scene_topology_evidence_v1", "[]")
    decoded_topology = _json_list(raw_topology)
    topology_relations: list[_SourceTopologyRelation] = []
    known_places = set(distinct_places)
    for raw_row in decoded_topology:
        row = _object_dict(raw_row)
        if row is None:
            continue
        source_place = row.get("source_place")
        target_place = row.get("target_place")
        relation_type = row.get("relation_type")
        if (
            not isinstance(source_place, str)
            or not isinstance(target_place, str)
            or not isinstance(relation_type, str)
            or source_place not in known_places
            or target_place not in known_places
        ):
            continue
        source_refs = _string_list(row.get("source_refs", []))
        raw_confidence = row.get("confidence", 0.0)
        confidence = float(raw_confidence) if isinstance(raw_confidence, (int, float)) else 0.0
        topology_relations.append(
            _SourceTopologyRelation(
                source_place=source_place,
                target_place=target_place,
                relation_type=relation_type,
                source_refs=source_refs,
                confidence=confidence,
            )
        )
    delivery_rights = package.draft.compiler_metadata.get("visual_asset_rights_v1", "source-gated")
    if delivery_rights not in {"public", "source-gated"}:
        delivery_rights = "source-gated"
    external_processing_allowed = (
        package.draft.compiler_metadata.get("external_visual_processing_allowed_v1", "false")
        == "true"
    )
    style_key = hashlib.sha256(f"{source_digest}:story-visual-profile:v1".encode()).hexdigest()[:24]
    raw_evidence = package.draft.compiler_metadata.get("scene_evidence_v1", "[]")
    evidence_rows = _json_list(raw_evidence)

    place_positions = {place: index for index, place in enumerate(distinct_places)}

    def place_rank(place: str) -> tuple[int, float, int, int, str, int]:
        matching = [
            row
            for raw_row in evidence_rows
            if (row := _object_dict(raw_row)) is not None and row.get("name") == place
        ]
        refs = {ref for row in matching for ref in _string_list(row.get("source_refs", []))}
        confidence_values = [
            float(raw_confidence)
            for row in matching
            if isinstance((raw_confidence := row.get("confidence", 0.0)), (int, float))
        ]
        confidence = max(confidence_values, default=0.0)
        context_count = sum(
            len(cast(list[object], raw_context))
            for row in matching
            if isinstance((raw_context := row.get("cooccurring_candidates", [])), list)
        )
        first_ref = min(refs, default="")
        return (
            -len(refs),
            -confidence,
            -context_count,
            0 if refs else 1,
            first_ref,
            place_positions[place],
        )

    ranked_places = tuple(sorted(distinct_places, key=place_rank))
    preferred = tuple(
        dict.fromkeys(
            place.strip()
            for place in preferred_places
            if place.strip() and place.strip() in place_positions
        )
    )
    selected = tuple(dict.fromkeys((*preferred, *ranked_places)))[:max_preview_scenes]

    requests: list[_SourceSceneRequest] = []
    for place in selected:
        matching = [
            row
            for raw_row in evidence_rows
            if (row := _object_dict(raw_row)) is not None and row.get("name") == place
        ]
        source_refs = tuple(
            sorted({ref for row in matching for ref in _string_list(row.get("source_refs", []))})
        )
        confidence_values = [
            float(raw_confidence)
            for row in matching
            if isinstance((raw_confidence := row.get("confidence", 0.0)), (int, float))
        ]
        confidence = max(confidence_values, default=0.0)
        context_candidates: list[str] = []
        for row in matching:
            raw_context = row.get("cooccurring_candidates", [])
            if not isinstance(raw_context, list):
                continue
            for raw_item in cast(list[object], raw_context):
                item = _object_dict(raw_item)
                if item is None:
                    continue
                kind, label = item.get("kind"), item.get("label")
                if isinstance(kind, str) and isinstance(label, str) and label:
                    context_candidates.append(f"{kind}:{label}")
        context_candidates = list(dict.fromkeys(context_candidates))[:8]
        stable_key = hashlib.sha256(
            json.dumps((source_digest, place), ensure_ascii=False).encode("utf-8")
        ).hexdigest()[:24]
        # Style/media decisions are made by the Experience / provider, not by a
        # city-specific hand-authored renderer. Label is source-derived context.
        spec = SemanticSceneSpec(
            spec_id=f"source-scene-{stable_key}",
            semantic_id=f"place:{stable_key}",
            kind="illustrated-environment",
            requirements=(
                f"source_place_name:{place}",
                f"source_identity_digest:{source_digest}",
                *(f"source_locator:{ref}" for ref in source_refs),
                *(f"source_context_candidate:{item}" for item in context_candidates),
                f"source_confidence:{confidence:.3f}",
                "noncanonical_asset_candidate",
                "no_unverified_character_placement",
            ),
        )
        requests.append(
            _SourceSceneRequest(
                place_name=place,
                stable_key=stable_key,
                spec=spec,
                cache_key=hashlib.sha256(
                    (
                        f"{source_digest}:{stable_key}:illustrated-environment:"
                        f"{style_key}:prompt-v1"
                    ).encode()
                ).hexdigest(),
                source_refs=source_refs,
                confidence=confidence,
                style_key=style_key,
                context_candidates=tuple(context_candidates),
            )
        )
    status = "READY_FOR_ASSET_PROVIDER" if requests else "BUDGET_ZERO"
    return _SourceVisualPlan(
        package_id=package.package_id,
        source_digest=source_digest,
        status=status,
        scene_requests=tuple(requests),
        deferred_scene_count=len(distinct_places) - len(requests),
        delivery_rights=delivery_rights,
        external_processing_allowed=external_processing_allowed,
        topology_relations=tuple(dict.fromkeys(topology_relations)),
        place_names=distinct_places,
    )
