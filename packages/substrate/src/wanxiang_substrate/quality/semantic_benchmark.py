"""Deterministic sampling for the M80 semantic quality protocol."""

from __future__ import annotations

from random import Random

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.quality.semantic_metrics import evaluate_gold_set
from wanxiang_substrate.quality.semantic_models import (
    QUALITY_METRICS,
    GoldAssertion,
    GoldSet,
    MetricResult,
    SamplingManifest,
    SemanticQualityReport,
)


def sample_candidates(
    candidates: tuple[CandidateEnvelope, ...], *, sample_size: int = 24, seed: int = 83
) -> tuple[tuple[CandidateEnvelope, ...], SamplingManifest]:
    """Select random, high-impact, low-confidence, and conflict/merge strata."""
    if sample_size < 1:
        raise ValueError("sample_size must be positive")
    ordered = tuple(sorted(candidates, key=lambda item: item.candidate_id))
    if not ordered:
        return (), SamplingManifest(seed, sample_size, (), ())
    limit = min(sample_size, len(ordered))
    chosen: list[CandidateEnvelope] = []
    strata: dict[str, list[str]] = {}

    def add(name: str, item: CandidateEnvelope) -> None:
        if item.candidate_id in {candidate.candidate_id for candidate in chosen}:
            return
        chosen.append(item)
        strata.setdefault(name, []).append(item.candidate_id)

    random_pool = list(ordered)
    Random(seed).shuffle(random_pool)
    high_impact = sorted(
        ordered,
        key=lambda item: (
            item.kind not in {"identity", "alias", "event", "relation", "place", "organization"},
            -item.confidence,
            item.candidate_id,
        ),
    )
    low_confidence = sorted(ordered, key=lambda value: (value.confidence, value.candidate_id))
    conflict_merge = tuple(
        item
        for item in ordered
        if item.kind in {"alias", "coreference", "relation"} or len(item.source_refs) > 1
    )
    pools = (
        ("random", tuple(random_pool)),
        ("high_impact", tuple(high_impact)),
        ("low_confidence", tuple(low_confidence)),
        ("conflict_merge", conflict_merge),
    )
    for name, pool in pools:
        for item in pool:
            before = len(chosen)
            add(name, item)
            if len(chosen) > before or len(chosen) >= limit:
                break
    for item in random_pool + high_impact + low_confidence + list(conflict_merge) + list(ordered):
        if len(chosen) >= limit:
            break
        add("fill", item)
    selected = tuple(sorted(chosen, key=lambda item: item.candidate_id))
    return selected, SamplingManifest(
        seed,
        sample_size,
        tuple(item.candidate_id for item in selected),
        tuple((name, tuple(ids)) for name, ids in sorted(strata.items())),
    )


__all__ = [
    "GoldAssertion",
    "GoldSet",
    "MetricResult",
    "QUALITY_METRICS",
    "SamplingManifest",
    "SemanticQualityReport",
    "evaluate_gold_set",
    "sample_candidates",
]
