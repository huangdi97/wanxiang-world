"""G94C: actor patterns become evidence-bound, decaying candidates only."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.evolution.habit_candidate import (
    create_habit_candidate,
    create_skill_candidate,
    decay_habit_candidate,
    evaluate_habit_candidate,
)
from wanxiang_substrate.evolution.habit_candidate_model import HabitPromotionPolicy
from wanxiang_substrate.evolution.pattern_detector_model import PatternDetection


def _detection(*, qualified: bool = True, actor: str = "alice") -> PatternDetection:
    return PatternDetection(
        detection_id="pattern_detection_g94c",
        kind="behavior",
        key="entity.update:status",
        subject_refs=(actor,),
        window_start=0,
        window_end=300,
        window_size=100,
        occurrence_count=3,
        observed_window_count=3,
        evaluated_window_count=3,
        support_ratio=1.0,
        counterexample_rate=0.0,
        confidence=1.0,
        event_refs=("evt_g94c_1", "evt_g94c_2", "evt_g94c_3"),
        counterexamples=(),
        qualified=qualified,
    )


@pytest.mark.unit
def test_habit_candidate_uses_window_stability_and_decay_without_auto_truth() -> None:
    policy = HabitPromotionPolicy(
        minimum_occurrences=3,
        minimum_windows=2,
        minimum_stability=0.8,
        minimum_confidence=0.7,
        decay_per_window=0.1,
        maximum_age_windows=5,
    )
    candidate = create_habit_candidate(
        _detection(),
        candidate_id="habit_g94c_watch",
        actor_id=EntityId("alice"),
        now_ticks=300,
        policy=policy,
    )
    assert candidate.actor_id == EntityId("alice")
    assert candidate.source_event_refs == ("evt_g94c_1", "evt_g94c_2", "evt_g94c_3")
    assert candidate.stability_score == 1.0
    assert candidate.base_confidence == 1.0
    assert evaluate_habit_candidate(candidate, now_ticks=300, policy=policy).eligible is True
    aged = decay_habit_candidate(candidate, now_ticks=700, policy=policy)
    assert aged.evaluated_at == 700
    assert aged.decayed_confidence == 0.6
    evaluation = evaluate_habit_candidate(aged, now_ticks=700, policy=policy)
    assert evaluation.eligible is False
    assert evaluation.reasons == ("decayed_confidence_below_floor",)
    skill = create_skill_candidate(
        _detection(),
        candidate_id="skill_g94c_watch",
        actor_id=EntityId("alice"),
        now_ticks=300,
        policy=policy,
    )
    assert skill.kind == "skill"


@pytest.mark.unit
def test_candidate_rejects_unqualified_or_unowned_patterns() -> None:
    with pytest.raises(ContractError, match="qualified"):
        create_habit_candidate(
            _detection(qualified=False),
            candidate_id="habit_rejected",
            actor_id=EntityId("alice"),
            now_ticks=300,
        )
    with pytest.raises(ContractError, match="absent"):
        create_habit_candidate(
            _detection(),
            candidate_id="habit_wrong_actor",
            actor_id=EntityId("bob"),
            now_ticks=300,
        )
    with pytest.raises(ContractError, match="cannot precede"):
        create_habit_candidate(
            _detection(),
            candidate_id="habit_early",
            actor_id=EntityId("alice"),
            now_ticks=299,
        )
