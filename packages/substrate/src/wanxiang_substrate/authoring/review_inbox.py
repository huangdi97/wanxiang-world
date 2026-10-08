"""Impact-scored review inbox and reversible batch decisions (M68)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.review.decisions import ReviewDecision, ReviewLedger


@dataclass(frozen=True, slots=True)
class ImpactContext:
    downstream_count: int = 0
    conflict: bool = False
    rights_blocked: bool = False
    uncertainty: float | None = None
    affected_entities: tuple[str, ...] = ()
    affected_events: tuple[str, ...] = ()
    affected_scenarios: tuple[str, ...] = ()
    package_sections: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ImpactScore:
    candidate_id: str
    score: float
    reasons: tuple[str, ...]
    uncertainty: float = 0.0
    conflict: bool = False
    rights_blocked: bool = False


@dataclass(frozen=True, slots=True)
class ImpactPreview:
    candidate_id: str
    entities: tuple[str, ...]
    events: tuple[str, ...]
    scenarios: tuple[str, ...]
    package_sections: tuple[str, ...]
    source_refs: tuple[str, ...]
    preview_hash: str


@dataclass(frozen=True, slots=True)
class AutoApprovalPolicy:
    max_impact: float = 0.3
    min_confidence: float = 0.7
    max_uncertainty: float = 0.3
    allow_conflicts: bool = False
    allow_rights_blocked: bool = False

    def allows(self, candidate: CandidateEnvelope, impact: ImpactScore) -> bool:
        return (
            impact.score <= self.max_impact
            and candidate.confidence >= self.min_confidence
            and impact.uncertainty <= self.max_uncertainty
            and (self.allow_conflicts or not impact.conflict)
            and (self.allow_rights_blocked or not impact.rights_blocked)
        )


@dataclass(frozen=True, slots=True)
class InboxItem:
    candidate: CandidateEnvelope
    impact: ImpactScore
    auto_approved: bool
    preview: ImpactPreview | None = None

    @property
    def needs_human_review(self) -> bool:
        return not self.auto_approved


@dataclass(frozen=True, slots=True)
class ReviewAudit:
    audit_id: str
    decision_id: str
    target_id: str
    actor_type: str
    actor_id: str
    rationale: str
    impact_score: float
    source_refs: tuple[str, ...]


class ReviewInbox:
    """Routes low-impact items automatically and preserves review provenance."""

    def __init__(self, ledger: ReviewLedger | None = None) -> None:
        self.ledger = ledger or ReviewLedger()
        self._audits: tuple[ReviewAudit, ...] = ()

    def score(
        self, candidate: CandidateEnvelope, context: ImpactContext | None = None
    ) -> ImpactScore:
        context = context or self._context_from_candidate(candidate)
        uncertainty = (
            context.uncertainty if context.uncertainty is not None else 1.0 - candidate.confidence
        )
        reasons: list[str] = []
        score = min(0.3, max(0.0, uncertainty) * 0.3)
        if uncertainty > 0.3:
            reasons.append("uncertainty")
        if candidate.kind in ("identity", "relation", "event", "organization"):
            score += 0.35
            reasons.append("downstream identity/topology effect")
        if context.downstream_count:
            score += min(0.25, context.downstream_count * 0.05)
            reasons.append("downstream references")
        if context.conflict:
            score += 0.2
            reasons.append("source conflict")
        if context.rights_blocked:
            score += 0.3
            reasons.append("rights blocker")
        return ImpactScore(
            candidate.candidate_id,
            min(score, 1.0),
            tuple(reasons),
            uncertainty,
            context.conflict,
            context.rights_blocked,
        )

    def build(
        self,
        candidates: tuple[CandidateEnvelope, ...],
        *,
        contexts: dict[str, ImpactContext] | None = None,
        policy: AutoApprovalPolicy | None = None,
    ) -> tuple[InboxItem, ...]:
        active_policy = policy or AutoApprovalPolicy()
        contexts = contexts or {}
        return tuple(
            InboxItem(
                candidate,
                impact,
                active_policy.allows(candidate, impact),
                self.preview(candidate, contexts.get(candidate.candidate_id)),
            )
            for candidate in candidates
            for impact in (self.score(candidate, contexts.get(candidate.candidate_id)),)
        )

    def review_queue(self, items: tuple[InboxItem, ...]) -> tuple[InboxItem, ...]:
        """Return only human work, highest downstream impact first."""
        return tuple(
            sorted(
                (item for item in items if item.needs_human_review),
                key=lambda item: (-item.impact.score, item.candidate.candidate_id),
            )
        )

    def preview(
        self, candidate: CandidateEnvelope, context: ImpactContext | None = None
    ) -> ImpactPreview:
        context = context or self._context_from_candidate(candidate)
        fields = candidate.fields
        entities = context.affected_entities or tuple(
            fields[key]
            for key in ("entity", "entity_id", "identity_key", "source_key", "target_key")
            if fields.get(key)
        )
        events = context.affected_events or tuple(
            fields[key] for key in ("event", "event_id", "event_type") if fields.get(key)
        )
        scenarios = context.affected_scenarios or tuple(
            fields[key] for key in ("scenario", "scenario_id") if fields.get(key)
        )
        sections = context.package_sections or (
            f"candidates.{candidate.kind}",
            "world_draft",
            "preview",
        )
        material = "|".join((*entities, *events, *scenarios, *sections, *candidate.source_refs))
        return ImpactPreview(
            candidate.candidate_id,
            tuple(dict.fromkeys(entities)),
            tuple(dict.fromkeys(events)),
            tuple(dict.fromkeys(scenarios)),
            tuple(dict.fromkeys(sections)),
            candidate.source_refs,
            hashlib.sha256(material.encode()).hexdigest(),
        )

    def approve_low_risk(
        self, items: tuple[InboxItem, ...], *, reviewer: str = "reference"
    ) -> tuple[ReviewDecision, ...]:
        decisions: list[ReviewDecision] = []
        for item in items:
            if not item.auto_approved:
                continue
            existing = self.ledger.latest(item.candidate.candidate_id)
            if existing is not None and existing.action == "approve":
                decisions.append(existing)
                continue
            decision = self.ledger.record(
                ReviewDecision(
                    decision_id=f"auto_{item.candidate.candidate_id}",
                    target_id=item.candidate.candidate_id,
                    action="approve",
                    reviewer=reviewer,
                    rationale="low-impact candidate under deterministic policy",
                )
            )
            self._audit(decision, item, "rule", reviewer)
            decisions.append(decision)
        return tuple(decisions)

    def batch(
        self, candidate_ids: tuple[str, ...], *, action: str, reviewer: str, rationale: str
    ) -> tuple[ReviewDecision, ...]:
        normalized = "defer" if action == "keep_unknown" else action
        decisions: list[ReviewDecision] = []
        for candidate_id in dict.fromkeys(candidate_ids):
            existing = self.ledger.latest(candidate_id)
            if existing is not None and existing.action == normalized:
                decisions.append(existing)
                continue
            decision = self.ledger.record(
                ReviewDecision(
                    decision_id=f"batch_{candidate_id}_{normalized}",
                    target_id=candidate_id,
                    action=normalized,  # type: ignore[arg-type]
                    reviewer=reviewer,
                    rationale=rationale,
                )
            )
            self._audit(decision, None, "human", reviewer)
            decisions.append(decision)
        return tuple(decisions)

    def audit(self) -> tuple[ReviewAudit, ...]:
        return self._audits

    def _audit(
        self,
        decision: ReviewDecision,
        item: InboxItem | None,
        actor_type: str,
        actor_id: str,
    ) -> None:
        self._audits += (
            ReviewAudit(
                f"audit_{decision.decision_id}",
                decision.decision_id,
                decision.target_id,
                actor_type,
                actor_id,
                decision.rationale,
                item.impact.score if item else 0.0,
                item.candidate.source_refs if item else decision.evidence_refs,
            ),
        )

    @staticmethod
    def _context_from_candidate(candidate: CandidateEnvelope) -> ImpactContext:
        fields = candidate.fields
        try:
            downstream = max(0, int(fields.get("downstream_count", "0")))
        except ValueError:
            downstream = 0
        raw_uncertainty = fields.get("uncertainty")
        try:
            uncertainty = float(raw_uncertainty) if raw_uncertainty is not None else None
        except ValueError:
            uncertainty = None
        return ImpactContext(
            downstream_count=downstream,
            conflict=fields.get("conflict", "").lower() in ("1", "true", "yes"),
            rights_blocked=fields.get("rights", "").lower() in ("blocked", "denied"),
            uncertainty=uncertainty,
        )
