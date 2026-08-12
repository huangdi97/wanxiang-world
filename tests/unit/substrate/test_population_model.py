"""G02F: population/scheduler value-object invariants."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.population.model import SchedulerConfig, SchedulerEvent


@pytest.mark.unit
def test_scheduler_event_ordering_is_deterministic() -> None:
    a = SchedulerEvent(due_ticks=10, priority=5, actor_id=EntityId("z"), action="rest")
    b = SchedulerEvent(due_ticks=10, priority=5, actor_id=EntityId("a"), action="rest")
    c = SchedulerEvent(due_ticks=5, priority=1, actor_id=EntityId("m"), action="rest")
    events = sorted([a, b, c])
    assert [e.actor_id.value for e in events] == ["m", "a", "z"]


@pytest.mark.unit
def test_higher_priority_runs_first() -> None:
    low = SchedulerEvent(due_ticks=10, priority=1, actor_id=EntityId("a"), action="rest")
    high = SchedulerEvent(due_ticks=10, priority=9, actor_id=EntityId("a"), action="rest")
    assert high < low


@pytest.mark.unit
def test_scheduler_config_validation() -> None:
    assert SchedulerConfig().max_events_per_tick == 8
    with pytest.raises(ContractError):
        SchedulerConfig(max_events_per_tick=0)
