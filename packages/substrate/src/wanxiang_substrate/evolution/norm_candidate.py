"""Population-level social-norm candidates over repeated detections (G94D)."""

from __future__ import annotations

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.evolution.norm_candidate_model import (
    NormCandidate,
    NormEvaluation,
    NormOutcomeEvidence,
    NormPromotionPolicy,
    NormScope,
)
from wanxiang_substrate.evolution.pattern_detector_model import PatternDetection


def create_norm_candidate(
    detection: PatternDetection,
    *,
    candidate_id: str,
    scope: NormScope,
    scope_ref: str,
    now_ticks: int,
    population_refs: tuple[str, ...] | None = None,
    outcome_evidence: tuple[NormOutcomeEvidence, ...] = (),
) -> NormCandidate:
    """Build a norm candidate from a qualified detection and explicit evidence."""
    if not detection.qualified:
        raise ContractError("only a qualified pattern detection can form a norm candidate")
    population = tuple(sorted(set(population_refs or detection.subject_refs)))
    if len(population) < 2:
        raise ContractError("norm candidate requires at least two population refs")
    if now_ticks < detection.window_end:
        raise ContractError("norm candidate time cannot precede evidence")
    source_refs = set(detection.event_refs)
    outcomes = tuple(item for item in outcome_evidence if item.event_ref in source_refs)
    sanctions = sum(item.outcome == "sanction" for item in outcomes)
    rewards = sum(item.outcome == "reward" for item in outcomes)
    correlation = len(outcomes) / len(outcome_evidence) if outcome_evidence else 0.0
    return NormCandidate(
        candidate_id=candidate_id,
        pattern_key=detection.key,
        detection_id=detection.detection_id,
        scope=scope,
        scope_ref=scope_ref,
        population_refs=population,
        source_event_refs=detection.event_refs,
        exception_event_refs=tuple(
            sorted(
                {
                    ref
                    for counterexample in detection.counterexamples
                    for ref in counterexample.event_refs
                }
            )
        ),
        occurrence_count=detection.occurrence_count,
        observed_window_count=detection.observed_window_count,
        support_ratio=detection.support_ratio,
        exception_rate=detection.counterexample_rate,
        confidence=detection.confidence,
        sanction_count=sanctions,
        reward_count=rewards,
        outcome_correlation=round(correlation, 6),
        created_at=now_ticks,
    )


def evaluate_norm_candidate(
    candidate: NormCandidate,
    *,
    policy: NormPromotionPolicy | None = None,
) -> NormEvaluation:
    """Apply population and exception guards without approving a norm."""
    policy = policy or NormPromotionPolicy()
    reasons: list[str] = []
    if len(candidate.population_refs) < policy.minimum_population:
        reasons.append("population_below_floor")
    if candidate.occurrence_count < policy.minimum_occurrences:
        reasons.append("occurrence_count_below_floor")
    if candidate.observed_window_count < policy.minimum_windows:
        reasons.append("evidence_window_count_below_floor")
    if candidate.support_ratio < policy.minimum_support:
        reasons.append("support_below_floor")
    if candidate.exception_rate > policy.maximum_exception_rate:
        reasons.append("exception_rate_above_ceiling")
    if candidate.confidence < policy.minimum_confidence:
        reasons.append("confidence_below_floor")
    if candidate.outcome_correlation < policy.minimum_outcome_correlation:
        reasons.append("outcome_correlation_below_floor")
    return NormEvaluation(candidate.candidate_id, not reasons, tuple(reasons))
