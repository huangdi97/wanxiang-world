"""Book source adapters: TXT/MD/EPUB/DOCX/text-PDF (G55D).

Stdlib-only (zipfile + xml.etree + zlib) deterministic extraction:
- EPUB: container -> OPF manifest/spine -> XHTML chapters in spine order.
- DOCX: word/document.xml -> paragraphs + table text.
- text-PDF: best-effort content-stream text extraction; scanned PDFs with no
  extractable text honestly report OCR_REQUIRED (never fake extraction).
Adapters produce IngestResult only; they never mutate sources or canon.
"""

from __future__ import annotations

import posixpath
import re
import zipfile
import zlib
from dataclasses import dataclass
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from wanxiang_substrate.sources.adapter import IngestResult, SourceAdapter, SourceInspection
from wanxiang_substrate.sources.errors import MalformedSourceContent, OcrRequired, UnsupportedSource
from wanxiang_substrate.sources.model import SourceRecord

_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_EPUB_NS = "{urn:oasis:names:tc:opendocument:xmlns:container}"
_OPF_NS = "{http://www.idpf.org/2007/opf}"
_XHTML_NS = "{http://www.w3.org/1999/xhtml}"


def _local_name(tag: str) -> str:
    """Return an XML local name for EPUB 2 (no namespace) and EPUB 3."""
    return tag.rsplit("}", 1)[-1].lower()


@dataclass(frozen=True, slots=True)
class Chapter:
    """One extracted book chapter with a stable ordinal."""

    chapter_id: str
    title: str
    text: str
    href: str = ""

    @property
    def heading(self) -> str:
        return self.title or self.chapter_id

    @property
    def locator_ref(self) -> str:
        spine = self.chapter_id.removeprefix("chapter_")
        return f"spine={spine};href={self.href}"


def _decode(blob: bytes, *, kind: str) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return blob.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise MalformedSourceContent(f"cannot decode {kind} source bytes")


def _extract_epub(blob: bytes) -> tuple[Chapter, ...]:
    try:
        archive = zipfile.ZipFile(__import__("io").BytesIO(blob))
    except (zipfile.BadZipFile, OSError) as exc:
        raise MalformedSourceContent(f"invalid EPUB zip: {exc}") from exc
    try:
        container = archive.read("META-INF/container.xml")
    except KeyError as exc:
        raise MalformedSourceContent("EPUB missing META-INF/container.xml") from exc
    root = ElementTree.fromstring(container)
    rootfile = next((item for item in root.iter() if _local_name(item.tag) == "rootfile"), None)
    if rootfile is None:
        raise MalformedSourceContent("EPUB container has no rootfile")
    opf_path = rootfile.attrib.get("full-path", "")
    if not opf_path:
        raise MalformedSourceContent("EPUB rootfile has no full-path")
    opf = ElementTree.fromstring(archive.read(opf_path))
    base = opf_path.rsplit("/", 1)[0] if "/" in opf_path else ""
    manifest: dict[str, tuple[str, str]] = {}
    for item in opf.iter():
        if _local_name(item.tag) != "item":
            continue
        item_id = item.attrib.get("id", "")
        href = item.attrib.get("href", "")
        media = item.attrib.get("media-type", "")
        if item_id and href:
            manifest[item_id] = (href, media)
    spine = [ref.attrib.get("idref", "") for ref in opf.iter() if _local_name(ref.tag) == "itemref"]
    chapters: list[Chapter] = []
    for index, idref in enumerate(spine):
        entry = manifest.get(idref)
        if entry is None:
            continue
        href, media = entry
        if media not in ("application/xhtml+xml", "application/xml", "text/html"):
            continue
        href_path = unquote(urlsplit(href).path)
        path = posixpath.normpath(posixpath.join(base, href_path)) if base else href_path
        if path in ("", ".", "..") or path.startswith("../"):
            raise MalformedSourceContent(f"EPUB manifest path escapes package: {href!r}")
        try:
            content = archive.read(path)
        except KeyError:
            continue
        text, title = _xhtml_text(content)
        chapters.append(
            Chapter(
                chapter_id=f"chapter_{index + 1}",
                title=title,
                text=text,
                href=path,
            )
        )
    if not chapters:
        raise MalformedSourceContent("EPUB spine produced no chapters")
    return tuple(chapters)


def _xhtml_text(content: bytes) -> tuple[str, str]:
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as exc:
        raise MalformedSourceContent(f"invalid XHTML: {exc}") from exc
    title_el = next(
        (element for element in root.iter() if _local_name(element.tag) == "title"), None
    )
    title = "".join(title_el.itertext()).strip() if title_el is not None else ""
    parts: list[str] = []
    for element in root.iter():
        if _local_name(element.tag) in ("p", "h1", "h2", "h3"):
            text = "".join(element.itertext()).strip()
            if text:
                parts.append(text)
    return "\n".join(parts), title


