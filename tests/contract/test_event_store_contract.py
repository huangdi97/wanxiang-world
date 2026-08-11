"""GOAL_01C: reusable EventStore contract tests.

Every adapter (in-memory now; SQLite in GOAL_01E) must pass this suite so
ordering/idempotency/integrity semantics stay identical across adapters.
"""

from __future__ import annotations

import pytest
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.errors import Conflict, DuplicateCommandConflict, PersistenceError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId, EntityId, EventId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.ports import EventStore, InMemoryEventStore

INSTANCE = WorldInstanceId("wld_c1")
BRANCH = BranchId("br_c1")


def make_event(seq: int, command: str = "cmd_a") -> CommittedEvent:
    return CommittedEvent(
        event_id=EventId(f"evt_{seq}"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        event_seq=EventSeq(seq),
        revision=BranchRevision(seq),
        schema_version=SchemaVersion(1),
        command_id=CommandId(command),
        delta=ProposedWorldDelta(
            operations=(EntityCreate(entity_id=EntityId(f"ent_{seq}"), entity_type="token_holder"),)
        ),
        world_time=WorldTime(seq),
        rule_version=RuntimeVersion(1),
    )


class EventStoreContract:
    """Abstract contract; subclasses provide the adapter."""

    @pytest.fixture
    def store(self) -> EventStore:
        raise NotImplementedError

    @pytest.mark.contract
    def test_sequential_appends_advance_seq(self, store: EventStore) -> None:
        store.append(make_event(1, "cmd_1"))
        store.append(make_event(2, "cmd_2"))
        assert store.last_event_seq(INSTANCE, BRANCH) == EventSeq(2)

    @pytest.mark.contract
    def test_load_returns_ordered_events(self, store: EventStore) -> None:
        store.append(make_event(1, "cmd_1"))
        store.append(make_event(2, "cmd_2"))
        events = store.load(INSTANCE, BRANCH)
        assert [e.event_seq.value for e in events] == [1, 2]

    @pytest.mark.contract
    def test_range_loading(self, store: EventStore) -> None:
        for i in range(1, 5):
            store.append(make_event(i, f"cmd_{i}"))
        assert [e.event_seq.value for e in store.load(INSTANCE, BRANCH, from_seq=2, to_seq=3)] == [
            2,
            3,
        ]
        assert [e.event_seq.value for e in store.load(INSTANCE, BRANCH, from_seq=3)] == [3, 4]

    @pytest.mark.contract
    def test_out_of_order_append_is_rejected(self, store: EventStore) -> None:
        store.append(make_event(1, "cmd_1"))
        with pytest.raises(Conflict):
            store.append(make_event(3, "cmd_3"))

    @pytest.mark.contract
    def test_duplicate_command_id_is_rejected(self, store: EventStore) -> None:
        store.append(make_event(1, "cmd_1"))
        with pytest.raises(DuplicateCommandConflict):
            store.append(make_event(2, "cmd_1"))
        assert store.last_event_seq(INSTANCE, BRANCH) == EventSeq(1)

    @pytest.mark.contract
    def test_command_result_retrieval(self, store: EventStore) -> None:
        store.append(make_event(1, "cmd_dup"))
        assert store.has_command(CommandId("cmd_dup")) is True
        assert store.command_result_event(CommandId("cmd_dup")) is not None
        assert store.command_result_event(CommandId("cmd_missing")) is None

    @pytest.mark.contract
    def test_integrity_check_passes_for_clean_stream(self, store: EventStore) -> None:
        store.append(make_event(1, "cmd_1"))
        store.append(make_event(2, "cmd_2"))
        store.integrity_check(INSTANCE, BRANCH)

    @pytest.mark.contract
    def test_wall_clock_does_not_change_order(self, store: EventStore) -> None:
        # Events carry no wall clock in the contract; ordering is by event_seq.
        store.append(make_event(1, "cmd_1"))
        store.append(make_event(2, "cmd_2"))
        assert [e.event_seq.value for e in store.load(INSTANCE, BRANCH)] == [1, 2]

    @pytest.mark.contract
    def test_failure_injection_leaves_no_partial_append(self, store: EventStore) -> None:
        assert isinstance(store, InMemoryEventStore)
        store.fail_append = True  # type: ignore[attr-defined]
        with pytest.raises(PersistenceError):
            store.append(make_event(1, "cmd_1"))
        assert store.last_event_seq(INSTANCE, BRANCH) == EventSeq(0)


class TestInMemoryEventStoreContract(EventStoreContract):
    @pytest.fixture
    def store(self) -> EventStore:
        return InMemoryEventStore()
