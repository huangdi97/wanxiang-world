"""Visual compiler metadata derived from source rights and fused evidence."""

# pyright: reportUnusedFunction=false

from __future__ import annotations

import json

from wanxiang_substrate.authoring.pipeline_support import field
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.sources.model import SourceRecord


def _compact(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _ownership(candidate: CandidateEnvelope) -> str:
    """Return the first concrete owner, ignoring placeholder 'unknown'."""
    for key in ("actor", "owner", "custodian"):
        value = candidate.fields.get(key, "").strip()
        if value and value.casefold() != "unknown":
            return value
    return ""


def _visual_compiler_metadata(
    records: tuple[SourceRecord, ...],
    candidates: tuple[CandidateEnvelope, ...],
) -> dict[str, str]:
    """Build source-pinned visual metadata without creating canonical facts."""
    source_map = {record.source_id: record.fingerprint() for record in records}
    context_kinds = {"identity", "character", "organization", "object", "event"}
    scene_evidence = [
        {
            "candidate_id": candidate.candidate_id,
            "name": field(candidate, "name"),
            "source_refs": list(candidate.source_refs),
            "confidence": candidate.confidence,
            "place_role": field(candidate, "place_role"),
            "subject_xref": field(candidate, "subject_xref"),
            "cooccurring_candidates": [
                {
                    "candidate_id": other.candidate_id,
                    "kind": other.kind,
                    "label": field(
                        other,
                        "display_name",
                        "name",
                        "event_type",
                        "statement",
                    ),
                    "confidence": other.confidence,
                    "actor": _ownership(other),
                }
                for other in candidates
                if other.candidate_id != candidate.candidate_id
                and set(other.source_refs).intersection(candidate.source_refs)
                and other.kind in context_kinds
                and field(
                    other,
                    "display_name",
                    "name",
                    "event_type",
                    "statement",
                )
            ][:16],
        }
        for candidate in candidates
        if candidate.kind == "place" and field(candidate, "name")
    ]
    topology = [
        {
            "candidate_id": candidate.candidate_id,
            "source_place": field(candidate, "source_place"),
            "target_place": field(candidate, "target_place"),
            "relation_type": field(candidate, "relation_type"),
            "source_refs": list(candidate.source_refs),
            "confidence": candidate.confidence,
        }
        for candidate in candidates
        if candidate.kind in {"place_relation", "topology", "connectivity", "containment"}
        and field(candidate, "source_place")
        and field(candidate, "target_place")
    ]
    return {
        "source_fingerprints_v1": _compact(sorted(source_map.values())),
        "source_fingerprint_map_v1": _compact(source_map),
        "visual_asset_rights_v1": (
            "public"
            if records
            and all(
                record.access == "public"
                and record.rights is not None
                and record.rights.allows("public_export")
                for record in records
            )
            else "source-gated"
        ),
        "external_visual_processing_allowed_v1": (
            "true"
            if records
            and all(
                record.rights is not None and record.rights.allows("external_model_processing")
                for record in records
            )
            else "false"
        ),
        "visual_private_source_v1": (
            "true" if any(record.access != "public" for record in records) else "false"
        ),
        "scene_evidence_v1": _compact(scene_evidence),
        "scene_topology_evidence_v1": _compact(topology),
    }
