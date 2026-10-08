"""Shared policy and proposal construction for G93E organization evolution."""

from __future__ import annotations

from typing import cast

from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.evolution.delta import (
    EvolutionProvenance,
    OrganizationDelta,
    OrganizationLifecycle,
)
from wanxiang_substrate.evolution.organization_model import (
    OrganizationAction,
    OrganizationLifecycleEvent,
    OrganizationLifecycleState,
    OrganizationResource,
    OrganizationStatus,
)
from wanxiang_substrate.evolution.organization_proposal import OrganizationLifecycleProposal
from wanxiang_substrate.institution.query import InstitutionQuery

AUTHORITY_PERMISSIONS = {
    "role_change": "organization.manage_roles",
    "grant_permission": "organization.manage_permissions",
    "revoke_permission": "organization.manage_permissions",
    "dissolve": "organization.dissolve",
    "split": "organization.split",
    "join": "organization.manage_members",
    "leave": "organization.manage_members",
}
_LIFECYCLE_BY_ACTION: dict[str, str] = {
    "create": "formed",
    "join": "joined",
    "leave": "left",
    "role_change": "role_changed",
    "grant_permission": "permission_changed",
    "revoke_permission": "permission_changed",
    "dissolve": "dissolved",
    "split": "split",
}


class OrganizationAuthorityPolicy:
    """Check organization authority without becoming a commit authority."""

    def authorize(
        self, state: OrganizationLifecycleState, event: OrganizationLifecycleEvent
    ) -> None:
        if event.action == "create":
            if state.status != "forming" or state.memberships:
                raise ContractError(
                    "organization can only be created from an empty forming projection"
                )
            if event.subject_actor_id != event.initiator_id:
                raise PermissionDenied("organization founder must create their own organization")
            return
        if state.status != "active":
            raise ContractError("organization lifecycle action requires an active organization")
        if event.action in ("join", "leave") and event.subject_actor_id == event.initiator_id:
            return
        permission = AUTHORITY_PERMISSIONS.get(event.action)
        if (
            permission is None
            or not state.check_permission(
                event.initiator_id, permission, at_ticks=event.at_ticks
            ).allow
        ):
            raise PermissionDenied(
                f"actor {event.initiator_id.value} lacks {permission or 'organization authority'}"
            )


DEFAULT_AUTHORITY_POLICY = OrganizationAuthorityPolicy()


def empty_organization(organization_id: EntityId) -> OrganizationLifecycleState:
    """Create an empty projection; it has no canonical persistence side effect."""
    return OrganizationLifecycleState(organization_id=organization_id)


def organization_state_from_canonical(
    state: InMemoryCanonicalState,
    organization_id: EntityId,
    *,
    now_ticks: int = 0,
    resources: tuple[OrganizationResource, ...] = (),
) -> OrganizationLifecycleState:
    """Build a lifecycle view from existing institution components and canonical state."""
    query = InstitutionQuery(state, now_ticks=now_ticks)
    memberships = tuple(
        item for item in query.all_memberships() if item.institution_id == organization_id
    )
    role_ids = {item.role_id for item in memberships}
    roles = tuple(item for item in query.all_roles() if item.role_id in role_ids)
    actors = {item.actor_id for item in memberships if item.is_active_at(now_ticks)}
    permissions = tuple(
        item
        for item in query.delegated_permissions()
        if item.actor_id in actors
        and (item.granter_id == organization_id or item.granter_id in actors)
    )
    status: OrganizationStatus = (
        "active" if state.entity(organization_id) is not None else "forming"
    )
    return OrganizationLifecycleState(
        organization_id=organization_id,
        status=status,
        roles=roles,
        memberships=memberships,
        permissions=permissions,
        resources=tuple(sorted(resources, key=lambda item: item.resource_id.value)),
    )


