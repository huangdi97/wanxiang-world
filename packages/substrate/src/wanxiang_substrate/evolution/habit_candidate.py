"""Evidence-window Habit/Skill candidates derived from repeated patterns."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.evolution.habit_candidate_model import (
    HabitCandidate,
    HabitEvaluation,
    HabitKind,
    HabitPromotionPolicy,
)
from wanxiang_substrate.evolution.pattern_detector_model import PatternDetection

SkillCandidate = HabitCandidate


def _decay(
    candidate: PatternDetection, now_ticks: int, policy: HabitPromotionPolicy
) -> tuple[int, float]:
    if now_ticks < candidate.window_end:
        raise ContractError("candidate evaluation time cannot precede evidence")
    age = max(0, (now_ticks - candidate.window_end) // candidate.window_size)
    factor = max(0.0, 1.0 - policy.decay_per_window * age)
    return age, round(candidate.confidence * factor, 6)


def create_habit_candidate(
    detection: PatternDetection,
    *,
    candidate_id: str,
    actor_id: EntityId,
    now_ticks: int,
    kind: HabitKind = "habit",
    policy: HabitPromotionPolicy | None = None,
) -> HabitCandidate:
    """Create a candidate only from a qualified actor-observed detection."""
    if not detection.qualified:
        raise ContractError("only a qualified pattern detection can form a habit candidate")
    if actor_id.value not in detection.subject_refs:
        raise ContractError("habit candidate actor is absent from detection subjects")
    policy = policy or HabitPromotionPolicy()
    _age, decayed = _decay(detection, now_ticks, policy)
    stability = round(detection.support_ratio * (1.0 - detection.counterexample_rate), 6)
    return HabitCandidate(
        candidate_id=candidate_id,
        actor_id=actor_id,
        kind=kind,
        pattern_key=detection.key,
        detection_id=detection.detection_id,
        window_start=detection.window_start,
        window_end=detection.window_end,
        window_size=detection.window_size,
        occurrence_count=detection.occurrence_count,
        observed_window_count=detection.observed_window_count,
        support_ratio=detection.support_ratio,
        stability_score=stability,
        base_confidence=detection.confidence,
        source_event_refs=detection.event_refs,
        created_at=now_ticks,
        evaluated_at=now_ticks,
        decayed_confidence=decayed,
    )


def create_skill_candidate(
    detection: PatternDetection,
    *,
    candidate_id: str,
    actor_id: EntityId,
    now_ticks: int,
    policy: HabitPromotionPolicy | None = None,
) -> SkillCandidate:
    """Create the same evidence-bound record with the explicit skill label."""
    return create_habit_candidate(
        detection,
        candidate_id=candidate_id,
        actor_id=actor_id,
        now_ticks=now_ticks,
        kind="skill",
        policy=policy,
    )


def evaluate_habit_candidate(
    candidate: HabitCandidate,
    *,
    now_ticks: int,
    policy: HabitPromotionPolicy | None = None,
) -> HabitEvaluation:
    """Evaluate stability/decay; this returns evidence, not an automatic promotion."""
    policy = policy or HabitPromotionPolicy()
    if now_ticks < candidate.evaluated_at:
        raise ContractError("habit evaluation time cannot move backwards")
    age = max(0, (now_ticks - candidate.window_end) // candidate.window_size)
    factor = max(0.0, 1.0 - policy.decay_per_window * age)
    decayed = round(candidate.base_confidence * factor, 6)
    reasons: list[str] = []
    if candidate.occurrence_count < policy.minimum_occurrences:
        reasons.append("occurrence_count_below_floor")
    if candidate.observed_window_count < policy.minimum_windows:
        reasons.append("evidence_window_count_below_floor")
    if candidate.stability_score < policy.minimum_stability:
        reasons.append("stability_below_floor")
    if decayed < policy.minimum_confidence:
        reasons.append("decayed_confidence_below_floor")
    if age > policy.maximum_age_windows:
        reasons.append("evidence_window_expired")
    return HabitEvaluation(
        candidate_id=candidate.candidate_id,
        eligible=not reasons,
        age_windows=age,
        decay_factor=round(factor, 6),
        decayed_confidence=decayed,
        reasons=tuple(reasons),
    )


def decay_habit_candidate(
    candidate: HabitCandidate,
    *,
    now_ticks: int,
    policy: HabitPromotionPolicy | None = None,
) -> HabitCandidate:
    """Return a time-updated candidate without changing its evidence history."""
    policy = policy or HabitPromotionPolicy()
    evaluation = evaluate_habit_candidate(candidate, now_ticks=now_ticks, policy=policy)
    return replace(
        candidate,
        evaluated_at=now_ticks,
        decayed_confidence=evaluation.decayed_confidence,
    )
