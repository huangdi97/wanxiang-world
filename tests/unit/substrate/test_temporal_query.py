"""G02B: temporal query semantics."""

from __future__ import annotations

import pytest
from wanxiang_domain.delta import EntityUpdate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta
from wanxiang_substrate.temporal.fixture import (
    APPT_MORNING,
    DAY,
    RECUR_GUARD,
    calendar_delta,
)
from wanxiang_substrate.temporal.query import TemporalQuery


def _state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=WorldInstanceId("wld_tq"),
        branch_id=BranchId("br_tq"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )


@pytest.fixture
def calendar_state() -> InMemoryCanonicalState:
    return apply_delta(_state(), calendar_delta())


@pytest.mark.unit
def test_clock_and_due_queries(calendar_state: InMemoryCanonicalState) -> None:
    query = TemporalQuery(calendar_state)
    assert query.now() == 0
    assert query.due_appointments() == ()
    # Advance the clock locally to the morning appointment window.
    from wanxiang_substrate.temporal.components import clock_component

    advanced = calendar_state.apply(
        ProposedWorldDelta(
            operations=(
                EntityUpdate(
                    entity_id=EntityId("world_clock"),
                    components=(clock_component(DAY + 15),),
                ),
            )
        )
    )
    q2 = TemporalQuery(advanced)
    assert q2.now() == DAY + 15
    due = q2.due_appointments()
    assert len(due) == 1
    assert due[0].appointment_id == APPT_MORNING


@pytest.mark.unit
def test_deadlines_and_recurrence(calendar_state: InMemoryCanonicalState) -> None:
    query = TemporalQuery(calendar_state)
    assert query.due_deadlines() == ()  # due at 2*DAY
    assert query.next_occurrences(RECUR_GUARD, 3 * DAY) == (DAY, 2 * DAY, 3 * DAY)
    assert query.calendar().day_of(DAY) == 1


@pytest.mark.unit
def test_schedule_conflict_detection(calendar_state: InMemoryCanonicalState) -> None:
    query = TemporalQuery(calendar_state)
    conflicts = query.conflicts(EntityId("actor_a"), DAY + 5, DAY + 25)
    assert any(a.appointment_id == APPT_MORNING for a in conflicts)
    assert query.conflicts(EntityId("actor_b"), DAY + 5, DAY + 25) == ()
