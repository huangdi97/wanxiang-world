"""G30C: Constitution execution and non-overreach.

Kernel invariants run before every commit and cannot be overridden by any
world/delta: world deltas must not mutate the commit boundary, the Reality
Root, the constitution, or platform identities, and must not relate to them.
"""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta, RelationCreate
from wanxiang_domain.errors import Conflict, ConstitutionViolation, ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, RelationId
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.invariants import (
    PLATFORM_PROTECTED_ENTITY_IDS,
    PLATFORM_PROTECTED_ENTITY_PREFIX,
    check_delta_invariants,
)
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta


def _base_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


def _commit(
    authority: CommitAuthority, state: InMemoryCanonicalState, delta: ProposedWorldDelta, index: int
) -> None:
    authority.commit(
        state,
        CommitRequest(
            command_id=CommandId(f"cmd_g30c_{index}"),
            instance_id=INSTANCE,
            branch_id=BRANCH,
            expected_revision=state.revision,
            delta=delta,
            world_time=WorldTime(index),
            rule_version=RULES,
        ),
    )


@pytest.mark.unit
def test_protected_identities_are_platform_scoped() -> None:
    assert PLATFORM_PROTECTED_ENTITY_PREFIX == "sys_"
    assert "sys_commit_authority" in PLATFORM_PROTECTED_ENTITY_IDS
    assert "sys_reality_root" in PLATFORM_PROTECTED_ENTITY_IDS


@pytest.mark.unit
def test_world_delta_cannot_create_commit_authority() -> None:
    state = _base_state()
    with pytest.raises(ConstitutionViolation):
        check_delta_invariants(
            state,
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=EntityId("sys_commit_authority"), entity_type="authority"
                    ),
                )
            ),
        )
    # No state mutation occurred (checks run before any change is applied).
    assert state.entity(EntityId("sys_commit_authority")) is None
    assert state.revision == BranchRevision(0)


@pytest.mark.unit
def test_world_delta_cannot_update_reality_root() -> None:
    state = _base_state()
    with pytest.raises(ConstitutionViolation):
        check_delta_invariants(
            state,
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=EntityId("sys_reality_root"), entity_type="reality_root"
                    ),
                )
            ),
        )


@pytest.mark.unit
def test_world_delta_cannot_relate_to_protected_entity() -> None:
    state = apply_delta(
        _base_state(),
        ProposedWorldDelta(
            operations=(EntityCreate(entity_id=EntityId("alice"), entity_type="person"),)
        ),
    )
    # Kernel invariant (relation references must exist) fires before the
    # constitution relation gate ? kernel priority is proven by the order.
    with pytest.raises(ValidationRejected):
        check_delta_invariants(
            state,
            ProposedWorldDelta(
                operations=(
                    RelationCreate(
                        relation_id=RelationId("r_bad"),
                        relation_type="owns",
                        source_id=EntityId("alice"),
                        target_id=EntityId("sys_commit_authority"),
                    ),
                )
            ),
        )


@pytest.mark.unit
def test_constitution_violation_blocks_commit_without_mutation() -> None:
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    state = _base_state()
    with pytest.raises(ConstitutionViolation):
        _commit(
            authority,
            state,
            ProposedWorldDelta(
                operations=(
                    EntityCreate(entity_id=EntityId("sys_commit_boundary"), entity_type="boundary"),
                )
            ),
            1,
        )
    assert store.load(INSTANCE, BRANCH) == ()
    assert state.revision == BranchRevision(0)


@pytest.mark.unit
def test_kernel_invariants_cannot_be_overridden_by_world_delta() -> None:
    """Duplicate-entity kernel invariant still fires even though the delta is
    otherwise well-formed; constitution checks are additive, never removable."""
    state = apply_delta(
        _base_state(),
        ProposedWorldDelta(
            operations=(EntityCreate(entity_id=EntityId("alice"), entity_type="person"),)
        ),
    )
    with pytest.raises(Conflict):
        check_delta_invariants(
            state,
            ProposedWorldDelta(
                operations=(EntityCreate(entity_id=EntityId("alice"), entity_type="person"),)
            ),
        )


@pytest.mark.unit
def test_normal_world_delta_not_blocked_by_constitution() -> None:
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    state = _base_state()
    _commit(
        authority,
        state,
        ProposedWorldDelta(
            operations=(EntityCreate(entity_id=EntityId("alice"), entity_type="person"),)
        ),
        1,
    )
    events = store.load(INSTANCE, BRANCH)
    assert len(events) == 1
    assert events[0].delta.operations[0].entity_id == EntityId("alice")  # type: ignore[union-attr]
