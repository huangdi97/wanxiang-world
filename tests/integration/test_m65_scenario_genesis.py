"""M65 scenario mining, genesis, activation, policy, and seed contracts."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.scenario_engine import ScenarioEngine
from wanxiang_substrate.draft.model import WorldDraft


def _draft() -> WorldDraft:
    return WorldDraft(
        draft_id="draft_m65",
        revision=2,
        status="READY_TO_COMPILE",
        source_refs=("source_m65",),
        source_versions=(("source_m65", "1"),),
        constitution_ref="constitution:v1",
        selected_domains=("family", "narrative"),
        dependency_lock=("family", "narrative"),
        entities=(("alice", "Alice"), ("bob", "Bob")),
        relations=(("alice", "bob", "knows"),),
        places=("Beijing",),
        objects=("letter",),
        events=(("arrival", "1985"), ("return", "1990")),
        coverage=0.8,
    )


@pytest.mark.integration
def test_scenario_mining_builds_three_reproducible_genesis_plans() -> None:
    engine = ScenarioEngine()
    first = engine.build_three(_draft())
    second = engine.build_three(_draft())
    assert first == second
    assert len(first) == 3
    assert {plan.scenario.canon_mode for plan in first} == {
        "canonical_replay",
        "soft_canon",
        "living_open",
    }
    assert len({plan.snapshot_hash for plan in first}) == 3
    assert all(plan.initial_snapshot is not None for plan in first)
    assert all(plan.activation_set is not None for plan in first)
    assert all(plan.runtime_profile is not None for plan in first)
    assert all(plan.canon_policy is not None for plan in first)
    assert all(plan.genesis_draft.world_ref == "draft_m65" for plan in first)


@pytest.mark.integration
def test_activation_and_canon_policy_do_not_commit_runtime_state() -> None:
    engine = ScenarioEngine()
    plans = engine.build_three(_draft())
    for plan in plans:
        assert plan.activation_set is not None
        assert plan.activation_set.strategy == "affected_entities"
        assert plan.activation_set.budget <= 100
        assert plan.canon_policy is not None
        assert plan.canon_policy.preserve_dissent is True
        assert plan.canon_policy.completion_policy != "promote_to_e0"
    assert engine.reproducible_seed(_draft(), "scenario_a") == engine.reproducible_seed(
        _draft(), "scenario_a"
    )
    assert engine.reproducible_seed(_draft(), "scenario_a") != engine.reproducible_seed(
        _draft(), "scenario_b"
    )
