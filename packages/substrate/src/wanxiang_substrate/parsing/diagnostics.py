"""Parse diagnostics API (G56G).

Structure preview, warnings/errors, and locator preview for a ParsedDocument.
Read-only; never mutates sources, parses, or canon.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.parsing.model import ParsedDocument
from wanxiang_substrate.parsing.segment import Segment, StableLocator, build_segments


@dataclass(frozen=True, slots=True)
class DiagnosticsReport:
    """Aggregated parse diagnostics + structure/locator preview."""

    document_id: str
    node_counts: dict[str, int]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
    locator_preview: tuple[str, ...]
    ok: bool

    def summary(self) -> str:
        parts = [
            f"document {self.document_id}",
            f"nodes={sum(self.node_counts.values())}",
            f"warnings={len(self.warnings)}",
            f"errors={len(self.errors)}",
            f"ok={self.ok}",
        ]
        return "; ".join(parts)


def collect(parsed: ParsedDocument) -> DiagnosticsReport:
    counts: dict[str, int] = {}
    for node in parsed.nodes:
        counts[node.kind] = counts.get(node.kind, 0) + 1
    warnings = tuple(d.message for d in parsed.diagnostics if d.level == "warning")
    errors = tuple(d.message for d in parsed.diagnostics if d.level == "error")
    locators = tuple(
        StableLocator(
            source_id=parsed.metadata.source_id,
            fmt=parsed.metadata.detected_format,  # type: ignore[arg-type]
            kind=node.kind,
            ref=str(node.ordinal),
        ).to_string()
        for node in parsed.nodes[:5]
    )
    return DiagnosticsReport(
        document_id=parsed.document_id,
        node_counts=counts,
        warnings=warnings,
        errors=errors,
        locator_preview=locators,
        ok=parsed.ok,
    )


def structure_preview(parsed: ParsedDocument, *, limit: int = 10) -> str:
    """Human-readable structural preview (first N nodes)."""
    lines = [f"document: {parsed.document_id}"]
    for node in parsed.nodes[:limit]:
        text = node.text[:40].replace("\n", " ")
        lines.append(f"  [{node.kind}] {node.node_id}: {text}")
    if len(parsed.nodes) > limit:
        lines.append(f"  ... {len(parsed.nodes) - limit} more nodes")
    return "\n".join(lines)


def locator_preview(segments: tuple[Segment, ...], *, limit: int = 10) -> tuple[str, ...]:
    """Preview locator strings for the first N segments."""
    return tuple(segment.locator.to_string() for segment in segments[:limit])


def build_preview_report(parsed: ParsedDocument, *, fmt: str, limit: int = 10) -> DiagnosticsReport:
    """Build a report with segments + locator preview for a given format."""
    segments = build_segments(parsed, fmt=fmt)  # type: ignore[arg-type]
    report = collect(parsed)
    return DiagnosticsReport(
        document_id=report.document_id,
        node_counts=report.node_counts,
        warnings=report.warnings,
        errors=report.errors,
        locator_preview=locator_preview(segments, limit=limit),
        ok=report.ok,
    )
