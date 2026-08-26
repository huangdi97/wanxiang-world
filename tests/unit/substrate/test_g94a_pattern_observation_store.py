"""G94A: pattern observations are deterministic, typed, and rebuildable."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    ProposedWorldDelta,
    RelationCreate,
    RelationDelete,
)
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ContractError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import (
    ActorId,
    BranchId,
    CommandId,
    ComponentId,
    EntityId,
    EventId,
    RelationId,
    WorldInstanceId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_substrate.evolution.pattern_observation import PatternObservationStore

INSTANCE = WorldInstanceId("wld_g94a_unit")
BRANCH = BranchId("br_g94a_unit")
SCHEMA = SchemaVersion(1)


def _event(index: int, tick: int, operation: object, *, actor: str = "alice") -> CommittedEvent:
    return CommittedEvent(
        event_id=EventId(f"evt_g94a_{index}"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        event_seq=EventSeq(index),
        revision=BranchRevision(index),
        schema_version=SCHEMA,
        command_id=CommandId(f"cmd_g94a_{index}"),
        delta=ProposedWorldDelta(operations=(operation,)),  # type: ignore[arg-type]
        world_time=WorldTime(tick),
        rule_version=RuntimeVersion(1),
        actor_id=ActorId(actor) if actor else None,
    )


def _events() -> tuple[CommittedEvent, ...]:
    return (
        _event(1, 5, EntityCreate(EntityId("alice"), "person")),
        _event(
            2,
            105,
            EntityUpdate(
                EntityId("alice"),
                (ComponentData(ComponentId("status_2"), "synthetic.status", SCHEMA),),
            ),
        ),
        _event(
            3,
            110,
            RelationCreate(RelationId("ally_3"), "ally", EntityId("alice"), EntityId("bob")),
        ),
        _event(
            4,
            205,
            EntityUpdate(
                EntityId("alice"),
                (ComponentData(ComponentId("custody_4"), "material.custody", SCHEMA),),
            ),
        ),
        _event(5, 305, EntityCreate(EntityId("club_5"), "institution.club")),
        _event(6, 405, RelationDelete(RelationId("ally_3"))),
        _event(7, 505, EntityDelete(EntityId("alice"))),
    )


@pytest.mark.unit
def test_store_derives_typed_windowed_observations_and_statistics() -> None:
    store = PatternObservationStore.rebuild(_events(), window_size=100)

    assert {item.kind for item in store.observations()} == {
        "behavior",
        "relationship",
        "exchange",
        "organization",
    }
    assert store.query_window(100, 200, kind="behavior")[0].key == (
        "entity.update:synthetic.status"
    )
    assert store.query(kind="relationship", key="relation.create:ally")[0].event_refs == (
        "evt_g94a_3",
    )
    assert store.query(kind="exchange")[0].window_start == 200
    stats = store.statistics(window_start=0, window_end=600)
    assert stats.observation_count == 7
    assert stats.total_occurrences == 7
    assert stats.unique_event_count == 7
    assert stats.unique_key_count == 7
    assert stats.unique_subject_count == 4
    assert stats.by_kind == (
        ("behavior", 3),
        ("exchange", 1),
        ("organization", 1),
        ("relationship", 2),
    )
    assert store.event_refs() == tuple(f"evt_g94a_{index}" for index in range(1, 8))


@pytest.mark.unit
def test_store_rebuild_is_order_independent_and_rejects_invalid_history() -> None:
    events = _events()
    forward = PatternObservationStore.from_events(events, window_size=100)
    reverse = PatternObservationStore.from_events(reversed(events), window_size=100)
    assert reverse.cache_hash() == forward.cache_hash()
    assert reverse.to_dict() == forward.to_dict()

    duplicate = events + (events[0],)
    with pytest.raises(ContractError, match="duplicate event refs"):
        PatternObservationStore.rebuild(duplicate)
    other_branch = _event(8, 605, EntityCreate(EntityId("other"), "person"))
    other_branch = replace(other_branch, branch_id=BranchId("br_other"))
    with pytest.raises(ContractError, match="one instance and branch"):
        PatternObservationStore.rebuild(events + (other_branch,))
    with pytest.raises(ContractError, match="positive"):
        PatternObservationStore.rebuild(events, window_size=0)
    with pytest.raises(ContractError, match="invalid pattern query"):
        forward.query(window_start=10, window_end=10)
