"""SourceAdapter ABI (G55C).

Unified can_handle / inspect / ingest / resume contract with typed failures so
the SourceRegistry pipeline never silently falls back to "success". Adapters
produce ParsedContent / inspection only; they never mutate sources or canon.
The reference text adapter provides the deterministic no-API path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_substrate.sources.blob import BlobRef
from wanxiang_substrate.sources.errors import MalformedSourceContent, OcrRequired, UnsupportedSource
from wanxiang_substrate.sources.model import SourceRecord


@dataclass(frozen=True, slots=True)
class SourceInspection:
    """What an adapter knows about a source BEFORE ingesting it."""

    source_id: str
    detected_format: str
    text_available: bool
    ocr_required: bool
    size_bytes: int
    diagnostics: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return self.text_available and not self.ocr_required


@dataclass(frozen=True, slots=True)
class IngestResult:
    """Parsed content from an adapter; references, never raw business bytes."""

    source_id: str
    kind: str
    content: str
    detected_format: str
    blob_ref: BlobRef | None = None
    diagnostics: tuple[str, ...] = ()


class SourceAdapter(Protocol):
    """Adapter contract: detect, inspect, ingest, resume (typed failures)."""

    name: str

    def can_handle(
        self,
        *,
        kind: str,
        filename: str = "",
        content_type: str = "",
    ) -> bool: ...

    def inspect(self, record: SourceRecord) -> SourceInspection: ...

    def ingest(
        self,
        record: SourceRecord,
        blob: bytes | None = None,
    ) -> IngestResult: ...

    def resume(self, source_id: str) -> IngestResult | None: ...


class ReferenceTextAdapter:
    """Deterministic TXT/Markdown adapter (no API, no OCR)."""

    name = "reference_text"

    def can_handle(
        self,
        *,
        kind: str,
        filename: str = "",
        content_type: str = "",
    ) -> bool:
        lowered = filename.lower() if filename else ""
        return kind in ("text", "markdown") or lowered.endswith((".txt", ".md"))

    def inspect(self, record: SourceRecord) -> SourceInspection:
        payload = record.payload.encode("utf-8")
        return SourceInspection(
            source_id=record.source_id,
            detected_format=record.kind,
            text_available=True,
            ocr_required=False,
            size_bytes=len(payload),
        )

    def ingest(self, record: SourceRecord, blob: bytes | None = None) -> IngestResult:
        if record.kind not in ("text", "markdown"):
            raise UnsupportedSource(f"reference text adapter cannot ingest {record.kind!r}")
        content = record.payload if blob is None else blob.decode("utf-8", errors="strict")
        return IngestResult(
            source_id=record.source_id,
            kind=record.kind,
            content=content,
            detected_format=record.kind,
        )

    def resume(self, source_id: str) -> IngestResult | None:
        # Reference adapter is stateless; resume is a no-op (idempotent).
        return None


class AdapterRegistry:
    """Selects the first adapter that can handle a source; runs the pipeline."""

    def __init__(self, adapters: tuple[SourceAdapter, ...] = ()) -> None:
        self._adapters = tuple(adapters)

    def add(self, adapter: SourceAdapter) -> None:
        self._adapters = self._adapters + (adapter,)

    def select(
        self,
        *,
        kind: str,
        filename: str = "",
        content_type: str = "",
    ) -> SourceAdapter | None:
        for adapter in self._adapters:
            if adapter.can_handle(kind=kind, filename=filename, content_type=content_type):
                return adapter
        return None

    def inspect(self, record: SourceRecord, *, filename: str = "") -> SourceInspection:
        adapter = self.select(kind=record.kind, filename=filename)
        if adapter is None:
            raise UnsupportedSource(
                f"no adapter for source {record.source_id!r} kind {record.kind!r}"
            )
        return adapter.inspect(record)

    def ingest(
        self,
        record: SourceRecord,
        blob: bytes | None = None,
        *,
        filename: str = "",
    ) -> IngestResult:
        adapter = self.select(kind=record.kind, filename=filename)
        if adapter is None:
            raise UnsupportedSource(
                f"no adapter for source {record.source_id!r} kind {record.kind!r}"
            )
        return adapter.ingest(record, blob)


def require_text(inspection: SourceInspection) -> None:
    """Pipeline guard: refuse to proceed when OCR is required but unavailable."""
    if inspection.ocr_required:
        raise OcrRequired(
            f"source {inspection.source_id!r} requires OCR; no OCR provider available"
        )
    if not inspection.text_available:
        raise MalformedSourceContent(f"source {inspection.source_id!r} has no extractable text")
