"""G32B: multi-scale evolution scheduler."""

from __future__ import annotations

import pytest
from wanxiang_substrate.evolution.scheduler import (
    EVOLUTION_SCALES,
    EvolutionCadence,
    EvolutionScheduler,
)


@pytest.mark.unit
def test_scales_evaluate_on_their_cadence() -> None:
    cadence = EvolutionCadence(actor=1, relation=5, group=10, institution=30, world=100)
    scheduler = EvolutionScheduler(cadence=cadence, seed=0)
    assert scheduler.due_scales(1) == ("actor",)
    assert scheduler.due_scales(5) == ("actor", "relation")
    assert scheduler.due_scales(10) == ("actor", "relation", "group")
    assert scheduler.due_scales(30) == ("actor", "relation", "group", "institution")
    assert scheduler.due_scales(100) == ("actor", "relation", "group", "world")  # 100 % 30 != 0
    assert scheduler.due_scales(101) == ("actor",)


@pytest.mark.unit
def test_same_seed_cadence_is_deterministic() -> None:
    a = EvolutionScheduler(cadence=EvolutionCadence(), seed=7)
    b = EvolutionScheduler(cadence=EvolutionCadence(), seed=7)
    for tick in range(1, 500):
        assert a.due_scales(tick) == b.due_scales(tick)


@pytest.mark.unit
def test_no_full_scan_and_no_exponential_explosion() -> None:
    cadence = EvolutionCadence(actor=1, relation=5, group=10, institution=30, world=100)
    scheduler = EvolutionScheduler(cadence=cadence, seed=0)
    total = scheduler.total_activations(10_000)
    # Expected linear sum: T/1 + T/5 + T/10 + T/30 + T/100 (approx 1.3433*T).
    expected = 10_000 // 1 + 10_000 // 5 + 10_000 // 10 + 10_000 // 30 + 10_000 // 100
    assert total <= expected + 10
    assert total < 15_000  # linear, never exponential
    # The window limits how many entities activate per tick (no full scan).
    assert scheduler.bounded_window(100, window=3) == ("actor", "relation", "group")


@pytest.mark.unit
def test_scale_names_stable() -> None:
    assert EVOLUTION_SCALES == ("actor", "relation", "group", "institution", "world")
