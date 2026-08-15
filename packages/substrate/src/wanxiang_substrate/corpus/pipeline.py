"""Large-corpus pipeline capacity baseline (G38F).

Deterministic synthetic large corpus + incremental parse/distill/cache/resume
pipeline with a memory/disk profile. Reuses G35B segmentation and the identity
distiller; no real《红楼梦》canon (synthetic only).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from wanxiang_substrate.sources.identity import IdentityCandidate, IdentityDistiller
from wanxiang_substrate.sources.locator import SourceLocator, segment_source


def generate_synthetic_corpus(*, chapters: int, lines_per_chapter: int = 4) -> str:
    """Deterministic synthetic corpus with N chapters (explicitly synthetic)."""
    parts: list[str] = []
    for chapter in range(1, chapters + 1):
        parts.append(f"第{chapter}回")
        for line in range(lines_per_chapter):
            parts.append(f"c{chapter % 5 + 1} 于第{chapter}回活动第{line}行。")
        parts.append("")
    return "\n".join(parts)


@dataclass(frozen=True, slots=True)
class CorpusProfile:
    """Memory/disk profile of a parsed corpus."""

    characters: int
    segments: int
    candidates: int
    est_memory_bytes: int
    est_disk_bytes: int

    @property
    def ok_within_bounds(self) -> bool:
        # Bounded profile: < 64 MiB estimated memory for 1000+ chapters.
        return self.est_memory_bytes < 64 * 1024 * 1024


class CorpusPipeline:
    """Incremental parse -> distill -> cache -> resume over a synthetic corpus."""

    def __init__(
        self,
        distiller: IdentityDistiller,
        *,
        source_id: str = "src_corpus_synth",
    ) -> None:
        self._distiller = distiller
        self._source_id = source_id
        self._cache: dict[str, tuple[SourceLocator, ...]] = {}

    def cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def parse(self, text: str) -> tuple[SourceLocator, ...]:
        return segment_source(self._source_id, text)

    def distill(self, text: str) -> tuple[IdentityCandidate, ...]:
        return self._distiller.distill(self._source_id, text)

    def process(
        self, text: str
    ) -> tuple[tuple[SourceLocator, ...], tuple[IdentityCandidate, ...], bool]:
        """Process a corpus; returns (locators, candidates, was_cached)."""
        key = self.cache_key(text)
        if key in self._cache:
            return self._cache[key], (), True
        locators = self.parse(text)
        candidates = self.distill(text)
        self._cache[key] = locators
        return locators, candidates, False

    def resume(self, text: str) -> bool:
        """Resume skips already-processed corpora (idempotent)."""
        key = self.cache_key(text)
        if key in self._cache:
            return True
        _locators, _candidates, _ = self.process(text)
        return False

    def profile(self, text: str) -> CorpusProfile:
        locators = self.parse(text)
        candidates = self.distill(text)
        chars = len(text)
        est_memory = chars * 2 + len(locators) * 128 + len(candidates) * 256
        est_disk = chars
        return CorpusProfile(
            characters=chars,
            segments=len(locators),
            candidates=len(candidates),
            est_memory_bytes=est_memory,
            est_disk_bytes=est_disk,
        )
