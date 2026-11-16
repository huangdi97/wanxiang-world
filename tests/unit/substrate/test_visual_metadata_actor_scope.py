"""Owned objects carry ownership metadata into the visual plan, not just labels."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json

import pytest
from wanxiang_substrate.authoring.visual_metadata import (
    _ownership,
    _visual_compiler_metadata,
)
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def test_visual_metadata_records_object_actor() -> None:
    text = "# Chapter\nCharacter: Alice\nShe carries the Key.\n"
    source = SourceRecord(
        source_id="actor-scope",
        kind="text",
        content_hash=payload_hash(text),
        content_ref="memory://actor-scope",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=text,
        access="public",
    )
    refs = ("source://actor-scope#chapter-1",)
    place = CandidateEnvelope(
        candidate_id="place-garden",
        kind="place",
        origin_pass="test",
        payload=(("name", "Garden"),),
        confidence=0.8,
        source_refs=refs,
        distiller_version=1,
    )
    key = CandidateEnvelope(
        candidate_id="object-key",
        kind="object",
        origin_pass="test",
        payload=(("name", "Key"), ("actor", "Alice")),
        confidence=0.7,
        source_refs=refs,
        distiller_version=1,
    )

    metadata = _visual_compiler_metadata((source,), (place, key))
    evidence = json.loads(metadata["scene_evidence_v1"])

    context = evidence[0]["cooccurring_candidates"]
    assert context == [
        {
            "candidate_id": "object-key",
            "kind": "object",
            "label": "Key",
            "confidence": 0.7,
            "actor": "Alice",
        }
    ]


@pytest.mark.parametrize(
    "sentinel",
    ["unknown", "none", "N/A", "na", "null", "nil", "anonymous", "-", "?"],
)
def test_ownership_sentinels_do_not_mask_concrete_owner(sentinel: str) -> None:
    text = "# Chapter\nCharacter: Alice\nShe carries the Key.\n"
    source = SourceRecord(
        source_id="actor-unknown-scope",
        kind="text",
        content_hash=payload_hash(text),
        content_ref="memory://actor-unknown-scope",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=text,
        access="public",
    )
    refs = ("source://actor-unknown-scope#chapter-1",)
    place = CandidateEnvelope(
        candidate_id="place-garden",
        kind="place",
        origin_pass="test",
        payload=(("name", "Garden"),),
        confidence=0.8,
        source_refs=refs,
        distiller_version=1,
    )
    key = CandidateEnvelope(
        candidate_id="object-key",
        kind="object",
        origin_pass="test",
        payload=(("name", "Key"), ("actor", sentinel), ("owner", "Alice")),
        confidence=0.7,
        source_refs=refs,
        distiller_version=1,
    )

    metadata = _visual_compiler_metadata((source,), (place, key))
    context = json.loads(metadata["scene_evidence_v1"])[0]["cooccurring_candidates"]

    assert context[0]["actor"] == "Alice"


def test_sentinel_only_ownership_is_not_recorded() -> None:
    key = CandidateEnvelope(
        candidate_id="object-key",
        kind="object",
        origin_pass="test",
        payload=(("name", "Key"), ("actor", "none"), ("owner", "N/A")),
        confidence=0.7,
        source_refs=("source://actor-scope#chapter-1",),
        distiller_version=1,
    )

    assert _ownership(key) == ""
