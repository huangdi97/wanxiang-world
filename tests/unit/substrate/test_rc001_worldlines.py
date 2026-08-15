"""G37B: three-worldline generation + comparison (mechanism; synthetic)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.rc001.worldlines import (
    compare_worldlines,
    run_worldlines,
    verify_parent_hash,
)

PARENT = "hash_parent_abc"


@pytest.mark.unit
def test_three_worldlines_generated_from_parent() -> None:
    runs = run_worldlines(
        parent_hash=PARENT,
        parent_items=("letter",),
        parent_beliefs=("b1",),
        parent_relations=("r1",),
    )
    assert len(runs) == 3
    assert {r.strategy for r in runs} == {
        "canonical_replay",
        "soft_canon",
        "living_open",
    }
    replay = next(r for r in runs if r.strategy == "canonical_replay")
    assert replay.event_count == 0
    assert replay.items == ("letter",)


@pytest.mark.unit
def test_comparison_reports_divergence_and_parent_verified() -> None:
    runs = run_worldlines(
        parent_hash=PARENT,
        parent_items=("letter",),
        parent_beliefs=("b1",),
        parent_relations=("r1",),
    )
    comparison = compare_worldlines(runs)
    assert comparison.parent_hash_verified is True
    assert comparison.diverged is True
    assert len(comparison.state_hashes) == 3
    assert comparison.diffs  # soft/living diverged in items/beliefs/relations


@pytest.mark.unit
def test_parent_hash_never_mutated_by_children() -> None:
    runs = run_worldlines(
        parent_hash=PARENT,
        parent_items=("letter",),
        parent_beliefs=("b1",),
        parent_relations=("r1",),
    )
    assert verify_parent_hash(PARENT, runs) is True
    assert all(r.parent_hash == PARENT for r in runs)


@pytest.mark.unit
def test_canonical_replay_matches_parent_baseline() -> None:
    runs = run_worldlines(
        parent_hash=PARENT,
        parent_items=("letter",),
        parent_beliefs=("b1",),
        parent_relations=("r1",),
    )
    replay = next(r for r in runs if r.strategy == "canonical_replay")
    # Canonical replay adds no items/beliefs/relations beyond the parent.
    assert replay.items == ("letter",)
    assert replay.beliefs == ("b1",)
    assert replay.relations == ("r1",)
