"""Organization split projection with member, permission, and resource partitioning (G93E)."""

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
from wanxiang_substrate.institution.model import DelegatedPermission


def _partition_resources(
    resources: tuple[OrganizationResource, ...],
    child_resources: tuple[OrganizationResource, ...],
) -> tuple[tuple[OrganizationResource, ...], tuple[OrganizationResource, ...]]:
    allocations = {item.resource_id: item for item in child_resources}
    remaining: list[OrganizationResource] = []
    for item in resources:
        allocation = allocations.pop(item.resource_id, None)
        if allocation is None:
            remaining.append(item)
            continue
        if allocation.kind != item.kind or allocation.quantity > item.quantity:
            raise ContractError("organization split resource allocation exceeds parent custody")
        leftover = item.quantity - allocation.quantity
        if leftover:
            remaining.append(OrganizationResource(item.resource_id, item.kind, leftover))
    if allocations:
        raise ContractError("organization split references an unknown resource")
    return (
        tuple(sorted(remaining, key=lambda item: item.resource_id.value)),
        tuple(sorted(child_resources, key=lambda item: item.resource_id.value)),
    )


def _partition_permissions(
    permissions: tuple[DelegatedPermission, ...],
    members: set[EntityId],
    organization_id: EntityId,
) -> tuple[DelegatedPermission, ...]:
    return tuple(
        sorted(
            (
                item
                for item in permissions
                if item.actor_id in members
                and (item.granter_id in members or item.granter_id == organization_id)
            ),
            key=lambda item: item.permission_id.value,
        )
    )


def propose_split(
    before: OrganizationLifecycleState,
    *,
    proposal_id: str,
    initiator_id: EntityId,
    child_organization_id: EntityId,
    child_member_ids: tuple[EntityId, ...],
    event_ref: str,
    at_ticks: int,
    provenance: EvolutionProvenance,
    child_resources: tuple[OrganizationResource, ...] = (),
    provider_ref: str = "policy:organization",
    policy: OrganizationAuthorityPolicy = DEFAULT_AUTHORITY_POLICY,
) -> OrganizationLifecycleProposal:
    """Propose a non-destructive partition; cross-partition grants are removed."""
    active = set(before.active_members(at_ticks))
    child_members = set(child_member_ids)
    if not child_members.issubset(active):
        raise ContractError("organization split members must be active members")
    if not active - child_members:
        raise ContractError("organization split requires a non-empty parent remainder")
    parent_members = active - child_members
    parent_resources, projected_child_resources = _partition_resources(
        before.resources, child_resources
    )
    event = _event(
        event_ref=event_ref,
        organization_id=before.organization_id,
        action="split",
        initiator_id=initiator_id,
        at_ticks=at_ticks,
        child_organization_id=child_organization_id,
        child_member_ids=tuple(sorted(child_members, key=lambda actor: actor.value)),
        child_resources=projected_child_resources,
        evidence_refs=provenance.source_refs,
    )
    parent_memberships = tuple(
        item for item in before.memberships if item.actor_id not in child_members
    )
    child_memberships = tuple(
        sorted(
            (
                replace(item, institution_id=child_organization_id)
                for item in before.memberships
                if item.actor_id in child_members
            ),
            key=lambda item: item.membership_id.value,
        )
    )
    child_role_ids = {item.role_id for item in child_memberships}
    child_roles = tuple(
        sorted(
            (role for role in before.roles if role.role_id in child_role_ids),
            key=lambda role: role.role_id.value,
        )
    )
    parent_permissions = _partition_permissions(
        before.permissions, parent_members, before.organization_id
    )
    child_permissions = _partition_permissions(
        before.permissions, child_members, child_organization_id
    )
    after = replace(
        before,
        status="split",
        memberships=tuple(sorted(parent_memberships, key=lambda item: item.membership_id.value)),
        permissions=parent_permissions,
        resources=parent_resources,
        child_organization_ids=tuple(
            sorted(
                set(before.child_organization_ids + (child_organization_id,)),
                key=lambda item: item.value,
            )
        ),
        history_refs=tuple(sorted(set(before.history_refs + (event_ref,)))),
    )
    child_after = OrganizationLifecycleState(
        organization_id=child_organization_id,
        status="active",
        roles=child_roles,
        memberships=child_memberships,
        permissions=child_permissions,
        resources=projected_child_resources,
        history_refs=(event_ref,),
        parent_organization_id=before.organization_id,
    )
    return _authorized_proposal(
        proposal_id=proposal_id,
        before=before,
        after=after,
        event=event,
        provenance=provenance,
        provider_ref=provider_ref,
        policy=policy,
        child_after=child_after,
    )


__all__ = ["propose_split"]
