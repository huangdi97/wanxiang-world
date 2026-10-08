"""Completion planner (G58F).

Turns missing runtime requirements into a CompletionPlan: E0-E5 candidates
when completable, explicit keep-unknown for what cannot be safely completed.
Unknown stays unknown; nothing is fabricated.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.completion.candidates import CompletionCandidate

RequirementKind = Literal[
    "actor_initial_location",
    "location_connectivity",
    "object_ownership",
    "scenario_initial_time",
    "rule_resolver",
    "knowledge_boundary",
    "schedule_coverage",
    "domain_requirement",
]
VALID_KINDS = (
    "actor_initial_location",
    "location_connectivity",
    "object_ownership",
    "scenario_initial_time",
    "rule_resolver",
    "knowledge_boundary",
    "schedule_coverage",
    "domain_requirement",
)


@dataclass(frozen=True, slots=True)
class MissingRequirement:
    requirement_id: str
    kind: RequirementKind
    detail: str
    blocking: bool = True

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.detail:
            raise ContractError("requirement requires id and detail")
        if self.kind not in VALID_KINDS:
            raise ContractError(f"invalid requirement kind {self.kind!r}")


@dataclass(frozen=True, slots=True)
class CompletionPlan:
    plan_id: str
    requirements: tuple[MissingRequirement, ...]
    candidates: tuple[CompletionCandidate, ...]
    keep_unknown: bool
    unknown: tuple[MissingRequirement, ...]

    @property
    def has_blocking_unknown(self) -> bool:
        return any(r.blocking for r in self.unknown)


class CompletionPlanner:
    """Builds a completion plan; keep-unknown preserves honesty."""

    def plan(
        self,
        requirements: tuple[MissingRequirement, ...],
        *,
        plan_id: str = "plan_1",
        keep_unknown: bool = True,
    ) -> CompletionPlan:
        candidates: list[CompletionCandidate] = []
        unknown: list[MissingRequirement] = []
        for index, requirement in enumerate(requirements, start=1):
            candidate = self._candidate_for(requirement, index)
            if candidate is None or keep_unknown:
                unknown.append(requirement)
            if candidate is not None:
                candidates.append(candidate)
        return CompletionPlan(
            plan_id=plan_id,
            requirements=requirements,
            candidates=tuple(candidates),
            keep_unknown=keep_unknown,
            unknown=tuple(unknown),
        )

    def _candidate_for(
        self,
        requirement: MissingRequirement,
        index: int,
    ) -> CompletionCandidate | None:
        kind = requirement.kind
        if kind == "actor_initial_location":
            return CompletionCandidate(
                completion_id=f"cmp_{index}",
                description=f"initial location for {requirement.detail}",
                completion_class="E3",  # runtime-required default
                support_refs=(),
                confidence=0.3,
            )
        if kind == "scenario_initial_time":
            return CompletionCandidate(
                completion_id=f"cmp_{index}",
                description=f"initial time for {requirement.detail}",
                completion_class="E3",
                support_refs=(),
                confidence=0.3,
            )
        if kind == "domain_requirement":
            return CompletionCandidate(
                completion_id=f"cmp_{index}",
                description=f"domain rule for {requirement.detail}",
                completion_class="E2",  # domain/era rule derivation
                support_refs=(),
                confidence=0.4,
            )
        # Other kinds stay unknown unless explicit source evidence exists.
        return None
