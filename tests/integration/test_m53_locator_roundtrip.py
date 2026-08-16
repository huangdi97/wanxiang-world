"""G56H: M53 cross-format locator round-trip E2E.

For every foundation format (EPUB, DOCX, text-PDF, JSON, CSV, GEDCOM, TXT):
SourceAdapter -> IngestResult -> StructureParser -> build_segments ->
resolve(locator) must return the exact source text.
"""

from __future__ import annotations

import io
import zipfile
from typing import cast

import pytest
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, build_segments, resolve
from wanxiang_substrate.sources.book import BookAdapter
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.sources.structured import StructuredAdapter


def _record(kind: str, content_ref: str = "ref://src") -> SourceRecord:
    return SourceRecord(
        source_id="src_e2e",
        kind=kind,
        content_hash=payload_hash(f"fixture:{kind}"),
        content_ref=content_ref,
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload="",
        provenance="fixture:m53",
    )


def _epub() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("mimetype", "application/epub+zip")
        z.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0"?><container '
            'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="content.opf" '
            'media-type="application/oebps-package+xml"/>'
            "</rootfiles></container>",
        )
        z.writestr(
            "content.opf",
            '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
            '<manifest><item id="c1" href="c1.xhtml" '
            'media-type="application/xhtml+xml"/></manifest>'
            '<spine><itemref idref="c1"/></spine></package>',
        )
        z.writestr(
            "c1.xhtml",
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>T</title></head>'
            "<body><h1>Opening</h1><p>The round-trip works.</p></body></html>",
        )
    return buf.getvalue()


def _docx() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(
            "word/document.xml",
            '<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:body><w:p><w:r><w:t>Docx paragraph one.</w:t></w:r></w:p></w:body></w:document>",
        )
    return buf.getvalue()


def _pdf() -> bytes:
    stream = b"stream\nBT (PDF text here) Tj ET\nendstream"
    return (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /Contents 4 0 R >> endobj\n"
        b"4 0 obj << /Length 100 >>\n" + stream + b"\nendobj\ntrailer << /Root 1 0 R >>\n%%EOF\n"
    )


def _roundtrip_fixture(kind: str, blob: bytes | None, fmt: LocatorFormat) -> None:
    adapter = (
        BookAdapter()
        if kind in ("epub", "docx", "pdf", "text", "markdown")
        else StructuredAdapter()
    )
    record = _record(kind)
    result = adapter.ingest(record, blob)
    parsed = StructureParser().parse(result, source_id="src_e2e", version="1")
    segments = build_segments(parsed, fmt=fmt)
    assert segments, f"no segments for {kind}"
    for segment in segments:
        if segment.text:
            assert resolve(parsed, segment.locator) == segment.text, (
                f"{kind} locator {segment.locator.to_string()} did not round-trip"
            )


@pytest.mark.integration
def test_epub_locator_roundtrip() -> None:
    _roundtrip_fixture("epub", _epub(), cast(LocatorFormat, "epub"))


@pytest.mark.integration
def test_docx_locator_roundtrip() -> None:
    _roundtrip_fixture("docx", _docx(), cast(LocatorFormat, "docx"))


@pytest.mark.integration
def test_pdf_locator_roundtrip() -> None:
    _roundtrip_fixture("pdf", _pdf(), cast(LocatorFormat, "pdf"))


@pytest.mark.integration
def test_json_locator_roundtrip() -> None:
    _roundtrip_fixture("json", b'{"name": "Alice"}', cast(LocatorFormat, "json"))


@pytest.mark.integration
def test_csv_locator_roundtrip() -> None:
    _roundtrip_fixture("csv", b"id,name\n1,Alice\n", cast(LocatorFormat, "csv"))


@pytest.mark.integration
def test_gedcom_locator_roundtrip() -> None:
    ged = b"0 @I1@ INDI\n1 NAME Alice /Zhang/\n"
    _roundtrip_fixture("gedcom", ged, cast(LocatorFormat, "gedcom"))


@pytest.mark.integration
def test_text_locator_roundtrip() -> None:
    _roundtrip_fixture("text", b"# Chapter\n\nHello world.\n", cast(LocatorFormat, "text"))
