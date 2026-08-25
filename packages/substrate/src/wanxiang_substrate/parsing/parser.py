"""Structural parsing into unified nodes (G56B).

Turns canonical adapter content (G55D/G55E IngestResult) into a
ParsedDocument node tree: chapters/sections/paragraphs for books,
records for JSON/YAML/CSV/GEDCOM, tables for CSV. Deterministic and
versioned; never mutates sources or canon.
"""

from __future__ import annotations

import re
from typing import Any, cast

from wanxiang_substrate.parsing.model import (
    DocumentMetadata,
    ParsedDocument,
    ParseDiagnostic,
    StructuralNode,
)
from wanxiang_substrate.sources.adapter import IngestResult

_CHAPTER_HEADING = re.compile(
    r"^(?:#\s*)?(?:(?:第\s*[零〇一二三四五六七八九十百千万0-9]+\s*[章节回部卷])|"
    r"(?:卷\s*[零〇一二三四五六七八九十百千万0-9]+))"
    r"(?:\s*[:：.．、-]?\s*(.*))?$"
)
_MARKDOWN_CHAPTER = re.compile(r"^#\s+(.+)$")
_HEADING = re.compile(r"^(#{2,6})\s+(.+)$")
_NUMBERED_SECTION = re.compile(r"^[一二三四五六七八九十百千万0-9]+[、.．]\s*(.+)$")


