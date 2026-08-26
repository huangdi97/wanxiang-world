"""G93E: source/playable/preview/SQLite chain feeds organization evolution proposals."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.delta import EvolutionCommitPolicy, EvolutionProvenance
from wanxiang_substrate.evolution.organization_lifecycle import (
    apply_organization_proposal,
    create_organization_proposal,
    organization_state_from_canonical,
    propose_join,
    propose_permission_grant,
    propose_role_change,
    propose_split,
    review_organization_proposal,
    split_child_projection,
)
from wanxiang_substrate.evolution.organization_model import OrganizationResource
from wanxiang_substrate.evolution.organization_proposal import OrganizationLifecycleProposal
from wanxiang_substrate.institution.model import Role
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Organization Chain\nCharacter: Alice\nCharacter: Bob\nCharacter: Carol\n"
        "Alice keeps the ledger. Bob carries messages. Carol guards the archive.\n"
        "organization: the archive circle\nrelationship: Alice -> Bob\n"
        "rule: members share responsibility for the archive\n"
    )
    return SourceRecord(
        source_id="g93e_organization_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g93e_organization_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="qualification",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g93e",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                name = component.fields.get("display_name")
                if isinstance(name, str):
                    found[name] = entity.entity_id.value
    return found


def _approved(proposal: OrganizationLifecycleProposal) -> OrganizationLifecycleProposal:
    return review_organization_proposal(proposal, reviewer="policy")


@pytest.mark.integration
def test_organization_lifecycle_uses_real_product_chain_without_canonical_bypass(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g93e_organization", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g93e_owner", visibility="private")
    character = playable.entry.create_character(
        "g93e_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g93e_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g93e_owner",
        mode="embodiment",
        session_id="session_g93e_alice",
        character_id=character.character_id,
    )
    instance_id = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance_id.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance_id, branch))
    alice = EntityId(actors["Alice"])
    bob = EntityId(actors["Bob"])
    carol = EntityId(actors["Carol"])
    committed = playable.action(
        instance_id.value,
        viewer_id="g93e_owner",
        action_type="set_status",
        payload={"entity_id": alice.value, "status": "active"},
    )
    canonical_before = runtime.current_state(instance_id, branch)
    before_hash = canonical_before.semantic_hash()
    before_revision = canonical_before.revision.value
    projection = organization_state_from_canonical(
        canonical_before,
        EntityId("org_g93e_product"),
        resources=(OrganizationResource(EntityId("resource_g93e_product"), "ledger", 12),),
    )
    admin = Role(
        EntityId("role_g93e_product_admin"),
        "admin",
        (
            "organization.manage_members",
            "organization.manage_roles",
            "organization.manage_permissions",
            "organization.split",
        ),
    )
    member = Role(EntityId("role_g93e_product_member"), "member")
    provenance = EvolutionProvenance(
        origin_ref=f"package:{package.package_id}",
        source_refs=(source.content_ref,),
        event_refs=(committed.event_id,),
        producer="runtime_projection",
    )
    created = create_organization_proposal(
        projection,
        proposal_id="product_create",
        founder_id=alice,
        founder_role=admin,
        additional_roles=(member,),
        membership_id=EntityId("membership_g93e_product_alice"),
        event_ref=committed.event_id,
        at_ticks=0,
        provenance=provenance,
        resources=projection.resources,
    )
    state = apply_organization_proposal(projection, _approved(created))
    joined_bob = propose_join(
        state,
        proposal_id="product_join_bob",
        initiator_id=bob,
        member_id=bob,
        membership_id=EntityId("membership_g93e_product_bob"),
        role_id=member.role_id,
        event_ref="event:g93e:product:join:bob",
        at_ticks=1,
        provenance=provenance,
    )
    state = apply_organization_proposal(state, _approved(joined_bob))
    joined_carol = propose_join(
        state,
        proposal_id="product_join_carol",
        initiator_id=carol,
        member_id=carol,
        membership_id=EntityId("membership_g93e_product_carol"),
        role_id=member.role_id,
        event_ref="event:g93e:product:join:carol",
        at_ticks=1,
        provenance=provenance,
    )
    state = apply_organization_proposal(state, _approved(joined_carol))
    role_changed = propose_role_change(
        state,
        proposal_id="product_role_bob",
        initiator_id=alice,
        member_id=bob,
        new_role_id=admin.role_id,
        event_ref="event:g93e:product:role",
        at_ticks=2,
        provenance=provenance,
    )
    state = apply_organization_proposal(state, _approved(role_changed))
    grant = propose_permission_grant(
        state,
        proposal_id="product_grant_bob",
        initiator_id=alice,
        member_id=bob,
        permission_id=EntityId("permission_g93e_product"),
        permission="read.archive",
        target="archive:g93e",
        event_ref="event:g93e:product:grant",
        at_ticks=3,
        provenance=provenance,
    )
    state = apply_organization_proposal(state, _approved(grant))
    assert state.check_permission(bob, "read.archive", "archive:g93e", 3).allow is True
    for proposal in (created, joined_bob, joined_carol, role_changed, grant):
        EvolutionCommitPolicy.validate_proposal(proposal.delta)
        assert committed.event_id in proposal.provenance.event_refs
    split = propose_split(
        state,
        proposal_id="product_split_bob",
        initiator_id=alice,
        child_organization_id=EntityId("org_g93e_product_child"),
        child_member_ids=(bob,),
        child_resources=(OrganizationResource(EntityId("resource_g93e_product"), "ledger", 4),),
        event_ref="event:g93e:product:split",
        at_ticks=4,
        provenance=provenance,
    )
    parent_after_split = apply_organization_proposal(state, _approved(split))
    child_after_split = split_child_projection(_approved(split))
    assert parent_after_split.active_members(4) == (alice, carol)
    assert child_after_split.active_members(4) == (bob,)
    assert parent_after_split.permissions == ()
    assert child_after_split.permissions == ()
    assert parent_after_split.resources[0].quantity + child_after_split.resources[0].quantity == 12
    assert runtime.current_state(instance_id, branch).semantic_hash() == before_hash
    assert runtime.current_state(instance_id, branch).revision.value == before_revision
    assert len(runtime.events(instance_id, branch)) == committed.revision
    assert runtime.restore_and_replay(instance_id, branch).state.semantic_hash() == before_hash
