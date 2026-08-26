"""Organization authority, permission, dissolution, and review proposals (G93E)."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.organization_lifecycle_core import (
    DEFAULT_AUTHORITY_POLICY,
    OrganizationAuthorityPolicy,
    _authorized_proposal,
    _event,
)
from wanxiang_substrate.evolution.organization_model import (
    OrganizationLifecycleState,
)
from wanxiang_substrate.evolution.organization_proposal import OrganizationLifecycleProposal
from wanxiang_substrate.institution.model import DelegatedPermission


def propose_permission_grant(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    initiator_id: EntityId,
    member_id: EntityId,
    permission_id: EntityId,
    permission: str,
    target: str,
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    end_ticks: int | None = None,
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose a time-scoped grant by an active authorized member."""
    if not before.is_active_member(member_id, at_ticks):
        raise ContractError("permission recipient is not an active organization member")
    if any(item.permission_id == permission_id for item in before.permissions):
        raise ContractError("permission id is already present")
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="grant_permission",
        initiator_id=initiator_id,
        subject_actor_id=member_id,
        permission_id=permission_id,
        permission=permission,
        target=target,
        end_ticks=end_ticks,
        at_ticks=at_ticks,
        evidence_refs=provenance.source_refs,
    )
    delegated = DelegatedPermission(
        permission_id=permission_id,
        actor_id=member_id,
        permission=permission,
        target=target,
        granter_id=initiator_id,
        start_ticks=at_ticks,
        end_ticks=end_ticks,
    )
    after = replace(
        before,
        permissions=tuple(
            sorted(before.permissions + (delegated,), key=lambda item: item.permission_id.value)
        ),
        history_refs=tuple(sorted(set(before.history_refs + (event_ref,)))),
    )
    return _authorized_proposal(
        proposal_id=proposal_id,
        before=before,
        after=after,
        event=event,
        provenance=provenance,
        provider_ref=provider_ref,
        policy=policy,
    )


def propose_permission_revoke(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    initiator_id: EntityId,
    member_id: EntityId,
    permission_id: EntityId,
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose removal of one explicit grant; missing grants fail loudly."""
    existing = next(
        (item for item in before.permissions if item.permission_id == permission_id), None
    )
    if existing is None or existing.actor_id != member_id:
        raise ContractError("permission to revoke does not belong to the target actor")
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="revoke_permission",
        initiator_id=initiator_id,
        subject_actor_id=member_id,
        permission_id=permission_id,
        at_ticks=at_ticks,
        evidence_refs=provenance.source_refs,
    )
    after = replace(
        before,
        permissions=tuple(
            item for item in before.permissions if item.permission_id != permission_id
        ),
        history_refs=tuple(sorted(set(before.history_refs + (event_ref,)))),
    )
    return _authorized_proposal(
        proposal_id=proposal_id,
        before=before,
        after=after,
        event=event,
        provenance=provenance,
        provider_ref=provider_ref,
        policy=policy,
    )


def propose_dissolve(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    initiator_id: EntityId,
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose dissolution while retaining resources for explicit settlement."""
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="dissolve",
        initiator_id=initiator_id,
        at_ticks=at_ticks,
        evidence_refs=provenance.source_refs,
    )
    after = replace(
        before,
        status="dissolved",
        memberships=(),
        permissions=(),
        history_refs=tuple(sorted(set(before.history_refs + (event_ref,)))),
    )
    return _authorized_proposal(
        proposal_id=proposal_id,
        before=before,
        after=after,
        event=event,
        provenance=provenance,
        provider_ref=provider_ref,
        policy=policy,
    )


def review_organization_proposal(
    proposal: OrganizationLifecycleProposal, *, reviewer: str, approved: bool = True
) -> OrganizationLifecycleProposal:
    """Record explicit policy/reviewer approval; this does not commit canonical state."""
    if reviewer not in ("reviewer", "policy"):
        raise PermissionDenied(f"organization reviewer {reviewer!r} is not authorized")
    return replace(proposal, approved=approved)


def apply_organization_proposal(
    current: OrganizationLifecycleState, proposal: OrganizationLifecycleProposal
) -> OrganizationLifecycleState:
    """Advance only the projection after review and an exact before-state match."""
    if not proposal.approved:
        raise PermissionDenied("organization proposal requires explicit review")
    if current != proposal.before:
        raise ContractError("organization proposal is stale")
    return proposal.after


def split_child_projection(proposal: OrganizationLifecycleProposal) -> OrganizationLifecycleState:
    """Return the separately projected child from an approved split proposal."""
    if proposal.event.action != "split" or proposal.child_after is None:
        raise ContractError("proposal is not an organization split")
    if not proposal.approved:
        raise PermissionDenied("organization split requires explicit review")
    return proposal.child_after


__all__ = [
    "apply_organization_proposal",
    "propose_dissolve",
    "propose_permission_grant",
    "propose_permission_revoke",
    "review_organization_proposal",
    "split_child_projection",
]
