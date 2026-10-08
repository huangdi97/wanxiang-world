"""SimulationLOD activity scoring, transitions, and cohort projections."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

SimulationLevel = Literal["L0", "L1", "L2", "L3", "L4"]
SIMULATION_LEVELS: tuple[SimulationLevel, ...] = ("L0", "L1", "L2", "L3", "L4")


def _bounded(value: float, name: str) -> None:
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ContractError(f"{name} must be finite and bounded in [0, 1]")


@dataclass(frozen=True, slots=True)
class ActorActivityInput:
    """Deterministic activity signals read from projections, not state writes."""

    actor_id: str
    current_tick: int
    last_active_tick: int
    goal_urgency: float = 0.0
    interaction_rate: float = 0.0
    proximity: float = 0.0

    def __post_init__(self) -> None:
        if not self.actor_id:
            raise ContractError("actor_id must be non-empty")
        if self.current_tick < 0 or self.last_active_tick < 0:
            raise ContractError("activity ticks must be non-negative")
        if self.last_active_tick > self.current_tick:
            raise ContractError("last_active_tick cannot be in the future")
        _bounded(self.goal_urgency, "goal_urgency")
        _bounded(self.interaction_rate, "interaction_rate")
        _bounded(self.proximity, "proximity")


@dataclass(frozen=True, slots=True)
class ActivityScore:
    actor_id: str
    score: float
    recency: float
    reason: str

    def __post_init__(self) -> None:
        if not self.actor_id or not self.reason:
            raise ContractError("activity score refs must be non-empty")
        _bounded(self.score, "score")
        _bounded(self.recency, "recency")


@dataclass(frozen=True, slots=True)
class SimulationLODPolicy:
    """Thresholds for focal, active, background, cohort, and population tiers."""

    l0_threshold: float = 0.80
    l1_threshold: float = 0.60
    l2_threshold: float = 0.35
    l3_threshold: float = 0.10

    def __post_init__(self) -> None:
        values = (self.l0_threshold, self.l1_threshold, self.l2_threshold, self.l3_threshold)
        for index, value in enumerate(values):
            _bounded(value, f"l{index}_threshold")
        if not self.l0_threshold > self.l1_threshold > self.l2_threshold > self.l3_threshold:
            raise ContractError("LOD thresholds must be strictly descending")

    def level_for(self, score: float) -> SimulationLevel:
        _bounded(score, "score")
        if score >= self.l0_threshold:
            return "L0"
        if score >= self.l1_threshold:
            return "L1"
        if score >= self.l2_threshold:
            return "L2"
        if score >= self.l3_threshold:
            return "L3"
        return "L4"


@dataclass(frozen=True, slots=True)
class LODState:
    """Actor LOD envelope; state and memory remain owned by the World."""

    actor_id: str
    level: SimulationLevel
    state_ref: str
    memory_summary_ref: str

    def __post_init__(self) -> None:
        if not self.actor_id or not self.state_ref or not self.memory_summary_ref:
            raise ContractError("LOD state refs must be non-empty")


@dataclass(frozen=True, slots=True)
class LODTransition:
    actor_id: str
    from_level: SimulationLevel
    to_level: SimulationLevel
    state_ref: str
    continuity_ref: str
    score: float
    reason: str

    def __post_init__(self) -> None:
        if not self.actor_id or not self.state_ref or not self.continuity_ref:
            raise ContractError("LOD transition refs must be non-empty")
        _bounded(self.score, "score")


@dataclass(frozen=True, slots=True)
class CohortAggregate:
    cohort_id: str
    level: Literal["L3", "L4"]
    actor_ids: tuple[str, ...]
    state_refs: tuple[str, ...]
    mean_score: float

    def __post_init__(self) -> None:
        if (
            not self.cohort_id
            or not self.actor_ids
            or len(self.actor_ids) != len(set(self.actor_ids))
        ):
            raise ContractError("cohort must have unique non-empty actor ids")
        if len(self.actor_ids) != len(self.state_refs):
            raise ContractError("cohort actor/state refs must align")
        _bounded(self.mean_score, "mean_score")


class SimulationLODRuntime:
    """Stateless-worker LOD policy; every method returns proposal evidence."""

    def __init__(self, policy: SimulationLODPolicy | None = None) -> None:
        self._policy = policy or SimulationLODPolicy()

    @property
    def policy(self) -> SimulationLODPolicy:
        return self._policy

    def score(self, activity: ActorActivityInput) -> ActivityScore:
        idle = activity.current_tick - activity.last_active_tick
        recency = max(0.0, 1.0 - min(idle, 1000) / 1000)
        score = (
            recency * 0.35
            + activity.goal_urgency * 0.30
            + activity.interaction_rate * 0.20
            + activity.proximity * 0.15
        )
        return ActivityScore(
            actor_id=activity.actor_id,
            score=score,
            recency=recency,
            reason=f"recency={recency:.3f};goal={activity.goal_urgency:.3f};"
            f"interaction={activity.interaction_rate:.3f};proximity={activity.proximity:.3f}",
        )

    def transition(self, state: LODState, score: ActivityScore) -> LODTransition:
        if state.actor_id != score.actor_id:
            raise ContractError("LOD state and score actor ids differ")
        target = self._policy.level_for(score.score)
        return self._transition(state, target, score)

    def promote_to_active(self, state: LODState, score: ActivityScore) -> LODTransition:
        if state.actor_id != score.actor_id:
            raise ContractError("LOD state and score actor ids differ")
        return self._transition(state, "L0", score, reason="promotion_back_to_focal")

    def aggregate(
        self,
        cohort_id: str,
        states: tuple[LODState, ...],
        scores: tuple[ActivityScore, ...],
    ) -> CohortAggregate:
        if not states or len(states) != len(scores):
            raise ContractError("cohort states and scores must be non-empty and aligned")
        if any(state.level not in ("L3", "L4") for state in states):
            raise ContractError("only L3/L4 states can be aggregated")
        by_actor = {score.actor_id: score for score in scores}
        if {state.actor_id for state in states} != set(by_actor):
            raise ContractError("cohort scores must cover each actor exactly once")
        ordered = tuple(sorted(states, key=lambda state: state.actor_id))
        mean = sum(by_actor[state.actor_id].score for state in ordered) / len(ordered)
        level: Literal["L3", "L4"] = "L4" if all(state.level == "L4" for state in ordered) else "L3"
        return CohortAggregate(
            cohort_id=cohort_id,
            level=level,
            actor_ids=tuple(state.actor_id for state in ordered),
            state_refs=tuple(state.state_ref for state in ordered),
            mean_score=mean,
        )

    @staticmethod
    def _transition(
        state: LODState,
        target: SimulationLevel,
        score: ActivityScore,
        *,
        reason: str | None = None,
    ) -> LODTransition:
        continuity_ref = hashlib.sha256(
            f"{state.actor_id}|{state.state_ref}|{state.memory_summary_ref}".encode()
        ).hexdigest()
        return LODTransition(
            actor_id=state.actor_id,
            from_level=state.level,
            to_level=target,
            state_ref=state.state_ref,
            continuity_ref=continuity_ref,
            score=score.score,
            reason=reason or "activity_threshold_transition",
        )


__all__ = [
    "SIMULATION_LEVELS",
    "ActivityScore",
    "ActorActivityInput",
    "CohortAggregate",
    "LODState",
    "LODTransition",
    "SimulationLevel",
    "SimulationLODPolicy",
    "SimulationLODRuntime",
]
