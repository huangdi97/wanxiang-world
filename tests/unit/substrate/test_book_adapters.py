"""G55D: Book adapters — TXT/MD/EPUB/DOCX/text-PDF (M52)."""

from __future__ import annotations

import io
import zipfile

import pytest
from wanxiang_substrate.sources.book import BookAdapter
from wanxiang_substrate.sources.errors import MalformedSourceContent, OcrRequired, UnsupportedSource
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _record(kind: str, payload: str = "", *, content_ref: str = "ref://src") -> SourceRecord:
    return SourceRecord(
        source_id="src_book",
        kind=kind,
        content_hash=payload_hash(payload or "fixture:g55d"),
        content_ref=content_ref,
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload=payload,
        provenance="fixture:g55d",
    )


def make_epub() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("mimetype", "application/epub+zip")
        z.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0"?>'
            '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="OEBPS/content.opf" '
            'media-type="application/oebps-package+xml"/>'
            "</rootfiles></container>",
        )
        z.writestr(
            "OEBPS/content.opf",
            '<?xml version="1.0"?>'
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
            '<manifest><item id="c1" href="chap1.xhtml" media-type="application/xhtml+xml"/>'
            '<item id="c2" href="chap2.xhtml" media-type="application/xhtml+xml"/></manifest>'
            '<spine><itemref idref="c1"/><itemref idref="c2"/></spine></package>',
        )
        z.writestr(
            "OEBPS/chap1.xhtml",
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Chapter One</title></head>'
            "<body><h1>Chapter One</h1><p>It was a dark and stormy night.</p></body></html>",
        )
        z.writestr(
            "OEBPS/chap2.xhtml",
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Chapter Two</title></head>'
            "<body><p>Morning came.</p></body></html>",
        )
    return buf.getvalue()


def make_docx() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(
            "word/document.xml",
            '<?xml version="1.0"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:body>"
            "<w:p><w:r><w:t>First paragraph.</w:t></w:r></w:p>"
            "<w:p><w:r><w:t>Second paragraph.</w:t></w:r></w:p>"
            "</w:body></w:document>",
        )
    return buf.getvalue()


def make_pdf(text: str | None) -> bytes:
    content = f"BT /F1 24 Tf 72 720 Td ({text}) Tj ET" if text else "q Q"
    stream = f"stream\n{content}\nendstream"
    return (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >> endobj\n"
        b"4 0 obj << /Length 100 >>\n"
        + stream.encode("latin-1")
        + b"\nendobj\ntrailer << /Root 1 0 R >>\n%%EOF\n"
    )


@pytest.mark.unit
def test_handles_book_formats() -> None:
    adapter = BookAdapter()
    for kind in ("text", "markdown", "epub", "docx", "pdf"):
        assert adapter.can_handle(kind=kind), kind
    assert adapter.can_handle(kind="text", filename="book.txt")
    assert adapter.can_handle(kind="text", filename="book.epub")
    assert not adapter.can_handle(kind="gedcom")


@pytest.mark.unit
def test_ingest_text_and_markdown() -> None:
    adapter = BookAdapter()
    assert adapter.ingest(_record("text", "hello")).content == "hello"
    assert adapter.ingest(_record("markdown", "# Title\nbody")).content == "# Title\nbody"


@pytest.mark.unit
def test_ingest_epub_in_spine_order() -> None:
    result = BookAdapter().ingest(_record("epub"), make_epub())
    assert "# Chapter One" in result.content
    assert "dark and stormy night" in result.content
    assert "# Chapter Two" in result.content
    assert result.content.index("Chapter One") < result.content.index("Chapter Two")


@pytest.mark.unit
def test_ingest_docx_paragraphs() -> None:
    result = BookAdapter().ingest(_record("docx"), make_docx())
    assert "First paragraph." in result.content
    assert "Second paragraph." in result.content


@pytest.mark.unit
def test_ingest_text_pdf() -> None:
    result = BookAdapter().ingest(_record("pdf"), make_pdf("Hello World"))
    assert "Hello World" in result.content


@pytest.mark.unit
def test_scanned_pdf_requires_ocr() -> None:
    with pytest.raises(OcrRequired):
        BookAdapter().ingest(_record("pdf"), make_pdf(None))


@pytest.mark.unit
def test_malformed_epub_rejected() -> None:
    with pytest.raises(MalformedSourceContent):
        BookAdapter().ingest(_record("epub"), b"not a zip")


@pytest.mark.unit
def test_unsupported_kind_rejected() -> None:
    with pytest.raises(UnsupportedSource):
        BookAdapter().ingest(_record("gedcom"))
