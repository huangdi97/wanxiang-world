"""M83 structured evidence, mixed fusion, and single WorldDraft contracts."""

from __future__ import annotations

import json

import pytest
from wanxiang_substrate.authoring.fusion import fuse_candidates
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.pipeline import SourceToDraftPipeline
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.sources.structured_evidence import (
    csv_cell_locator,
    json_leaf_evidence,
    json_pointer_locator,
    resolve_csv_cell,
    resolve_json_pointer,
)


def _record(source_id: str, kind: str, payload: str) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind=kind,
        content_hash=payload_hash(payload),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic-m83", usage="qualification", approved=True),
        payload=payload,
        provenance="synthetic:m83",
        access="public",
    )


@pytest.mark.integration
def test_json_pointer_and_csv_cell_locators_round_trip() -> None:
    payload = json.dumps({"people": [{"name": "Ada"}], "place": "Harbor"})
    pointer = json_pointer_locator("json_m83", "/people/0/name")
    assert pointer.to_string() == "json://json_m83#record//people/0/name"
    assert resolve_json_pointer(payload, pointer.ref) == '"Ada"'
    assert json_leaf_evidence("json_m83", payload)
    csv_payload = "name,year,place\nAda,1980,Harbor\n"
    cell = csv_cell_locator("csv_m83", 2, 3)
    assert cell.ref == "row_2/column_3"
    assert resolve_csv_cell(csv_payload, 2, 3) == "Harbor"


@pytest.mark.integration
def test_structured_and_mixed_sources_converge_to_one_draft_and_preserve_conflict() -> None:
    book = _record(
        "book_m83",
        "text",
        "# Chapter\nCharacter: Ada\nAda arrived in 1980 at Harbor.\n",
    )
    structured = _record(
        "json_m83",
        "json",
        json.dumps({"people": [{"name": "Ada"}], "place": "Harbor"}),
    )
    csv = _record("csv_m83", "csv", "name,year,place\nAda,1980,Harbor\n")
    build = SourceToDraftPipeline().run((book, structured, csv), draft_id="wd_m83_mixed")
    assert build.draft.draft_id == "wd_m83_mixed"
    assert build.draft.source_refs == ("book_m83", "csv_m83", "json_m83")
    assert build.draft.entities
    assert all(candidate.source_refs for candidate in build.candidates)
    assert any(key == "identity:ada" for key, _ids, _sources in build.fusion_alignments)
    result = fuse_candidates(
        build.candidates
        + (
            CandidateEnvelope(
                "contradiction_m83",
                "place",
                "m83_conflict",
                (("name", "Harbor"), ("claim", "alternate")),
                0.7,
                ("json_m83#record//place",),
                1,
            ),
        )
    )
    assert result.alignments
    assert result.conflict_ids
    assert len(build.draft.source_refs) == 3
    one_click = OneClickAuthoring().run("job_m83_mixed", (book, structured, csv), profile="mixed")
    assert one_click.package.draft.draft_id == "wd_job_m83_mixed"
    assert one_click.preview.scoped_ref.startswith("preview://")
    assert one_click.package.manifest.content_hash
