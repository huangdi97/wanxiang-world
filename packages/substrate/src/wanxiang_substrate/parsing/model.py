"""ParsedDocument intermediate representation (G56A).

Unified middle representation between SourceAdapter output and semantic
distillation: DocumentMetadata + StructuralNode tree + asset references +
diagnostics. Nothing here is Canon; parsed structure is a Forge intermediate.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.blob import BlobRef

NodeKind = Literal[
    "document", "chapter", "section", "paragraph", "dialogue", "table", "record", "asset"
]
VALID_NODE_KINDS = (
    "document",
    "chapter",
    "section",
    "paragraph",
    "dialogue",
    "table",
    "record",
    "asset",
)

DiagnosticLevel = Literal["info", "warning", "error"]
VALID_DIAGNOSTIC_LEVELS = ("info", "warning", "error")


@dataclass(frozen=True, slots=True)
class DocumentMetadata:
    """Provenance + versioning for one parsed document."""

    source_id: str
    kind: str
    version: str
    parser_version: int
    segmenter_version: int
    content_hash: str
    detected_format: str
    size_bytes: int = 0
    title: str = ""

    def __post_init__(self) -> None:
        if not self.source_id or not self.kind:
            raise ContractError("metadata requires source_id and kind")
        if self.parser_version <= 0 or self.segmenter_version <= 0:
            raise ContractError("parser/segmenter versions must be positive")


@dataclass(frozen=True, slots=True)
class StructuralNode:
    """One parsed structural node with stable identity + parent/ordinal."""

    node_id: str
    kind: NodeKind
    text: str
    ordinal: int
    parser_version: int
    segmenter_version: int
    parent_id: str = ""
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ContractError("node requires an id")
        if self.kind not in VALID_NODE_KINDS:
            raise ContractError(f"invalid node kind {self.kind!r}")
        if self.ordinal < 0:
            raise ContractError("node ordinal must be non-negative")
        if self.parser_version <= 0 or self.segmenter_version <= 0:
            raise ContractError("node versions must be positive")

    def compute_hash(self) -> str:
        payload = json.dumps(
            {
                "node_id": self.node_id,
                "kind": self.kind,
                "text": self.text,
                "ordinal": self.ordinal,
                "parent_id": self.parent_id,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_hash(self) -> StructuralNode:
        return StructuralNode(
            node_id=self.node_id,
            kind=self.kind,
            text=self.text,
            ordinal=self.ordinal,
            parser_version=self.parser_version,
            segmenter_version=self.segmenter_version,
            parent_id=self.parent_id,
            content_hash=self.compute_hash(),
        )


@dataclass(frozen=True, slots=True)
class ParseDiagnostic:
    """Parser warning/error with node or locator context."""

    level: DiagnosticLevel
    code: str
    message: str
    node_id: str = ""

    def __post_init__(self) -> None:
        if self.level not in VALID_DIAGNOSTIC_LEVELS:
            raise ContractError(f"invalid diagnostic level {self.level!r}")
        if not self.code or not self.message:
            raise ContractError("diagnostic requires code and message")


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    """Unified parsed document: metadata + node tree + assets + diagnostics."""

    document_id: str
    metadata: DocumentMetadata
    nodes: tuple[StructuralNode, ...]
    asset_refs: tuple[BlobRef, ...] = ()
    diagnostics: tuple[ParseDiagnostic, ...] = ()

    def __post_init__(self) -> None:
        if not self.document_id:
            raise ContractError("parsed document requires an id")
        if not self.nodes:
            raise ContractError("parsed document requires at least one node")

    @property
    def ok(self) -> bool:
        return not any(d.level == "error" for d in self.diagnostics)
