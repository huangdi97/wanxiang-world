"""Safe source readers for TXT/MD/JSON/YAML with size/type validation (G04C)."""

from __future__ import annotations

import json
from typing import cast

from wanxiang_substrate.compiler.errors import MalformedSource, OversizedSource, UnsupportedFormat
from wanxiang_substrate.compiler.model import EXPLICITLY_UNSUPPORTED, SUPPORTED_KINDS
from wanxiang_substrate.sources.model import MAX_PAYLOAD_BYTES, SourceRecord


def read_source(record: SourceRecord) -> dict[str, object]:
    """Read a source into a plain mapping; unsupported formats fail explicitly."""
    if record.kind in EXPLICITLY_UNSUPPORTED:
        raise UnsupportedFormat(
            f"format {record.kind!r} is explicitly unsupported (no fake extraction)"
        )
    if record.kind not in SUPPORTED_KINDS:
        raise UnsupportedFormat(f"unknown source kind {record.kind!r}")
    if len(record.payload.encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise OversizedSource(f"source {record.source_id!r} exceeds size limit")
    if record.kind == "json":
        return _read_json(record)
    if record.kind == "yaml":
        return _read_yaml(record)
    if record.kind == "markdown":
        return _read_markdown(record)
    return {"text": record.payload}


def _read_json(record: SourceRecord) -> dict[str, object]:
    try:
        decoded = json.loads(record.payload)
    except ValueError as exc:
        raise MalformedSource(f"source {record.source_id!r} is not valid JSON") from exc
    if not isinstance(decoded, dict):
        raise MalformedSource(f"source {record.source_id!r} JSON must be an object")
    return cast(dict[str, object], decoded)


def _read_yaml(record: SourceRecord) -> dict[str, object]:
    from wanxiang_substrate.compiler.yaml_mini import parse_yaml_subset

    try:
        return parse_yaml_subset(record.payload)
    except MalformedSource as exc:
        raise MalformedSource(f"source {record.source_id!r}: {exc}") from exc


def _read_markdown(record: SourceRecord) -> dict[str, object]:
    """Limited explicit-markup pathway: '## <id>' sections with 'key: value'."""
    sections: dict[str, dict[str, object]] = {}
    current_id: str | None = None
    for line_number, raw in enumerate(record.payload.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("## "):
            current_id = stripped[3:].strip()
            if not current_id:
                raise MalformedSource(
                    f"source {record.source_id!r} line {line_number}: empty section id"
                )
            sections[current_id] = {}
            continue
        if current_id is None:
            raise MalformedSource(
                f"source {record.source_id!r} line {line_number}: content before first section"
            )
        if ":" not in stripped:
            raise MalformedSource(
                f"source {record.source_id!r} line {line_number}: expected key: value"
            )
        key, value = stripped.split(":", 1)
        sections[current_id][key.strip()] = _parse_scalar(value.strip())
    return {"objects": sections}


def _parse_scalar(text: str) -> object:
    if text in ("true", "True"):
        return True
    if text in ("false", "False"):
        return False
    return text


def is_supported_kind(kind: str) -> bool:
    return kind in SUPPORTED_KINDS
