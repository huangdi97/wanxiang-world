"""Synthetic compiler input sources for G04C (explicitly synthetic)."""

from __future__ import annotations

import json

from wanxiang_substrate.sources.model import SourceRecord, payload_hash


def json_source() -> SourceRecord:
    payload = json.dumps(
        {
            "objects": {
                "town": {
                    "kind": "entity",
                    "payload": {
                        "entity_id": "town",
                        "entity_type": "spatial.place",
                        "name": "Town",
                    },
                }
            }
        },
        sort_keys=True,
    )
    return SourceRecord(
        source_id="src_objects_json",
        kind="json",
        content_hash=payload_hash(payload),
        content_ref="ref://objects.json",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance="fixture:json",
    )


def yaml_source() -> SourceRecord:
    payload = (
        "objects:\n"
        "  town:\n"
        "    kind: entity\n"
        "    payload:\n"
        "      entity_id: town\n"
        "      entity_type: spatial.place\n"
        "      name: Town\n"
    )
    return SourceRecord(
        source_id="src_objects_yaml",
        kind="yaml",
        content_hash=payload_hash(payload),
        content_ref="ref://objects.yaml",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance="fixture:yaml",
    )


def markdown_source() -> SourceRecord:
    payload = "## town\nentity_id: town\nentity_type: spatial.place\nname: Town\n"
    return SourceRecord(
        source_id="src_objects_md",
        kind="markdown",
        content_hash=payload_hash(payload),
        content_ref="ref://objects.md",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance="fixture:markdown",
    )


def text_source() -> SourceRecord:
    payload = "A plain historical note about the town."
    return SourceRecord(
        source_id="src_note_txt",
        kind="text",
        content_hash=payload_hash(payload),
        content_ref="ref://note.txt",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance="fixture:text",
    )


def pdf_source() -> SourceRecord:
    payload = "fake pdf bytes"
    return SourceRecord(
        source_id="src_doc_pdf",
        kind="pdf",
        content_hash=payload_hash(payload),
        content_ref="ref://doc.pdf",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance="fixture:pdf",
    )


def malformed_json_source() -> SourceRecord:
    payload = '{"objects": {'
    return SourceRecord(
        source_id="src_bad_json",
        kind="json",
        content_hash=payload_hash(payload),
        content_ref="ref://bad.json",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance="fixture:bad_json",
    )


def oversized_source() -> SourceRecord:
    payload = "x" * (64 * 1024 + 1)
    return SourceRecord(
        source_id="src_huge_txt",
        kind="text",
        content_hash=payload_hash(payload),
        content_ref="ref://huge.txt",
        stage="E3",
        rights=approved_rights(),
        payload=payload,
        provenance="fixture:oversized",
    )


def approved_rights():
    from wanxiang_substrate.sources.model import RightsEnvelope

    return RightsEnvelope(owner="town-archive", usage="canonical", approved=True)
