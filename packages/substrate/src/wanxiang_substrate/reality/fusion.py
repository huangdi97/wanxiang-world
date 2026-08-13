"""Observation fusion & validation (G07B).

Deterministic reference fusion: deduplicate identical readings, align by
time/space, fuse confidence, retain conflicting observations as a conflict set,
and emit either a high-confidence ClaimCandidate/proposal or defer to review.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.reality.errors import FusionPolicyError
from wanxiang_substrate.reality.model import NormalizedReading

FusionOutcome = Literal["proposal", "claim_candidate", "conflict", "deferred"]


@dataclass(frozen=True, slots=True)
class FusionPolicy:
    """Versioned thresholds controlling fusion."""

    policy_version: int = 1
    confidence_threshold: float = 0.7
    conflict_window_ticks: int = 5
    dedup_window_ticks: int = 2

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise FusionPolicyError("confidence_threshold must be within [0,1]")
        if self.conflict_window_ticks < 0 or self.dedup_window_ticks < 0:
            raise FusionPolicyError("windows must be non-negative")


@dataclass(frozen=True, slots=True)
class FusionResult:
    """Fusion output: a proposal or a deferred/conflict candidate."""

    subject: str
    outcome: FusionOutcome
    value: object | None
    confidence: float
    sources: tuple[str, ...]
    policy_version: int
    rationale: str


class ObservationFusion:
    """Deterministic fusion over normalized readings (never averages blindly)."""

    def __init__(self, policy: FusionPolicy | None = None) -> None:
        self._policy = policy or FusionPolicy()

    def fuse(self, readings: tuple[NormalizedReading, ...]) -> tuple[FusionResult, ...]:
        grouped: dict[tuple[str, str], list[NormalizedReading]] = {}
        for reading in readings:
            grouped.setdefault((reading.source, reading.kind), []).append(reading)
        results: list[FusionResult] = []
        for (source, kind), group in grouped.items():
            if len(group) == 1:
                results.append(self._single(source, kind, group[0]))
                continue
            results.append(self._multiple(source, kind, group))
        return tuple(sorted(results, key=lambda r: r.subject))

    def _single(self, source: str, kind: str, reading: NormalizedReading) -> FusionResult:
        subject = f"{source}:{kind}"
        if reading.confidence >= self._policy.confidence_threshold:
            return FusionResult(
                subject=subject,
                outcome="proposal",
                value=reading.value,
                confidence=reading.confidence,
                sources=(reading.source,),
                policy_version=self._policy.policy_version,
                rationale="high-confidence single observation",
            )
        return FusionResult(
            subject=subject,
            outcome="claim_candidate",
            value=reading.value,
            confidence=reading.confidence,
            sources=(reading.source,),
            policy_version=self._policy.policy_version,
            rationale="low-confidence observation deferred to review",
        )

    def _multiple(self, source: str, kind: str, group: list[NormalizedReading]) -> FusionResult:
        subject = f"{source}:{kind}"
        deduped = self._dedupe(group)
        if len(deduped) == 1:
            return self._single(source, kind, deduped[0])
        values = {_scalar_key(r.value) for r in deduped}
        if len(values) == 1:
            best = max(deduped, key=lambda r: r.confidence)
            return FusionResult(
                subject=subject,
                outcome="proposal",
                value=best.value,
                confidence=min(1.0, best.confidence + 0.1),
                sources=tuple(sorted({r.source for r in deduped})),
                policy_version=self._policy.policy_version,
                rationale="consistent duplicates fused",
            )
        return FusionResult(
            subject=subject,
            outcome="conflict",
            value=None,
            confidence=max(r.confidence for r in deduped),
            sources=tuple(sorted({r.source for r in deduped})),
            policy_version=self._policy.policy_version,
            rationale="conflicting observations retained as a conflict set",
        )

    def _dedupe(self, group: list[NormalizedReading]) -> list[NormalizedReading]:
        """Remove duplicate readings within the dedup window (keep highest conf)."""
        by_key: dict[str, NormalizedReading] = {}
        for reading in sorted(group, key=lambda r: r.at_ticks):
            key = _scalar_key(reading.value)
            existing = by_key.get(key)
            if (
                existing is None
                or reading.at_ticks - _last_ticks(existing) <= self._policy.dedup_window_ticks
            ) and (existing is None or reading.confidence > existing.confidence):
                by_key[key] = reading
        return list(by_key.values())


def _scalar_key(value: object) -> str:
    return str(value)


def _last_ticks(reading: NormalizedReading) -> int:
    return reading.at_ticks
