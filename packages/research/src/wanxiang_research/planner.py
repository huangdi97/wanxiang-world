"""World-model / planner proposal engine research (G19E, experimental).

The planner PROPOSES multi-step actions; it never mutates canonical state.
Rollouts run on disposable simulations and are labeled predictions, never
truth. Bad proposals are rejected by the existing validators.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class PlanProposal:
    plan_id: str
    steps: tuple[str, ...]
    predicted_outcome: str
    confidence: float
    model_version: str
    seed: int


class Planner(Protocol):
    def propose(self, goal: str, state: dict[str, Any]) -> PlanProposal: ...


class HeuristicPlanner:
    """Deterministic baseline planner (no learned model)."""

    def __init__(self, model_version: str = "heuristic-1", seed: int = 0) -> None:
        self._model_version = model_version
        self._seed = seed

    def propose(self, goal: str, state: dict[str, Any]) -> PlanProposal:
        return PlanProposal(
            plan_id=f"plan_{goal}_{self._seed}",
            steps=("sample.step_1", "sample.step_2"),
            predicted_outcome=f"goal achieved: {goal}",
            confidence=0.6,
            model_version=self._model_version,
            seed=self._seed,
        )


class PlannerEngine:
    def __init__(self, planner: Planner) -> None:
        self._planner = planner

    def propose(self, goal: str, state: dict[str, Any]) -> PlanProposal:
        return self._planner.propose(goal, state)

    def validate(self, proposal: PlanProposal, validator: Callable[[str], bool]) -> dict[str, Any]:
        """Reject impossible actions through the existing validator."""
        rejected = [step for step in proposal.steps if not validator(step)]
        return {
            "plan_id": proposal.plan_id,
            "rejected_steps": rejected,
            "ok": not rejected,
        }

    def rollout(
        self, proposal: PlanProposal, simulate: Callable[[tuple[str, ...]], dict[str, Any]]
    ) -> dict[str, Any]:
        """Run on a disposable simulation; results are labeled predictions."""
        result = simulate(proposal.steps)
        result["_label"] = "simulation_prediction"
        result["model_version"] = proposal.model_version
        result["seed"] = proposal.seed
        return result
