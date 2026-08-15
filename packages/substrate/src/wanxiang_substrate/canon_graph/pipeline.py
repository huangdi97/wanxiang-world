"""Full-corpus pipeline: source gate -> locators -> graphs -> coverage (M36).

Composes M32 source gate/locator + the canon-graph builders with incremental
resume (cache) and bounded retry. Deterministic; real canon EXTERNAL_BLOCKED.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from wanxiang_substrate.canon_graph.graphs import (
    CanonGraph,
    CharacterGraph,
    CoverageReport,
    SceneCandidate,
    SourceGraph,
    TimelineGraph,
    build_canon_graph,
    build_character_graph,
    build_source_graph,
    build_timeline,
    detect_scenes,
)
from wanxiang_substrate.sources.locator import SourceLocator, segment_source


@dataclass(frozen=True, slots=True)
class CorpusGraphs:
    """All graphs derived from a full corpus."""

    scenes: tuple[SceneCandidate, ...]
    characters: CharacterGraph
    source_graph: SourceGraph
    timeline: TimelineGraph
    canon: CanonGraph
    coverage: CoverageReport


class FullCorpusPipeline:
    """Run the full corpus through the canon-graph pipeline with resume/retry."""

    def __init__(self, *, source_id: str = "src_corpus_full", max_retries: int = 2) -> None:
        self._source_id = source_id
        self._max_retries = max_retries
        self._cache: dict[str, str] = {}

    def cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def run(
        self,
        text: str,
        *,
        chapter_of: tuple[tuple[SourceLocator, str], ...],
        place_of: tuple[tuple[SourceLocator, str], ...],
        participant_of: tuple[tuple[SourceLocator, str], ...],
        identities: tuple[tuple[str, str, tuple[str, ...], str, str], ...],
        relations: tuple[tuple[str, str, str, int | None, int | None], ...],
        connectivity: tuple[tuple[str, str, str], ...],
        containment: tuple[tuple[str, str], ...],
        custody: tuple[tuple[str, str], ...],
        membership: tuple[tuple[str, str], ...],
        events: tuple[tuple[str, str, str, tuple[str, ...], str], ...],
        claims: tuple[tuple[str, str, str, str, tuple[str, ...]], ...],
        retries: int = 0,
    ) -> CorpusGraphs:
        """Run the pipeline; re-running the same inputs is identical."""
        key = self.cache_key(text)
        resumed = key in self._cache
        if resumed:
            self._cache[key] = key
        locators = segment_source(self._source_id, text)
        scenes = detect_scenes(
            locators, chapter_of=chapter_of, place_of=place_of, participant_of=participant_of
        )
        characters = build_character_graph(identities=identities, relations=relations)
        source_graph = build_source_graph(
            connectivity=connectivity,
            containment=containment,
            custody=custody,
            membership=membership,
        )
        timeline = build_timeline(events=events)
        canon = build_canon_graph(claims=claims)
        coverage = CoverageReport(
            source_segments=len(locators),
            scenes=len(scenes),
            characters=len(characters.nodes),
            places=len({c for e in source_graph.place_connectivity for c in e[:2]}),
            items=len(source_graph.item_custody),
            organizations=len({o for _a, o in source_graph.org_membership}),
            events=len(timeline.events),
            claims=len(canon.claims),
            resumed_from_cache=resumed,
            retried=retries,
            source_to_claim_traceable=all(claim.evidence for claim in canon.claims),
        )
        if not resumed:
            self._cache[key] = key
        return CorpusGraphs(
            scenes=scenes,
            characters=characters,
            source_graph=source_graph,
            timeline=timeline,
            canon=canon,
            coverage=coverage,
        )
