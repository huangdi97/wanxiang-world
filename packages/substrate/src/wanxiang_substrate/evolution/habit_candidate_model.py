"""Typed habit/skill candidate records and their promotion policy."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

HabitKind = Literal["habit", "skill"]


@dataclass(frozen=True, slots=True)
class HabitPromotionPolicy:
    """Evidence and decay thresholds for actor-local candidate evaluation."""

    minimum_occurrences: int = 3
    minimum_windows: int = 2
    minimum_stability: float = 0.6
    minimum_confidence: float = 0.6
    decay_per_window: float = 0.1
    maximum_age_windows: int = 6

    def __post_init__(self) -> None:
        for name, value in (
            ("minimum occurrences", self.minimum_occurrences),
            ("minimum windows", self.minimum_windows),
            ("maximum age windows", self.maximum_age_windows),
        ):
            if type(value) is not int or value < 1:
                raise ContractError(f"{name} must be a positive integer")
        for name, value in (
            ("minimum stability", self.minimum_stability),
            ("minimum confidence", self.minimum_confidence),
            ("decay per window", self.decay_per_window),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError(f"{name} must be within [0, 1]")

    def to_dict(self) -> dict[str, object]:
        return {
            "minimum_occurrences": self.minimum_occurrences,
            "minimum_windows": self.minimum_windows,
            "minimum_stability": self.minimum_stability,
            "minimum_confidence": self.minimum_confidence,
            "decay_per_window": self.decay_per_window,
            "maximum_age_windows": self.maximum_age_windows,
        }


@dataclass(frozen=True, slots=True)
class HabitCandidate:
    """Actor-local candidate; eligibility is not actor truth or a skill commit."""

    candidate_id: str
    actor_id: EntityId
    kind: HabitKind
    pattern_key: str
    detection_id: str
    window_start: int
    window_end: int
    window_size: int
    occurrence_count: int
    observed_window_count: int
    support_ratio: float
    stability_score: float
    base_confidence: float
    source_event_refs: tuple[str, ...]
    created_at: int
    evaluated_at: int
    decayed_confidence: float

    def __post_init__(self) -> None:
        if not self.candidate_id.strip() or not self.pattern_key.strip():
            raise ContractError("habit candidate requires id and pattern key")
        if not self.detection_id.strip() or self.kind not in ("habit", "skill"):
            raise ContractError("habit candidate requires valid detection and kind")
        if self.window_start < 0 or self.window_end <= self.window_start:
            raise ContractError("habit evidence window must be non-empty")
        if self.window_size < 1 or self.occurrence_count < 1:
            raise ContractError("habit candidate counts must be positive")
        if self.observed_window_count < 1 or self.observed_window_count > self.occurrence_count:
            raise ContractError("habit candidate window count is inconsistent")
        if self.created_at < self.window_end or self.evaluated_at < self.created_at:
            raise ContractError("habit candidate evaluation time is not monotonic")
        for name, value in (
            ("support ratio", self.support_ratio),
            ("stability score", self.stability_score),
            ("base confidence", self.base_confidence),
            ("decayed confidence", self.decayed_confidence),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError(f"{name} must be within [0, 1]")
        if not self.source_event_refs or len(set(self.source_event_refs)) != len(
            self.source_event_refs
        ):
            raise ContractError("habit candidate requires unique event evidence")

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "actor_id": self.actor_id.value,
            "kind": self.kind,
            "pattern_key": self.pattern_key,
            "detection_id": self.detection_id,
            "window_start": self.window_start,
            "window_end": self.window_end,
            "window_size": self.window_size,
            "occurrence_count": self.occurrence_count,
            "observed_window_count": self.observed_window_count,
            "support_ratio": self.support_ratio,
            "stability_score": self.stability_score,
            "base_confidence": self.base_confidence,
            "source_event_refs": list(self.source_event_refs),
            "created_at": self.created_at,
            "evaluated_at": self.evaluated_at,
            "decayed_confidence": self.decayed_confidence,
        }


@dataclass(frozen=True, slots=True)
class HabitEvaluation:
    """Pure evaluation result used by a later explicit review/promotion gate."""

    candidate_id: str
    eligible: bool
    age_windows: int
    decay_factor: float
    decayed_confidence: float
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.candidate_id.strip() or self.age_windows < 0:
            raise ContractError("invalid habit evaluation")
        if not 0.0 <= self.decay_factor <= 1.0 or not 0.0 <= self.decayed_confidence <= 1.0:
            raise ContractError("habit evaluation scores must be within [0, 1]")

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "eligible": self.eligible,
            "age_windows": self.age_windows,
            "decay_factor": self.decay_factor,
            "decayed_confidence": self.decayed_confidence,
            "reasons": list(self.reasons),
        }
