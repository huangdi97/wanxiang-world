"""G38F: large-corpus pipeline capacity baseline (mechanism; synthetic)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.corpus import (
    CorpusPipeline,
    generate_synthetic_corpus,
)
from wanxiang_substrate.sources.identity import IdentityDistiller


def _distiller() -> IdentityDistiller:
    known = {"c1", "c2", "c3", "c4", "c5"}

    def extract(text: str) -> tuple[str, ...]:
        return tuple(t for t in known if t in text)

    return IdentityDistiller(extract_mentions=extract, resolve_identity=lambda m: m)


@pytest.mark.unit
def test_large_synthetic_corpus_parses_and_distills() -> None:
    corpus = generate_synthetic_corpus(chapters=1000)
    pipeline = CorpusPipeline(_distiller())
    locators, candidates, cached = pipeline.process(corpus)
    assert cached is False
    assert len(locators) == 1000
    assert candidates
    assert len(corpus) > 50_000


@pytest.mark.unit
def test_incremental_cache_and_resume() -> None:
    corpus = generate_synthetic_corpus(chapters=100)
    pipeline = CorpusPipeline(_distiller())
    first = pipeline.process(corpus)
    assert first[2] is False
    second = pipeline.process(corpus)
    assert second[2] is True
    assert pipeline.resume(corpus) is True
    assert pipeline.cache_key(corpus) == pipeline.cache_key(corpus)


@pytest.mark.unit
def test_profile_within_memory_bounds() -> None:
    corpus = generate_synthetic_corpus(chapters=1000)
    profile = CorpusPipeline(_distiller()).profile(corpus)
    assert profile.segments == 1000
    assert profile.candidates > 0
    assert profile.ok_within_bounds is True
    assert profile.est_disk_bytes == len(corpus)


@pytest.mark.unit
def test_synthetic_corpus_is_deterministic() -> None:
    first = generate_synthetic_corpus(chapters=50)
    second = generate_synthetic_corpus(chapters=50)
    assert first == second
