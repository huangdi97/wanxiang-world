"""Immutable types for the semantic Gold Set protocol."""

from __future__ import annotations

from dataclasses import dataclass

QUALITY_METRICS = (
    "identity_precision",
    "alias_merge_precision",
    "false_merge_rate",
    "duplicate_rate",
    "missing_evidence_rate",
    "event_precision",
    "participant_correctness",
    "temporal_ordering",
    "uncertainty_honesty",
    "relation_place_org_precision",
    "knowledge_boundary_safety",
    "evidence_traceability",
)


@dataclass(frozen=True, slots=True)
class SamplingManifest:
    seed: int
    requested: int
    selected_ids: tuple[str, ...]
    strata: tuple[tuple[str, tuple[str, ...]], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "seed": self.seed,
            "requested": self.requested,
            "selected_ids": list(self.selected_ids),
            "strata": {name: list(ids) for name, ids in self.strata},
        }


@dataclass(frozen=True, slots=True)
class GoldAssertion:
    """One anonymized reviewer assertion for one sampled candidate."""

    candidate_id: str
    kind: str
    accepted: bool
    expected_payload: tuple[tuple[str, str], ...] = ()
    expected_source_refs: tuple[str, ...] = ()
    expected_uncertain: bool | None = None
    expected_order: int | None = None
    expected_merge_target: str = ""
    boundary_safe: bool = True

    @property
    def expected(self) -> dict[str, str]:
        return dict(self.expected_payload)


@dataclass(frozen=True, slots=True)
class GoldSet:
    protocol_version: str
    assertions: tuple[GoldAssertion, ...]
    sampling: SamplingManifest


@dataclass(frozen=True, slots=True)
class MetricResult:
    name: str
    numerator: int
    denominator: int
    value: float
    direction: str = "higher_is_better"

    def to_dict(self) -> dict[str, object]:
        return {
            "numerator": self.numerator,
            "denominator": self.denominator,
            "value": self.value,
            "direction": self.direction,
        }


@dataclass(frozen=True, slots=True)
class SemanticQualityReport:
    protocol_version: str
    sample_count: int
    labeled_count: int
    metrics: tuple[MetricResult, ...]
    passed: bool
    failures: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "protocol_version": self.protocol_version,
            "sample_count": self.sample_count,
            "labeled_count": self.labeled_count,
            "metrics": {item.name: item.to_dict() for item in self.metrics},
            "passed": self.passed,
            "failures": list(self.failures),
        }


__all__ = [
    "GoldAssertion",
    "GoldSet",
    "MetricResult",
    "QUALITY_METRICS",
    "SamplingManifest",
    "SemanticQualityReport",
]
