"""Opportunity / Challenge / Event compiler (G07C).

Deterministic opportunity detectors over world conditions compile EventCandidates
into executable ChallengeSpecs with prerequisites, safety/rights/evidence
requirements and verifiable outcome requirements. Domain-neutral composer port.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from wanxiang_substrate.reality.errors import ChallengeValidationError


@dataclass(frozen=True, slots=True)
class Opportunity:
    opportunity_id: str
    kind: str
    condition: str
    score: float
    at_ticks: int

    def __post_init__(self) -> None:
        if not (0.0 <= self.score <= 1.0):
            raise ChallengeValidationError("opportunity score must be within [0,1]")


@dataclass(frozen=True, slots=True)
class ChallengeSpec:
    """Executable challenge with prerequisites and verifiable outcomes."""

    challenge_id: str
    title: str
    action_type: str
    prerequisites: tuple[str, ...] = ()
    safety_requirements: tuple[str, ...] = ()
    rights_requirements: tuple[str, ...] = ()
    evidence_requirements: tuple[str, ...] = ()
    end_conditions: tuple[str, ...] = ()
    composer_version: int = 1

    def validate(self) -> None:
        if not self.challenge_id or not self.title or not self.action_type:
            raise ChallengeValidationError("challenge requires id, title and action")


class OpportunityDetector(Protocol):
    """Domain-neutral composer port."""

    def detect(self, world_state: Mapping[str, bool], at_ticks: int) -> tuple[Opportunity, ...]: ...


class DefaultOpportunityDetector:
    """Deterministic detector: world_state is a mapping of condition -> truth."""

    def detect(self, world_state: Mapping[str, bool], at_ticks: int) -> tuple[Opportunity, ...]:
        opportunities: list[Opportunity] = []
        for condition, value in sorted(world_state.items()):
            if value is True:
                opportunities.append(
                    Opportunity(
                        opportunity_id=f"opp_{condition}",
                        kind=condition,
                        condition=condition,
                        score=0.8,
                        at_ticks=at_ticks,
                    )
                )
        return tuple(opportunities)


class ChallengeCompiler:
    """Compiles opportunities into executable ChallengeSpecs."""

    def __init__(self, detector: OpportunityDetector | None = None) -> None:
        self._detector = detector or DefaultOpportunityDetector()

    def detect(self, world_state: Mapping[str, bool], at_ticks: int) -> tuple[Opportunity, ...]:
        return self._detector.detect(world_state, at_ticks)

    def compile(
        self,
        opportunity: Opportunity,
        *,
        action_type: str,
        title: str | None = None,
        prerequisites: tuple[str, ...] = (),
        safety: tuple[str, ...] = ("no_harm",),
        rights: tuple[str, ...] = ("authorized",),
        evidence: tuple[str, ...] = ("outcome_recorded",),
        end_conditions: tuple[str, ...] = ("outcome_verified",),
    ) -> ChallengeSpec:
        spec = ChallengeSpec(
            challenge_id=f"challenge_{opportunity.opportunity_id}",
            title=title or opportunity.condition,
            action_type=action_type,
            prerequisites=prerequisites,
            safety_requirements=safety,
            rights_requirements=rights,
            evidence_requirements=evidence,
            end_conditions=end_conditions,
            composer_version=1,
        )
        spec.validate()
        return spec
