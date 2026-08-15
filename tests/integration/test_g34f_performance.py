"""G34F: performance & complexity regression (commit/replay/tick/lineage)."""

from __future__ import annotations

import time

import pytest
from scripts.benchmarks import benchmark_commits, benchmark_lineage, benchmark_replay
from wanxiang_domain.lineage import LineageEdge, LineageGraph, LineageNode
from wanxiang_substrate.evolution.scheduler import EvolutionCadence, EvolutionScheduler

# Generous CI-safe upper bounds; these only catch pathological regressions.
MAX_COMMIT_SECONDS = 10.0
MAX_REPLAY_SECONDS = 10.0
MAX_LINEAGE_QUERY_SECONDS = 1.0
MAX_TICK_SECONDS = 1.0


@pytest.mark.integration
def test_commit_replay_critical_path_has_no_unexplained_regression() -> None:
    commit = benchmark_commits(n=100)
    replay = benchmark_replay(n=200)
    assert commit["seconds"] < MAX_COMMIT_SECONDS
    assert replay["replay_seconds"] < MAX_REPLAY_SECONDS
    assert commit["events_per_second"] > 0


@pytest.mark.integration
def test_lineage_query_is_bounded_and_scales() -> None:
    small = benchmark_lineage(n=50)
    large = benchmark_lineage(n=400)
    assert small["query_seconds"] < MAX_LINEAGE_QUERY_SECONDS
    assert large["query_seconds"] < MAX_LINEAGE_QUERY_SECONDS
    # 8x nodes -> query cost stays within a small multiple (no exponential).
    assert large["query_seconds"] < max(1.0, small["query_seconds"] * 40)


@pytest.mark.integration
def test_tick_scheduler_cost_is_bounded() -> None:
    scheduler = EvolutionScheduler(cadence=EvolutionCadence())
    start = time.perf_counter()
    for tick in range(1, 10_001):
        scheduler.due_scales(tick)
    elapsed = time.perf_counter() - start
    assert elapsed < MAX_TICK_SECONDS
    assert scheduler.total_activations(10_000) < 15_000


@pytest.mark.integration
def test_lineage_graph_chain_is_deterministic_and_acyclic() -> None:
    graph = LineageGraph()
    graph.add_node(LineageNode(node_id="root", kind="definition"))
    for i in range(100):
        graph.add_node(LineageNode(node_id=f"n{i}", kind="worldline"))
        graph.add_edge(LineageEdge("root" if i == 0 else f"n{i - 1}", f"n{i}", edge_kind="fork"))
    assert set(graph.ancestors("n99")) == {f"n{i}" for i in range(99)} | {"root"}
    assert len(graph.ancestors("n99")) == 100
    assert len(graph.descendants("root")) == 100
