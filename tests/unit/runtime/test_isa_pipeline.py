"""G30E: ISA -> existing pipeline mapping invariants."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata, BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, RelationId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.world_isa import WorldIsaOp
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.isa_pipeline import PromotionUseCase, execute_isa
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState


def _base_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


def _parent_metadata() -> BranchMetadata:
    return BranchMetadata(
        branch_id=BRANCH,
        instance_id=INSTANCE,
        ancestry=BranchAncestry(),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


@pytest.mark.unit
def test_isa_declare_matches_business_action_semantic_outcome() -> None:
    # Old entry: business action through the application pipeline.
    store_old = InMemoryEventStore()
    authority_old = CommitAuthority(store_old, RULES, SCHEMA)
    state_old = _base_state()
    authority_old.commit(
        state_old,
        CommitRequest(
            command_id=CommandId("cmd_business"),
            instance_id=INSTANCE,
            branch_id=BRANCH,
            expected_revision=BranchRevision(0),
            delta=ProposedWorldDelta(
                operations=(EntityCreate(entity_id=EntityId("alice"), entity_type="person"),)
            ),
            world_time=WorldTime(1),
            rule_version=RULES,
        ),
    )
    old_hash = ReplayEngine(RULES, SCHEMA).replay(store_old.load(INSTANCE, BRANCH)).semantic_hash()

    # ISA entry: same semantic instruction through the same pipeline type.
    store_isa = InMemoryEventStore()
    authority_isa = CommitAuthority(store_isa, RULES, SCHEMA)
    result = execute_isa(
        WorldIsaOp(op="DECLARE", payload={"entity_id": "alice", "entity_type": "person"}),
        authority_isa,
        _base_state(),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        world_time=WorldTime(1),
    )
    assert result.event is not None
    isa_hash = ReplayEngine(RULES, SCHEMA).replay(store_isa.load(INSTANCE, BRANCH)).semantic_hash()
    assert isa_hash == old_hash
    # No second event stream: one store, one schema, same shape.
    assert len(store_isa.load(INSTANCE, BRANCH)) == 1
    assert len(store_old.load(INSTANCE, BRANCH)) == 1


@pytest.mark.unit
def test_assert_reuses_relation_transition() -> None:
    authority = CommitAuthority(InMemoryEventStore(), RULES, SCHEMA)
    state = _base_state()
    # declare both entities first
    for i, entity in enumerate(("alice", "bob"), start=1):
        result = execute_isa(
            WorldIsaOp(op="DECLARE", payload={"entity_id": entity, "entity_type": "person"}),
            authority,
            state,
            instance_id=INSTANCE,
            branch_id=BRANCH,
            world_time=WorldTime(i),
        )
        assert result.state_after is not None
        state = result.state_after
    result = execute_isa(
        WorldIsaOp(
            op="ASSERT",
            payload={
                "relation_id": "gift",
                "relation_type": "gift",
                "source_id": "alice",
                "target_id": "bob",
            },
        ),
        authority,
        state,
        instance_id=INSTANCE,
        branch_id=BRANCH,
        world_time=WorldTime(3),
    )
    assert result.state_after is not None
    assert result.state_after.relation(RelationId("gift")) is not None


@pytest.mark.unit
def test_validate_runs_kernel_invariants_only() -> None:
    authority = CommitAuthority(InMemoryEventStore(), RULES, SCHEMA)
    state = _base_state()
    result = execute_isa(
        WorldIsaOp(op="VALIDATE", payload={"entity_id": "alice", "entity_type": "person"}),
        authority,
        state,
        instance_id=INSTANCE,
        branch_id=BRANCH,
        world_time=WorldTime(1),
    )
    assert result.validated is True
    assert result.event is None  # validation never commits


@pytest.mark.unit
def test_fork_reuses_branch_semantics() -> None:
    authority = CommitAuthority(InMemoryEventStore(), RULES, SCHEMA)
    state = _base_state()
    result = execute_isa(
        WorldIsaOp(op="FORK", payload={"snapshot_ref": "mem://isa-fork"}),
        authority,
        state,
        instance_id=INSTANCE,
        branch_id=BRANCH,
        world_time=WorldTime(1),
        parent=_parent_metadata(),
    )
    assert result.branch is not None
    assert result.branch.ancestry.parent_branch_id == BRANCH
    assert result.event is None


@pytest.mark.unit
def test_promote_generates_use_case_without_committing_parent() -> None:
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    state = _base_state()
    result = execute_isa(
        WorldIsaOp(
            op="PROMOTE",
            payload={
                "source_worldline": "wld_parent",
                "target_world_definition": "pack://derived@1.0.0",
                "candidate": "cand_001",
            },
        ),
        authority,
        state,
        instance_id=INSTANCE,
        branch_id=BRANCH,
        world_time=WorldTime(1),
    )
    assert isinstance(result.promotion, PromotionUseCase)
    assert result.event is None
    # Parent worldline untouched: no commit happened.
    assert store.load(INSTANCE, BRANCH) == ()
