"""Impact-scored review inbox and reversible batch decisions (M68)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.review.decisions import ReviewDecision, ReviewLedger


@dataclass(frozen=True, slots=True)
class ImpactScore:
    candidate_id: str
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InboxItem:
    candidate: CandidateEnvelope
    impact: ImpactScore
    auto_approved: bool


class ReviewInbox:
    """Routes only low-impact candidates to automatic review decisions."""

    def __init__(self, ledger: ReviewLedger | None = None) -> None:
        self.ledger = ledger or ReviewLedger()

    def score(self, candidate: CandidateEnvelope) -> ImpactScore:
        reasons: list[str] = []
        score = 0.0
        if candidate.kind in ("identity", "relation", "event"):
            score += 0.5
            reasons.append("world topology or identity")
        if candidate.confidence < 0.5:
            score += 0.3
            reasons.append("low confidence")
        if len(candidate.source_refs) > 1:
            score += 0.2
            reasons.append("multi-source effect")
        return ImpactScore(candidate.candidate_id, min(score, 1.0), tuple(reasons))

    def build(self, candidates: tuple[CandidateEnvelope, ...]) -> tuple[InboxItem, ...]:
        return tuple(
            InboxItem(candidate, impact, impact.score < 0.3)
            for candidate in candidates
            for impact in (self.score(candidate),)
        )

    def approve_low_risk(
        self, items: tuple[InboxItem, ...], *, reviewer: str = "reference"
    ) -> tuple[ReviewDecision, ...]:
        decisions: list[ReviewDecision] = []
        for item in items:
            if not item.auto_approved:
                continue
            decisions.append(
                self.ledger.record(
                    ReviewDecision(
                        decision_id=f"auto_{item.candidate.candidate_id}",
                        target_id=item.candidate.candidate_id,
                        action="approve",
                        reviewer=reviewer,
                        rationale="low-impact candidate under deterministic policy",
                    )
                )
            )
        return tuple(decisions)

    def batch(
        self, candidate_ids: tuple[str, ...], *, action: str, reviewer: str, rationale: str
    ) -> tuple[ReviewDecision, ...]:
        return tuple(
            self.ledger.record(
                ReviewDecision(
                    decision_id=f"batch_{candidate_id}_{index}",
                    target_id=candidate_id,
                    action=action,  # type: ignore[arg-type]
                    reviewer=reviewer,
                    rationale=rationale,
                )
            )
            for index, candidate_id in enumerate(candidate_ids, start=1)
        )
