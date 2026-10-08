"""Director runtime (G07D).

Directors propose; they never directly commit or rewrite actor beliefs/persona.
WorldDirector schedules focus/time/events, NarrativeDirector scores goals/
attractors as signals, PerformanceDirector emits projection-only metadata, and
every world-changing proposal must traverse normal validation. Character/persona
delta candidates require actor-logic review.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from wanxiang_substrate.reality.errors import DirectorError

DirectorMode = Literal["CANON", "DIRECTED", "LIVING", "EXPERIMENT"]
DIRECTOR_MODES = ("CANON", "DIRECTED", "LIVING", "EXPERIMENT")
DEFAULT_PROPOSAL_TYPES: dict[DirectorMode, tuple[str, ...]] = {
    "CANON": ("opportunity", "constraint", "score", "canon_attractor"),
    "DIRECTED": ("opportunity", "challenge", "constraint", "focus", "score"),
    "LIVING": ("opportunity", "challenge", "event", "relationship", "focus"),
    "EXPERIMENT": ("opportunity", "challenge", "intervention", "branch", "experiment"),
}


@dataclass(frozen=True, slots=True)
class DirectorAudit:
    """Projection-only audit record for a policy decision or mode switch."""

    audit_id: str
    event_type: str
    mode: DirectorMode
    proposal_type: str = ""
    previous_mode: DirectorMode | None = None
    next_mode: DirectorMode | None = None
    at_ticks: int = 0
    reason: str = ""

    def __post_init__(self) -> None:
        if not self.audit_id or not self.event_type or self.mode not in DIRECTOR_MODES:
            raise DirectorError("director audit requires id, event type and valid mode")
        if self.at_ticks < 0:
            raise DirectorError("director audit time must be non-negative")


@dataclass(frozen=True, slots=True)
class DirectorDecision:
    """A policy evaluation, never an authorization to commit."""

    allowed: bool
    mode: DirectorMode
    proposal_type: str
    reason: str
    audit: DirectorAudit


@dataclass(frozen=True, slots=True)
class DirectorTransition:
    """A new policy plus its auditable mode transition."""

    policy: DirectorPolicy
    audit: DirectorAudit


@dataclass(frozen=True, slots=True)
class DirectorPolicy:
    """Mode contract for director proposals; it has no commit/runtime handle."""

    mode: DirectorMode = "LIVING"
    allowed_proposal_types: tuple[str, ...] = ()
    policy_version: int = 1

    def __post_init__(self) -> None:
        if self.mode not in DIRECTOR_MODES:
            raise DirectorError(f"invalid director mode {self.mode!r}")
        if self.policy_version < 1:
            raise DirectorError("director policy version must be positive")
        configured = self.allowed_proposal_types or DEFAULT_PROPOSAL_TYPES[self.mode]
        if not configured or any(not item for item in configured):
            raise DirectorError("director policy needs non-empty proposal types")
        object.__setattr__(self, "allowed_proposal_types", tuple(dict.fromkeys(configured)))

    @classmethod
    def for_mode(cls, mode: DirectorMode, *, policy_version: int = 1) -> DirectorPolicy:
        return cls(mode=mode, policy_version=policy_version)

    def allows(self, proposal_type: str) -> bool:
        return proposal_type in self.allowed_proposal_types

    def can_emit(self, proposal_type: str) -> bool:
        """Alias used by proposal producers; still only evaluates policy."""

        return self.allows(proposal_type)

    def evaluate(self, proposal: DirectorProposal, *, at_ticks: int = 0) -> DirectorDecision:
        proposal_type = proposal.action_type
        allowed = self.allows(proposal_type)
        audit = DirectorAudit(
            audit_id=f"director_policy:{self.mode}:{proposal.proposal_id}",
            event_type="proposal_evaluated",
            mode=self.mode,
            proposal_type=proposal_type,
            at_ticks=at_ticks,
            reason="allowed" if allowed else "proposal type is not allowed in this mode",
        )
        return DirectorDecision(
            allowed=allowed,
            mode=self.mode,
            proposal_type=proposal_type,
            reason=audit.reason,
            audit=audit,
        )

    def transition(
        self,
        next_mode: DirectorMode,
        *,
        at_ticks: int,
        reason: str,
    ) -> DirectorTransition:
        if next_mode not in DIRECTOR_MODES:
            raise DirectorError(f"invalid director mode {next_mode!r}")
        if at_ticks < 0 or not reason:
            raise DirectorError("mode transition requires non-negative time and reason")
        next_policy = replace(self, mode=next_mode, allowed_proposal_types=())
        audit = DirectorAudit(
            audit_id=f"director_transition:{self.mode}:{next_mode}:{at_ticks}",
            event_type="mode_transition",
            mode=next_mode,
            previous_mode=self.mode,
            next_mode=next_mode,
            at_ticks=at_ticks,
            reason=reason,
        )
        return DirectorTransition(policy=next_policy, audit=audit)


@dataclass(frozen=True, slots=True)
class DirectorProposal:
    """A proposal a director wants the world to execute (never a commit)."""

    proposal_id: str
    director: str
    action_type: str
    payload: dict[str, object] | None = None
    version: int = 1
    rationale: str = ""

    def __post_init__(self) -> None:
        if self.payload is None:
            object.__setattr__(self, "payload", {})


@dataclass(frozen=True, slots=True)
class NarrativeSignal:
    """Scoring/attractor signal (projection-only, non-authoritative)."""

    goal_id: str
    attractor: str
    score: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.score <= 1.0):
            raise DirectorError("narrative score must be within [0,1]")


class WorldDirector:
    """Deterministic reference director for focus/time/event scheduling."""

    def __init__(self, version: int = 1) -> None:
        self._version = version

    def propose_focus(
        self, focus_id: str, at_ticks: int, *, action_type: str = "focus.set"
    ) -> DirectorProposal:
        return DirectorProposal(
            proposal_id=f"dir_focus_{focus_id}",
            director="world",
            action_type=action_type,
            payload={"focus_id": focus_id, "at_ticks": at_ticks},
            version=self._version,
            rationale="scheduled focus",
        )


class NarrativeDirector:
    """Goals/attractors as scoring signals; no canonical mutation."""

    def __init__(self, version: int = 1) -> None:
        self._version = version

    def score(
        self, goal_id: str, attractor: str, reached: bool, weight: float = 1.0
    ) -> NarrativeSignal:
        base = 1.0 if reached else 0.2
        return NarrativeSignal(goal_id=goal_id, attractor=attractor, score=min(1.0, base * weight))


class PerformanceDirector:
    """Directives are projection-only metadata (camera/lighting/focus)."""

    def __init__(self, version: int = 1) -> None:
        self._version = version

    def directive(self, directive_id: str, kind: str, target: str) -> dict[str, object]:
        return {
            "directive_id": directive_id,
            "kind": kind,
            "target": target,
            "projection_only": True,
            "version": self._version,
        }


class DirectorReview:
    """Character/persona delta candidates require actor-logic review."""

    def __init__(self) -> None:
        self._reviews: dict[str, str] = {}

    def require_review(self, proposal: DirectorProposal) -> bool:
        return proposal.action_type.startswith("character.") or proposal.action_type.startswith(
            "persona."
        )

    def approve(self, proposal: DirectorProposal, reviewer: str) -> None:
        if not self.require_review(proposal):
            raise DirectorError(f"{proposal.action_type!r} does not require actor-logic review")
        self._reviews[proposal.proposal_id] = reviewer

    def reviewed(self, proposal_id: str) -> bool:
        return proposal_id in self._reviews