def _extract_docx(blob: bytes) -> str:
    try:
        archive = zipfile.ZipFile(__import__("io").BytesIO(blob))
    except (zipfile.BadZipFile, OSError) as exc:
        raise MalformedSourceContent(f"invalid DOCX zip: {exc}") from exc
    try:
        document = archive.read("word/document.xml")
    except KeyError as exc:
        raise MalformedSourceContent("DOCX missing word/document.xml") from exc
    root = ElementTree.fromstring(document)
    lines: list[str] = []
    for paragraph in root.iter(f"{_W_NS}p"):
        text = "".join(run.text or "" for run in paragraph.iter(f"{_W_NS}t")).strip()
        if text:
            lines.append(text)
    for row in root.iter(f"{_W_NS}tr"):
        cells = [
            "".join(run.text or "" for run in cell.iter(f"{_W_NS}t")).strip()
            for cell in row.iter(f"{_W_NS}tc")
        ]
        if cells:
            lines.append(" | ".join(cells))
    if not lines:
        raise MalformedSourceContent("DOCX contains no extractable text")
    return "\n".join(lines)


def _extract_pdf_text(blob: bytes) -> tuple[str, bool]:
    """Best-effort text extraction; returns (text, ocr_required).

    Scanned/image-only PDFs have no text-showing operators -> ocr_required True
    (honest, never fabricated).
    """
    streams = re.findall(rb"stream\r?\n(.*?)\r?\nendstream", blob, re.DOTALL)
    text_ops = re.compile(rb"\((?:[^()\\]|\\.)*\)\s*Tj|\[(?:[^\]])*\]\s*TJ")
    pages: list[str] = []
    for stream in streams:
        raw = stream
        with __import__("contextlib").suppress(zlib.error):
            raw = zlib.decompress(raw)
        found = text_ops.findall(raw)
        if not found:
            continue
        parts: list[str] = []
        for token in found:
            inner = token[: token.rfind(b")") + 1] if token.endswith(b"Tj") else token
            inner = inner.replace(b"\\(", b"(").replace(b"\\)", b")").replace(b"\\\\", b"\\")
            if inner.startswith(b"(") and inner.endswith(b")"):
                parts.append(inner[1:-1].decode("latin-1", errors="replace"))
        if parts:
            pages.append(" ".join(parts))
    text = "\n".join(pages)
    return text, not text.strip()


class BookAdapter(SourceAdapter):
    """TXT/MD/EPUB/DOCX/text-PDF adapter (deterministic, no external deps)."""

    name = "book"

    def can_handle(
        self,
        *,
        kind: str,
        filename: str = "",
        content_type: str = "",
    ) -> bool:
        lowered = filename.lower() if filename else ""
        return (
            kind in ("text", "markdown", "epub", "docx", "pdf")
            or lowered.endswith((".txt", ".md", ".epub", ".docx", ".pdf"))
            or content_type in ("application/epub+zip", "application/pdf")
        )

    def inspect(self, record: SourceRecord) -> SourceInspection:
        size = len(record.payload.encode("utf-8"))
        if record.kind == "pdf":
            # Without OCR provider, scanned PDFs are detected at ingest; the
            # size-only inspection cannot assert text yet.
            return SourceInspection(
                source_id=record.source_id,
                detected_format="pdf",
                text_available=True,
                ocr_required=False,
                size_bytes=size,
            )
        return SourceInspection(
            source_id=record.source_id,
            detected_format=record.kind,
            text_available=True,
            ocr_required=False,
            size_bytes=size,
        )

    def ingest(self, record: SourceRecord, blob: bytes | None = None) -> IngestResult:
        data = blob if blob is not None else record.payload.encode("utf-8")
        kind = record.kind
        node_refs: list[str] = []
        if kind in ("text", "markdown"):
            content = _decode(data, kind=kind)
            detected = kind
        elif kind == "epub":
            chapters = _extract_epub(data)
            lines: list[str] = []
            node_refs: list[str] = []
            for chapter in chapters:
                lines.append(f"# {chapter.heading}")
                node_refs.append(chapter.locator_ref)
                for line_index, line in enumerate(chapter.text.splitlines(), start=1):
                    lines.append(line)
                    node_refs.append(f"{chapter.locator_ref};line={line_index}")
                lines.append("")
                node_refs.append("")
            content = "\n".join(lines)
            detected = "epub"
        elif kind == "docx":
            content = _extract_docx(data)
            detected = "docx"
        elif kind == "pdf":
            content, ocr_required = _extract_pdf_text(data)
            if ocr_required:
                raise OcrRequired(
                    f"source {record.source_id!r} is a scanned/image PDF; OCR provider required"
                )
            detected = "pdf"
        else:
            raise UnsupportedSource(f"book adapter cannot ingest {kind!r}")
        return IngestResult(
            source_id=record.source_id,
            kind=record.kind,
            content=content,
            detected_format=detected,
            node_refs=tuple(node_refs) if kind == "epub" else (),
        )

    def resume(self, source_id: str) -> IngestResult | None:
        return None
