"""Versioned trajectory measurements and comparison evidence (G95F)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.registry_support import integer, parameters, ref, sequence

COMPARISON_SCHEMA_VERSION = 1
MetricCategory = Literal["actor", "relation", "institution", "macro", "cost"]
METRIC_CATEGORIES: tuple[MetricCategory, ...] = (
    "actor",
    "relation",
    "institution",
    "macro",
    "cost",
)
_CATEGORY_SET = frozenset(METRIC_CATEGORIES)


def _number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ContractError(f"{name} must be a finite number")
    return float(value)


def _category(value: object) -> MetricCategory:
    if not isinstance(value, str) or value not in _CATEGORY_SET:
        raise ContractError(f"unsupported metric category {value!r}")
    return value


@dataclass(frozen=True, slots=True)
class TrajectoryPoint:
    """One measurable point in an actor/relation/institution/macro/cost series."""

    category: MetricCategory
    name: str
    tick: int
    value: float

    def __post_init__(self) -> None:
        _category(self.category)
        ref(self.name, "metric name")
        integer(self.tick, "metric tick")
        _number(self.value, "metric value")

    @property
    def key(self) -> tuple[str, str, int]:
        return (self.category, self.name, self.tick)

    def to_dict(self) -> dict[str, object]:
        return {
            "category": self.category,
            "name": self.name,
            "tick": self.tick,
            "value": self.value,
        }


@dataclass(frozen=True, slots=True)
class WorldlineMeasurement:
    """Sanitized measurements linked to one existing world-run artifact."""

    worldline_id: str
    worldline_ref: str
    artifact_ref: str
    alignment_ref: str
    points: tuple[TrajectoryPoint, ...]
    seed: int = 0
    parameters: tuple[tuple[str, object], ...] = ()
    schema_version: int = COMPARISON_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in ("worldline_id", "worldline_ref", "artifact_ref", "alignment_ref"):
            ref(getattr(self, name), name)
        integer(self.seed, "seed")
        if self.schema_version != COMPARISON_SCHEMA_VERSION:
            raise ContractError("unsupported worldline measurement schema")
        if not self.points:
            raise ContractError("worldline measurement requires trajectory points")
        keys = tuple(point.key for point in self.points)
        if len(keys) != len(set(keys)):
            raise ContractError("worldline measurement points must be unique")
        object.__setattr__(self, "points", tuple(sorted(self.points, key=lambda p: p.key)))
        object.__setattr__(self, "parameters", parameters(self.parameters, "parameters"))

    @property
    def metric_keys(self) -> frozenset[tuple[str, str, int]]:
        return frozenset(point.key for point in self.points)

    @property
    def categories(self) -> frozenset[MetricCategory]:
        return frozenset(point.category for point in self.points)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "worldline_id": self.worldline_id,
            "worldline_ref": self.worldline_ref,
            "artifact_ref": self.artifact_ref,
            "alignment_ref": self.alignment_ref,
            "seed": self.seed,
            "parameters": [list(item) for item in self.parameters],
            "points": [point.to_dict() for point in sorted(self.points, key=lambda p: p.key)],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> WorldlineMeasurement:
        return cls(
            worldline_id=ref(data.get("worldline_id"), "worldline_id"),
            worldline_ref=ref(data.get("worldline_ref"), "worldline_ref"),
            artifact_ref=ref(data.get("artifact_ref"), "artifact_ref"),
            alignment_ref=ref(data.get("alignment_ref"), "alignment_ref"),
            points=parse_points(sequence(data.get("points", ()), "points")),
            seed=integer(data.get("seed", 0), "seed"),
            parameters=parameters(sequence(data.get("parameters", ()), "parameters"), "parameters"),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class MetricDifference:
    """One complete aligned metric delta against the selected baseline."""

    worldline_id: str
    category: MetricCategory
    name: str
    tick: int
    baseline: float
    current: float

    def __post_init__(self) -> None:
        ref(self.worldline_id, "worldline_id")
        _category(self.category)
        ref(self.name, "metric name")
        integer(self.tick, "metric tick")
        _number(self.baseline, "baseline metric")
        _number(self.current, "current metric")

    @property
    def delta(self) -> float:
        return self.current - self.baseline

    @property
    def absolute_delta(self) -> float:
        return abs(self.delta)

    def to_dict(self) -> dict[str, object]:
        return {
            "worldline_id": self.worldline_id,
            "category": self.category,
            "name": self.name,
            "tick": self.tick,
            "baseline": self.baseline,
            "current": self.current,
            "delta": self.delta,
            "absolute_delta": self.absolute_delta,
        }


@dataclass(frozen=True, slots=True)
class CategoryComparison:
    """All aligned differences summarized without selecting one metric."""

    category: MetricCategory
    metric_count: int
    mean_absolute_delta: float
    maximum_absolute_delta: float

    def __post_init__(self) -> None:
        _category(self.category)
        integer(self.metric_count, "metric count")
        _number(self.mean_absolute_delta, "mean absolute delta")
        _number(self.maximum_absolute_delta, "maximum absolute delta")
        if self.metric_count == 0 and (self.mean_absolute_delta or self.maximum_absolute_delta):
            raise ContractError("empty category summary cannot have a delta")

    def to_dict(self) -> dict[str, object]:
        return {
            "category": self.category,
            "metric_count": self.metric_count,
            "mean_absolute_delta": self.mean_absolute_delta,
            "maximum_absolute_delta": self.maximum_absolute_delta,
        }


@dataclass(frozen=True, slots=True)
class LabWorldlineComparison:
    """Read-only comparison report; it never represents canonical world state."""

    alignment_ref: str
    baseline_worldline_id: str
    worldline_ids: tuple[str, ...]
    aligned: bool
    qualified: bool
    missing_metrics: tuple[str, ...]
    extra_metrics: tuple[str, ...]
    differences: tuple[MetricDifference, ...]
    categories: tuple[CategoryComparison, ...]
    schema_version: int = COMPARISON_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.alignment_ref, "alignment_ref")
        ref(self.baseline_worldline_id, "baseline_worldline_id")
        if len(self.worldline_ids) < 2 or len(set(self.worldline_ids)) != len(self.worldline_ids):
            raise ContractError("comparison requires unique baseline and candidate worldlines")
        if self.baseline_worldline_id not in self.worldline_ids:
            raise ContractError("comparison baseline is not in worldline ids")
        if self.schema_version != COMPARISON_SCHEMA_VERSION:
            raise ContractError("unsupported worldline comparison schema")
        if not self.aligned and self.qualified:
            raise ContractError("unaligned comparison cannot be qualified")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "alignment_ref": self.alignment_ref,
            "baseline_worldline_id": self.baseline_worldline_id,
            "worldline_ids": list(self.worldline_ids),
            "aligned": self.aligned,
            "qualified": self.qualified,
            "missing_metrics": list(self.missing_metrics),
            "extra_metrics": list(self.extra_metrics),
            "differences": [item.to_dict() for item in self.differences],
            "categories": [item.to_dict() for item in self.categories],
        }


def parse_point(data: Mapping[str, object]) -> TrajectoryPoint:
    """Parse one compatibility payload without accepting raw source content."""
    return TrajectoryPoint(
        category=_category(data.get("category")),
        name=ref(data.get("name"), "metric name"),
        tick=integer(data.get("tick"), "metric tick"),
        value=_number(data.get("value"), "metric value"),
    )


def parse_points(values: Sequence[object]) -> tuple[TrajectoryPoint, ...]:
    points: list[TrajectoryPoint] = []
    for value in values:
        if not isinstance(value, Mapping):
            raise ContractError("trajectory point must be a mapping")
        points.append(parse_point(cast(Mapping[str, object], value)))
    return tuple(points)


__all__ = [
    "COMPARISON_SCHEMA_VERSION",
    "CategoryComparison",
    "MetricCategory",
    "MetricDifference",
    "METRIC_CATEGORIES",
    "TrajectoryPoint",
    "LabWorldlineComparison",
    "WorldlineMeasurement",
    "parse_point",
    "parse_points",
]
