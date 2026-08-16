"""Structured source adapters: JSON/YAML/CSV/GEDCOM (G55E).

Deterministic, stdlib-only adapters that normalize structured sources into a
canonical text representation (JSON round-trip, CSV row lines, GEDCOM
re-serialization). Reuses the compiler yaml_mini subset parser and the G09A
GEDCOM parser; introduces no second parser/registry.
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any

from wanxiang_substrate.compiler.yaml_mini import parse_yaml_subset
from wanxiang_substrate.genealogy.gedcom import parse_gedcom, serialize_gedcom
from wanxiang_substrate.sources.adapter import IngestResult, SourceAdapter, SourceInspection
from wanxiang_substrate.sources.errors import MalformedSourceContent, UnsupportedSource
from wanxiang_substrate.sources.model import SourceRecord

_SUPPORTED = ("json", "yaml", "csv", "gedcom")
_EXTENSIONS = (".json", ".yaml", ".yml", ".csv", ".ged")


class StructuredAdapter(SourceAdapter):
    """JSON/YAML/CSV/GEDCOM adapter (deterministic, no external deps)."""

    name = "structured"

    def can_handle(
        self,
        *,
        kind: str,
        filename: str = "",
        content_type: str = "",
    ) -> bool:
        lowered = filename.lower() if filename else ""
        return kind in _SUPPORTED or lowered.endswith(_EXTENSIONS)

    def inspect(self, record: SourceRecord) -> SourceInspection:
        return SourceInspection(
            source_id=record.source_id,
            detected_format=record.kind,
            text_available=True,
            ocr_required=False,
            size_bytes=len(record.payload.encode("utf-8")),
        )

    def ingest(self, record: SourceRecord, blob: bytes | None = None) -> IngestResult:
        raw = record.payload if blob is None else blob.decode("utf-8", errors="strict")
        kind = record.kind
        if kind == "json":
            content = _normalize_json(raw)
        elif kind == "yaml":
            content = _normalize_yaml(raw)
        elif kind == "csv":
            content = _normalize_csv(raw)
        elif kind == "gedcom":
            content = _normalize_gedcom(raw)
        else:
            raise UnsupportedSource(f"structured adapter cannot ingest {kind!r}")
        return IngestResult(
            source_id=record.source_id,
            kind=record.kind,
            content=content,
            detected_format=kind,
        )

    def resume(self, source_id: str) -> IngestResult | None:
        return None


def _normalize_json(raw: str) -> str:
    try:
        decoded = json.loads(raw)
    except ValueError as exc:
        raise MalformedSourceContent(f"invalid JSON: {exc}") from exc
    return _canonical(decoded)


def _normalize_yaml(raw: str) -> str:
    try:
        decoded: Any = parse_yaml_subset(raw)
    except Exception as exc:  # noqa: BLE001 - yaml_mini raises its own taxonomy
        raise MalformedSourceContent(f"invalid YAML subset: {exc}") from exc
    return _canonical(decoded)


def _normalize_csv(raw: str) -> str:
    try:
        rows = list(csv.reader(io.StringIO(raw)))
    except csv.Error as exc:
        raise MalformedSourceContent(f"invalid CSV: {exc}") from exc
    if not rows:
        raise MalformedSourceContent("CSV has no rows")
    lines = ["\t".join(cell for cell in row) for row in rows]
    return "\n".join(lines)


def _normalize_gedcom(raw: str) -> str:
    document = parse_gedcom(raw)
    if not document.individuals and not document.families:
        raise MalformedSourceContent("GEDCOM has no individuals or families")
    return serialize_gedcom(document)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
