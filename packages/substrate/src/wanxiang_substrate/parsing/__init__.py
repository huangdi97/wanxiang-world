"""ParsedDocument / structural parsing substrate (G56A/G56B)."""

from wanxiang_substrate.parsing.model import (
    DocumentMetadata,
    ParsedDocument,
    ParseDiagnostic,
    StructuralNode,
)
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import (
    Segment,
    StableLocator,
    build_segments,
    locator_for_node,
    resolve,
)

__all__ = [
    "DocumentMetadata",
    "ParseDiagnostic",
    "ParsedDocument",
    "Segment",
    "StableLocator",
    "StructuralNode",
    "StructureParser",
    "build_segments",
    "locator_for_node",
    "resolve",
]
