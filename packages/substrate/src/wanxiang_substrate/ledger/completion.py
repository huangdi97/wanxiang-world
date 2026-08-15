"""Completion records with support refs / confidence / review status (G35H).

Extends the G04D CompletionLedger truth taxonomy with runnable completion
records: content needed to run but not explicit in source. can_enter_canon is
FALSE by default; only a human/rule review with evidence may lift it. Review
status follows source E0-E5 semantics: pending (E0-E2), approved (E3),
rejected (E4), superseded (E5); E4/E5 are terminal and never auto-upgrade back
to E0. Conflicting completion claims are preserved (never overwritten).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.ledger.errors import InvalidPromotion, ItemNotFound, ReviewRequired
from wanxiang_substrate.sources.evidence import AUTHORIZED_REVIEWERS

ReviewStatus = Literal["pending", "approved", "rejected", "superseded"]
VALID_REVIEW_STATUSES = ("pending", "approved", "rejected", "superseded")
REVIEW_STAGE: dict[ReviewStatus, str] = {
    "pending": "E0-E2",
    "approved": "E3",
    "rejected": "E4",
    "superseded": "E5",
}

ReviewKind = Literal["approve", "reject"]
VALID_REVIEW_KINDS = ("approve", "reject")


@dataclass(frozen=True, slots=True)
class CompletionRecord:
    """A completion record: needed but not source-explicit, with review status."""

    completion_id: str
    description: str
    support_refs: tuple[str, ...]
    confidence: float
    review_status: ReviewStatus = "pending"
    reviewer: str = ""
    rationale: str = ""
    review_version: int = 0
    can_enter_canon: bool = False
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.completion_id or not self.description:
            raise ContractError("completion record requires id and description")
        if not self.support_refs:
            raise ContractError("completion record requires at least one support ref")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("confidence must be within [0,1]")
        if self.review_status not in VALID_REVIEW_STATUSES:
            raise ContractError(f"invalid review status {self.review_status!r}")
        if self.review_version < 0:
            raise ContractError("review_version must be non-negative")

    @property
    def stage(self) -> str:
        return REVIEW_STAGE[self.review_status]


@dataclass(frozen=True, slots=True)
class CompletionDecision:
    """An immutable review decision for a completion record."""

    decision_id: str
    completion_id: str
    decision: ReviewKind
    reviewer: str
    rationale: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.decision_id or not self.completion_id or not self.reviewer:
            raise ContractError("decision requires id, completion id and reviewer")
        if self.decision not in VALID_REVIEW_KINDS:
            raise ContractError(f"invalid decision {self.decision!r}")
        if not self.rationale:
            raise ContractError("decision requires a rationale")


class CompletionReviewLedger:
    """Append-only completion records + review decisions.

    submit() never overwrites (conflicting claims preserved). review() follows
    E0-E5 stage semantics: pending -> approved/rejected; approved -> superseded
    via supersede(); rejected/superseded are terminal and never auto-upgrade.
    """

    def __init__(
        self,
        *,
        min_confidence: float = 0.7,
        require_evidence: bool = True,
        authorized_reviewers: tuple[str, ...] = AUTHORIZED_REVIEWERS,
    ) -> None:
        if not (0.0 <= min_confidence <= 1.0):
            raise ValueError("min_confidence must be within [0,1]")
        self._min_confidence = min_confidence
        self._require_evidence = require_evidence
        self._authorized = authorized_reviewers
        self._records: dict[str, CompletionRecord] = {}
        self._history: dict[str, tuple[CompletionDecision, ...]] = {}

    def submit(self, record: CompletionRecord) -> CompletionRecord:
        """Register a completion record; conflicting claims are never merged.

        A completion_id is registered once: re-submitting (which could reset a
        terminal E4/E5 record back to E0) is rejected so history is preserved.
        """
        if record.completion_id in self._records:
            raise InvalidPromotion(
                f"completion {record.completion_id!r} already registered; "
                "conflicting claims must use distinct ids"
            )
        self._records[record.completion_id] = record
        self._history.setdefault(record.completion_id, ())
        return record

    def get(self, completion_id: str) -> CompletionRecord | None:
        return self._records.get(completion_id)

    def require(self, completion_id: str) -> CompletionRecord:
        record = self.get(completion_id)
        if record is None:
            raise ItemNotFound(f"completion {completion_id!r} not found")
        return record

    def review(self, decision: CompletionDecision) -> CompletionRecord:
        """Apply a review decision under E0-E5 stage semantics."""
        record = self.require(decision.completion_id)
        if record.review_status in ("rejected", "superseded"):
            raise InvalidPromotion(
                f"completion {record.completion_id!r} is terminal ({record.stage}); "
                "E4/E5 never auto-upgrade to E0",
            )
        if decision.reviewer not in self._authorized:
            raise ReviewRequired(f"reviewer {decision.reviewer!r} is not authorized")
        if decision.decision == "approve":
            if record.confidence < self._min_confidence:
                raise ReviewRequired("confidence is below the policy threshold")
            if self._require_evidence and not decision.evidence_refs:
                raise ReviewRequired("approval requires evidence refs")
            status: ReviewStatus = "approved"
            can_enter_canon = True
        else:
            status = "rejected"
            can_enter_canon = False
        updated = CompletionRecord(
            completion_id=record.completion_id,
            description=record.description,
            support_refs=record.support_refs,
            confidence=record.confidence,
            review_status=status,
            reviewer=decision.reviewer,
            rationale=decision.rationale,
            review_version=record.review_version + 1,
            can_enter_canon=can_enter_canon,
            evidence_refs=tuple(sorted(set(record.evidence_refs) | set(decision.evidence_refs))),
        )
        self._records[record.completion_id] = updated
        self._history[record.completion_id] = self._history[record.completion_id] + (decision,)
        return updated

    def supersede(self, completion_id: str, *, reviewer: str, rationale: str) -> CompletionRecord:
        """Mark a record superseded (E5) when a newer source claim replaces it."""
        record = self.require(completion_id)
        if record.review_status in ("rejected", "superseded"):
            raise InvalidPromotion(
                f"completion {completion_id!r} is already terminal ({record.stage})"
            )
        if reviewer not in self._authorized:
            raise ReviewRequired(f"reviewer {reviewer!r} is not authorized")
        updated = CompletionRecord(
            completion_id=record.completion_id,
            description=record.description,
            support_refs=record.support_refs,
            confidence=record.confidence,
            review_status="superseded",
            reviewer=reviewer,
            rationale=rationale,
            review_version=record.review_version + 1,
            can_enter_canon=False,
            evidence_refs=record.evidence_refs,
        )
        self._records[completion_id] = updated
        return updated

    def history(self, completion_id: str) -> tuple[CompletionDecision, ...]:
        self.require(completion_id)
        return self._history.get(completion_id, ())

    def by_status(self, status: ReviewStatus) -> tuple[CompletionRecord, ...]:
        return tuple(
            record
            for record in sorted(self._records.values(), key=lambda r: r.completion_id)
            if record.review_status == status
        )

    def conflicts(self) -> tuple[tuple[str, str], ...]:
        """Pairs of records sharing a description but with different support refs."""
        by_desc: dict[str, list[str]] = {}
        for record in self._records.values():
            by_desc.setdefault(record.description, []).append(record.completion_id)
        pairs: list[tuple[str, str]] = []
        for ids in by_desc.values():
            for index, first in enumerate(ids):
                for second in ids[index + 1 :]:
                    if self._records[first].support_refs != self._records[second].support_refs:
                        pairs.append((first, second))
        return tuple(sorted(pairs))

    def all(self) -> tuple[CompletionRecord, ...]:
        return tuple(sorted(self._records.values(), key=lambda r: r.completion_id))


class CompletionStudio:
    """Read-only Studio queries over the completion review ledger."""

    def __init__(self, ledger: CompletionReviewLedger) -> None:
        self._ledger = ledger

    def pending_review(self) -> tuple[CompletionRecord, ...]:
        return self._ledger.by_status("pending")

    def canon_candidates(self) -> tuple[CompletionRecord, ...]:
        """Approved records that may enter canon (reviewed + evidence)."""
        return tuple(
            record for record in self._ledger.by_status("approved") if record.can_enter_canon
        )

    def conflicts(self) -> tuple[tuple[str, str], ...]:
        return self._ledger.conflicts()

    def stage_summary(self) -> dict[ReviewStatus, int]:
        summary = dict.fromkeys(VALID_REVIEW_STATUSES, 0)
        for record in self._ledger.all():
            summary[record.review_status] += 1
        return summary


def apply_batch_review(
    ledger: CompletionReviewLedger,
    decisions: tuple[CompletionDecision, ...],
) -> tuple[CompletionRecord, ...]:
    """Apply a batch of review decisions in order (CLI/API batch use case)."""
    return tuple(ledger.review(decision) for decision in decisions)
