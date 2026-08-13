"""G07C-G07E: challenge compiler, director runtime and experiments."""

from __future__ import annotations

import pytest
from wanxiang_substrate.reality.challenge import ChallengeCompiler
from wanxiang_substrate.reality.director import (
    DirectorReview,
    NarrativeDirector,
    PerformanceDirector,
    WorldDirector,
)
from wanxiang_substrate.reality.errors import DirectorError, ExperimentError
from wanxiang_substrate.reality.experiment import (
    ExperimentRuntime,
    ExperimentSpec,
)
from wanxiang_substrate.recovery.budget import ResourceBudget


def _run_value(seed: int, param: str, value: object) -> float:
    return seed * float(value if isinstance(value, (int, float)) else 0.0)


@pytest.mark.unit
def test_challenge_spec_includes_prerequisites_and_outcomes() -> None:
    compiler = ChallengeCompiler()
    opportunities = compiler.detect({"supply_low": True, "idle": False}, at_ticks=10)
    assert len(opportunities) == 1
    spec = compiler.compile(
        opportunities[0],
        action_type="material.transfer",
        prerequisites=("has_item",),
        safety=("no_harm",),
        rights=("authorized",),
        evidence=("outcome_recorded",),
        end_conditions=("outcome_verified",),
    )
    assert spec.prerequisites == ("has_item",)
    assert "no_harm" in spec.safety_requirements
    assert "authorized" in spec.rights_requirements
    assert "outcome_verified" in spec.end_conditions


@pytest.mark.unit
def test_director_proposes_but_never_commits() -> None:
    director = WorldDirector(version=3)
    proposal = director.propose_focus("town_square", at_ticks=20)
    assert proposal.director == "world"
    assert proposal.version == 3
    # A proposal is not a commit; there is no commit method on directors.
    assert not hasattr(director, "commit")


@pytest.mark.unit
def test_directors_cannot_rewrite_actor_persona_without_review() -> None:
    director = WorldDirector()
    review = DirectorReview()
    proposal = director.propose_focus("persona_shift", at_ticks=1, action_type="persona.rewrite")
    assert review.require_review(proposal) is True
    assert review.reviewed(proposal.proposal_id) is False
    review.approve(proposal, reviewer="actor_logic")
    assert review.reviewed(proposal.proposal_id) is True
    plain = director.propose_focus("focus_a", at_ticks=1)
    with pytest.raises(DirectorError):
        review.approve(plain, reviewer="actor_logic")


@pytest.mark.unit
def test_narrative_and_performance_are_projection_only() -> None:
    narrative = NarrativeDirector()
    signal = narrative.score("goal_1", "curiosity", reached=True, weight=0.9)
    assert 0.0 <= signal.score <= 1.0
    performance = PerformanceDirector()
    directive = performance.directive("d1", "camera", "alice")
    assert directive["projection_only"] is True


@pytest.mark.unit
def test_experiment_runs_multi_seed_from_baseline_deterministically() -> None:
    spec = ExperimentSpec(
        experiment_id="exp_1",
        baseline_ref="snap://baseline_v1",
        parameter_variants=(("speed", 2), ("speed", 4)),
        seeds=(1, 2, 3),
    )
    runtime = ExperimentRuntime(budget=ResourceBudget(max_commands=100))
    results = runtime.run(spec, mutate=_run_value)
    assert len(results) == 6  # 3 seeds x 2 variants
    assert {m.seed for m in results} == {1, 2, 3}
    assert {m.rule_version for m in results} == {1}
    again = runtime.run(spec, mutate=_run_value)
    assert [m.value for m in results] == [m.value for m in again]
    # Distribution aggregates all variants across seeds (not point outputs).
    dist = runtime.distribution(spec, "speed")
    assert len(dist) == 6


@pytest.mark.unit
def test_finding_requires_assumptions_and_validity_envelope() -> None:
    spec = ExperimentSpec(
        experiment_id="exp_2",
        baseline_ref="snap://b",
        parameter_variants=(("speed", 2),),
        seeds=(7,),
    )
    runtime = ExperimentRuntime()
    with pytest.raises(ExperimentError):
        runtime.finding(spec, "conclusion", supported=True, assumptions=())
    runtime.run(spec, mutate=_run_value)
    finding = runtime.finding(
        spec,
        "higher speed wins",
        supported=True,
        assumptions=("flat terrain", "no weather"),
    )
    assert finding.assumptions == ("flat terrain", "no weather")
    assert "reproduce" in finding.validity_envelope
    envelope = runtime.envelope(spec)
    assert envelope.seeds == (7,)


@pytest.mark.unit
def test_experiment_baseline_never_mutated() -> None:
    spec = ExperimentSpec(
        experiment_id="exp_3",
        baseline_ref="snap://baseline_v1",
        parameter_variants=(("x", 1),),
        seeds=(1,),
    )
    runtime = ExperimentRuntime()
    results = runtime.run(spec, mutate=_run_value)
    assert results[0].run_id.startswith("exp_3")
    # Running again uses the same baseline spec; nothing is mutated.
    again = runtime.run(spec, mutate=_run_value)
    assert again[0].value == results[0].value
