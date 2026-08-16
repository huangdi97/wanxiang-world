"""G56G: Diagnostics API — structure preview / warnings / errors / locator preview."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_substrate.parsing.diagnostics import (
    DiagnosticsReport,
    build_preview_report,
    collect,
    locator_preview,
    structure_preview,
)
from wanxiang_substrate.parsing.model import ParsedDocument, ParseDiagnostic
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, build_segments
from wanxiang_substrate.sources.adapter import IngestResult


def _parsed() -> ParsedDocument:
    result = IngestResult(
        source_id="s1",
        kind="text",
        content="# One\n\nfirst\n\n# Two\n\nsecond",
        detected_format="text",
    )
    return StructureParser().parse(result, source_id="s1", version="1")


@pytest.mark.unit
def test_collect_counts_and_preview() -> None:
    parsed = _parsed()
    report = collect(parsed)
    assert report.ok is True
    assert report.node_counts["chapter"] == 2
    assert report.node_counts["paragraph"] == 2
    assert "document doc:s1:1" in report.summary()
    assert report.locator_preview


@pytest.mark.unit
def test_warnings_and_errors_grouped() -> None:

    parsed = _parsed()
    doc_with_diag = ParsedDocument(
        document_id=parsed.document_id,
        metadata=parsed.metadata,
        nodes=parsed.nodes,
        diagnostics=(
            ParseDiagnostic("warning", "w1", "possible missing chapter"),
            ParseDiagnostic("error", "e1", "unparseable section"),
        ),
    )
    report = collect(doc_with_diag)
    assert report.warnings == ("possible missing chapter",)
    assert report.errors == ("unparseable section",)
    assert report.ok is False


@pytest.mark.unit
def test_structure_preview_text() -> None:
    preview = structure_preview(_parsed(), limit=3)
    assert preview.startswith("document:")
    assert "[chapter]" in preview


@pytest.mark.unit
def test_locator_preview_roundtrip() -> None:
    parsed = _parsed()
    segments = build_segments(parsed, fmt=cast(LocatorFormat, "text"))
    locators = locator_preview(segments, limit=2)
    assert len(locators) == 2
    assert all(locator.startswith("text://s1#") for locator in locators)


@pytest.mark.unit
def test_build_preview_report_with_segments() -> None:
    parsed = _parsed()
    report = build_preview_report(parsed, fmt="text", limit=3)
    assert isinstance(report, DiagnosticsReport)
    assert report.locator_preview
