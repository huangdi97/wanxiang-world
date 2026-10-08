"""G91G: matched deterministic pressure/no-pressure behavior benchmark."""

from __future__ import annotations

from wanxiang_substrate.reality.benchmark import PressureBehaviorBenchmark
from wanxiang_substrate.reality.pressure import PressureProfile


def _profile() -> PressureProfile:
    return PressureProfile(
        profile_id="profile_market_v1",
        scenario_ref="scenario_market",
        domain_ref="domain_town",
        scarcity=0.8,
        goals=0.7,
        reward=0.6,
        risk=0.5,
        time=0.9,
        norm=0.4,
    )


def test_benchmark_matches_seed_profile_and_horizon() -> None:
    report = PressureBehaviorBenchmark().compare(_profile(), seed=17, horizon_ticks=24)
    assert report.same_seed is True
    assert report.same_profile is True
    assert report.repeatable is True
    assert report.baseline.pressure_enabled is False
    assert report.pressured.pressure_enabled is True
    assert report.baseline.profile_fingerprint == report.pressured.profile_fingerprint
    assert any(value != 0.0 for value in report.metric_deltas.values())


def test_benchmark_is_explicitly_not_a_scientific_claim() -> None:
    benchmark = PressureBehaviorBenchmark()
    first = benchmark.compare(_profile(), seed=3, horizon_ticks=8)
    second = benchmark.compare(_profile(), seed=3, horizon_ticks=8)
    assert first.baseline.trace_hash == second.baseline.trace_hash
    assert first.pressured.trace_hash == second.pressured.trace_hash
    assert first.scientific_claim is False
    assert "engineering" in first.claim_scope
    assert first.validity_envelope
