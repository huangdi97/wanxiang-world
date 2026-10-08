"""Review decision ledger (G58D).

Approve / reject / edit / merge / split / defer / request-evidence decisions
are append-only and reversible: history is never erased; a later decision may
supersede an earlier one. Decisions never mutate the reviewed candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

ReviewAction = Literal["approve", "reject", "edit", "merge", "split", "defer", "request_evidence"]
VALID_ACTIONS = ("approve", "reject", "edit", "merge", "split", "defer", "request_evidence")


@dataclass(frozen=True, slots=True)
class ReviewDecision:
    decision_id: str
    target_id: str
    action: ReviewAction
    reviewer: str
    rationale: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.decision_id or not self.target_id or not self.reviewer:
            raise ContractError("decision requires ids and reviewer")
        if self.action not in VALID_ACTIONS:
            raise ContractError(f"invalid review action {self.action!r}")
        if not self.rationale:
            raise ContractError("decision requires a rationale")


class ReviewLedger:
    """Append-only, reversible review history per target."""

    def __init__(self) -> None:
        self._history: dict[str, tuple[ReviewDecision, ...]] = {}

    def record(self, decision: ReviewDecision) -> ReviewDecision:
        self._history[decision.target_id] = self._history.get(decision.target_id, ()) + (decision,)
        return decision

    def history(self, target_id: str) -> tuple[ReviewDecision, ...]:
        return self._history.get(target_id, ())

    def latest(self, target_id: str) -> ReviewDecision | None:
        history = self.history(target_id)
        return history[-1] if history else None

    def targets(self) -> tuple[str, ...]:
        return tuple(sorted(self._history))
