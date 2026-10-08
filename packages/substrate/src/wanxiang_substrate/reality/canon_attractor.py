"""Canon-attractor guidance for living worlds (M88 / G91D).

The policy measures divergence and emits a branch recommendation.  It never
rewrites the observed actor choice, actor goals, canonical state, or history.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.reality.errors import DirectorError

CanonConstraintKind = Literal["soft", "hard"]


@dataclass(frozen=True, slots=True)
class CanonConstraint:
    """A numeric attractor constraint, used for scoring only."""

    constraint_id: str
    dimension: str
    expected: float
    kind: CanonConstraintKind = "soft"
    tolerance: float = 0.0
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not self.constraint_id or not self.dimension:
            raise DirectorError("canon constraint requires id and dimension")
        if self.kind not in {"soft", "hard"}:
            raise DirectorError("canon constraint kind must be soft or hard")
        for field_name in ("expected", "tolerance", "weight"):
            value = float(getattr(self, field_name))
            if not math.isfinite(value) or value < 0.0:
                raise DirectorError(
                    f"canon constraint {field_name} must be finite and non-negative"
                )
        if self.expected > 1.0 or self.tolerance > 1.0 or self.weight > 1.0:
            raise DirectorError("canon constraint values must be within [0,1]")

    @property
    def hardness(self) -> CanonConstraintKind:
        return self.kind


@dataclass(frozen=True, slots=True)
class CanonDistance:
    """Measured distance and violations, with no mutation semantics."""

    total: float
    metrics: Mapping[str, float]
    soft_violations: tuple[str, ...]
    hard_violations: tuple[str, ...]

    @property
    def major(self) -> bool:
        return bool(self.hard_violations) or self.total >= 0.5


@dataclass(frozen=True, slots=True)
class CanonAttractorProposal:
    """Projection proposal emitted when a choice diverges from an attractor."""

    proposal_id: str
    observed_choice: str
    recommendation: str
    branch_required: bool
    reason: str
    free_will_preserved: bool = True


@dataclass(frozen=True, slots=True)
class CanonAttractorAssessment:
    """Assessment retaining the actor choice and the measured distance."""

    choice_ref: str
    at_ticks: int
    distance: CanonDistance
    proposal: CanonAttractorProposal

    @property
    def branch_recommended(self) -> bool:
        return self.proposal.branch_required

    @property
    def choice_preserved(self) -> bool:
        return self.proposal.free_will_preserved


class CanonAttractorPolicy:
    """Score canon distance and recommend, never force, a worldline branch."""

    def __init__(
        self,
        constraints: tuple[CanonConstraint, ...] = (),
        *,
        major_divergence_threshold: float = 0.5,
        policy_version: int = 1,
    ) -> None:
        if not 0.0 < major_divergence_threshold <= 1.0:
            raise DirectorError("major divergence threshold must be within (0,1]")
        if policy_version < 1:
            raise DirectorError("canon policy version must be positive")
        ids = [constraint.constraint_id for constraint in constraints]
        if len(ids) != len(set(ids)):
            raise DirectorError("canon constraint ids must be unique")
        self._constraints = constraints
        self._threshold = major_divergence_threshold
        self._version = policy_version

    @property
    def constraints(self) -> tuple[CanonConstraint, ...]:
        return self._constraints

    @property
    def policy_version(self) -> int:
        return self._version

    def measure(self, observed: Mapping[str, object]) -> CanonDistance:
        """Measure normalized weighted deviations from the policy constraints."""

        metrics: dict[str, float] = {}
        soft: list[str] = []
        hard: list[str] = []
        weighted_total = 0.0
        total_weight = 0.0
        for constraint in self._constraints:
            value = observed.get(constraint.dimension, 0.0)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise DirectorError(f"canon metric {constraint.dimension!r} must be numeric")
            numeric = float(value)
            if not math.isfinite(numeric) or not 0.0 <= numeric <= 1.0:
                raise DirectorError(f"canon metric {constraint.dimension!r} must be within [0,1]")
            delta = abs(numeric - constraint.expected)
            contribution = min(1.0, delta * constraint.weight)
            metrics[constraint.constraint_id] = contribution
            weighted_total += contribution
            total_weight += constraint.weight
            if delta > constraint.tolerance:
                (hard if constraint.kind == "hard" else soft).append(constraint.constraint_id)
        total = weighted_total / total_weight if total_weight else 0.0
        return CanonDistance(total, metrics, tuple(soft), tuple(hard))

    def assess(
        self,
        choice_ref: str,
        observed: Mapping[str, object],
        *,
        at_ticks: int,
    ) -> CanonAttractorAssessment:
        if not choice_ref or at_ticks < 0:
            raise DirectorError("canon assessment requires choice and non-negative time")
        distance = self.measure(observed)
        major = bool(distance.hard_violations) or distance.total >= self._threshold
        recommendation = "fork_worldline" if major else "continue_worldline"
        reason = (
            "major canon divergence; branch is recommended while retaining the choice"
            if major
            else "choice remains within the canon attractor tolerance"
        )
        proposal = CanonAttractorProposal(
            proposal_id=f"canon_attractor:{choice_ref}:{at_ticks}",
            observed_choice=choice_ref,
            recommendation=recommendation,
            branch_required=major,
            reason=reason,
        )
        return CanonAttractorAssessment(choice_ref, at_ticks, distance, proposal)
