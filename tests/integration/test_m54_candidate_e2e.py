"""G57I: M54 deterministic candidate E2E — book / GEDCOM / structured.

Source -> Adapter -> Parse -> Segment -> Distill DAG -> CandidateEnvelopes,
deterministic (no API), every candidate has source refs and status=pending.
"""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill.passes import (
    EventTimeSpacePass,
    IdentityPass,
    RelationOrganizationPass,
)
from wanxiang_substrate.distill.passes_knowledge import (
    CharacterKnowledgePass,
    ObjectRuleSkillPass,
)
from wanxiang_substrate.distill.protocol import DistillerDAG
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, build_segments
from wanxiang_substrate.sources.book import BookAdapter
from wanxiang_substrate.sources.structured import StructuredAdapter

GEDCOM = """0 @I1@ INDI
1 NAME Alice /Zhang/
1 BIRT
2 DATE 1980-01-01
2 PLAC Beijing
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
"""

BOOK = """# Chapter One

Alice Zhang entered the garden at dawn.
rule: no duels at dawn
secret: the garden key is hidden.

# Chapter Two

In 1985, she left Beijing.
"""

JSON_SRC = '{"person": {"name": "Alice", "year": 1980}, "place": "Beijing"}'
CSV_SRC = "id,name,year\n1,Alice,1980\n2,Bob,1982\n"


def _dag() -> DistillerDAG:
    return DistillerDAG(
        (
            IdentityPass(),
            EventTimeSpacePass(),
            RelationOrganizationPass(),
            CharacterKnowledgePass(),
            ObjectRuleSkillPass(),
        )
    )


def _run(
    kind: str, content: str, fmt: str, blob: bytes | None = None
) -> tuple[CandidateEnvelope, ...]:
    adapter = (
        BookAdapter()
        if kind in ("epub", "docx", "pdf", "text", "markdown")
        else StructuredAdapter()
    )
    record = None
    from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

    record = SourceRecord(
        source_id="src_e2e",
        kind=kind,
        content_hash=payload_hash(content),
        content_ref="ref://e2e",
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload=content,
        provenance="fixture:m54",
    )
    result = adapter.ingest(record, blob)
    parsed = StructureParser().parse(result, source_id="src_e2e", version="1")
    segments = build_segments(parsed, fmt=cast(LocatorFormat, fmt))
    return _dag().run(segments, source_id="src_e2e")


@pytest.mark.integration
def test_book_deterministic_candidates() -> None:
    first = _run("text", BOOK, "text")
    second = _run("text", BOOK, "text")
    assert [c.compute_hash() for c in first] == [c.compute_hash() for c in second]
    kinds = {c.kind for c in first}
    assert "rule" in kinds  # ObjectRuleSkillPass
    assert "time" in kinds  # EventTimeSpacePass (1985)
    assert "knowledge_boundary" in kinds  # secret line
    assert all(c.source_refs for c in first)
    assert all(c.status == "pending" for c in first)


@pytest.mark.integration
def test_gedcom_deterministic_candidates() -> None:
    candidates = _run("gedcom", GEDCOM, "gedcom")
    assert candidates
    kinds = {c.kind for c in candidates}
    assert "identity" in kinds
    assert "event" in kinds
    assert "relation" in kinds
    assert all(c.status == "pending" for c in candidates)
    identities = [c for c in candidates if c.kind == "identity"]
    assert dict(identities[0].payload)["display_name"] == "Alice Zhang"


@pytest.mark.integration
def test_structured_deterministic_candidates() -> None:
    json_candidates = _run("json", JSON_SRC, "json")
    assert all(c.status == "pending" for c in json_candidates)
    csv_candidates = _run("csv", CSV_SRC, "csv")
    assert all(c.status == "pending" for c in csv_candidates)


@pytest.mark.integration
def test_no_candidate_is_canon() -> None:
    """CandidateEnvelope never carries a canonical-eligible flag."""
    candidates = _run("text", BOOK, "text")
    assert all(c.status == "pending" for c in candidates)
