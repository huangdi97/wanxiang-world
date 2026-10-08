"""M59 book/blob, large-source, integrity, and package hardening contracts."""

from __future__ import annotations

import hashlib
import io
import zipfile

import pytest
from wanxiang_substrate.authoring.pipeline import SourceToDraftPipeline
from wanxiang_substrate.authoring.scaling import ContentHashCache, SourceChunker
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.sources.errors import ContentHashMismatch
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord


def _epub() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0"?><container '
            'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="content.opf" '
            'media-type="application/oebps-package+xml"/></rootfiles></container>',
        )
        archive.writestr(
            "content.opf",
            '<?xml version="1.0"?><package '
            'xmlns="http://www.idpf.org/2007/opf" version="3.0">'
            '<manifest><item id="c1" href="c1.xhtml" '
            'media-type="application/xhtml+xml"/></manifest>'
            '<spine><itemref idref="c1"/></spine></package>',
        )
        archive.writestr(
            "c1.xhtml",
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Opening</title>'
            "</head><body><h1>Chapter One</h1><p>In Beijing in 1985.</p>"
            "<p>object: garden key</p><p>rule: keep promises</p>"
            "</body></html>",
        )
    return buffer.getvalue()


def _binary_record(source_id: str, kind: str, blob: bytes) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind=kind,
        content_hash=hashlib.sha256(blob).hexdigest(),
        content_ref=f"blob://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="fixture", usage="test", approved=True),
        payload="",
        provenance="synthetic:m59",
        access="public",
    )


@pytest.mark.integration
def test_epub_blob_reaches_draft_package_and_preview_without_api() -> None:
    blob = _epub()
    record = _binary_record("epub_m59", "epub", blob)
    pipeline = SourceToDraftPipeline(
        blob_loader=lambda source: blob if source.source_id == record.source_id else None
    )
    service = AuthoringService(pipeline=pipeline)
    service.create_job("job_epub", sources=(record,))
    assert service.start("job_epub").draft_id == "wd_job_epub"
    package = service.build_package("job_epub")
    assert package.source_versions == (("epub_m59", "1"),)
    assert service.preview("job_epub").scoped_ref.startswith("preview://")


@pytest.mark.unit
def test_large_source_chunking_is_bounded_and_restartable() -> None:
    content = "0123456789" * 1000
    chunker = SourceChunker(chunk_chars=37)
    chunks = tuple(chunker.iter_chunks("large", content))
    assert chunks
    assert all(0 < len(chunk.text) <= 37 for chunk in chunks)
    assert "".join(chunk.text for chunk in chunks) == content
    assert chunker.recovery("large", content, 0).completed is False
    assert chunker.recovery("large", content, len(chunks)).completed is True
    with pytest.raises(ValueError, match="non-negative"):
        chunker.recovery("large", content, -1)


@pytest.mark.unit
def test_source_chunk_cache_is_content_and_version_addressed() -> None:
    chunker = SourceChunker(chunk_chars=8)
    content = "Alice in Beijing"
    chunks = chunker.chunks("source", content)
    cache = ContentHashCache()
    cache.put("source", "1", content, chunks)
    assert cache.get("source", "1", content) == chunks
    assert cache.get("source", "2", content) is None
    assert cache.get("source", "1", content + " changed") is None


@pytest.mark.unit
def test_resolved_blob_must_match_immutable_source_hash() -> None:
    record = _binary_record("epub_tampered", "epub", _epub())
    pipeline = SourceToDraftPipeline(blob_loader=lambda _source: b"tampered")
    with pytest.raises(ContentHashMismatch):
        pipeline.run((record,), draft_id="wd_tampered")
