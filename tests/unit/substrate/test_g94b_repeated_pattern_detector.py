"""G94B: repeated-pattern detections expose thresholds and false positives."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.evolution.pattern_detector import (
    RepeatedPatternDetector,
    detect_repeated_patterns,
)
from wanxiang_substrate.evolution.pattern_detector_model import RepeatedPatternPolicy
from wanxiang_substrate.evolution.pattern_observation import PatternObservationStore
from wanxiang_substrate.evolution.pattern_observation_model import PatternObservation


def _observation(
    observation_id: str, key: str, window_start: int, event_number: int
) -> PatternObservation:
    return PatternObservation(
        observation_id=observation_id,
        kind="behavior",
        key=key,
        subject_refs=("alice",),
        observed_at=window_start + 1,
        window_start=window_start,
        window_end=window_start + 100,
        event_refs=(f"evt_g94b_{event_number}",),
        features=(("operation_count", 1.0),),
    )


def _store() -> PatternObservationStore:
    return PatternObservationStore(
        window_size=100,
        _observations=(
            _observation("obs_repeat_1", "watch", 0, 1),
            _observation("obs_repeat_2", "watch", 100, 2),
            _observation("obs_repeat_3", "watch", 200, 3),
            _observation("obs_oneoff", "rare", 0, 4),
        ),
    )


@pytest.mark.unit
def test_detector_is_deterministic_and_reports_qualified_repetition() -> None:
    policy = RepeatedPatternPolicy(
        minimum_occurrences=3,
        minimum_windows=2,
        minimum_support=0.75,
        maximum_counterexample_rate=0.25,
        minimum_confidence=0.8,
    )
    detections = RepeatedPatternDetector(policy).detect(_store(), window_end=300)
    repeated = next(item for item in detections if item.key == "watch")
    rare = next(item for item in detections if item.key == "rare")
    assert repeated.qualified is True
    assert repeated.confidence == 1.0
    assert repeated.observed_window_count == 3
    assert repeated.counterexamples == ()
    assert repeated.event_refs == ("evt_g94b_1", "evt_g94b_2", "evt_g94b_3")
    assert rare.qualified is False
    assert rare.counterexample_rate == pytest.approx(2 / 3)
    assert len(rare.counterexamples) == 2
    assert {item.reason for item in rare.counterexamples} == {"missing_window"}
    assert detections == detect_repeated_patterns(_store(), policy=policy, window_end=300)


@pytest.mark.unit
def test_detector_does_not_treat_same_window_duplicates_as_stable_windows() -> None:
    repeated_same_window = PatternObservationStore(
        window_size=100,
        _observations=tuple(
            _observation(f"obs_same_{index}", "burst", 0, index) for index in range(1, 4)
        ),
    )
    result = RepeatedPatternDetector().detect(repeated_same_window, window_end=300)
    assert result[0].occurrence_count == 3
    assert result[0].observed_window_count == 1
    assert result[0].qualified is False
    assert result[0].counterexample_rate == pytest.approx(2 / 3)

    with pytest.raises(ContractError, match="minimum confidence"):
        RepeatedPatternPolicy(minimum_confidence=1.1)
    changed = replace(_store(), window_size=200)
    assert changed.window_size == 200
