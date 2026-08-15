"""M40: long-horizon & derived worlds (mechanism; synthetic)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.long_horizon import (
    create_derived_world,
    evaluate_candidates,
    prepare_promotion_candidate,
    run_living_open,
    run_population_benchmark,
    windowed_distill,
)


@pytest.mark.unit
def test_windowed_distill_with_budget() -> None:
    patterns = windowed_distill(
        windows=(("a", "b"), ("a", "c"), ("a", "d")),
        cost_budget=10,
        min_windows=2,
    )
    assert len(patterns) == 1
    assert patterns[0].pattern == "a"
    assert patterns[0].windows_seen == 3
    assert patterns[0].cost_budget_used == 1


@pytest.mark.unit
def test_cost_budget_limits_patterns() -> None:
    patterns = windowed_distill(
        windows=(("a", "b"), ("a", "b"), ("a", "b")),
        cost_budget=1,
        min_windows=2,
    )
    assert len(patterns) == 1


@pytest.mark.unit
def test_candidate_counterfactual_and_approval() -> None:
    patterns = windowed_distill(
        windows=(("habit_x",), ("habit_x",)),
        cost_budget=10,
    )
    candidates = evaluate_candidates(patterns, counterfactual=True)
    assert candidates[0].counterfactual_ok is True
    assert candidates[0].approved is True
    rejected = evaluate_candidates(patterns, counterfactual=False)
    assert rejected[0].approved is False


@pytest.mark.unit
def test_living_open_marks_generated_entities() -> None:
    summary = run_living_open(actors=("c1", "c2"), horizon=12)
    assert summary.generated_entities
    assert all(e.startswith("gen_") for e in summary.generated_entities)
    assert len(summary.character_stages) == 2


@pytest.mark.unit
def test_promotion_candidate_and_derived_world() -> None:
    candidate = prepare_promotion_candidate(genesis_ref="g1")
    assert candidate.frozen is True
    assert candidate.invariants_ok is True
    derived = create_derived_world(parent_definition_id="wd_rc001", candidate=candidate)
    assert derived.derived_definition_id.startswith("wd_derived_")
    assert derived.lineage_edge.startswith("promotion://")
    assert derived.inherited_history_ref == "history://wd_rc001"


@pytest.mark.unit
def test_population_benchmark() -> None:
    benchmark = run_population_benchmark(actors=100, duties=1000)
    assert benchmark.actor_count == 100
    assert benchmark.duty_count == 1000
    assert benchmark.aggregate_ok is True
