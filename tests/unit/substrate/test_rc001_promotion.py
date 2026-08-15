"""G37C: RC-001 long-horizon evolution + promotion candidate (mechanism)."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.lineage import LineageGraph
from wanxiang_substrate.evolution.promotion.pipeline import WorldlinePromotionPipeline
from wanxiang_substrate.rc001.promotion import (
    accelerate,
    distill_stable,
    promote_long_horizon,
)


def _pipeline() -> WorldlinePromotionPipeline:
    return WorldlinePromotionPipeline()


@pytest.mark.unit
def test_time_acceleration_is_bounded() -> None:
    assert accelerate(1000, ticks_per_step=100) == 10
    assert accelerate(0) == 0
    assert accelerate(101, ticks_per_step=10) == 11


@pytest.mark.unit
def test_distill_stable_produces_snapshot() -> None:
    snapshot = distill_stable(_pipeline(), "wl_rc001", ("habit:a", "relation:b"))
    assert snapshot.content_hash
    assert snapshot.genesis_ref == "genesis://wl_rc001"


@pytest.mark.unit
def test_promotion_gate_not_reached_no_derived_world() -> None:
    result = promote_long_horizon(
        _pipeline(),
        worldline_ref="wl_rc001",
        facts=("habit:a", "relation:b"),
        stability=0.6,
        evidence_count=3,
        cross_scenario=False,
        approved=False,
        gate_stability=0.8,
    )
    assert result.gate_reached is False
    assert result.derived is None
    assert result.lineage_edge_recorded is False


@pytest.mark.unit
def test_promotion_gate_reached_creates_derived_world() -> None:
    graph = LineageGraph()
    result = promote_long_horizon(
        _pipeline(),
        worldline_ref="wl_rc001",
        facts=("habit:a", "relation:b", "institution:c"),
        stability=0.9,
        evidence_count=4,
        cross_scenario=True,
        approved=True,
        gate_stability=0.8,
        graph=graph,
    )
    assert result.gate_reached is True
    assert result.derived is not None
    assert result.derived.content_hash
    assert result.lineage_edge_recorded is True
    # Derived definition is a NEW definition id; parent is never mutated.
    assert result.derived.definition_id.value.startswith("wd_derived_")
    assert graph.get_node("wl_rc001") is not None


@pytest.mark.unit
def test_insufficient_evidence_rejected_at_promotion() -> None:
    with pytest.raises(PermissionDenied):
        promote_long_horizon(
            _pipeline(),
            worldline_ref="wl_rc001",
            facts=("habit:a",),
            stability=0.9,
            evidence_count=1,
            cross_scenario=True,
            approved=True,
            gate_stability=0.8,
        )
