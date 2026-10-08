"""G93E: organization lifecycle, authority, partitioning, and orphan cleanup."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.organization_lifecycle import (
    apply_organization_proposal,
    create_organization_proposal,
    empty_organization,
    propose_dissolve,
    propose_join,
    propose_leave,
    propose_permission_grant,
    propose_permission_revoke,
    propose_role_change,
    propose_split,
    review_organization_proposal,
    split_child_projection,
)
from wanxiang_substrate.evolution.organization_model import (
    OrganizationLifecycleState,
    OrganizationResource,
)
from wanxiang_substrate.evolution.organization_proposal import OrganizationLifecycleProposal
from wanxiang_substrate.institution.model import Role

ORG = EntityId("org_g93e")
ALICE = EntityId("actor_alice")
BOB = EntityId("actor_bob")
CAROL = EntityId("actor_carol")
ADMIN = Role(
    EntityId("role_admin_g93e"),
    "admin",
    (
        "organization.manage_members",
        "organization.manage_roles",
        "organization.manage_permissions",
        "organization.dissolve",
        "organization.split",
    ),
)
MEMBER = Role(EntityId("role_member_g93e"), "member")
PROVENANCE = EvolutionProvenance(
    origin_ref="run:g93e",
    source_refs=("source:g93e",),
    event_refs=("event:g93e:root",),
    producer="runtime_projection",
)


def _approve(proposal: OrganizationLifecycleProposal) -> OrganizationLifecycleProposal:
    return review_organization_proposal(proposal, reviewer="policy")


def _create() -> OrganizationLifecycleState:
    proposal = create_organization_proposal(
        empty_organization(ORG),
        proposal_id="create",
        founder_id=ALICE,
        founder_role=ADMIN,
        additional_roles=(MEMBER,),
        membership_id=EntityId("membership_alice_g93e"),
        event_ref="event:g93e:create",
        at_ticks=0,
        provenance=PROVENANCE,
        resources=(OrganizationResource(EntityId("resource_g93e"), "ledger", 10),),
    )
    return apply_organization_proposal(empty_organization(ORG), _approve(proposal))


def _join(state: OrganizationLifecycleState, actor: EntityId, number: str):
    return apply_organization_proposal(
        state,
        _approve(
            propose_join(
                state,
                proposal_id=f"join_{number}",
                initiator_id=actor,
                member_id=actor,
                membership_id=EntityId(f"membership_{number}_g93e"),
                role_id=MEMBER.role_id,
                event_ref=f"event:g93e:join:{number}",
                at_ticks=1,
                provenance=PROVENANCE,
            )
        ),
    )


def test_create_join_role_change_and_explicit_review() -> None:
    state = _create()
    assert state.status == "active"
    state = _join(state, BOB, "bob")
    assert state.active_members(1) == (ALICE, BOB)
    changed = propose_role_change(
        state,
        proposal_id="role_bob_admin",
        initiator_id=ALICE,
        member_id=BOB,
        new_role_id=ADMIN.role_id,
        event_ref="event:g93e:role",
        at_ticks=2,
        provenance=PROVENANCE,
    )
    assert changed.delta.lifecycle == "role_changed"
    with pytest.raises(PermissionDenied, match="explicit review"):
        apply_organization_proposal(state, changed)
    state = apply_organization_proposal(state, _approve(changed))
    assert state.roles_for(BOB, 2) == (ADMIN,)
    assert state.history_refs[-1] == "event:g93e:role"


def test_authority_cannot_be_bypassed_by_a_member_or_provider() -> None:
    state = _join(_create(), BOB, "bob")
    with pytest.raises(PermissionDenied, match="manage_roles"):
        propose_role_change(
            state,
            proposal_id="unauthorized_role",
            initiator_id=BOB,
            member_id=ALICE,
            new_role_id=MEMBER.role_id,
            event_ref="event:g93e:bad-role",
            at_ticks=2,
            provenance=PROVENANCE,
        )
    with pytest.raises(ContractError, match="Commit Authority"):
        create_organization_proposal(
            empty_organization(EntityId("org_provider")),
            proposal_id="provider-bypass",
            founder_id=ALICE,
            founder_role=ADMIN,
            membership_id=EntityId("membership_provider"),
            event_ref="event:g93e:provider",
            at_ticks=0,
            provenance=PROVENANCE,
            provider_ref="commit_authority",
        )


def test_leave_removes_orphan_permissions_and_revoke_is_explicit() -> None:
    state = _join(_create(), BOB, "bob")
    grant = propose_permission_grant(
        state,
        proposal_id="grant_bob",
        initiator_id=ALICE,
        member_id=BOB,
        permission_id=EntityId("permission_bob_g93e"),
        permission="read.archive",
        target="archive:g93e",
        event_ref="event:g93e:grant",
        at_ticks=2,
        provenance=PROVENANCE,
    )
    state = apply_organization_proposal(state, _approve(grant))
    assert state.check_permission(BOB, "read.archive", "archive:g93e", 2).allow is True
    revoke = propose_permission_revoke(
        state,
        proposal_id="revoke_bob",
        initiator_id=ALICE,
        member_id=BOB,
        permission_id=EntityId("permission_bob_g93e"),
        event_ref="event:g93e:revoke",
        at_ticks=3,
        provenance=PROVENANCE,
    )
    state = apply_organization_proposal(state, _approve(revoke))
    assert state.check_permission(BOB, "read.archive", "archive:g93e", 3).allow is False
    grant_again = propose_permission_grant(
        state,
        proposal_id="grant_bob_again",
        initiator_id=ALICE,
        member_id=BOB,
        permission_id=EntityId("permission_bob_g93e_2"),
        permission="read.archive",
        target="archive:g93e",
        event_ref="event:g93e:grant-again",
        at_ticks=4,
        provenance=PROVENANCE,
    )
    state = apply_organization_proposal(state, _approve(grant_again))
    state = apply_organization_proposal(
        state,
        _approve(
            propose_leave(
                state,
                proposal_id="leave_bob",
                initiator_id=BOB,
                member_id=BOB,
                event_ref="event:g93e:leave",
                at_ticks=5,
                provenance=PROVENANCE,
            )
        ),
    )
    assert BOB not in state.active_members()
    assert state.permissions == ()
    assert state.orphan_permissions() == ()
    assert state.effective_permissions(BOB) == ()


def test_split_partitions_members_permissions_and_resources() -> None:
    state = _join(_join(_create(), BOB, "bob"), CAROL, "carol")
    grant = propose_permission_grant(
        state,
        proposal_id="cross_grant",
        initiator_id=ALICE,
        member_id=BOB,
        permission_id=EntityId("permission_cross_g93e"),
        permission="read.archive",
        target="archive:g93e",
        event_ref="event:g93e:cross-grant",
        at_ticks=2,
        provenance=PROVENANCE,
    )
    state = apply_organization_proposal(state, _approve(grant))
    split = propose_split(
        state,
        proposal_id="split_bob",
        initiator_id=ALICE,
        child_organization_id=EntityId("org_g93e_child"),
        child_member_ids=(BOB,),
        child_resources=(OrganizationResource(EntityId("resource_g93e"), "ledger", 3),),
        event_ref="event:g93e:split",
        at_ticks=6,
        provenance=PROVENANCE,
    )
    state = apply_organization_proposal(state, _approve(split))
    child = split_child_projection(_approve(split))
    assert state.status == "split"
    assert state.active_members(6) == (ALICE, CAROL)
    assert child.active_members(6) == (BOB,)
    assert state.permissions == ()
    assert child.permissions == ()
    assert state.resources[0].quantity == 7
    assert child.resources[0].quantity == 3
    assert state.resources[0].quantity + child.resources[0].quantity == 10


def test_dissolve_clears_members_and_permissions_but_retains_resources_for_settlement() -> None:
    state = _join(_create(), BOB, "bob")
    proposal = propose_dissolve(
        state,
        proposal_id="dissolve",
        initiator_id=ALICE,
        event_ref="event:g93e:dissolve",
        at_ticks=7,
        provenance=PROVENANCE,
    )
    dissolved = apply_organization_proposal(state, _approve(proposal))
    assert dissolved.status == "dissolved"
    assert dissolved.active_members() == ()
    assert dissolved.permissions == ()
    assert dissolved.resources == (OrganizationResource(EntityId("resource_g93e"), "ledger", 10),)
