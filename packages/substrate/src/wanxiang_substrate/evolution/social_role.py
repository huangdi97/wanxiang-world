"""Evidence-backed social role projections, separate from institution roles (G93F)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.reputation_model import ReputationScope, ReputationState

SocialRoleStatus = Literal["review", "approved", "rejected"]
SOCIAL_ROLE_REVIEWERS = ("reviewer", "policy", "actor")


@dataclass(frozen=True, slots=True)
class SocialRole:
    """A bounded social label; it does not grant institutional permissions."""

    role_id: EntityId
    name: str
    dimension: str
    minimum_score: float
    scope: ReputationScope
    scope_ref: str
    observer_actor_id: EntityId | None = None

    def __post_init__(self) -> None:
        if not self.role_id.value or not self.name.strip() or not self.dimension.strip():
            raise ContractError("social role identity is incomplete")
        if not -1.0 <= self.minimum_score <= 1.0:
            raise ContractError("social role threshold is out of bounds")
        if self.scope not in ("local", "global") or not self.scope_ref.strip():
            raise ContractError("social role scope is invalid")


@dataclass(frozen=True, slots=True)
class SocialRoleProposal:
    """Eligibility proposal that cannot mutate an institution or canonical state."""

    proposal_id: str
    subject_actor_id: EntityId
    role: SocialRole
    reputation: ReputationState
    eligible: bool
    provenance: EvolutionProvenance
    provider_ref: str
    status: SocialRoleStatus = "review"

    def __post_init__(self) -> None:
        if not self.proposal_id.strip() or not self.provider_ref.strip():
            raise ContractError("social role proposal requires id and provider")
        if self.provider_ref in {"commit_authority", "commit-authority"}:
            raise ContractError("Commit Authority cannot produce social role proposals")
        if self.provenance.producer in {"commit_authority", "commit-authority"}:
            raise ContractError("Commit Authority cannot produce social role proposals")
        if self.subject_actor_id != self.reputation.subject_actor_id:
            raise ContractError("social role subject does not match reputation")
        if (
            self.role.dimension,
            self.role.scope,
            self.role.scope_ref,
            self.role.observer_actor_id,
        ) != (
            self.reputation.dimension,
            self.reputation.scope,
            self.reputation.scope_ref,
            self.reputation.observer_actor_id,
        ):
            raise ContractError("social role scope does not match reputation")
        if self.eligible != (self.reputation.score >= self.role.minimum_score):
            raise ContractError("social role eligibility is not derived from reputation")
        if not self.reputation.event_refs and not self.reputation.evidence_refs:
            raise ContractError("social role proposal requires reputation evidence")
        if self.status not in ("review", "approved", "rejected"):
            raise ContractError(f"invalid social role proposal status {self.status!r}")


@dataclass(frozen=True, slots=True)
class SocialRoleAssignment:
    """A read-only social projection assignment, not an institution Role."""

    subject_actor_id: EntityId
    role: SocialRole
    reputation_score: float
    assigned_ticks: int
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not -1.0 <= self.reputation_score <= 1.0 or self.assigned_ticks < 0:
            raise ContractError("social role assignment values are invalid")
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ContractError("social role assignment evidence refs cannot be blank")


@dataclass(frozen=True, slots=True)
class SocialRoleProjection:
    """Immutable role assignments, intentionally separate from institution state."""

    assignments: tuple[SocialRoleAssignment, ...] = ()

    def __post_init__(self) -> None:
        keys = tuple((item.subject_actor_id, item.role.role_id) for item in self.assignments)
        if len(set(keys)) != len(keys):
            raise ContractError("social role projection assignments must be unique")

    def assignments_for(self, subject_actor_id: EntityId) -> tuple[SocialRoleAssignment, ...]:
        return tuple(item for item in self.assignments if item.subject_actor_id == subject_actor_id)


def propose_social_role(
    *,
    proposal_id: str,
    subject_actor_id: EntityId,
    role: SocialRole,
    reputation: ReputationState,
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:social-role",
) -> SocialRoleProposal:
    """Derive eligibility from a reputation projection; no assignment is committed."""
    return SocialRoleProposal(
        proposal_id=proposal_id,
        subject_actor_id=subject_actor_id,
        role=role,
        reputation=reputation,
        eligible=reputation.score >= role.minimum_score,
        provenance=provenance,
        provider_ref=provider_ref,
    )


def review_social_role_proposal(
    proposal: SocialRoleProposal, *, reviewer: str, approved: bool = True
) -> SocialRoleProposal:
    """Record explicit review for a social role projection."""
    if reviewer not in SOCIAL_ROLE_REVIEWERS:
        raise PermissionDenied(f"social role reviewer {reviewer!r} is not authorized")
    return replace(proposal, status="approved" if approved else "rejected")


def assign_social_role(proposal: SocialRoleProposal) -> SocialRoleAssignment:
    """Materialize a reviewed social label as a non-canonical assignment."""
    if proposal.status != "approved":
        raise PermissionDenied("social role proposal requires explicit review")
    if not proposal.eligible:
        raise ContractError("ineligible social role proposal cannot be assigned")
    return SocialRoleAssignment(
        subject_actor_id=proposal.subject_actor_id,
        role=proposal.role,
        reputation_score=proposal.reputation.score,
        assigned_ticks=proposal.reputation.updated_ticks,
        evidence_refs=tuple(
            dict.fromkeys(proposal.reputation.evidence_refs + proposal.reputation.event_refs)
        ),
    )


def advance_social_role_projection(
    projection: SocialRoleProjection, proposal: SocialRoleProposal
) -> SocialRoleProjection:
    """Advance one reviewed role assignment without touching institution state."""
    assignment = assign_social_role(proposal)
    key = (assignment.subject_actor_id, assignment.role.role_id)
    existing = tuple(
        item for item in projection.assignments if (item.subject_actor_id, item.role.role_id) != key
    )
    return SocialRoleProjection(assignments=existing + (assignment,))
