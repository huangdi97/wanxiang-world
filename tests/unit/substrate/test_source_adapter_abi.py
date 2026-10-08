"""G55C: SourceAdapter ABI — can_handle/inspect/ingest/resume + typed failures."""

from __future__ import annotations

import pytest
from wanxiang_substrate.sources.adapter import (
    AdapterRegistry,
    ReferenceTextAdapter,
    require_text,
)
from wanxiang_substrate.sources.errors import (
    MalformedSourceContent,
    OcrRequired,
    UnsupportedSource,
)
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _record(kind: str = "text", payload: str = "hello world") -> SourceRecord:
    return SourceRecord(
        source_id="src_txt",
        kind=kind,
        content_hash=payload_hash(payload),
        content_ref="ref://src_txt",
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload=payload,
        provenance="fixture:g55c",
    )


@pytest.mark.unit
def test_text_adapter_handles_txt_and_markdown() -> None:
    adapter = ReferenceTextAdapter()
    assert adapter.can_handle(kind="text")
    assert adapter.can_handle(kind="markdown")
    assert adapter.can_handle(kind="text", filename="chapter.txt")
    assert adapter.can_handle(kind="text", filename="notes.md")
    assert not adapter.can_handle(kind="pdf")
    assert not adapter.can_handle(kind="gedcom")


@pytest.mark.unit
def test_inspect_reports_text_available_and_no_ocr() -> None:
    inspection = ReferenceTextAdapter().inspect(_record())
    assert inspection.text_available is True
    assert inspection.ocr_required is False
    assert inspection.ok is True
    assert inspection.size_bytes == len(b"hello world")


@pytest.mark.unit
def test_ingest_roundtrip() -> None:
    result = ReferenceTextAdapter().ingest(_record())
    assert result.content == "hello world"
    assert result.detected_format == "text"


@pytest.mark.unit
def test_ingest_rejects_unsupported_kind() -> None:
    with pytest.raises(UnsupportedSource):
        ReferenceTextAdapter().ingest(_record(kind="pdf"))


@pytest.mark.unit
def test_registry_selects_and_runs() -> None:
    registry = AdapterRegistry((ReferenceTextAdapter(),))
    assert registry.select(kind="text") is not None
    assert registry.select(kind="pdf") is None
    result = registry.ingest(_record())
    assert result.content == "hello world"
    with pytest.raises(UnsupportedSource):
        registry.inspect(_record(kind="gedcom"))


@pytest.mark.unit
def test_require_text_rejects_ocr_required() -> None:
    from wanxiang_substrate.sources.adapter import SourceInspection

    inspection = SourceInspection(
        source_id="s", detected_format="pdf", text_available=False, ocr_required=True, size_bytes=10
    )
    with pytest.raises(OcrRequired):
        require_text(inspection)


@pytest.mark.unit
def test_require_text_rejects_no_text() -> None:
    from wanxiang_substrate.sources.adapter import SourceInspection

    inspection = SourceInspection(
        source_id="s",
        detected_format="pdf",
        text_available=False,
        ocr_required=False,
        size_bytes=10,
    )
    with pytest.raises(MalformedSourceContent):
        require_text(inspection)


@pytest.mark.unit
def test_resume_is_idempotent_noop_for_reference() -> None:
    assert ReferenceTextAdapter().resume("src_txt") is None
