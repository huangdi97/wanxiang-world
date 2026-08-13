"""Director runtime (G07D).

Directors propose; they never directly commit or rewrite actor beliefs/persona.
WorldDirector schedules focus/time/events, NarrativeDirector scores goals/
attractors as signals, PerformanceDirector emits projection-only metadata, and
every world-changing proposal must traverse normal validation. Character/persona
delta candidates require actor-logic review.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.reality.errors import DirectorError


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
