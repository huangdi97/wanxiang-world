"""M66 worldness, bounded simulation, repair, branch, and determinism contracts."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_substrate.authoring.worldness import (
    BoundedSimulation,
    FailureLocalizer,
    RepairLoop,
    WorldnessEvaluator,
    WorldnessInput,
    determinism_envelope,
    prove_branch_isolation,
)


def _value() -> WorldnessInput:
    return WorldnessInput(
        2,
        1,
        2,
        1,
        0.1,
        replay_equal=True,
        branch_isolated=True,
        draft_id="draft_m66",
        draft_revision=1,
        source_refs=("source_m66",),
        domain_refs=("family",),
        completion_refs=("completion_1",),
        package_id="package_m66",
        provider_ids=("reference",),
        seed=66,
    )


@pytest.mark.integration
def test_worldness_evaluator_and_seven_day_accelerated_reference_run() -> None:
    score = WorldnessEvaluator().evaluate(_value())
    assert len(score.dimensions) == 10
    assert score.passed is True

    simulator = BoundedSimulation()
    first = simulator.run(_value(), branch_id="preview_a", horizon_days=7)
    second = simulator.run(_value(), branch_id="preview_a", horizon_days=7)
    other = simulator.run(_value(), branch_id="preview_b", horizon_days=7)
    assert len(first.steps) == 7
    assert first == second
    assert first.replay_hash == second.replay_hash
    assert first.final_hash != other.final_hash

    envelope = determinism_envelope(_value(), first, second)
    assert envelope.replay_equal is True
    assert envelope.valid is True
    assert envelope.provider_ids == ("reference",)


@pytest.mark.integration
def test_failure_localization_and_candidate_only_recompile_loop() -> None:
    poor = replace(
        _value(),
        entity_count=0,
        relation_count=0,
        event_count=0,
        source_count=0,
        uncertainty=0.9,
        replay_equal=False,
        branch_isolated=False,
    )
    score = WorldnessEvaluator().evaluate(poor)
    locations = FailureLocalizer().locate(score, poor)
    assert {item.layer for item in locations} >= {"draft", "completion", "domain"}
    assert {item.layer for item in locations} >= {"missingness", "package"}

    def recompile(
        current: WorldnessInput, _candidates: tuple[object, ...], _round: int
    ) -> WorldnessInput:
        return replace(
            current,
            entity_count=2,
            relation_count=1,
            event_count=2,
            source_count=1,
            uncertainty=0.1,
            replay_equal=True,
            branch_isolated=True,
            draft_revision=current.draft_revision + 1,
        )

    run = RepairLoop().run(poor, rounds=3, recompile=recompile)
    assert run.converged is True
    assert len(run.scores) == 2
    assert run.cycles[0].output_revision == 2
    assert run.cycles[0].committed is False
    assert run.candidates
    assert all(candidate.applied is False for candidate in run.candidates)


@pytest.mark.integration
def test_preview_and_repair_branches_are_namespaced_and_nondeterminism_is_visible() -> None:
    proof = prove_branch_isolation(_value(), "preview_a", "repair_a")
    assert proof.isolated is True
    assert proof.source_fingerprint
    assert len({fingerprint for _branch, fingerprint in proof.branch_fingerprints}) == 2

    simulator = BoundedSimulation()
    trace = simulator.run(_value(), branch_id="preview_a")
    envelope = determinism_envelope(
        _value(),
        trace,
        trace,
        nondeterminism=("external_provider_latency",),
    )
    assert envelope.valid is False
    assert envelope.nondeterminism == ("external_provider_latency",)


def test_simulation_bounds_are_explicit() -> None:
    with pytest.raises(ValueError):
        BoundedSimulation().run(_value(), horizon_days=0)
