"""Organization formation, membership, and role proposals (G93E)."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_domain.errors import ContractError
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
    OrganizationResource,
)
from wanxiang_substrate.evolution.organization_proposal import OrganizationLifecycleProposal
from wanxiang_substrate.institution.model import Membership, Role


def create_organization_proposal(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    founder_id: EntityId,
    founder_role: Role,
    membership_id: EntityId,
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    resources: tuple[OrganizationResource, ...] = (),
    additional_roles: tuple[Role, ...] = (),
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose formation with one founder, explicit roles, and owned resources."""
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="create",
        initiator_id=founder_id,
        subject_actor_id=founder_id,
        membership_id=membership_id,
        role_id=founder_role.role_id,
        at_ticks=at_ticks,
        evidence_refs=provenance.source_refs,
    )
    membership = Membership(
        membership_id=membership_id,
        actor_id=founder_id,
        role_id=founder_role.role_id,
        institution_id=before.organization_id,
        start_ticks=at_ticks,
    )
    after = replace(
        before,
        status="active",
        roles=tuple(
            sorted((founder_role,) + additional_roles, key=lambda role: role.role_id.value)
        ),
        memberships=(membership,),
        resources=tuple(sorted(resources, key=lambda item: item.resource_id.value)),
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


def propose_join(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    initiator_id: EntityId,
    member_id: EntityId,
    membership_id: EntityId,
    role_id: EntityId,
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose self-join or an authorized invitation into an existing organization."""
    if before.is_active_member(member_id, at_ticks):
        raise ContractError("actor is already an active organization member")
    if any(item.membership_id == membership_id for item in before.memberships):
        raise ContractError("membership id is already present")
    if not any(role.role_id == role_id for role in before.roles):
        raise ContractError("organization join references an unknown role")
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="join",
        initiator_id=initiator_id,
        subject_actor_id=member_id,
        membership_id=membership_id,
        role_id=role_id,
        at_ticks=at_ticks,
        evidence_refs=provenance.source_refs,
    )
    after = replace(
        before,
        memberships=tuple(
            sorted(
                before.memberships
                + (
                    Membership(
                        membership_id,
                        member_id,
                        role_id,
                        before.organization_id,
                        at_ticks,
                    ),
                ),
                key=lambda item: item.membership_id.value,
            )
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


def propose_leave(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    initiator_id: EntityId,
    member_id: EntityId,
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose exit or authorized removal and revoke the member's organization grants."""
    if not before.is_active_member(member_id, at_ticks):
        raise ContractError("actor is not an active organization member")
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="leave",
        initiator_id=initiator_id,
        subject_actor_id=member_id,
        at_ticks=at_ticks,
        evidence_refs=provenance.source_refs,
    )
    after = replace(
        before,
        memberships=tuple(item for item in before.memberships if item.actor_id != member_id),
        permissions=tuple(
            item
            for item in before.permissions
            if item.actor_id != member_id and item.granter_id != member_id
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


def propose_role_change(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    initiator_id: EntityId,
    member_id: EntityId,
    new_role_id: EntityId,
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose an authorized role replacement for one unambiguous active membership."""
    current = tuple(
        item
        for item in before.memberships
        if item.actor_id == member_id and item.is_active_at(at_ticks)
    )
    if len(current) != 1:
        raise ContractError("role change requires exactly one active membership")
    if not any(role.role_id == new_role_id for role in before.roles):
        raise ContractError("organization role change references an unknown role")
    old_role_id = current[0].role_id
    if old_role_id == new_role_id:
        raise ContractError("organization role change must change the role")
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="role_change",
        initiator_id=initiator_id,
        subject_actor_id=member_id,
        from_role_id=old_role_id,
        to_role_id=new_role_id,
        at_ticks=at_ticks,
        evidence_refs=provenance.source_refs,
    )
    memberships = tuple(
        replace(item, role_id=new_role_id)
        if item.membership_id == current[0].membership_id
        else item
        for item in before.memberships
    )
    after = replace(
        before,
        memberships=memberships,
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


__all__ = [
    "create_organization_proposal",
    "propose_join",
    "propose_leave",
    "propose_role_change",
]
