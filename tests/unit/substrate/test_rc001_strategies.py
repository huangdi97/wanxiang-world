"""G36G: Canonical Replay / Soft Canon / Living Open strategies (mechanism).

Synthetic facts only - never real《红楼梦》canon.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.ledger.errors import CanonLocked
from wanxiang_substrate.rc001.strategies import (
    CanonLocks,
    SoftAttractor,
    compare_to_baseline,
    strategy_for,
)


@pytest.mark.unit
def test_three_strategy_policy_configs() -> None:
    replay = strategy_for("canonical_replay", baseline_ref="base_1")
    assert replay.strategy == "canonical_replay"
    assert replay.canon_lock_depth == 1
    assert replay.soft_attractor is None
    soft = strategy_for("soft_canon")
    assert soft.strategy == "soft_canon"
    assert soft.soft_attractor == "canon"
    assert soft.canon_lock_depth == 0
    open_world = strategy_for("living_open")
    assert open_world.strategy == "living_open"
    assert open_world.canon_lock_depth == 0


@pytest.mark.unit
def test_canonical_lock_rejects_mutation() -> None:
    locks = CanonLocks().lock("c1进府")
    assert locks.is_locked("c1进府")
    with pytest.raises(CanonLocked):
        locks.assert_mutable("c1进府")
    # Unlocked facts remain mutable.
    locks.assert_mutable("c2病于室")


@pytest.mark.unit
def test_soft_attractor_pulls_toward_canon() -> None:
    attractor = SoftAttractor(target="canon", condition=lambda: True)
    assert attractor.pull("canon") == 1.0
    assert attractor.pull("drift") == 0.5
    assert attractor.pull("drift", strength=0.8) == 0.8
    blocked = SoftAttractor(target="canon", condition=lambda: False)
    assert blocked.pull("drift") == 0.0


@pytest.mark.unit
def test_open_branch_baseline_comparison() -> None:
    matching = compare_to_baseline(
        baseline_hash="h1", current_hash="h1", current_revision=5, baseline_revision=5
    )
    assert matching.matches is True
    assert matching.diverged is False
    diverged = compare_to_baseline(
        baseline_hash="h1", current_hash="h2", current_revision=7, baseline_revision=5
    )
    assert diverged.matches is False
    assert diverged.diverged is True
    assert diverged.revision_delta == 2


@pytest.mark.unit
def test_replay_strategy_pins_baseline() -> None:
    config = strategy_for("canonical_replay", baseline_ref="base_1")
    assert config.branch_baseline_ref == "base_1"
    # A canonical-replay branch must not diverge from its baseline.
    comparison = compare_to_baseline(
        baseline_hash="b", current_hash="b", current_revision=1, baseline_revision=1
    )
    assert comparison.matches is True
