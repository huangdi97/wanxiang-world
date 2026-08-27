"""G95F: aligned all-plane worldline comparison and API-safe reporting."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.world_lab import (
    METRIC_CATEGORIES,
    TrajectoryPoint,
    WorldlineComparator,
    WorldlineMeasurement,
)


def _measurement(
    worldline_id: str,
    *,
    alignment_ref: str = "input:g95f:shared",
    offset: float = 0.0,
    drop_cost: bool = False,
) -> WorldlineMeasurement:
    points = tuple(
        TrajectoryPoint(category, f"{category}.outcome", 30, index + offset)
        for index, category in enumerate(METRIC_CATEGORIES, start=1)
        if not (drop_cost and category == "cost")
    )
    return WorldlineMeasurement(
        worldline_id=worldline_id,
        worldline_ref=f"worldline:g95f:{worldline_id}",
        artifact_ref=f"artifact:g95f:{worldline_id}",
        alignment_ref=alignment_ref,
        points=points,
        seed=7,
        parameters=(("pressure", "medium"),),
    )


def test_comparator_aligns_all_categories_and_reports_every_difference() -> None:
    baseline = _measurement("baseline")
    candidate = _measurement("candidate", offset=2.0)
    comparator = WorldlineComparator()

    comparison = comparator.compare((baseline, candidate))
    report = comparator.api_report(comparison, (baseline, candidate))

    assert comparison.aligned is True
    assert comparison.qualified is True
    assert len(comparison.differences) == len(METRIC_CATEGORIES)
    assert {item.category for item in comparison.differences} == set(METRIC_CATEGORIES)
    assert {item.category for item in comparison.categories} == set(METRIC_CATEGORIES)
    assert all(item.metric_count == 1 for item in comparison.categories)
    series = report["series"]
    assert isinstance(series, list)
    assert len(cast(list[object], series)) == 2
    assert report["qualified"] is True
    assert "source_text" not in repr(report)


def test_missing_metric_is_reported_and_cannot_be_qualified() -> None:
    baseline = _measurement("baseline")
    candidate = _measurement("candidate", offset=1.0, drop_cost=True)

    comparison = WorldlineComparator().compare((baseline, candidate))

    assert comparison.aligned is False
    assert comparison.qualified is False
    assert any("cost:cost.outcome:30" in item for item in comparison.missing_metrics)
    assert comparison.extra_metrics == ()


def test_measurement_round_trip_and_alignment_mismatch_are_typed() -> None:
    baseline = _measurement("baseline")
    assert WorldlineMeasurement.from_dict(baseline.to_dict()) == baseline

    with pytest.raises(ContractError, match="alignment"):
        WorldlineComparator().compare(
            (baseline, _measurement("other", alignment_ref="input:g95f:other"))
        )


def test_comparison_requires_at_least_two_worldlines() -> None:
    with pytest.raises(ContractError, match="at least two"):
        WorldlineComparator().compare((_measurement("baseline"),))
