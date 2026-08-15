"""Full Corpus -> Canon Graph substrate (M36)."""

from wanxiang_substrate.canon_graph.graphs import (
    CanonClaim,
    CanonGraph,
    CharacterEdge,
    CharacterGraph,
    CharacterNode,
    CoverageReport,
    SceneCandidate,
    SourceGraph,
    TimelineEvent,
    TimelineGraph,
    build_canon_graph,
    build_character_graph,
    build_source_graph,
    build_timeline,
    detect_scenes,
)
from wanxiang_substrate.canon_graph.pipeline import CorpusGraphs, FullCorpusPipeline

__all__ = [
    "CanonClaim",
    "CanonGraph",
    "CharacterEdge",
    "CharacterGraph",
    "CharacterNode",
    "CorpusGraphs",
    "CoverageReport",
    "FullCorpusPipeline",
    "SceneCandidate",
    "SourceGraph",
    "TimelineEvent",
    "TimelineGraph",
    "build_canon_graph",
    "build_character_graph",
    "build_source_graph",
    "build_timeline",
    "detect_scenes",
]
