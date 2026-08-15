"""M38: full living runtime (mechanism; synthetic)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.living import (
    WORLDNESS_CLASSES,
    build_propagation_graph,
    evolve_institutions,
    evolve_long_term,
    instantiate_scenarios,
    resolve_population,
    run_autonomous_loop,
    run_long_horizon,
)
from wanxiang_substrate.rc001.strategies import strategy_for


@pytest.mark.unit
def test_multi_scenario_instantiation_fixed_genesis() -> None:
    instances = instantiate_scenarios(
        genesis_snapshot_hash="snap_1",
        scenarios=("arrival", "illness", "feast"),
        strategy=strategy_for("canonical_replay"),
    )
    assert len(instances) == 3
    assert all(i.genesis_snapshot_hash == "snap_1" for i in instances)
    assert all(i.initial_revision == 1 for i in instances)


@pytest.mark.unit
def test_population_resolution_budget_and_identity() -> None:
    result = resolve_population(
        actor_keys=("c1", "c2", "c3"),
        roles=(("c1", "lady"), ("c2", "maid"), ("c3", "guest")),
        budget_limit=2,
        seed=0,
    )
    assert result.budget_used <= result.budget_limit
    assert result.identity_preserved is True
    assert len(result.promoted) + len(result.demoted) == 3


@pytest.mark.unit
def test_autonomous_loop_deterministic_with_fallback() -> None:
    first = run_autonomous_loop(horizon_ticks=10, seed=1)
    second = run_autonomous_loop(horizon_ticks=10, seed=1)
    assert first == second
    assert len(first) == 10
    assert any(step.fallback_used for step in first)


@pytest.mark.unit
def test_propagation_graph_scopes_and_correction() -> None:
    graph = build_propagation_graph(
        facts=(("f1", "public"), ("f2", "private")),
        edges=(("c1", "c2"),),
        corrected=("f1",),
        forgotten=("f2",),
    )
    assert ("f1", "public") in graph.scoped_facts
    assert graph.corrected == ("f1",)
    assert graph.forgotten == ("f2",)


@pytest.mark.unit
def test_long_term_evolution_separates_deltas() -> None:
    summary = evolve_long_term(
        trajectories=("t1", "t2"),
        capability_deltas=(("c1", "poetry", 1),),
        persona_deltas=(("c1", "temperament", "reserved"),),
        relation_evolution=(("c1", "c2", "friend", "strengthened"),),
    )
    assert summary.trajectories == ("t1", "t2")
    assert summary.capability_deltas == (("c1", "poetry", 1),)
    assert summary.persona_deltas == (("c1", "temperament", "reserved"),)


@pytest.mark.unit
def test_institution_evolution_law_commit_gate() -> None:
    low = evolve_institutions(patterns=("habit_a",), stability=0.6)
    assert low.law_commit_gate_passed is False
    high = evolve_institutions(patterns=("habit_a",), stability=0.9)
    assert high.law_commit_gate_passed is True
    assert "habit_a" in high.norms
    assert "habit_a" in high.institution_candidates


@pytest.mark.unit
def test_long_run_report_and_worldness_matrix() -> None:
    report = run_long_horizon(days=30, accelerated_years=1)
    assert report.days_30_ticks == 300
    assert report.year_1_accelerated_steps == 12
    assert report.final_stable is True
    assert len(report.worldness_classes) == 12
    assert set(WORLDNESS_CLASSES) == set(report.worldness_classes)
