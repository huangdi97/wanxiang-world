"""G19E: world-model / planner proposal engine research.

- Bad proposals cannot bypass invariants (rejected by the validator).
- Planner can be disabled with no core regression.
- Rollout results are labeled predictions/simulations.
"""

from __future__ import annotations

from wanxiang_research.flags import DEFAULT_FLAGS
from wanxiang_research.planner import HeuristicPlanner, PlannerEngine


def test_bad_proposal_cannot_bypass_invariants() -> None:
    engine = PlannerEngine(HeuristicPlanner())
    proposal = engine.propose("reach market", {"pos": "home"})
    # The validator rejects an impossible step (no such action).
    result = engine.validate(proposal, validator=lambda step: step == "sample.step_1")
    assert result["ok"] is False
    assert "sample.step_2" in result["rejected_steps"]


def test_planner_disabled_no_core_regression() -> None:
    assert DEFAULT_FLAGS.is_enabled("world_model_planner") is False
    # The stable command path is unchanged with the planner flag off.
    from wanxiang_substrate.compiler.compiler import StructuredCompiler
    from wanxiang_substrate.sources.fixture import approved_source

    result = StructuredCompiler().compile("stable_2", {"src": approved_source()})
    assert result.ok


def test_rollout_results_labeled_predictions() -> None:
    engine = PlannerEngine(HeuristicPlanner(seed=7))
    proposal = engine.propose("goal", {"x": 1})
    result = engine.rollout(proposal, simulate=lambda steps: {"steps": list(steps)})
    assert result["_label"] == "simulation_prediction"
    assert result["model_version"] == "heuristic-1"
    assert result["seed"] == 7
