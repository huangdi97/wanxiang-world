"""G56C/G56D: Segment model + format-aware stable locators (M53)."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.parsing.model import ParsedDocument
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import (
    Segment,
    StableLocator,
    build_segments,
    resolve,
)
from wanxiang_substrate.sources.adapter import IngestResult


def _parsed(kind: str, content: str, fmt: str) -> ParsedDocument:
    result = IngestResult(source_id="s1", kind=kind, content=content, detected_format=fmt)
    return StructureParser().parse(result, source_id="s1", version="1")


@pytest.mark.unit
def test_locator_roundtrip_string() -> None:
    locator = StableLocator(source_id="s1", fmt="epub", kind="chapter", ref="2")
    restored = StableLocator.from_string(locator.to_string())
    assert restored == locator
    assert locator.to_string() == "epub://s1#chapter/2"


@pytest.mark.unit
def test_locator_validation() -> None:
    with pytest.raises(ContractError):
        StableLocator(source_id="", fmt="epub", kind="chapter", ref="1")
    with pytest.raises(ContractError):
        StableLocator.from_string("bogus")


@pytest.mark.unit
def test_segment_hash_stable_and_versioned() -> None:
    a = Segment(
        segment_id="seg1",
        locator=StableLocator("s", "text", "paragraph", "1"),
        text="x",
        kind="paragraph",
        ordinal=1,
        parser_version=1,
        segmenter_version=1,
    )
    b = Segment(
        segment_id="seg1",
        locator=StableLocator("s", "text", "paragraph", "1"),
        text="x",
        kind="paragraph",
        ordinal=1,
        parser_version=1,
        segmenter_version=1,
    )
    assert a.compute_hash() == b.compute_hash()


@pytest.mark.unit
def test_book_segments_and_resolve_roundtrip() -> None:
    parsed = _parsed(
        "text", "# Chapter One\n\nFirst para.\n\n# Chapter Two\n\nSecond para.", "text"
    )
    segments = build_segments(parsed, fmt="text")
    assert any(s.kind == "chapter" for s in segments)
    chapter = next(s for s in segments if s.kind == "chapter" and s.ordinal == 1)
    assert resolve(parsed, chapter.locator) == "Chapter One"
    para = next(s for s in segments if s.kind == "paragraph" and "First para." in s.text)
    assert resolve(parsed, para.locator) == "First para."


@pytest.mark.unit
def test_json_csv_gedcom_locators() -> None:
    json_doc = _parsed("json", '{"name": "Alice", "age": 30}', "json")
    json_segments = build_segments(json_doc, fmt="json")
    assert any(s.locator.fmt == "json" and s.locator.ref == "name" for s in json_segments)

    csv_doc = _parsed("csv", "id\tname\n1\tAlice", "csv")
    csv_segments = build_segments(csv_doc, fmt="csv")
    assert any(s.locator.fmt == "csv" and s.locator.ref == "2" for s in csv_segments)

    ged = "0 @I1@ INDI\n1 NAME Alice /Zhang/\n"
    ged_doc = _parsed("gedcom", ged, "gedcom")
    ged_segments = build_segments(ged_doc, fmt="gedcom")
    assert any(s.locator.fmt == "gedcom" and s.locator.ref == "I1" for s in ged_segments)


@pytest.mark.unit
def test_resolve_returns_none_for_missing() -> None:
    parsed = _parsed("text", "# One\n\ntext", "text")
    missing = StableLocator("s1", "text", "paragraph", "999")
    assert resolve(parsed, missing) is None


@pytest.mark.unit
def test_all_segments_have_hashes() -> None:
    parsed = _parsed("text", "# One\n\nbody", "text")
    assert all(s.content_hash for s in build_segments(parsed, fmt="text"))
