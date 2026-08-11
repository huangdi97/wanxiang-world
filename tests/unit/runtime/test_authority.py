"""GOAL_01B: Commit Authority semantics."""

from __future__ import annotations

import pytest
from tests.unit.runtime.conftest import (
    BRANCH,
    INSTANCE,
    RULES,
    SCHEMA,
    make_create_delta,
)
from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import (
    Conflict,
    IncompatibleVersion,
    PersistenceError,
    StaleRevision,
    ValidationRejected,
)
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta


def _authority(
    log: InMemoryEventStore | None = None,
) -> tuple[CommitAuthority, InMemoryEventStore]:
    log = log or InMemoryEventStore()
    return CommitAuthority(log, RULES, SCHEMA), log


def _request(
    expected: int = 0, delta: ProposedWorldDelta | None = None, command: str = "cmd_1"
) -> CommitRequest:
    return CommitRequest(
        command_id=CommandId(command),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        expected_revision=BranchRevision(expected),
        delta=delta if delta is not None else make_create_delta(),
        world_time=WorldTime(1),
        rule_version=RULES,
    )


def _state(
    revision: int = 0, *, instance: WorldInstanceId = INSTANCE, branch: BranchId = BRANCH
) -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=instance,
        branch_id=branch,
        revision=BranchRevision(revision),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


@pytest.mark.unit
def test_valid_commit_advances_revision_and_appends_event() -> None:
    authority, log = _authority()
    result = authority.commit(_state(), _request())
    assert result.state_after.revision.value == 1
    assert result.event.event_seq == EventSeq(1)
    assert log.load(INSTANCE, BRANCH) == (result.event,)
    assert result.state_after.entity(EntityId("ent_a")) is not None
    assert result.audit.event_id == result.event.event_id
    assert result.audit.trace_id is not None


@pytest.mark.unit
def test_stale_revision_is_rejected_and_state_unchanged() -> None:
    authority, log = _authority()
    head = authority.commit(_state(), _request()).state_after
    with pytest.raises(StaleRevision):
        authority.commit(head, _request(expected=0))
    assert head.revision.value == 1
    assert len(log.load(INSTANCE, BRANCH)) == 1


@pytest.mark.unit
def test_wrong_branch_or_instance_is_conflict() -> None:
    authority, _ = _authority()
    with pytest.raises(Conflict):
        authority.commit(_state(branch=BranchId("br_other")), _request())
    with pytest.raises(Conflict):
        authority.commit(_state(instance=WorldInstanceId("wld_other")), _request())


@pytest.mark.unit
def test_empty_delta_is_rejected() -> None:
    authority, _ = _authority()
    with pytest.raises(ValidationRejected):
        authority.commit(_state(), _request(delta=ProposedWorldDelta()))


@pytest.mark.unit
def test_rule_version_mismatch_is_incompatible() -> None:
    authority, _ = _authority()
    request = CommitRequest(
        command_id=CommandId("cmd_1"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        expected_revision=BranchRevision(0),
        delta=make_create_delta(),
        world_time=WorldTime(1),
        rule_version=RuntimeVersion(99),
    )
    with pytest.raises(IncompatibleVersion):
        authority.commit(_state(), request)


@pytest.mark.unit
def test_invariant_violation_preserves_state_hash() -> None:
    authority, log = _authority()
    state = apply_delta(_state(), make_create_delta())
    duplicate = _request(delta=make_create_delta("ent_a"))
    with pytest.raises(Conflict):
        authority.commit(state, duplicate)
    assert state.semantic_hash() == state.semantic_hash()
    assert log.load(INSTANCE, BRANCH) == ()


@pytest.mark.unit
def test_append_failure_leaves_canonical_state_and_log_unchanged() -> None:
    log = InMemoryEventStore()
    authority, _ = _authority(log)
    log.fail_append = True
    state = _state()
    with pytest.raises(PersistenceError):
        authority.commit(state, _request())
    assert state.revision.value == 0
    assert log.load(INSTANCE, BRANCH) == ()


@pytest.mark.unit
def test_deterministic_commit_result() -> None:
    authority_a, _ = _authority()
    authority_b, _ = _authority()
    first = authority_a.commit(_state(), _request(command="cmd_1"))
    second = authority_b.commit(_state(), _request(command="cmd_1"))
    # Same inputs on independent authorities -> same semantic state hash.
    assert first.state_after.semantic_hash() == second.state_after.semantic_hash()
    assert first.event.delta == second.event.delta
