"""Opportunity / Challenge / Event compiler (G07C).

Deterministic opportunity detectors over world conditions compile EventCandidates
into executable ChallengeSpecs with prerequisites, safety/rights/evidence
requirements and verifiable outcome requirements. Domain-neutral composer port.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Literal, Protocol

from wanxiang_substrate.reality.errors import ChallengeValidationError

OpportunityStatus = Literal[
    "proposed",
    "eligible",
    "offered",
    "accepted",
    "ignored",
    "declined",
    "expired",
    "completed",
]
OPPORTUNITY_STATUSES = (
    "proposed",
    "eligible",
    "offered",
    "accepted",
    "ignored",
    "declined",
    "expired",
    "completed",
)


@dataclass(frozen=True, slots=True)
class Opportunity:
    """A world proposal; it is not an actor goal or a canonical event."""

    opportunity_id: str
    kind: str
    condition: str
    score: float
    at_ticks: int
    eligibility: tuple[str, ...] = ()
    available_from: int = 0
    expires_at: int | None = None
    reward_refs: tuple[str, ...] = ()
    risk_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    world_state_refs: tuple[str, ...] = ()
    status: OpportunityStatus = "proposed"
    actor_id: str = ""
    decision_ref: str = ""
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.opportunity_id or not self.kind or not self.condition:
            raise ChallengeValidationError("opportunity requires id, kind and condition")
        if not (0.0 <= self.score <= 1.0):
            raise ChallengeValidationError("opportunity score must be within [0,1]")
        if self.at_ticks < 0 or self.available_from < 0:
            raise ChallengeValidationError("opportunity times must be non-negative")
        if self.expires_at is not None and self.expires_at <= self.available_from:
            raise ChallengeValidationError("opportunity expiry must follow availability")
        if self.status not in OPPORTUNITY_STATUSES:
            raise ChallengeValidationError(f"invalid opportunity status {self.status!r}")
        if self.schema_version != 1:
            raise ChallengeValidationError("unsupported opportunity schema")
        for field_name in (
            "eligibility",
            "reward_refs",
            "risk_refs",
            "evidence_refs",
            "world_state_refs",
        ):
            refs = getattr(self, field_name)
            if any(not isinstance(ref, str) or not ref for ref in refs):
                raise ChallengeValidationError(f"{field_name} must contain non-empty refs")

    def is_open(self, at_ticks: int) -> bool:
        """Return whether the proposal can still be offered or answered."""

        return (
            self.status in {"proposed", "eligible", "offered", "accepted"}
            and at_ticks >= self.available_from
            and (self.expires_at is None or at_ticks < self.expires_at)
        )

    def eligible_for(self, actor_id: str, world_state_refs: tuple[str, ...], at_ticks: int) -> bool:
        """Evaluate explicit actor/state refs without changing actor cognition."""

        if not actor_id or not self.is_open(at_ticks):
            return False
        available = set(world_state_refs)
        for requirement in self.eligibility:
            if requirement.startswith("actor:"):
                if requirement.removeprefix("actor:") != actor_id:
                    return False
            elif requirement not in available:
                return False
        return True

    def to_dict(self) -> dict[str, object]:
        return {
            "opportunity_id": self.opportunity_id,
            "kind": self.kind,
            "condition": self.condition,
            "score": self.score,
            "at_ticks": self.at_ticks,
            "eligibility": list(self.eligibility),
            "available_from": self.available_from,
            "expires_at": self.expires_at,
            "reward_refs": list(self.reward_refs),
            "risk_refs": list(self.risk_refs),
            "evidence_refs": list(self.evidence_refs),
            "world_state_refs": list(self.world_state_refs),
            "status": self.status,
            "actor_id": self.actor_id,
            "decision_ref": self.decision_ref,
            "schema_version": self.schema_version,
        }


class OpportunityLifecycle:
    """Pure lifecycle transitions for proposal records; no persistence or commit path."""

    def mark_eligible(
        self,
        opportunity: Opportunity,
        *,
        actor_id: str,
        world_state_refs: tuple[str, ...] = (),
        at_ticks: int,
    ) -> Opportunity:
        if not opportunity.eligible_for(actor_id, world_state_refs, at_ticks):
            raise ChallengeValidationError("opportunity is not eligible for this actor/context")
        return replace(opportunity, status="eligible", actor_id=actor_id)

    def offer(self, opportunity: Opportunity, *, at_ticks: int) -> Opportunity:
        if opportunity.status not in {"eligible", "proposed"} or not opportunity.is_open(at_ticks):
            raise ChallengeValidationError("only an open opportunity can be offered")
        if not opportunity.actor_id:
            raise ChallengeValidationError("an opportunity must be actor-eligible before offering")
        return replace(opportunity, status="offered")

    def accept(self, opportunity: Opportunity, *, at_ticks: int) -> Opportunity:
        if opportunity.status != "offered" or not opportunity.is_open(at_ticks):
            raise ChallengeValidationError("only an open offer can be accepted")
        return replace(opportunity, status="accepted")

    def ignore(self, opportunity: Opportunity, *, decision_ref: str = "") -> Opportunity:
        if opportunity.status not in {"eligible", "offered"}:
            raise ChallengeValidationError("only an eligible or offered opportunity can be ignored")
        return replace(opportunity, status="ignored", decision_ref=decision_ref)

    def decline(self, opportunity: Opportunity, *, decision_ref: str = "") -> Opportunity:
        if opportunity.status != "offered":
            raise ChallengeValidationError("only an offered opportunity can be declined")
        return replace(opportunity, status="declined", decision_ref=decision_ref)

    def expire(self, opportunity: Opportunity, *, at_ticks: int) -> Opportunity:
        if opportunity.expires_at is None or at_ticks < opportunity.expires_at:
            raise ChallengeValidationError("opportunity has not reached its expiry")
        if opportunity.status in {"completed", "ignored", "declined", "expired"}:
            return opportunity
        return replace(opportunity, status="expired")

    def complete(
        self,
        opportunity: Opportunity,
        *,
        evidence_refs: tuple[str, ...],
        at_ticks: int,
    ) -> Opportunity:
        if opportunity.status != "accepted" or not opportunity.is_open(at_ticks):
            raise ChallengeValidationError("only an active accepted opportunity can complete")
        if not set(opportunity.evidence_refs).issubset(evidence_refs):
            raise ChallengeValidationError("completion evidence does not satisfy the opportunity")
        return replace(opportunity, status="completed")


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
