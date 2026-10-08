"""ParsedDocument / structural parsing substrate (G56A/G56B)."""

from wanxiang_substrate.parsing.checkpoint import ParseCheckpointService
from wanxiang_substrate.parsing.diagnostics import (
    DiagnosticsReport,
    build_preview_report,
    collect,
    locator_preview,
    structure_preview,
)
from wanxiang_substrate.parsing.incremental import IncrementalParser, ParseCache, changed_segments
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
    "DiagnosticsReport",
    "DocumentMetadata",
    "IncrementalParser",
    "build_preview_report",
    "collect",
    "locator_preview",
    "structure_preview",
    "ParseCache",
    "ParseCheckpointService",
    "ParseDiagnostic",
    "ParsedDocument",
    "changed_segments",
    "Segment",
    "StableLocator",
    "StructuralNode",
    "StructureParser",
    "build_segments",
    "locator_for_node",
    "resolve",
]