class StructureParser:
    """Builds a versioned ParsedDocument from canonical adapter content."""

    def __init__(self, *, parser_version: int = 1, segmenter_version: int = 1) -> None:
        self._parser_version = parser_version
        self._segmenter_version = segmenter_version

    @property
    def parser_version(self) -> int:
        return self._parser_version

    @property
    def segmenter_version(self) -> int:
        return self._segmenter_version

    def parse(
        self,
        result: IngestResult,
        *,
        source_id: str,
        version: str,
        content_hash: str = "",
        title: str = "",
    ) -> ParsedDocument:
        fmt = result.detected_format
        if fmt in ("text", "markdown"):
            nodes, diagnostics = self._parse_book(result.content)
        elif fmt in ("json", "yaml"):
            nodes, diagnostics = self._parse_records(result.content, record_delimiter=None)
        elif fmt == "csv":
            nodes, diagnostics = self._parse_csv(result.content)
        elif fmt == "gedcom":
            nodes, diagnostics = self._parse_records(result.content, record_delimiter="@")
        else:
            nodes, diagnostics = self._parse_book(result.content)
        document = StructuralNode(
            node_id="document",
            kind="document",
            text="",
            ordinal=0,
            parser_version=self._parser_version,
            segmenter_version=self._segmenter_version,
        ).with_hash()
        metadata = DocumentMetadata(
            source_id=source_id,
            kind=result.kind,
            version=version,
            parser_version=self._parser_version,
            segmenter_version=self._segmenter_version,
            content_hash=content_hash,
            detected_format=fmt,
            title=title,
        )
        return ParsedDocument(
            document_id=f"doc:{source_id}:{version}",
            metadata=metadata,
            nodes=(document, *nodes),
            asset_refs=result.blob_ref and (result.blob_ref,) or (),
            diagnostics=tuple(diagnostics),
        )

    def _node(
        self,
        node_id: str,
        kind: str,
        text: str,
        ordinal: int,
        parent_id: str = "",
    ) -> StructuralNode:
        return StructuralNode(
            node_id=node_id,
            kind=kind,  # type: ignore[arg-type]
            text=text,
            ordinal=ordinal,
            parser_version=self._parser_version,
            segmenter_version=self._segmenter_version,
            parent_id=parent_id,
        ).with_hash()

    def _parse_book(self, content: str) -> tuple[tuple[StructuralNode, ...], list[ParseDiagnostic]]:
        nodes: list[StructuralNode] = []
        diagnostics: list[ParseDiagnostic] = []
        chapter_id = ""
        chapter_ordinal = 0
        paragraph_ordinal = 0
        for index, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            chapter_match = _CHAPTER_HEADING.match(stripped)
            markdown_chapter = _MARKDOWN_CHAPTER.match(stripped)
            if chapter_match or markdown_chapter:
                chapter_ordinal += 1
                paragraph_ordinal = 0
                chapter_id = f"chapter_{chapter_ordinal}"
                title = (
                    chapter_match.group(1) if chapter_match else markdown_chapter.group(1)  # type: ignore[union-attr]
                ).strip()
                nodes.append(
                    self._node(
                        chapter_id,
                        "chapter",
                        title,
                        chapter_ordinal,
                        parent_id="document",
                    )
                )
                continue
            heading_match = _HEADING.match(stripped)
            numbered_match = _NUMBERED_SECTION.match(stripped)
            if (heading_match or numbered_match) and chapter_id:
                paragraph_ordinal += 1
                title = (
                    heading_match.group(2).strip()
                    if heading_match
                    else numbered_match.group(1).strip()  # type: ignore[union-attr]
                )
                nodes.append(
                    self._node(
                        f"{chapter_id}:section_{paragraph_ordinal}",
                        "section",
                        title,
                        paragraph_ordinal,
                        parent_id=chapter_id,
                    )
                )
                continue
            paragraph_ordinal += 1
            parent = chapter_id or "document"
            nodes.append(
                self._node(
                    f"{parent}:p_{paragraph_ordinal}:{index}",
                    "paragraph",
                    stripped,
                    paragraph_ordinal,
                    parent_id=parent,
                )
            )
        if not nodes:
            diagnostics.append(
                ParseDiagnostic("error", "empty_document", "no structural nodes extracted")
            )
        return tuple(nodes), diagnostics

    def _parse_records(
        self,
        content: str,
        *,
        record_delimiter: str | None,
    ) -> tuple[tuple[StructuralNode, ...], list[ParseDiagnostic]]:
        nodes: list[StructuralNode] = []
        if record_delimiter is None:
            # JSON/YAML canonical text: treat top-level keys as records.
            import json

            try:
                decoded: Any = json.loads(content)
            except ValueError:
                decoded = {}
            if isinstance(decoded, dict):
                mapping = cast(dict[str, Any], decoded)
                for ordinal, key in enumerate(sorted(mapping), start=1):
                    nodes.append(
                        self._node(
                            f"record:{key}",
                            "record",
                            json.dumps(mapping[key], sort_keys=True),
                            ordinal,
                            parent_id="document",
                        )
                    )
            elif isinstance(decoded, list):
                items = cast(list[Any], decoded)
                for ordinal, item in enumerate(items, start=1):
                    nodes.append(
                        self._node(
                            f"record:{ordinal}",
                            "record",
                            json.dumps(item, sort_keys=True),
                            ordinal,
                            parent_id="document",
                        )
                    )
        else:
            # GEDCOM: split by xref lines starting with '@'.
            current: list[str] = []
            current_xref = ""
            ordinal = 0
            for line in content.splitlines():
                stripped_line = line.strip()
                if stripped_line.startswith("0 @") and "@" in stripped_line:
                    if current_xref and current:
                        ordinal += 1
                        nodes.append(
                            self._node(
                                f"record:{current_xref}",
                                "record",
                                "\n".join(current),
                                ordinal,
                                parent_id="document",
                            )
                        )
                    tokens = stripped_line.split()
                    current_xref = tokens[1].strip("@") if len(tokens) > 1 else "unknown"
                    current = [line]
                elif current_xref:
                    current.append(line)
            if current_xref and current:
                ordinal += 1
                nodes.append(
                    self._node(
                        f"record:{current_xref}",
                        "record",
                        "\n".join(current),
                        ordinal,
                        parent_id="document",
                    )
                )
        return tuple(nodes), []

    def _parse_csv(self, content: str) -> tuple[tuple[StructuralNode, ...], list[ParseDiagnostic]]:
        nodes: list[StructuralNode] = []
        for ordinal, line in enumerate(content.splitlines(), start=1):
            if not line.strip():
                continue
            nodes.append(
                self._node(
                    f"record:row_{ordinal}",
                    "record",
                    line,
                    ordinal,
                    parent_id="document",
                )
            )
        return tuple(nodes), []
