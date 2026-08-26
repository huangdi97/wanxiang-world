"""Typed outputs and policy for deterministic repeated-pattern detection."""

from __future__ import annotations

import math
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.evolution.pattern_observation_model import PatternKind


@dataclass(frozen=True, slots=True)
class RepeatedPatternPolicy:
    """Reference thresholds; passing detection remains a candidate signal."""

    minimum_occurrences: int = 3
    minimum_windows: int = 2
    minimum_support: float = 0.5
    maximum_counterexample_rate: float = 0.5
    minimum_confidence: float = 0.6

    def __post_init__(self) -> None:
        if type(self.minimum_occurrences) is not int or self.minimum_occurrences < 1:
            raise ContractError("minimum occurrences must be a positive integer")
        if type(self.minimum_windows) is not int or self.minimum_windows < 1:
            raise ContractError("minimum windows must be a positive integer")
        for name, value in (
            ("minimum support", self.minimum_support),
            ("maximum counterexample rate", self.maximum_counterexample_rate),
            ("minimum confidence", self.minimum_confidence),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError(f"{name} must be within [0, 1]")

    def to_dict(self) -> dict[str, object]:
        return {
            "minimum_occurrences": self.minimum_occurrences,
            "minimum_windows": self.minimum_windows,
            "minimum_support": self.minimum_support,
            "maximum_counterexample_rate": self.maximum_counterexample_rate,
            "minimum_confidence": self.minimum_confidence,
        }


@dataclass(frozen=True, slots=True)
class PatternCounterexample:
    """Concrete evaluated window where a pattern was absent."""

    window_start: int
    window_end: int
    reason: str = "missing_window"
    event_refs: tuple[str, ...] = ()
    subject_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.window_start < 0 or self.window_end <= self.window_start:
            raise ContractError("counterexample window must be non-empty")
        if not self.reason.strip():
            raise ContractError("counterexample reason is required")
        if len(set(self.event_refs)) != len(self.event_refs) or any(
            not ref.strip() for ref in self.event_refs
        ):
            raise ContractError("counterexample event refs must be unique and non-empty")

    def to_dict(self) -> dict[str, object]:
        return {
            "window_start": self.window_start,
            "window_end": self.window_end,
            "reason": self.reason,
            "event_refs": list(self.event_refs),
            "subject_refs": list(self.subject_refs),
        }


@dataclass(frozen=True, slots=True)
class PatternDetection:
    """A deterministic detection result, never an automatic world truth."""

    detection_id: str
    kind: PatternKind
    key: str
    subject_refs: tuple[str, ...]
    window_start: int
    window_end: int
    window_size: int
    occurrence_count: int
    observed_window_count: int
    evaluated_window_count: int
    support_ratio: float
    counterexample_rate: float
    confidence: float
    event_refs: tuple[str, ...]
    counterexamples: tuple[PatternCounterexample, ...]
    qualified: bool

    def __post_init__(self) -> None:
        if not self.detection_id.strip() or not self.key.strip():
            raise ContractError("pattern detection requires id and key")
        if self.window_start < 0 or self.window_end <= self.window_start:
            raise ContractError("pattern detection window must be non-empty")
        if self.window_size < 1 or self.occurrence_count < 1:
            raise ContractError("pattern detection counts must be positive")
        if not 0 <= self.observed_window_count <= self.evaluated_window_count:
            raise ContractError("pattern detection window counts are inconsistent")
        for name, value in (
            ("support ratio", self.support_ratio),
            ("counterexample rate", self.counterexample_rate),
            ("confidence", self.confidence),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError(f"{name} must be within [0, 1]")
        if len(set(self.event_refs)) != len(self.event_refs) or any(
            not ref.strip() for ref in self.event_refs
        ):
            raise ContractError("pattern detection event refs must be unique and non-empty")

    @property
    def meets_threshold(self) -> bool:
        return self.qualified

    def to_dict(self) -> dict[str, object]:
        return {
            "detection_id": self.detection_id,
            "kind": self.kind,
            "key": self.key,
            "subject_refs": list(self.subject_refs),
            "window_start": self.window_start,
            "window_end": self.window_end,
            "window_size": self.window_size,
            "occurrence_count": self.occurrence_count,
            "observed_window_count": self.observed_window_count,
            "evaluated_window_count": self.evaluated_window_count,
            "support_ratio": self.support_ratio,
            "counterexample_rate": self.counterexample_rate,
            "confidence": self.confidence,
            "event_refs": list(self.event_refs),
            "counterexamples": [item.to_dict() for item in self.counterexamples],
            "qualified": self.qualified,
        }
