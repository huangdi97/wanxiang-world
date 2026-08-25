"""Segment model + format-aware stable locators (G56C/G56D).

Segments carry stable ids, content hashes, parent/ordinal and parser/
segmenter versions. StableLocator is a format-aware, round-trippable locator:
EPUB (chapter), DOCX (paragraph), PDF (page), JSON (pointer), CSV (row/col),
GEDCOM (xref). Locators resolve back to the exact source slice/node.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.parsing.model import ParsedDocument, StructuralNode

LocatorFormat = Literal["text", "epub", "docx", "pdf", "json", "csv", "gedcom"]
VALID_FORMATS = ("text", "epub", "docx", "pdf", "json", "csv", "gedcom")
LOCATOR_KINDS = ("chapter", "section", "paragraph", "record", "row", "column", "page", "document")


@dataclass(frozen=True, slots=True)
class StableLocator:
    """Format-aware, round-trippable source locator."""

    source_id: str
    fmt: LocatorFormat
    kind: str
    ref: str

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ContractError("locator requires source_id")
        if self.fmt not in VALID_FORMATS:
            raise ContractError(f"invalid locator format {self.fmt!r}")
        if self.kind not in LOCATOR_KINDS:
            raise ContractError(f"invalid locator kind {self.kind!r}")
        if not self.ref:
            raise ContractError("locator requires a ref")

    def to_string(self) -> str:
        return f"{self.fmt}://{self.source_id}#{self.kind}/{self.ref}"

    @classmethod
    def from_string(cls, value: str) -> StableLocator:
        scheme, _, rest = value.partition("://")
        if not scheme or not rest:
            raise ContractError(f"invalid locator {value!r}")
        source_id, _, tail = rest.partition("#")
        kind, _, ref = tail.partition("/")
        if not kind or not ref:
            raise ContractError(f"invalid locator {value!r}")
        return cls(source_id=source_id, fmt=scheme, kind=kind, ref=ref)  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class Segment:
    """A locator-bearing parsed segment with stable identity."""

    segment_id: str
    locator: StableLocator
    text: str
    kind: str
    ordinal: int
    parser_version: int
    segmenter_version: int
    parent_id: str = ""
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.segment_id:
            raise ContractError("segment requires an id")
        if self.ordinal < 0:
            raise ContractError("segment ordinal must be non-negative")

    def compute_hash(self) -> str:
        payload = json.dumps(
            {
                "segment_id": self.segment_id,
                "locator": self.locator.to_string(),
                "text": self.text,
                "kind": self.kind,
                "ordinal": self.ordinal,
                "parent_id": self.parent_id,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_hash(self) -> Segment:
        return Segment(
            segment_id=self.segment_id,
            locator=self.locator,
            text=self.text,
            kind=self.kind,
            ordinal=self.ordinal,
            parser_version=self.parser_version,
            segmenter_version=self.segmenter_version,
            parent_id=self.parent_id,
            content_hash=self.compute_hash(),
        )


def locator_for_node(node: StructuralNode, *, source_id: str, fmt: LocatorFormat) -> StableLocator:
    """Build a format-aware locator ref from a structural node."""
    if fmt == "json":
        ref = node.node_id.removeprefix("record:").replace(".", "/")
    elif fmt == "csv":
        ref = node.node_id.removeprefix("record:row_")
    elif fmt == "gedcom":
        ref = node.node_id.removeprefix("record:")
    elif fmt == "text":
        # Text paragraphs retain the parser node id, whose final component is
        # the original source line. This keeps candidate evidence line-bound.
        ref = node.node_id
    elif node.kind in ("chapter", "section", "paragraph"):
        ref = node.ordinal
    else:
        ref = node.ordinal
    return StableLocator(source_id=source_id, fmt=fmt, kind=node.kind, ref=str(ref))


def build_segments(
    parsed: ParsedDocument,
    *,
    fmt: LocatorFormat,
    parser_version: int = 1,
    segmenter_version: int = 1,
) -> tuple[Segment, ...]:
    """Segment a ParsedDocument into locator-bearing Segments."""
    segments: list[Segment] = []
    for node in parsed.nodes:
        if node.kind == "document":
            continue
        locator = locator_for_node(node, source_id=parsed.metadata.source_id, fmt=fmt)
        segment = Segment(
            segment_id=node.node_id,
            locator=locator,
            text=node.text,
            kind=node.kind,
            ordinal=node.ordinal,
            parser_version=parser_version,
            segmenter_version=segmenter_version,
            parent_id=node.parent_id,
        ).with_hash()
        segments.append(segment)
    return tuple(segments)


def resolve(parsed: ParsedDocument, locator: StableLocator) -> str | None:
    """Resolve a locator back to the exact source node text (round-trip)."""
    for node in parsed.nodes:
        candidate = locator_for_node(node, source_id=parsed.metadata.source_id, fmt=locator.fmt)
        if candidate.to_string() == locator.to_string():
            return node.text
    return None
