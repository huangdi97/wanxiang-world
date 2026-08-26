"""Deterministic repeated-pattern detection over the G94A observation cache."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.evolution.pattern_detector_model import (
    PatternCounterexample,
    PatternDetection,
    RepeatedPatternPolicy,
)
from wanxiang_substrate.evolution.pattern_observation import PatternObservationStore
from wanxiang_substrate.evolution.pattern_observation_model import (
    PatternKind,
    PatternObservation,
)


def _window_range(start: int, end: int, size: int) -> tuple[int, ...]:
    if isinstance(start, bool) or isinstance(end, bool) or start < 0 or end <= start:
        raise ContractError("pattern detection window must be non-negative and non-empty")
    first = (start // size) * size
    return tuple(range(first, end, size))


def _detection(
    observations: tuple[PatternObservation, ...],
    evaluated: tuple[int, ...],
    window_size: int,
    policy: RepeatedPatternPolicy,
) -> PatternDetection:
    first = observations[0]
    by_window: dict[int, list[PatternObservation]] = defaultdict(list)
    for item in observations:
        by_window[item.window_start].append(item)
    present = tuple(sorted(by_window))
    counterexamples = tuple(
        PatternCounterexample(start, start + window_size)
        for start in evaluated
        if start not in by_window
    )
    occurrence_count = len(observations)
    observed_window_count = len(present)
    evaluated_window_count = len(evaluated)
    support = observed_window_count / evaluated_window_count
    counterexample_rate = len(counterexamples) / evaluated_window_count
    repetition = min(1.0, occurrence_count / policy.minimum_occurrences)
    window_score = min(1.0, observed_window_count / policy.minimum_windows)
    consistency = 1.0 - counterexample_rate
    confidence = round(
        0.35 * support + 0.25 * repetition + 0.20 * window_score + 0.20 * consistency,
        6,
    )
    qualified = (
        occurrence_count >= policy.minimum_occurrences
        and observed_window_count >= policy.minimum_windows
        and support >= policy.minimum_support
        and counterexample_rate <= policy.maximum_counterexample_rate
        and confidence >= policy.minimum_confidence
    )
    subjects = tuple(sorted({ref for item in observations for ref in item.subject_refs}))
    event_refs = tuple(sorted({ref for item in observations for ref in item.event_refs}))
    detection_id = "pattern_detection:" + semantic_sha256(
        {
            "kind": first.kind,
            "key": first.key,
            "window_start": evaluated[0],
            "window_end": evaluated[-1] + window_size,
        }
    )
    return PatternDetection(
        detection_id=detection_id,
        kind=first.kind,
        key=first.key,
        subject_refs=subjects,
        window_start=evaluated[0],
        window_end=evaluated[-1] + window_size,
        window_size=window_size,
        occurrence_count=occurrence_count,
        observed_window_count=observed_window_count,
        evaluated_window_count=evaluated_window_count,
        support_ratio=round(support, 6),
        counterexample_rate=round(counterexample_rate, 6),
        confidence=confidence,
        event_refs=event_refs,
        counterexamples=counterexamples,
        qualified=qualified,
    )


@dataclass(frozen=True, slots=True)
class RepeatedPatternDetector:
    """Read-only detector using a reference threshold and confidence policy."""

    policy: RepeatedPatternPolicy = RepeatedPatternPolicy()

    def detect(
        self,
        store: PatternObservationStore,
        *,
        window_start: int = 0,
        window_end: int | None = None,
        kind: PatternKind | None = None,
    ) -> tuple[PatternDetection, ...]:
        selected = store.query(window_start=window_start, window_end=window_end, kind=kind)
        if not selected:
            return ()
        resolved_end = window_end or max(item.window_end for item in selected)
        evaluated = _window_range(window_start, resolved_end, store.window_size)
        groups: dict[tuple[PatternKind, str], list[PatternObservation]] = defaultdict(list)
        for item in selected:
            groups[(item.kind, item.key)].append(item)
        return tuple(
            _detection(
                tuple(sorted(items, key=lambda item: item.observation_id)),
                evaluated,
                store.window_size,
                self.policy,
            )
            for _group, items in sorted(groups.items())
        )


def detect_repeated_patterns(
    store: PatternObservationStore,
    *,
    policy: RepeatedPatternPolicy | None = None,
    window_start: int = 0,
    window_end: int | None = None,
    kind: PatternKind | None = None,
) -> tuple[PatternDetection, ...]:
    """Convenience facade for a deterministic read-only detection run."""
    return RepeatedPatternDetector(policy or RepeatedPatternPolicy()).detect(
        store, window_start=window_start, window_end=window_end, kind=kind
    )
