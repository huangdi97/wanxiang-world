"""GOAL_01D: branch fork and isolation."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA, build_fixture_events
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata, BranchRevision, EventSeq
from wanxiang_domain.ids import CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.branch import fork_branch
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState


def _parent_metadata() -> BranchMetadata:
    return BranchMetadata(
        branch_id=BRANCH,
        instance_id=INSTANCE,
        ancestry=BranchAncestry(),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


@pytest.mark.unit
def test_fork_child_has_correct_ancestry() -> None:
    events = build_fixture_events()
    parent_state = ReplayEngine(RULES, SCHEMA).replay(events)
    child = fork_branch(
        _parent_metadata(),
        parent_state,
        fork_revision=BranchRevision(5),
        fork_event_seq=EventSeq(5),
        snapshot_ref="mem://snap_5",
    )
    assert child.ancestry == BranchAncestry(
        parent_branch_id=BRANCH,
        fork_revision=BranchRevision(5),
        fork_event_seq=EventSeq(5),
        fork_snapshot_ref="mem://snap_5",
    )
    assert child.branch_id != BRANCH


@pytest.mark.unit
def test_fork_beyond_head_is_rejected() -> None:
    parent_state = ReplayEngine(RULES, SCHEMA).replay(build_fixture_events())
    with pytest.raises(ValidationRejected):
        fork_branch(
            _parent_metadata(),
            parent_state,
            fork_revision=BranchRevision(9),
            fork_event_seq=EventSeq(9),
            snapshot_ref="x",
        )


@pytest.mark.unit
def test_child_commit_does_not_mutate_parent() -> None:
    events = build_fixture_events()
    engine = ReplayEngine(RULES, SCHEMA)
    parent_state = engine.replay(events)
    parent_hash = parent_state.semantic_hash()
    parent_stream = InMemoryEventStore()
    for event in events:
        parent_stream.append(event)

    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA, branch_base_revision=BranchRevision(5))
    child_state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(5),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    # Copy parent entities into the child baseline (forks share state content).
    for entity in parent_state.entities():
        child_state = child_state.apply(
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=entity.entity_id,
                        entity_type=entity.entity_type,
                        components=tuple(entity.components.values()),
                    ),
                )
            )
        )
    child_state = child_state.with_revision(BranchRevision(5))
    child_branch = fork_branch(
        _parent_metadata(),
        child_state,
        fork_revision=BranchRevision(5),
        fork_event_seq=EventSeq(5),
        snapshot_ref="mem://snap_5",
    )
    child_req = CommitRequest(
        command_id=CommandId("cmd_child"),
        instance_id=INSTANCE,
        branch_id=child_branch.branch_id,
        expected_revision=BranchRevision(5),
        delta=ProposedWorldDelta(
            operations=(EntityCreate(entity_id=EntityId("carol"), entity_type="person"),)
        ),
        world_time=WorldTime(6),
        rule_version=RULES,
    )
    # Tag the child baseline with the child branch id, then commit.
    child_committed = child_state.with_branch(child_branch.branch_id)
    authority.commit(child_committed, child_req)

    # Parent stream/hash unchanged.
    assert parent_stream.load(INSTANCE, BRANCH) == tuple(events)
    assert parent_hash == engine.replay(parent_stream.load(INSTANCE, BRANCH)).semantic_hash()
    # Child reports ancestry and has its own event.
    child_events = store.load(INSTANCE, child_branch.branch_id)
    assert len(child_events) == 1
    assert child_branch.ancestry.parent_branch_id == BRANCH