def _event(
    *,
    event_ref: str,
    organization_id: EntityId,
    action: OrganizationAction,
    initiator_id: EntityId,
    at_ticks: int,
    subject_actor_id: EntityId | None = None,
    membership_id: EntityId | None = None,
    role_id: EntityId | None = None,
    from_role_id: EntityId | None = None,
    to_role_id: EntityId | None = None,
    permission_id: EntityId | None = None,
    permission: str | None = None,
    target: str | None = None,
    end_ticks: int | None = None,
    child_organization_id: EntityId | None = None,
    child_member_ids: tuple[EntityId, ...] = (),
    child_resources: tuple[OrganizationResource, ...] = (),
    evidence_refs: tuple[str, ...] = (),
) -> OrganizationLifecycleEvent:
    return OrganizationLifecycleEvent(
        event_ref=event_ref,
        organization_id=organization_id,
        action=action,
        initiator_id=initiator_id,
        at_ticks=at_ticks,
        subject_actor_id=subject_actor_id,
        membership_id=membership_id,
        role_id=role_id,
        from_role_id=from_role_id,
        to_role_id=to_role_id,
        permission_id=permission_id,
        permission=permission,
        target=target,
        end_ticks=end_ticks,
        child_organization_id=child_organization_id,
        child_member_ids=child_member_ids,
        child_resources=child_resources,
        evidence_refs=evidence_refs,
    )


def _merged_provenance(provenance: EvolutionProvenance, event_ref: str) -> EvolutionProvenance:
    return EvolutionProvenance(
        origin_ref=provenance.origin_ref,
        source_refs=provenance.source_refs,
        event_refs=tuple(sorted(set(provenance.event_refs + (event_ref,)))),
        producer=provenance.producer,
    )


def _role_name(state: OrganizationLifecycleState, role_id: EntityId | None) -> str | None:
    if role_id is None:
        return None
    return next((role.name for role in state.roles if role.role_id == role_id), role_id.value)


def _build_proposal(
    *,
    proposal_id: str,
    before: OrganizationLifecycleState,
    after: OrganizationLifecycleState,
    event: OrganizationLifecycleEvent,
    provenance: EvolutionProvenance,
    provider_ref: str,
    child_after: OrganizationLifecycleState | None = None,
) -> OrganizationLifecycleProposal:
    merged = _merged_provenance(provenance, event.event_ref)
    lifecycle = cast(OrganizationLifecycle, _LIFECYCLE_BY_ACTION[event.action])
    actor_id = event.subject_actor_id or event.initiator_id
    delta = OrganizationDelta(
        delta_id=f"organization_{proposal_id}",
        organization_id=before.organization_id,
        lifecycle=lifecycle,
        actor_id=actor_id,
        from_role=_role_name(before, event.from_role_id),
        to_role=_role_name(after, event.to_role_id or event.role_id),
        reason=f"{event.action}:{proposal_id}",
        provenance=merged,
    )
    return OrganizationLifecycleProposal(
        proposal_id=proposal_id,
        before=before,
        after=after,
        event=event,
        delta=delta,
        provenance=merged,
        provider_ref=provider_ref,
        child_after=child_after,
    )


def _authorized_proposal(
    *,
    proposal_id: str,
    before: OrganizationLifecycleState,
    after: OrganizationLifecycleState,
    event: OrganizationLifecycleEvent,
    provenance: EvolutionProvenance,
    provider_ref: str,
    policy: OrganizationAuthorityPolicy,
    child_after: OrganizationLifecycleState | None = None,
) -> OrganizationLifecycleProposal:
    policy.authorize(before, event)
    return _build_proposal(
        proposal_id=proposal_id,
        before=before,
        after=after,
        event=event,
        provenance=provenance,
        provider_ref=provider_ref,
        child_after=child_after,
    )


__all__ = [
    "AUTHORITY_PERMISSIONS",
    "DEFAULT_AUTHORITY_POLICY",
    "OrganizationAuthorityPolicy",
    "_authorized_proposal",
    "_event",
    "_merged_provenance",
    "_role_name",
    "empty_organization",
    "organization_state_from_canonical",
]
