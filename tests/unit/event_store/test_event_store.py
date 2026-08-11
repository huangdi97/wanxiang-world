"""GOAL_01C: in-memory event store semantics beyond the shared contract."""

from __future__ import annotations

import pytest
from tests.contract.test_event_store_contract import BRANCH, INSTANCE, make_event
from wanxiang_domain.errors import CorruptEventStream
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId
from wanxiang_runtime.ports import InMemoryEventStore


@pytest.mark.unit
def test_streams_are_isolated_per_branch() -> None:
    store = InMemoryEventStore()
    other = BranchId("br_other")
    store.append(make_event(1, "cmd_1"))
    assert store.load(INSTANCE, other) == ()
    assert store.last_event_seq(INSTANCE, other) == EventSeq(0)


@pytest.mark.unit
def test_integrity_check_detects_gap() -> None:
    store = InMemoryEventStore()
    store.append(make_event(1, "cmd_1"))
    # Manually inject an event with a seq gap into the private stream.
    stream = store._streams[(INSTANCE.value, BRANCH.value)]  # type: ignore[attr-defined]
    stream.append(make_event(3, "cmd_3"))
    with pytest.raises(CorruptEventStream):
        store.integrity_check(INSTANCE, BRANCH)


@pytest.mark.unit
def test_concurrent_writers_same_revision_only_one_commits() -> None:
    from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
    from wanxiang_domain.errors import StaleRevision
    from wanxiang_domain.ids import EntityId
    from wanxiang_domain.time import WorldTime
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.authority import CommitAuthority, CommitRequest
    from wanxiang_runtime.state import InMemoryCanonicalState

    store = InMemoryEventStore()
    authority = CommitAuthority(store, RuntimeVersion(1), SchemaVersion(1))
    state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )

    def request(command: str, entity: str) -> CommitRequest:
        return CommitRequest(
            command_id=CommandId(command),
            instance_id=INSTANCE,
            branch_id=BRANCH,
            expected_revision=BranchRevision(0),
            delta=ProposedWorldDelta(
                operations=(EntityCreate(entity_id=EntityId(entity), entity_type="token_holder"),)
            ),
            world_time=WorldTime(1),
            rule_version=RuntimeVersion(1),
        )

    first = authority.commit(state, request("cmd_w1", "ent_w1"))
    # Second writer still holds the old state snapshot (revision 0).
    with pytest.raises(StaleRevision):
        authority.commit(state, request("cmd_w2", "ent_w2"))
    assert store.last_event_seq(INSTANCE, BRANCH) == EventSeq(1)
    assert first.state_after.revision.value == 1
