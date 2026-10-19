"""Budgeted source-driven visual scene requests over existing WorldDraft.

This is an Asset Foundry preparation step, NOT a renderer or a generated image.
No paid API calls, world-specific templates, canonical writes, or invented geography.
"""

# pyright: reportUnusedFunction=false, reportPrivateUsage=false

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.assets.book_scene_context import (
    _context_candidates,
    _place_identity,
)
from wanxiang_substrate.assets.book_scene_evidence import (
    _cache_evidence_ref,
    _json_list,
    _json_string_map,
    _object_dict,
)
from wanxiang_substrate.assets.book_scene_identity import _source_scene_key
from wanxiang_substrate.assets.book_scene_ranking import _rank_places
from wanxiang_substrate.assets.book_scene_topology import (
    _SourceTopologyRelation,
    _topology_relations,
)
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.compile.assembler import WorldPackageDraft


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
class _PlaceEvidence:
    """Per-place source support used by the Atlas; never canonical geography."""

    place_name: str
    source_ref_count: int
    confidence: float
    clue_count: int
    source_count: int = 1


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
    place_evidence: tuple[_PlaceEvidence, ...] = ()


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
        sorted({item for item in decoded_fingerprints if isinstance(item, str) and item})
    )
    fingerprint_map = _json_string_map(
        package.draft.compiler_metadata.get("source_fingerprint_map_v1", "{}")
    )
    if not fingerprint_map and len(package.source_versions) == len(fingerprints) == 1:
        fingerprint_map = {package.source_versions[0][0]: fingerprints[0]}
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
    # Case/whitespace variants of the same source place are one place; the first
    # spelling remains the display name and every source ref is retained.
    place_aliases: dict[str, str] = {}
    distinct_places_list: list[str] = []
    for raw_place in package.draft.places:
        name = raw_place.strip()
        if not name:
            continue
        identity = _place_identity(name)
        if identity not in place_aliases:
            place_aliases[identity] = name
            distinct_places_list.append(name)
    distinct_places = tuple(distinct_places_list)
    if not distinct_places:
        return _SourceVisualPlan(package.package_id, source_digest, "PLACES_NOT_EXTRACTED", (), 0)

    known_places = set(distinct_places)
    topology_relations = _topology_relations(
        package.draft.compiler_metadata.get("scene_topology_evidence_v1", "[]"),
        known_places,
        place_aliases,
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
    # Index source evidence once. Scanning every candidate for every place is
    # quadratic in large works with thousands of named locations.
    evidence_by_place: dict[str, list[dict[str, object]]] = {}
    for raw_row in evidence_rows:
        row = _object_dict(raw_row)
        if row is None:
            continue
        name = row.get("name")
        if isinstance(name, str):
            canonical = place_aliases.get(_place_identity(name))
            if canonical is not None and canonical in known_places:
                evidence_by_place.setdefault(canonical, []).append(row)

    ranked_places, stats_by_place = _rank_places(distinct_places, evidence_by_place)
    preferred_list: list[str] = []
    for requested_place in preferred_places:
        canonical = place_aliases.get(_place_identity(requested_place))
        if canonical is not None and canonical in stats_by_place:
            preferred_list.append(canonical)
    preferred = tuple(dict.fromkeys(preferred_list))
    selected = tuple(dict.fromkeys((*preferred, *ranked_places)))[:max_preview_scenes]

    requests: list[_SourceSceneRequest] = []
    for place in selected:
        matching = evidence_by_place.get(place, [])
        stats_refs, confidence, _ = stats_by_place[place]
        source_refs = tuple(sorted(stats_refs))
        context_candidates = _context_candidates(matching)
        # Cache identity may use content fingerprints, while audit/projection
        # keeps the original source locators unchanged.
        cache_evidence_refs = tuple(
            sorted(
                {
                    _cache_evidence_ref(ref, source_fingerprints=fingerprint_map)
                    for ref in source_refs
                }
            )
        )
        evidence_identity = json.dumps(
            {
                "source_refs": cache_evidence_refs,
                "confidence": confidence,
                "context_candidates": context_candidates,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        evidence_digest = hashlib.sha256(evidence_identity.encode("utf-8")).hexdigest()
        stable_key = _source_scene_key(source_digest, place)
        # Style/media decisions are made by the Experience / provider, not by a
        # city-specific hand-authored renderer. Label is source-derived context.
        spec = SemanticSceneSpec(
            spec_id=f"source-scene-{stable_key}",
            semantic_id=f"place:{stable_key}",
            kind="illustrated-environment",
            requirements=(
                f"source_place_name:{place}",
                f"source_identity_digest:{source_digest}",
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
                        f"{style_key}:prompt-v1:evidence-v1:{evidence_digest}"
                    ).encode()
                ).hexdigest(),
                source_refs=source_refs,
                confidence=confidence,
                style_key=style_key,
                context_candidates=tuple(context_candidates),
            )
        )
    status = "READY_FOR_ASSET_PROVIDER" if requests else "BUDGET_ZERO"
    place_evidence: list[_PlaceEvidence] = []
    for place in ranked_places:
        refs, confidence, context_count = stats_by_place[place]
        source_ids = {
            ref.partition("://")[2].partition("#")[0] if "://" in ref else ref.partition("#")[0]
            for ref in refs
        }
        place_evidence.append(
            _PlaceEvidence(
                place_name=place,
                source_ref_count=len(refs),
                confidence=confidence,
                clue_count=context_count,
                source_count=len(source_ids),
            )
        )
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
        place_evidence=tuple(place_evidence),
    )
