"""G30G: Fact Scope and Authority Partition."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta
from wanxiang_substrate.ledger.fact_scope import FACT_SCOPE_WRITERS, FACT_SCOPES, FactScopePolicy
from wanxiang_substrate.projection.model import ProjectionRequest
from wanxiang_substrate.projection.service import ProjectionService


def _fact_state() -> InMemoryCanonicalState:
    base = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )

    def fact(entity_id: str, scope: str, owner: str) -> EntityCreate:
        return EntityCreate(
            entity_id=EntityId(entity_id),
            entity_type="ledger.fact",
            components=(
                ComponentData(
                    component_id=ComponentId(f"{entity_id}_scope"),
                    component_type="fact_scope",
                    schema_version=SCHEMA,
                    fields={"scope": scope, "owner": owner},
                ),
            ),
        )

    return apply_delta(
        base,
        ProposedWorldDelta(
            operations=(
                fact("fact_canon", "canonical", "system"),
                fact("fact_public", "public", "system"),
                fact("fact_actor_a", "actor", "actor_a"),
                fact("fact_actor_b", "actor", "actor_b"),
                fact("fact_org", "org", "org_rongguo"),
                fact("fact_hyp", "hypothesis", "researcher"),
            )
        ),
    )


@pytest.mark.unit
def test_canonical_is_exclusive_to_commit_authority() -> None:
    assert FACT_SCOPE_WRITERS["canonical"] == ("commit_authority",)
    assert FactScopePolicy.can_view("canonical", "actor:a") is True
    with pytest.raises(PermissionDenied):
        FactScopePolicy.assert_write_allowed("canonical", "actor")
    # Commit authority may author canonical/public/org/hypothesis/reconstruction,
    # but never an actor's private belief (actor-owned scope).
    for scope in FACT_SCOPES:
        if scope == "actor":
            with pytest.raises(PermissionDenied):
                FactScopePolicy.assert_write_allowed(scope, "commit_authority")
        else:
            FactScopePolicy.assert_write_allowed(scope, "commit_authority")


@pytest.mark.unit
def test_scope_only_elevation_to_canonical_is_rejected() -> None:
    policy = FactScopePolicy()
    with pytest.raises(PermissionDenied):
        policy.assert_canonical_promotion_requires_commit("actor", "canonical", via_commit=False)
    with pytest.raises(PermissionDenied):
        policy.assert_canonical_promotion_requires_commit(
            "hypothesis", "canonical", via_commit=False
        )
    # Through Commit the promotion is allowed at the policy layer.
    policy.assert_canonical_promotion_requires_commit(
        "reconstruction", "canonical", via_commit=True
    )


@pytest.mark.unit
def test_any_scope_change_without_commit_is_rejected() -> None:
    policy = FactScopePolicy()
    with pytest.raises(PermissionDenied):
        policy.assert_canonical_promotion_requires_commit("actor", "org", via_commit=False)
    # Same-scope edit is fine.
    policy.assert_canonical_promotion_requires_commit("actor", "actor", via_commit=False)


@pytest.mark.unit
def test_actor_belief_does_not_leak_canonical_private_facts() -> None:
    state = _fact_state()
    projection = ProjectionService(state).compose(
        ProjectionRequest(session_id="s1", actor_id="actor_a", branch_id=BRANCH)
    )
    ids = {item.entity_id for item in projection.items}
    # canonical + public visible to the actor.
    assert "fact_canon" in ids
    assert "fact_public" in ids
    # The OTHER actor's private belief never leaks.
    assert "fact_actor_b" not in ids
    # An org fact and a hypothesis never leak to an ordinary actor.
    assert "fact_org" not in ids
    assert "fact_hyp" not in ids


@pytest.mark.unit
def test_cross_role_peeking_fails() -> None:
    state = _fact_state()
    # An actor outside the org cannot see org facts; a researcher can.
    actor_view = ProjectionService(state).compose(
        ProjectionRequest(session_id="s2", actor_id="actor_x", branch_id=BRANCH)
    )
    assert "fact_org" not in {i.entity_id for i in actor_view.items}
    # Admin sees everything (rights override).
    admin_view = ProjectionService(state, admin=True).compose(
        ProjectionRequest(session_id="s3", actor_id="admin", branch_id=BRANCH)
    )
    ids = {i.entity_id for i in admin_view.items}
    assert {"fact_canon", "fact_actor_a", "fact_actor_b", "fact_org", "fact_hyp"} <= ids
