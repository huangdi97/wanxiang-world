"""Full Corpus -> Canon Graph substrate (M36)."""

from wanxiang_substrate.canon_graph.graphs import (
    CharacterEdge,
    CharacterGraph,
    CharacterNode,
    SceneCandidate,
    SourceGraph,
    build_character_graph,
    build_source_graph,
    detect_scenes,
)
from wanxiang_substrate.canon_graph.pipeline import CorpusGraphs, FullCorpusPipeline
from wanxiang_substrate.canon_graph.timeline_canon import (
    CanonClaim,
    CanonGraph,
    CoverageReport,
    TimelineEvent,
    TimelineGraph,
    build_canon_graph,
    build_timeline,
)

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
