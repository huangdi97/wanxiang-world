"""Institution/Organization rule promotion chain (G32E).

A controlled chain: group pattern -> institution candidate (with evidence) ->
counterfactual/stability validation -> human/policy approval -> LawCommit.

An UNapproved candidate never changes Gamma (the law set); only an approved +
validated candidate may be committed as a Law Commit through the single
CommitAuthority, and that LawCommit is replayable like any other event.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.ids import BranchId, CommandId, ComponentId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.state import InMemoryCanonicalState

MIN_STABILITY = 0.5
APPROVERS = ("reviewer", "policy")


@dataclass(frozen=True, slots=True)
class InstitutionCandidate:
    """An institution rule candidate with evidence and stability score."""

    candidate_id: str
    rule: str
    evidence: tuple[str, ...]
    origin: str
    stability_score: float = 0.0
    approved: bool = False
    role_refs: tuple[str, ...] = ()
    resource_refs: tuple[str, ...] = ()
    process_refs: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    reviewed_by: str | None = None

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.rule or not self.evidence:
            raise ValueError("institution candidate requires id, rule and evidence")
        for name, refs in (
            ("role", self.role_refs),
            ("resource", self.resource_refs),
            ("process", self.process_refs),
            ("provenance", self.provenance_refs),
        ):
            if len(set(refs)) != len(refs) or any(not ref.strip() for ref in refs):
                raise ValueError(f"institution {name} refs must be unique and non-empty")


class InstitutionPromotionChain:
    """submit -> validate -> approve -> LawCommit (controlled, replayable)."""

    def __init__(
        self, authority: CommitAuthority, rules: RuntimeVersion, schema: SchemaVersion
    ) -> None:
        self._authority = authority
        self._rules = rules
        self._schema = schema

    def validate(self, candidate: InstitutionCandidate) -> bool:
        """Counterfactual/stability check: score >= threshold + evidence present."""
        return candidate.stability_score >= MIN_STABILITY and bool(candidate.evidence)

    def approve(self, candidate: InstitutionCandidate, approver: str) -> InstitutionCandidate:
        """Human/policy approval hook; approver must be a reviewer/policy."""
        if approver not in APPROVERS:
            raise PermissionDenied(f"approver {approver!r} is not authorized; expected {APPROVERS}")
        return replace(candidate, approved=True)

    def promote(
        self,
        candidate: InstitutionCandidate,
        state: InMemoryCanonicalState,
        *,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        world_time: WorldTime,
    ) -> CommittedEvent:
        """Only approved + validated candidates produce a LawCommit."""
        if not candidate.approved:
            raise PermissionDenied(
                f"candidate {candidate.candidate_id!r} is not approved; Gamma unchanged"
            )
        if not self.validate(candidate):
            raise PermissionDenied(
                f"candidate {candidate.candidate_id!r} fails stability validation"
            )
        law_entity = EntityId(f"law_{candidate.candidate_id}")
        result = self._authority.commit(
            state,
            CommitRequest(
                command_id=CommandId(f"law_{candidate.candidate_id}"),
                instance_id=instance_id,
                branch_id=branch_id,
                expected_revision=state.revision,
                delta=ProposedWorldDelta(
                    operations=(
                        EntityCreate(
                            entity_id=law_entity,
                            entity_type="institution.rule",
                            components=(
                                ComponentData(
                                    component_id=ComponentId("rule"),
                                    component_type="law",
                                    schema_version=self._schema,
                                    fields={"rule": candidate.rule, "origin": candidate.origin},
                                ),
                            ),
                        ),
                    )
                ),
                world_time=world_time,
                rule_version=self._rules,
                kind="law",
            ),
        )
        return result.event
