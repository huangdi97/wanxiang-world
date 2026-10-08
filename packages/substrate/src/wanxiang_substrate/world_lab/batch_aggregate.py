"""Deterministic batch metric aggregation models (G95D)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.batch_models import (
    BATCH_SCHEMA_VERSION,
    BatchCheckpoint,
    BatchPlan,
    BatchRunResult,
    count,
    names,
    ref,
)


@dataclass(frozen=True, slots=True)
class MetricSummary:
    """Deterministic descriptive summary across completed worldlines."""

    name: str
    count: int
    mean: float
    minimum: float
    maximum: float

    def __post_init__(self) -> None:
        ref(self.name, "metric name")
        count(self.count, "metric count", minimum=1)
        if any(not isfinite(value) for value in (self.mean, self.minimum, self.maximum)):
            raise ContractError("metric summary values must be finite")
        if self.minimum > self.maximum or not self.minimum <= self.mean <= self.maximum:
            raise ContractError("metric summary ordering is invalid")

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "count": self.count,
            "mean": self.mean,
            "minimum": self.minimum,
            "maximum": self.maximum,
        }


@dataclass(frozen=True, slots=True)
class BatchAggregate:
    """Aggregate over all result rows, never a cherry-picked metric."""

    batch_id: str
    total_runs: int
    completed_runs: int
    failed_runs: int
    metrics: tuple[MetricSummary, ...] = ()
    deterministic: bool = True

    def __post_init__(self) -> None:
        ref(self.batch_id, "batch_id")
        count(self.total_runs, "total_runs", minimum=1)
        count(self.completed_runs, "completed_runs")
        count(self.failed_runs, "failed_runs")
        if self.completed_runs + self.failed_runs != self.total_runs:
            raise ContractError("batch aggregate run counts do not balance")
        names(tuple(item.name for item in self.metrics), "aggregate metric names")
        if type(self.deterministic) is not bool:
            raise ContractError("deterministic must be boolean")

    def metric(self, name: str) -> MetricSummary | None:
        return next((item for item in self.metrics if item.name == name), None)

    def to_dict(self) -> dict[str, object]:
        return {
            "batch_id": self.batch_id,
            "total_runs": self.total_runs,
            "completed_runs": self.completed_runs,
            "failed_runs": self.failed_runs,
            "metrics": [item.to_dict() for item in self.metrics],
            "deterministic": self.deterministic,
        }


@dataclass(frozen=True, slots=True)
class BatchExecution:
    """Final materialized batch evidence plus its latest checkpoint."""

    plan: BatchPlan
    results: tuple[BatchRunResult, ...]
    checkpoint: BatchCheckpoint
    aggregate: BatchAggregate

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": BATCH_SCHEMA_VERSION,
            "plan": self.plan.to_dict(),
            "results": [result.to_dict() for result in self.results],
            "checkpoint": self.checkpoint.to_dict(),
            "aggregate": self.aggregate.to_dict(),
        }


def aggregate_results(batch_id: str, results: Sequence[BatchRunResult]) -> BatchAggregate:
    values = tuple(results)
    if not values:
        raise ContractError("cannot aggregate an empty batch")
    completed = tuple(item for item in values if item.status == "completed")
    by_name: dict[str, list[float]] = {}
    for result in completed:
        for name, value in result.metrics:
            by_name.setdefault(name, []).append(value)
    summaries = tuple(
        MetricSummary(
            name=name,
            count=len(points),
            mean=sum(points) / len(points),
            minimum=min(points),
            maximum=max(points),
        )
        for name, points in sorted(by_name.items())
        if points
    )
    return BatchAggregate(
        batch_id=batch_id,
        total_runs=len(values),
        completed_runs=len(completed),
        failed_runs=len(values) - len(completed),
        metrics=summaries,
    )


__all__ = [
    "BatchAggregate",
    "BatchExecution",
    "MetricSummary",
    "aggregate_results",
]
