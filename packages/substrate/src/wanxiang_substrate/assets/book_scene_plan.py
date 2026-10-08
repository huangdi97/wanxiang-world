"""Budgeted source-driven visual scene requests over existing WorldDraft.

This is an Asset Foundry preparation step, NOT a renderer or a generated image.
No paid API calls, world-specific templates, canonical writes, or invented geography.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

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


@dataclass(frozen=True, slots=True)
class _SourceVisualPlan:
    """Explicit budget/rights result for the generic book-to-visual pipeline."""

    package_id: str
    source_digest: str
    status: str
    scene_requests: tuple[_SourceSceneRequest, ...]
    deferred_scene_count: int

    @property
    def image_provider_calls(self) -> int:
        """Planning never calls a billable image provider."""
        return 0


def _plan_book_scene_assets(
    package: WorldPackageDraft, *, max_preview_scenes: int = 3
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

    source_identity = json.dumps(
        {
            "package_hash": package.manifest.content_hash,
            "source_versions": package.source_versions,
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

    selected = distinct_places[:max_preview_scenes]
    style_key = hashlib.sha256(
        f"{source_digest}:story-visual-profile:v1".encode()
    ).hexdigest()[:24]
    raw_evidence = package.draft.compiler_metadata.get("scene_evidence_v1", "[]")
    try:
        decoded = json.loads(raw_evidence)
    except (TypeError, ValueError):
        decoded = []
    evidence_rows = decoded if isinstance(decoded, list) else []

    requests: list[_SourceSceneRequest] = []
    for place in selected:
        matching = [
            row
            for row in evidence_rows
            if isinstance(row, dict) and row.get("name") == place
        ]
        source_refs = tuple(
            sorted(
                {
                    str(ref)
                    for row in matching
                    for ref in row.get("source_refs", [])
                    if isinstance(ref, str) and ref
                }
            )
        )
        confidence = max(
            (
                float(row.get("confidence", 0.0))
                for row in matching
                if isinstance(row.get("confidence", 0.0), (int, float))
            ),
            default=0.0,
        )
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
                    f"{source_digest}:{stable_key}:illustrated-environment:v1".encode()
                ).hexdigest(),
                source_refs=source_refs,
                confidence=confidence,
                style_key=style_key,
            )
        )
    status = "READY_FOR_ASSET_PROVIDER" if requests else "BUDGET_ZERO"
    return _SourceVisualPlan(
        package_id=package.package_id,
        source_digest=source_digest,
        status=status,
        scene_requests=tuple(requests),
        deferred_scene_count=len(distinct_places) - len(requests),
    )
