"""G94D: population norms require scope, exceptions, and outcome evidence."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.evolution.norm_candidate import (
    create_norm_candidate,
    evaluate_norm_candidate,
)
from wanxiang_substrate.evolution.norm_candidate_model import (
    NormOutcomeEvidence,
    NormPromotionPolicy,
)
from wanxiang_substrate.evolution.pattern_detector_model import (
    PatternCounterexample,
    PatternDetection,
)


def _detection(
    *, subjects: tuple[str, ...] = ("alice", "bob"), exception_rate: float = 0.0
) -> PatternDetection:
    counters = (
        (PatternCounterexample(300, 400, event_refs=("evt_exception",)),) if exception_rate else ()
    )
    return PatternDetection(
        detection_id="pattern_detection_g94d",
        kind="behavior",
        key="shared:gate-duty",
        subject_refs=subjects,
        window_start=0,
        window_end=400,
        window_size=100,
        occurrence_count=4,
        observed_window_count=4 if not exception_rate else 3,
        evaluated_window_count=4,
        support_ratio=1.0 if not exception_rate else 0.75,
        counterexample_rate=exception_rate,
        confidence=0.95 if not exception_rate else 0.7,
        event_refs=("evt_g94d_1", "evt_g94d_2", "evt_g94d_3", "evt_g94d_4"),
        counterexamples=counters,
        qualified=True,
    )


@pytest.mark.unit
def test_norm_candidate_records_population_scope_and_sanction_reward_correlation() -> None:
    candidate = create_norm_candidate(
        _detection(),
        candidate_id="norm_g94d_gate",
        scope="local",
        scope_ref="world:g94d",
        now_ticks=400,
        outcome_evidence=(
            NormOutcomeEvidence("evt_g94d_1", "alice", "reward"),
            NormOutcomeEvidence("evt_g94d_2", "bob", "sanction"),
            NormOutcomeEvidence("evt_unknown", "carol", "neutral"),
        ),
    )
    assert candidate.population_refs == ("alice", "bob")
    assert candidate.sanction_count == 1
    assert candidate.reward_count == 1
    assert candidate.outcome_correlation == pytest.approx(2 / 3)
    evaluation = evaluate_norm_candidate(
        candidate,
        policy=NormPromotionPolicy(
            minimum_population=2,
            minimum_occurrences=3,
            minimum_windows=2,
            minimum_support=0.75,
            maximum_exception_rate=0.25,
            minimum_confidence=0.8,
            minimum_outcome_correlation=0.5,
        ),
    )
    assert evaluation.eligible is True


@pytest.mark.unit
def test_norm_small_sample_and_exception_guards_do_not_promote_truth() -> None:
    with pytest.raises(ContractError, match="at least two"):
        create_norm_candidate(
            _detection(subjects=("alice",)),
            candidate_id="norm_small",
            scope="local",
            scope_ref="world:g94d",
            now_ticks=400,
        )
    candidate = create_norm_candidate(
        _detection(exception_rate=0.25),
        candidate_id="norm_exception",
        scope="global",
        scope_ref="worlds:g94d",
        now_ticks=400,
    )
    evaluation = evaluate_norm_candidate(
        candidate,
        policy=NormPromotionPolicy(maximum_exception_rate=0.2),
    )
    assert evaluation.eligible is False
    assert evaluation.reasons == ("exception_rate_above_ceiling",)
    with pytest.raises(ContractError, match="unknown norm outcome"):
        NormOutcomeEvidence("evt_bad", "alice", "rumor")  # type: ignore[arg-type]
