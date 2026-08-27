"""Alignment and all-metric worldline comparison (G95F)."""

from __future__ import annotations

from collections.abc import Sequence

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.comparison_models import (
    METRIC_CATEGORIES,
    CategoryComparison,
    LabWorldlineComparison,
    MetricCategory,
    MetricDifference,
    WorldlineMeasurement,
)


class WorldlineComparator:
    """Compare existing world-run measurements without any mutation path."""

    def compare(
        self,
        measurements: Sequence[WorldlineMeasurement],
        *,
        baseline_worldline_id: str | None = None,
    ) -> LabWorldlineComparison:
        runs = tuple(measurements)
        if len(runs) < 2:
            raise ContractError("worldline comparison requires at least two runs")
        if len({run.worldline_id for run in runs}) != len(runs):
            raise ContractError("worldline comparison requires unique run ids")
        alignment_refs = {run.alignment_ref for run in runs}
        if len(alignment_refs) != 1:
            raise ContractError("worldline runs do not share an alignment reference")
        baseline_id = baseline_worldline_id or runs[0].worldline_id
        baseline = next((run for run in runs if run.worldline_id == baseline_id), None)
        if baseline is None:
            raise ContractError("comparison baseline run is missing")
        missing: set[str] = set()
        extra: set[str] = set()
        for run in runs:
            if run.worldline_id == baseline.worldline_id:
                continue
            missing.update(_metric_labels(baseline.metric_keys - run.metric_keys, run.worldline_id))
            extra.update(_metric_labels(run.metric_keys - baseline.metric_keys, run.worldline_id))
        aligned = not missing and not extra
        differences = self._differences(baseline, runs)
        categories = _summaries(differences)
        required_categories = set(METRIC_CATEGORIES)
        complete_categories = all(required_categories.issubset(run.categories) for run in runs)
        qualified = aligned and complete_categories and bool(differences)
        return LabWorldlineComparison(
            alignment_ref=baseline.alignment_ref,
            baseline_worldline_id=baseline.worldline_id,
            worldline_ids=tuple(run.worldline_id for run in runs),
            aligned=aligned,
            qualified=qualified,
            missing_metrics=tuple(sorted(missing)),
            extra_metrics=tuple(sorted(extra)),
            differences=differences,
            categories=categories,
        )

    def api_report(
        self,
        comparison: LabWorldlineComparison,
        measurements: Sequence[WorldlineMeasurement],
    ) -> dict[str, object]:
        """Return a chart/API-safe report containing refs and numeric series only."""
        known = {item.worldline_id: item for item in measurements}
        if set(comparison.worldline_ids) != set(known):
            raise ContractError("API report measurements do not match comparison")
        return {
            "schema_version": comparison.schema_version,
            "alignment_ref": comparison.alignment_ref,
            "baseline_worldline_id": comparison.baseline_worldline_id,
            "aligned": comparison.aligned,
            "qualified": comparison.qualified,
            "series": [
                {
                    "worldline_id": worldline_id,
                    "worldline_ref": known[worldline_id].worldline_ref,
                    "artifact_ref": known[worldline_id].artifact_ref,
                    "points": [
                        point.to_dict()
                        for point in sorted(known[worldline_id].points, key=lambda item: item.key)
                    ],
                }
                for worldline_id in comparison.worldline_ids
            ],
            "differences": [item.to_dict() for item in comparison.differences],
            "categories": [item.to_dict() for item in comparison.categories],
            "missing_metrics": list(comparison.missing_metrics),
            "extra_metrics": list(comparison.extra_metrics),
        }

    @staticmethod
    def _differences(
        baseline: WorldlineMeasurement,
        runs: tuple[WorldlineMeasurement, ...],
    ) -> tuple[MetricDifference, ...]:
        baseline_values = {point.key: point.value for point in baseline.points}
        differences: list[MetricDifference] = []
        for run in runs:
            if run.worldline_id == baseline.worldline_id:
                continue
            for point in run.points:
                if point.key not in baseline_values:
                    continue
                differences.append(
                    MetricDifference(
                        worldline_id=run.worldline_id,
                        category=point.category,
                        name=point.name,
                        tick=point.tick,
                        baseline=baseline_values[point.key],
                        current=point.value,
                    )
                )
        return tuple(
            sorted(
                differences,
                key=lambda item: (
                    item.worldline_id,
                    item.category,
                    item.name,
                    item.tick,
                ),
            )
        )


def _metric_labels(
    keys: set[tuple[str, str, int]] | frozenset[tuple[str, str, int]], worldline_id: str
) -> tuple[str, ...]:
    return tuple(f"{worldline_id}:{category}:{name}:{tick}" for category, name, tick in keys)


def _summaries(differences: tuple[MetricDifference, ...]) -> tuple[CategoryComparison, ...]:
    by_category: dict[MetricCategory, list[float]] = {
        category: [] for category in METRIC_CATEGORIES
    }
    for difference in differences:
        by_category[difference.category].append(difference.absolute_delta)
    return tuple(
        CategoryComparison(
            category=category,
            metric_count=len(values),
            mean_absolute_delta=sum(values) / len(values) if values else 0.0,
            maximum_absolute_delta=max(values) if values else 0.0,
        )
        for category, values in by_category.items()
    )


__all__ = ["WorldlineComparator"]
