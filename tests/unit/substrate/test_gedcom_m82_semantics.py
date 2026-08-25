"""M82 generic GEDCOM semantics: identity, family facts, uncertainty, evidence."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_substrate.authoring.pipeline_support import default_domain_registry, distiller_dag
from wanxiang_substrate.distill.gedcom import identity_key
from wanxiang_substrate.genealogy.gedcom import parse_gedcom, serialize_gedcom
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, Segment, build_segments
from wanxiang_substrate.sources.adapter import IngestResult

_GEDCOM = """0 HEAD
1 SOUR generic-fixture
2 VERS 7.0
1 GEDC
2 VERS 5.5.1
0 @I1@ INDI
1 NAME Alex /Smith/
1 FAMC @F1@
1 FAMS @F2@
1 BIRT
2 DATE 1900
2 PLAC Leeds
1 DEAT
2 DATE ABT 1970
0 @I2@ INDI
1 NAME Alex /Smith/
1 BIRT
2 DATE 1901-02-03
0 @F1@ FAM
1 HUSB @I2@
1 WIFE @I1@
1 CHIL @I3@
1 MARR
2 DATE BET 1880 AND 1882
2 PLAC York
0 @F2@ FAM
1 HUSB @I1@
0 TRLR
"""


def _segments() -> tuple[Segment, ...]:
    result = IngestResult(source_id="m82", kind="gedcom", content=_GEDCOM, detected_format="gedcom")
    parsed = StructureParser().parse(result, source_id="m82", version="1")
    return build_segments(parsed, fmt=cast(LocatorFormat, "gedcom"))


@pytest.mark.unit
def test_parser_preserves_header_xrefs_family_refs_and_date_uncertainty() -> None:
    document = parse_gedcom(_GEDCOM)
    assert document.version == "5.5.1"
    assert document.header_source == "generic-fixture"
    assert document.header_source_version == "7.0"
    assert document.individual("I1").family_child_refs == ("F1",)  # type: ignore[union-attr]
    assert document.individual("I1").family_spouse_refs == ("F2",)  # type: ignore[union-attr]
    marriage = next(event for event in document.families[0].events if event.tag == "MARR")
    assert marriage.date_precision == "range"
    assert marriage.uncertain is True
    assert marriage.place == "York"
    serialized = serialize_gedcom(document)
    assert "2 VERS 5.5.1" in serialized
    assert "1 FAMC @F1@" in serialized
    assert "2 DATE BET 1880 AND 1882" in serialized


@pytest.mark.unit
def test_distillation_scopes_identity_to_xref_and_keeps_family_world_facts() -> None:
    segments = _segments()
    candidates = distiller_dag().run(segments, source_id="m82")
    identities = [candidate for candidate in candidates if candidate.kind == "identity"]
    assert len(identities) == 2
    assert {candidate.fields["key"] for candidate in identities} == {
        identity_key("m82", "I1"),
        identity_key("m82", "I2"),
    }
    family_entities = [
        candidate
        for candidate in candidates
        if candidate.kind == "organization" and candidate.fields.get("entity_type") == "family"
    ]
    assert {candidate.fields["family_xref"] for candidate in family_entities} == {"F1", "F2"}
    assert any(candidate.fields.get("relation_type") == "parent" for candidate in candidates)
    assert any(candidate.fields.get("relation_type") == "spouse" for candidate in candidates)
    marriage = [
        candidate for candidate in candidates if candidate.fields.get("event_type") == "marriage"
    ]
    assert marriage and marriage[0].fields["date_precision"] == "range"
    assert all(candidate.source_refs and candidate.evidence_refs for candidate in candidates)
    event_types = {candidate.fields.get("event_type") for candidate in candidates}
    assert not event_types.intersection({"residence", "migration", "education", "occupation"})


@pytest.mark.unit
def test_selected_domain_completion_does_not_require_unselected_rules() -> None:
    from wanxiang_substrate.authoring.draft_builder import build_pipeline_build
    from wanxiang_substrate.authoring.semantic_distillation import DistillationStats
    from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

    record = SourceRecord(
        source_id="m82",
        kind="gedcom",
        content_hash=payload_hash(_GEDCOM),
        content_ref="fixture://m82",
        stage="E3",
        rights=RightsEnvelope(
            owner="fixture", usage="test", approved=True, package_inclusion_allowed=True
        ),
        payload=_GEDCOM,
    )
    segments = _segments()
    candidates = distiller_dag().run(segments, source_id="m82")
    build = build_pipeline_build(
        (record,),
        draft_id="wd_m82_fixture",
        candidates=candidates,
        segments=segments,
        diagnostics=(),
        parsed_nodes=len(segments),
        distillation=DistillationStats(segment_count=len(segments)),
        domains=default_domain_registry(),
    )
    assert build.draft.coverage > 0
    assert build.draft.completion_items == ()
    assert build.draft.status == "READY_TO_COMPILE"
