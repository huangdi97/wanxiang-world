"""Aggregate, missing-aware M97 ExperienceQuality baseline distributions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from math import isfinite
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.quality.experience_models import (
    EXPERIENCE_QUALITY_SCHEMA,
    QUALITY_DIMENSIONS,
    ExperienceQualityRun,
    ScientificValidity,
)

AggregateHumanStatus = Literal["missing", "partial", "provided"]


def _refs(values: Sequence[object], name: str) -> tuple[str, ...]:
    result = tuple(str(value) for value in values)
    if (
        not result
        or len(set(result)) != len(result)
        or any(not value.strip() or any(char.isspace() for char in value) for value in result)
    ):
        raise ContractError(f"{name} must contain unique opaque refs")
    return tuple(sorted(result))


@dataclass(frozen=True, slots=True)
class QualityDistribution:
    """One dimension's values plus explicit missing/not-applicable counts."""

    dimension: str
    values: tuple[float, ...]
    measured_count: int
    missing_count: int
    not_applicable_count: int
    method_counts: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if self.dimension not in QUALITY_DIMENSIONS:
            raise ContractError(f"unknown quality dimension {self.dimension!r}")
        if self.measured_count != len(self.values) or self.measured_count < 0:
            raise ContractError("quality distribution measured count does not match values")
        if self.missing_count < 0 or self.not_applicable_count < 0:
            raise ContractError("quality distribution counts cannot be negative")
        if any(not isfinite(value) or not 0.0 <= value <= 1.0 for value in self.values):
            raise ContractError("quality distribution values must be within [0,1]")
        if any(count < 0 for _method, count in self.method_counts):
            raise ContractError("quality method counts cannot be negative")

    @property
    def mean(self) -> float | None:
        return sum(self.values) / len(self.values) if self.values else None

    def to_dict(self) -> dict[str, object]:
        return {
            "values": list(self.values),
            "measured_count": self.measured_count,
            "missing_count": self.missing_count,
            "not_applicable_count": self.not_applicable_count,
            "method_counts": dict(self.method_counts),
            "mean": self.mean,
            "min": min(self.values) if self.values else None,
            "max": max(self.values) if self.values else None,
        }


@dataclass(frozen=True, slots=True)
class ExperienceQualityAggregate:
    """A versioned aggregate that never replaces per-run evidence."""

    aggregate_id: str
    run_refs: tuple[str, ...]
    world_families: tuple[str, ...]
    distributions: tuple[QualityDistribution, ...]
    human_status: AggregateHumanStatus
    baseline_scope: str = "bounded_engineering_baseline_no_universal_threshold"
    worldness_separate: bool = True
    scientific_validity: ScientificValidity = "not_assessed"
    schema: str = EXPERIENCE_QUALITY_SCHEMA
    sanitized: bool = True
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.aggregate_id.strip() or any(char.isspace() for char in self.aggregate_id):
            raise ContractError("aggregate_id must be an opaque reference")
        object.__setattr__(self, "run_refs", _refs(self.run_refs, "run_refs"))
        object.__setattr__(self, "world_families", _refs(self.world_families, "world_families"))
        if set(self.world_families) - {"source", "prompt"}:
            raise ContractError("aggregate contains an unsupported world family")
        names = tuple(item.dimension for item in self.distributions)
        if set(names) != set(QUALITY_DIMENSIONS) or len(names) != len(QUALITY_DIMENSIONS):
            raise ContractError("aggregate must cover every required dimension once")
        if self.human_status not in {"missing", "partial", "provided"}:
            raise ContractError("invalid aggregate human status")
        if not self.baseline_scope or not self.worldness_separate:
            raise ContractError("aggregate must keep Worldness separate")
        if self.scientific_validity not in {"not_assessed", "external_review_required"}:
            raise ContractError("invalid scientific validity status")
        if not self.sanitized:
            raise ContractError("ExperienceQualityAggregate must be sanitized")
        if self.content_hash and (
            len(self.content_hash) != 64
            or any(char not in "0123456789abcdef" for char in self.content_hash)
        ):
            raise ContractError("aggregate content_hash must be lowercase SHA-256")

    def canonical_payload(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "aggregate_id": self.aggregate_id,
            "run_refs": list(self.run_refs),
            "world_families": list(self.world_families),
            "distributions": {item.dimension: item.to_dict() for item in self.distributions},
            "human_status": self.human_status,
            "baseline_scope": self.baseline_scope,
            "worldness_separate": self.worldness_separate,
            "scientific_validity": self.scientific_validity,
            "sanitized": self.sanitized,
        }

    def compute_hash(self) -> str:
        return semantic_sha256(self.canonical_payload())

    def with_hash(self) -> ExperienceQualityAggregate:
        return replace(self, content_hash=self.compute_hash())

    def verify_hash(self) -> bool:
        return bool(self.content_hash) and self.content_hash == self.compute_hash()

    def to_dict(self) -> dict[str, object]:
        payload = self.canonical_payload()
        payload["content_hash"] = self.content_hash
        return payload


def aggregate_quality_runs(
    aggregate_id: str, runs: tuple[ExperienceQualityRun, ...]
) -> ExperienceQualityAggregate:
    """Build distributions while retaining each run as an independent input."""
    if not runs:
        raise ContractError("cannot aggregate an empty ExperienceQuality run set")
    if len({run.run_id for run in runs}) != len(runs):
        raise ContractError("aggregate run references must be unique")
    distributions: list[QualityDistribution] = []
    for dimension in QUALITY_DIMENSIONS:
        measurements = [
            measurement
            for run in runs
            for item in run.dimensions
            if item.name == dimension
            for measurement in item.measurements
        ]
        values = tuple(
            measurement.value
            for measurement in measurements
            if measurement.status == "measured" and measurement.value is not None
        )
        method_counts: dict[str, int] = {}
        for measurement in measurements:
            method_counts[measurement.method] = method_counts.get(measurement.method, 0) + 1
        distributions.append(
            QualityDistribution(
                dimension,
                values,
                len(values),
                sum(measurement.status == "missing" for measurement in measurements),
                sum(measurement.status == "not_applicable" for measurement in measurements),
                tuple(sorted(method_counts.items())),
            )
        )
    human_status: AggregateHumanStatus
    if all(run.human_status == "missing" for run in runs):
        human_status = "missing"
    elif all(run.human_status == "provided" for run in runs):
        human_status = "provided"
    else:
        human_status = "partial"
    return ExperienceQualityAggregate(
        aggregate_id=aggregate_id,
        run_refs=tuple(run.run_id for run in runs),
        world_families=tuple(sorted({run.world_family for run in runs})),
        distributions=tuple(distributions),
        human_status=human_status,
    ).with_hash()


__all__ = [
    "ExperienceQualityAggregate",
    "QualityDistribution",
    "aggregate_quality_runs",
]
