"""G56A/G56B: ParsedDocument model + structural parsing (M53)."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.parsing.model import (
    DocumentMetadata,
    NodeKind,
    ParsedDocument,
    StructuralNode,
)
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.sources.adapter import IngestResult


@pytest.mark.unit
def test_metadata_and_node_validation() -> None:
    with pytest.raises(ContractError):
        DocumentMetadata(
            source_id="",
            kind="text",
            version="1",
            parser_version=1,
            segmenter_version=1,
            content_hash="",
            detected_format="text",
        )
    with pytest.raises(ContractError):
        StructuralNode(
            node_id="n",
            kind=cast(NodeKind, "bogus"),
            text="x",
            ordinal=0,
            parser_version=1,
            segmenter_version=1,
        )  # type: ignore[arg-type]


@pytest.mark.unit
def test_node_hash_is_stable() -> None:
    a = StructuralNode(
        node_id="n1",
        kind="paragraph",
        text="hello",
        ordinal=1,
        parser_version=1,
        segmenter_version=1,
    )
    b = StructuralNode(
        node_id="n1",
        kind="paragraph",
        text="hello",
        ordinal=1,
        parser_version=1,
        segmenter_version=1,
    )
    assert a.compute_hash() == b.compute_hash()
    assert (
        a.compute_hash()
        != StructuralNode(
            node_id="n1",
            kind="paragraph",
            text="hello!",
            ordinal=1,
            parser_version=1,
            segmenter_version=1,
        ).compute_hash()
    )


@pytest.mark.unit
def test_parse_book_chapters_and_paragraphs() -> None:
    result = IngestResult(
        source_id="s",
        kind="text",
        content="# Chapter One\n\nFirst para.\n\n# Chapter Two\n\nSecond para.",
        detected_format="text",
    )
    doc = StructureParser().parse(result, source_id="s", version="1")
    assert doc.ok
    kinds = [n.kind for n in doc.nodes]
    assert kinds[0] == "document"
    assert kinds.count("chapter") == 2
    assert kinds.count("paragraph") == 2
    chapters = [n for n in doc.nodes if n.kind == "chapter"]
    assert chapters[0].text == "Chapter One"
    assert all(n.content_hash for n in doc.nodes)


@pytest.mark.unit
def test_parse_json_records() -> None:
    result = IngestResult(
        source_id="s", kind="json", content='{"a": 1, "b": 2}', detected_format="json"
    )
    doc = StructureParser().parse(result, source_id="s", version="1")
    records = [n for n in doc.nodes if n.kind == "record"]
    assert {n.node_id for n in records} == {"record:a", "record:b"}


@pytest.mark.unit
def test_parse_csv_rows() -> None:
    result = IngestResult(
        source_id="s", kind="csv", content="id\tname\n1\tAlice", detected_format="csv"
    )
    doc = StructureParser().parse(result, source_id="s", version="1")
    records = [n for n in doc.nodes if n.kind == "record"]
    assert len(records) == 2
    assert records[0].node_id == "record:row_1"


@pytest.mark.unit
def test_parse_gedcom_records() -> None:
    gedcom = "0 @I1@ INDI\n1 NAME Alice /Zhang/\n0 @F1@ FAM\n1 HUSB @I1@\n"
    result = IngestResult(source_id="s", kind="gedcom", content=gedcom, detected_format="gedcom")
    doc = StructureParser().parse(result, source_id="s", version="1")
    records = [n for n in doc.nodes if n.kind == "record"]
    assert {n.node_id for n in records} == {"record:I1", "record:F1"}


@pytest.mark.unit
def test_parsed_document_requires_nodes() -> None:
    with pytest.raises(ContractError):
        ParsedDocument(
            document_id="d",
            metadata=DocumentMetadata(
                source_id="s",
                kind="text",
                version="1",
                parser_version=1,
                segmenter_version=1,
                content_hash="h",
                detected_format="text",
            ),
            nodes=(),
        )
