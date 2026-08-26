"""Typed population-level norm candidates and policy evaluation values."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

NormScope = Literal["local", "global"]
NormOutcomeKind = Literal["sanction", "reward", "neutral"]


@dataclass(frozen=True, slots=True)
class NormPromotionPolicy:
    """Small-sample, exception, stability, and outcome evidence thresholds."""

    minimum_population: int = 2
    minimum_occurrences: int = 3
    minimum_windows: int = 2
    minimum_support: float = 0.5
    maximum_exception_rate: float = 0.4
    minimum_confidence: float = 0.6
    minimum_outcome_correlation: float = 0.0

    def __post_init__(self) -> None:
        for name, value in (
            ("minimum population", self.minimum_population),
            ("minimum occurrences", self.minimum_occurrences),
            ("minimum windows", self.minimum_windows),
        ):
            if type(value) is not int or value < 2:
                raise ContractError(f"{name} must be an integer of at least two")
        for name, value in (
            ("minimum support", self.minimum_support),
            ("maximum exception rate", self.maximum_exception_rate),
            ("minimum confidence", self.minimum_confidence),
            ("minimum outcome correlation", self.minimum_outcome_correlation),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError(f"{name} must be within [0, 1]")

    def to_dict(self) -> dict[str, object]:
        return {
            "minimum_population": self.minimum_population,
            "minimum_occurrences": self.minimum_occurrences,
            "minimum_windows": self.minimum_windows,
            "minimum_support": self.minimum_support,
            "maximum_exception_rate": self.maximum_exception_rate,
            "minimum_confidence": self.minimum_confidence,
            "minimum_outcome_correlation": self.minimum_outcome_correlation,
        }


@dataclass(frozen=True, slots=True)
class NormOutcomeEvidence:
    """Committed-event-linked reward/sanction signal; never a world mutation."""

    event_ref: str
    actor_ref: str
    outcome: NormOutcomeKind

    def __post_init__(self) -> None:
        if not self.event_ref.strip() or not self.actor_ref.strip():
            raise ContractError("norm outcome evidence requires event and actor refs")
        if self.outcome not in ("sanction", "reward", "neutral"):
            raise ContractError(f"unknown norm outcome {self.outcome!r}")

    def to_dict(self) -> dict[str, str]:
        return {
            "event_ref": self.event_ref,
            "actor_ref": self.actor_ref,
            "outcome": self.outcome,
        }


@dataclass(frozen=True, slots=True)
class NormCandidate:
    """Population-level norm candidate, retained outside Canon until reviewed."""

    candidate_id: str
    pattern_key: str
    detection_id: str
    scope: NormScope
    scope_ref: str
    population_refs: tuple[str, ...]
    source_event_refs: tuple[str, ...]
    exception_event_refs: tuple[str, ...]
    occurrence_count: int
    observed_window_count: int
    support_ratio: float
    exception_rate: float
    confidence: float
    sanction_count: int
    reward_count: int
    outcome_correlation: float
    created_at: int

    def __post_init__(self) -> None:
        if not self.candidate_id.strip() or not self.pattern_key.strip():
            raise ContractError("norm candidate requires id and pattern key")
        if not self.detection_id.strip() or not self.scope_ref.strip():
            raise ContractError("norm candidate requires detection and scope refs")
        if self.scope not in ("local", "global"):
            raise ContractError(f"unknown norm scope {self.scope!r}")
        if not self.population_refs or len(set(self.population_refs)) != len(self.population_refs):
            raise ContractError("norm candidate requires unique population refs")
        for name, value in (
            ("occurrence count", self.occurrence_count),
            ("observed window count", self.observed_window_count),
            ("sanction count", self.sanction_count),
            ("reward count", self.reward_count),
        ):
            if type(value) is not int or value < 0:
                raise ContractError(f"{name} must be non-negative")
        for name, value in (
            ("support ratio", self.support_ratio),
            ("exception rate", self.exception_rate),
            ("confidence", self.confidence),
            ("outcome correlation", self.outcome_correlation),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError(f"{name} must be within [0, 1]")
        if not self.source_event_refs or len(set(self.source_event_refs)) != len(
            self.source_event_refs
        ):
            raise ContractError("norm candidate requires unique source event refs")
        if len(set(self.exception_event_refs)) != len(self.exception_event_refs):
            raise ContractError("norm exception event refs must be unique")

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "pattern_key": self.pattern_key,
            "detection_id": self.detection_id,
            "scope": self.scope,
            "scope_ref": self.scope_ref,
            "population_refs": list(self.population_refs),
            "source_event_refs": list(self.source_event_refs),
            "exception_event_refs": list(self.exception_event_refs),
            "occurrence_count": self.occurrence_count,
            "observed_window_count": self.observed_window_count,
            "support_ratio": self.support_ratio,
            "exception_rate": self.exception_rate,
            "confidence": self.confidence,
            "sanction_count": self.sanction_count,
            "reward_count": self.reward_count,
            "outcome_correlation": self.outcome_correlation,
            "created_at": self.created_at,
        }


@dataclass(frozen=True, slots=True)
class NormEvaluation:
    """Pure review input; eligibility is not approval or automatic truth."""

    candidate_id: str
    eligible: bool
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ContractError("norm evaluation requires candidate id")

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "eligible": self.eligible,
            "reasons": list(self.reasons),
        }
