"""Gold Set metric calculation, independent of candidate extraction."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.quality.semantic_models import (
    GoldAssertion,
    GoldSet,
    MetricResult,
    SemanticQualityReport,
)


def evaluate_gold_set(
    candidates: tuple[CandidateEnvelope, ...], gold: GoldSet, *, threshold: float = 0.8
) -> SemanticQualityReport:
    """Score reviewer assertions with explicit denominators and failure reasons."""
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be within [0,1]")
    by_id = {candidate.candidate_id: candidate for candidate in candidates}
    assertions = gold.assertions
    accepted = tuple(item for item in assertions if item.accepted)
    present = tuple(item for item in accepted if item.candidate_id in by_id)
    matched = tuple(item for item in present if _matches(by_id[item.candidate_id], item))
    metrics: list[MetricResult] = [
        _metric(
            "identity_precision",
            _kind_matches(by_id, assertions, "identity"),
            assertions,
            "identity",
        )
    ]
    alias_items = tuple(item for item in assertions if item.kind in {"alias", "coreference"})
    alias_good = sum(
        _matches(by_id[item.candidate_id], item) and _merge_matches(by_id[item.candidate_id], item)
        for item in alias_items
        if item.candidate_id in by_id
    )
    metrics.append(_ratio("alias_merge_precision", alias_good, len(alias_items)))
    false_merges = sum(
        1
        for item in alias_items
        if item.candidate_id in by_id
        and (not item.accepted or not _merge_matches(by_id[item.candidate_id], item))
    )
    metrics.append(
        _ratio("false_merge_rate", false_merges, len(alias_items), direction="lower_is_better")
    )
    identity_groups = Counter(
        candidate.fields.get("key", candidate.fields.get("identity_key", ""))
        for item in accepted
        if (candidate := by_id.get(item.candidate_id)) is not None and item.kind == "identity"
    )
    duplicate_count = sum(max(0, count - 1) for key, count in identity_groups.items() if key)
    metrics.append(
        _ratio(
            "duplicate_rate",
            duplicate_count,
            sum(identity_groups.values()),
            direction="lower_is_better",
        )
    )
    missing_evidence = sum(
        not (by_id[item.candidate_id].source_refs or by_id[item.candidate_id].evidence_refs)
        for item in accepted
        if item.candidate_id in by_id
    )
    metrics.append(
        _ratio("missing_evidence_rate", missing_evidence, len(present), direction="lower_is_better")
    )
    event_items = tuple(item for item in assertions if item.kind == "event")
    metrics.append(
        _ratio("event_precision", _kind_matches(by_id, event_items, "event"), len(event_items))
    )
    participant_items = tuple(item for item in event_items if "participants" in item.expected)
    participant_good = sum(
        _participant_match(by_id[item.candidate_id], item)
        for item in participant_items
        if item.candidate_id in by_id
    )
    metrics.append(_ratio("participant_correctness", participant_good, len(participant_items)))
    metrics.append(_temporal_metric(by_id, event_items))
    uncertainty_items = tuple(item for item in assertions if item.expected_uncertain is not None)
    uncertainty_good = sum(
        _uncertainty_match(by_id[item.candidate_id], item)
        for item in uncertainty_items
        if item.candidate_id in by_id
    )
    metrics.append(_ratio("uncertainty_honesty", uncertainty_good, len(uncertainty_items)))
    relational = tuple(
        item for item in assertions if item.kind in {"relation", "place", "organization"}
    )
    metrics.append(
        _ratio(
            "relation_place_org_precision", _kind_matches(by_id, relational, "any"), len(relational)
        )
    )
    boundaries = tuple(item for item in assertions if item.kind in {"knowledge_boundary", "belief"})
    safe = sum(
        item.boundary_safe
        and item.candidate_id in by_id
        and _evidence_present(by_id[item.candidate_id])
        for item in boundaries
    )
    metrics.append(_ratio("knowledge_boundary_safety", safe, len(boundaries)))
    traceable = sum(
        _evidence_present(by_id[item.candidate_id])
        for item in assertions
        if item.candidate_id in by_id and item.accepted
    )
    metrics.append(_ratio("evidence_traceability", traceable, len(accepted)))
    failures = tuple(
        item.name
        for item in metrics
        if (
            item.value < threshold
            if item.direction == "higher_is_better"
            else item.value > 1.0 - threshold
        )
    )
    return SemanticQualityReport(
        gold.protocol_version,
        len(gold.sampling.selected_ids),
        len(assertions),
        tuple(metrics),
        not failures and len(matched) == len(accepted),
        failures,
    )


def _evidence_present(candidate: CandidateEnvelope) -> bool:
    return bool(candidate.source_refs or candidate.evidence_refs)


def _matches(candidate: CandidateEnvelope, assertion: GoldAssertion) -> bool:
    refs_match = not assertion.expected_source_refs or set(assertion.expected_source_refs).issubset(
        candidate.source_refs
    )
    return (
        assertion.accepted
        and refs_match
        and all(candidate.fields.get(key) == value for key, value in assertion.expected_payload)
    )


def _merge_matches(candidate: CandidateEnvelope, assertion: GoldAssertion) -> bool:
    return (
        not assertion.expected_merge_target
        or candidate.fields.get("identity_key", "") == assertion.expected_merge_target
    )


def _kind_matches(
    by_id: dict[str, CandidateEnvelope], items: Iterable[GoldAssertion], kind: str
) -> int:
    return sum(
        item.accepted
        and item.candidate_id in by_id
        and (kind == "any" or item.kind == kind)
        and _matches(by_id[item.candidate_id], item)
        for item in items
    )


def _participant_match(candidate: CandidateEnvelope, assertion: GoldAssertion) -> bool:
    expected = assertion.expected.get("participants", "")
    return bool(expected) and candidate.fields.get("participants", "") == expected


def _uncertainty_match(candidate: CandidateEnvelope, assertion: GoldAssertion) -> bool:
    uncertain = (
        candidate.fields.get("uncertain", "").lower() == "true"
        or candidate.fields.get("date", "") == "unknown"
    )
    return uncertain == assertion.expected_uncertain


def _temporal_metric(
    by_id: dict[str, CandidateEnvelope], items: tuple[GoldAssertion, ...]
) -> MetricResult:
    ordered = [
        item for item in items if item.expected_order is not None and item.candidate_id in by_id
    ]
    actual = sorted(
        ordered,
        key=lambda item: (
            by_id[item.candidate_id].fields.get("date", "unknown"),
            item.candidate_id,
        ),
    )
    expected = sorted(ordered, key=lambda item: (item.expected_order, item.candidate_id))
    return _ratio(
        "temporal_ordering",
        sum(
            left.candidate_id == right.candidate_id
            for left, right in zip(actual, expected, strict=True)
        ),
        len(expected),
    )


def _metric(name: str, numerator: int, items: Iterable[GoldAssertion], kind: str) -> MetricResult:
    return _ratio(name, numerator, sum(item.kind == kind for item in items))


def _ratio(
    name: str, numerator: int, denominator: int, *, direction: str = "higher_is_better"
) -> MetricResult:
    value = numerator / denominator if denominator else 1.0
    return MetricResult(name, numerator, denominator, value, direction)


__all__ = ["evaluate_gold_set"]
