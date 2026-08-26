"""Evidence-bound belief revision projections, separate from world truth."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.epistemic.model import BeliefAssertion, BeliefStance

RevisionKind = Literal["support", "contradict", "refine", "unknown"]
TemporalScope = Literal["past", "present", "future"]


@dataclass(frozen=True, slots=True)
class BeliefEvidence:
    """A reference to actor-visible evidence; content remains outside this record."""

    evidence_ref: str
    actor_id: EntityId
    at_ticks: int
    strength: float
    temporal: TemporalScope = "present"

    def __post_init__(self) -> None:
        if not self.evidence_ref.strip():
            raise ContractError("belief evidence ref cannot be blank")
        if self.at_ticks < 0 or not 0.0 <= self.strength <= 1.0:
            raise ContractError("belief evidence time or strength is invalid")
        if self.temporal not in ("past", "present", "future"):
            raise ContractError(f"invalid belief evidence temporal scope {self.temporal!r}")


@dataclass(frozen=True, slots=True)
class BeliefRevision:
    """Before/after lineage for one belief projection revision."""

    revision_id: str
    actor_id: EntityId
    kind: RevisionKind
    before: BeliefAssertion
    after: BeliefAssertion
    evidence_ref: str
    reason: str

    def __post_init__(self) -> None:
        if not self.revision_id.strip() or not self.reason.strip():
            raise ContractError("belief revision requires id and reason")
        if self.kind not in ("support", "contradict", "refine", "unknown"):
            raise ContractError(f"invalid belief revision kind {self.kind!r}")
        if self.before.actor_id != self.actor_id or self.after.actor_id != self.actor_id:
            raise ContractError("belief revision actor does not match lineage")
        if self.before.belief_id == self.after.belief_id:
            raise ContractError("belief revision must create a new assertion id")
        if not self.evidence_ref.strip():
            raise ContractError("belief revision evidence ref cannot be blank")

    @property
    def is_world_truth(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class BeliefRevisionChain:
    """Small actor-local lineage projection; it is not a canonical event store."""

    actor_id: EntityId
    assertions: tuple[BeliefAssertion, ...]
    revisions: tuple[BeliefRevision, ...] = ()

    @classmethod
    def start(cls, assertion: BeliefAssertion) -> BeliefRevisionChain:
        return cls(assertion.actor_id, (assertion,))

    @property
    def current(self) -> BeliefAssertion:
        return self.assertions[-1]

    def append(self, revision: BeliefRevision) -> BeliefRevisionChain:
        if revision.actor_id != self.actor_id or revision.before != self.current:
            raise ContractError("belief revision does not continue the current lineage")
        return BeliefRevisionChain(
            actor_id=self.actor_id,
            assertions=self.assertions + (revision.after,),
            revisions=self.revisions + (revision,),
        )


class BeliefRevisionEngine:
    """Create support/contradict/refine/unknown proposals without committing."""

    def revise(
        self,
        before: BeliefAssertion,
        *,
        revision_id: str,
        kind: RevisionKind,
        evidence: BeliefEvidence,
        reason: str,
        new_belief_id: EntityId,
        refined_proposition: str | None = None,
    ) -> BeliefRevision:
        if evidence.actor_id != before.actor_id:
            raise ContractError("belief evidence belongs to a different actor")
        if evidence.temporal == "future":
            raise ContractError("future evidence cannot revise a runtime belief")
        if new_belief_id == before.belief_id:
            raise ContractError("belief revision id must differ from source belief")
        confidence, stance, proposition = self._outcome(before, kind, evidence, refined_proposition)
        after = BeliefAssertion(
            belief_id=new_belief_id,
            actor_id=before.actor_id,
            proposition=proposition,
            confidence=confidence,
            at_ticks=evidence.at_ticks,
            source_ref=evidence.evidence_ref,
            status="active",
            supersedes=before.belief_id,
            stance=stance,
        )
        return BeliefRevision(
            revision_id=revision_id,
            actor_id=before.actor_id,
            kind=kind,
            before=before,
            after=after,
            evidence_ref=evidence.evidence_ref,
            reason=reason,
        )

    @staticmethod
    def _outcome(
        before: BeliefAssertion,
        kind: RevisionKind,
        evidence: BeliefEvidence,
        refined_proposition: str | None,
    ) -> tuple[float, BeliefStance, str]:
        if kind == "support":
            return (
                round(min(1.0, before.confidence + evidence.strength), 6),
                "supported",
                before.proposition,
            )
        if kind == "contradict":
            return (
                round(max(0.0, before.confidence - evidence.strength), 6),
                "contested",
                before.proposition,
            )
        if kind == "refine":
            if not refined_proposition or not refined_proposition.strip():
                raise ContractError("refinement requires a proposition")
            return (
                round(min(1.0, before.confidence + evidence.strength / 2), 6),
                "supported",
                refined_proposition,
            )
        return 0.5, "unknown", before.proposition
