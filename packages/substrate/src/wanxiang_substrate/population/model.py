"""Pure population/scheduler value objects (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

PopulationLevel = Literal["focus", "lightweight", "duty", "aggregate"]
VALID_LEVELS = ("focus", "lightweight", "duty", "aggregate")


@dataclass(frozen=True, slots=True)
class SchedulerEvent:
    """A due scheduler event; ordering is deterministic.

    Heap order: earliest due first; higher priority first; then actor id and
    action for a stable tie-break.
    """

    due_ticks: int
    priority: int
    actor_id: EntityId
    action: str
    seq: int = 0

    def __lt__(self, other: SchedulerEvent) -> bool:
        return (
            self.due_ticks,
            -self.priority,
            self.actor_id.value,
            self.action,
            self.seq,
        ) < (
            other.due_ticks,
            -other.priority,
            other.actor_id.value,
            other.action,
            other.seq,
        )


@dataclass(frozen=True, slots=True)
class SchedulerConfig:
    """Resource budgets and rates for the autonomous scheduler."""

    max_events_per_tick: int = 8
    total_event_budget: int = 2000
    focus_rate_ticks: int = 10
    lightweight_rate_ticks: int = 50
    duty_rate_ticks: int = 25

    def __post_init__(self) -> None:
        if self.max_events_per_tick <= 0 or self.total_event_budget <= 0:
            raise ContractError("scheduler budgets must be positive")


@dataclass(frozen=True, slots=True)
class SchedulerRunResult:
    run_id: str
    seed: int
    events_submitted: int
    final_hash: str
    ticks_advanced: int
    queue_stats: dict[str, int]
    rejected_events: int = 0
