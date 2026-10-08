"""Deterministic pressure behavior comparison (M88 / G91G)."""

from __future__ import annotations

import random
from collections.abc import Mapping
from dataclasses import dataclass

from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.reality.errors import ExperimentError
from wanxiang_substrate.reality.pressure import PRESSURE_DIMENSIONS, PressureProfile


@dataclass(frozen=True, slots=True)
class BehaviorTrace:
    """One deterministic engineering trace, not a scientific observation."""

    run_id: str
    seed: int
    profile_id: str
    profile_fingerprint: str
    pressure_enabled: bool
    actions: tuple[str, ...]
    metrics: Mapping[str, float]
    trace_hash: str


@dataclass(frozen=True, slots=True)
class PressureBenchmarkReport:
    """Matched pressure/no-pressure output with an explicit validity boundary."""

    benchmark_id: str
    seed: int
    profile_id: str
    profile_fingerprint: str
    horizon_ticks: int
    baseline: BehaviorTrace
    pressured: BehaviorTrace
    metric_deltas: Mapping[str, float]
    same_seed: bool
    same_profile: bool
    repeatable: bool
    claim_scope: str = "deterministic engineering reference benchmark only"
    scientific_claim: bool = False
    validity_envelope: tuple[str, ...] = (
        "synthetic deterministic rule set",
        "matched seed and horizon",
        "profile dimensions are configuration inputs",
    )


class PressureBehaviorBenchmark:
    """Compare two deterministic worldline traces without model training."""

    def run(
        self,
        profile: PressureProfile,
        *,
        seed: int,
        horizon_ticks: int,
        pressure_enabled: bool,
    ) -> BehaviorTrace:
        if seed < 0 or horizon_ticks < 1:
            raise ExperimentError("benchmark seed must be non-negative and horizon positive")
        dimensions = (
            profile.dimensions() if pressure_enabled else dict.fromkeys(PRESSURE_DIMENSIONS, 0.0)
        )
        rng = random.Random(seed)
        actions: list[str] = []
        totals = {
            "action_count": 0.0,
            "risk_acceptance": 0.0,
            "opportunity_acceptance": 0.0,
            "resource_hoarding": 0.0,
            "norm_adherence": 0.0,
        }
        for _tick in range(horizon_ticks):
            urgency = (dimensions["scarcity"] + dimensions["goals"] + dimensions["time"]) / 3.0
            risk_signal = rng.random()
            act = risk_signal < 0.25 + urgency * 0.5
            if act:
                actions.append("act")
                totals["action_count"] += 1.0
                totals["risk_acceptance"] += risk_signal * dimensions["risk"]
                totals["opportunity_acceptance"] += dimensions["reward"] * (1.0 - risk_signal)
            else:
                actions.append("wait")
                totals["resource_hoarding"] += dimensions["scarcity"] * (1.0 - risk_signal)
            totals["norm_adherence"] += dimensions["norm"] * (1.0 if risk_signal < 0.8 else 0.5)
        metrics = {name: round(value / horizon_ticks, 12) for name, value in totals.items()}
        payload = {
            "seed": seed,
            "profile_id": profile.profile_id,
            "profile_fingerprint": profile.fingerprint(),
            "pressure_enabled": pressure_enabled,
            "actions": actions,
            "metrics": metrics,
        }
        return BehaviorTrace(
            run_id=f"pressure:{profile.profile_id}:{seed}:{pressure_enabled}",
            seed=seed,
            profile_id=profile.profile_id,
            profile_fingerprint=profile.fingerprint(),
            pressure_enabled=pressure_enabled,
            actions=tuple(actions),
            metrics=metrics,
            trace_hash=semantic_sha256(payload),
        )

    def compare(
        self,
        profile: PressureProfile,
        *,
        seed: int,
        horizon_ticks: int,
        benchmark_id: str = "pressure_behavior",
    ) -> PressureBenchmarkReport:
        baseline = self.run(
            profile,
            seed=seed,
            horizon_ticks=horizon_ticks,
            pressure_enabled=False,
        )
        pressured = self.run(
            profile,
            seed=seed,
            horizon_ticks=horizon_ticks,
            pressure_enabled=True,
        )
        repeat_baseline = self.run(
            profile,
            seed=seed,
            horizon_ticks=horizon_ticks,
            pressure_enabled=False,
        )
        repeat_pressured = self.run(
            profile,
            seed=seed,
            horizon_ticks=horizon_ticks,
            pressure_enabled=True,
        )
        names = tuple(sorted(pressured.metrics))
        deltas = {
            name: round(pressured.metrics[name] - baseline.metrics[name], 12) for name in names
        }
        return PressureBenchmarkReport(
            benchmark_id=benchmark_id,
            seed=seed,
            profile_id=profile.profile_id,
            profile_fingerprint=profile.fingerprint(),
            horizon_ticks=horizon_ticks,
            baseline=baseline,
            pressured=pressured,
            metric_deltas=deltas,
            same_seed=baseline.seed == pressured.seed,
            same_profile=baseline.profile_fingerprint == pressured.profile_fingerprint,
            repeatable=(
                baseline.trace_hash == repeat_baseline.trace_hash
                and pressured.trace_hash == repeat_pressured.trace_hash
            ),
        )
