"""Typed pattern observation values and aggregate statistics (G94A)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

PatternKind = Literal["behavior", "relationship", "exchange", "organization"]


def _require_range(window_start: int, window_end: int) -> None:
    if isinstance(window_start, bool) or isinstance(window_end, bool):
        raise ContractError("pattern windows require integer ticks")
    if window_start < 0 or window_end <= window_start:
        raise ContractError("pattern window must be non-negative and non-empty")


@dataclass(frozen=True, slots=True)
class PatternObservation:
    """One typed signal derived from one committed operation."""

    observation_id: str
    kind: PatternKind
    key: str
    subject_refs: tuple[str, ...]
    observed_at: int
    window_start: int
    window_end: int
    event_refs: tuple[str, ...]
    features: tuple[tuple[str, float], ...]

    def __post_init__(self) -> None:
        if not self.observation_id.strip() or not self.key.strip():
            raise ContractError("pattern observation requires id and key")
        if self.kind not in ("behavior", "relationship", "exchange", "organization"):
            raise ContractError(f"unknown pattern kind {self.kind!r}")
        if self.observed_at < 0:
            raise ContractError("pattern observation tick cannot be negative")
        _require_range(self.window_start, self.window_end)
        if not self.window_start <= self.observed_at < self.window_end:
            raise ContractError("observation tick must be inside its window")
        if not self.event_refs or len(set(self.event_refs)) != len(self.event_refs):
            raise ContractError("pattern observation requires unique event refs")
        if any(not ref.strip() for ref in self.event_refs):
            raise ContractError("pattern observation event refs cannot be blank")
        if not self.subject_refs or len(set(self.subject_refs)) != len(self.subject_refs):
            raise ContractError("pattern observation requires unique subject refs")
        if any(not ref.strip() for ref in self.subject_refs):
            raise ContractError("pattern observation subject refs cannot be blank")
        feature_names = [name for name, _ in self.features]
        if len(feature_names) != len(set(feature_names)) or any(
            not name.strip() or not math.isfinite(value) for name, value in self.features
        ):
            raise ContractError("pattern observation features must be unique and finite")

    @property
    def occurrence_count(self) -> int:
        return len(self.event_refs)

    def to_dict(self) -> dict[str, object]:
        return {
            "observation_id": self.observation_id,
            "kind": self.kind,
            "key": self.key,
            "subject_refs": list(self.subject_refs),
            "observed_at": self.observed_at,
            "window_start": self.window_start,
            "window_end": self.window_end,
            "event_refs": list(self.event_refs),
            "features": [[name, value] for name, value in self.features],
        }


@dataclass(frozen=True, slots=True)
class PatternStatistics:
    """Aggregate statistics over a filtered observation window."""

    window_start: int
    window_end: int
    observation_count: int
    total_occurrences: int
    unique_event_count: int
    unique_key_count: int
    unique_subject_count: int
    mean_subject_count: float
    span_ticks: int
    by_kind: tuple[tuple[str, int], ...]
    feature_means: tuple[tuple[str, float], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "window_start": self.window_start,
            "window_end": self.window_end,
            "observation_count": self.observation_count,
            "total_occurrences": self.total_occurrences,
            "unique_event_count": self.unique_event_count,
            "unique_key_count": self.unique_key_count,
            "unique_subject_count": self.unique_subject_count,
            "mean_subject_count": self.mean_subject_count,
            "span_ticks": self.span_ticks,
            "by_kind": [list(item) for item in self.by_kind],
            "feature_means": [list(item) for item in self.feature_means],
        }
