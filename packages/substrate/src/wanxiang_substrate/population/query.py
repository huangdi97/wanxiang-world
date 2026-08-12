"""Deterministic population/scheduler queries over canonical state."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.population.components import (
    RESOLUTION_COMPONENT,
    SCHEDULER_RUN_COMPONENT,
)
from wanxiang_substrate.population.model import PopulationLevel, SchedulerConfig, SchedulerEvent


class PopulationQuery:
    """Read-only population projection over the canonical state."""

    def __init__(self, state: InMemoryCanonicalState, now_ticks: int = 0) -> None:
        self._resolutions: dict[EntityId, tuple[str, int]] = {}
        self._runs: list[dict[str, int]] = []
        self._now = now_ticks
        self._scan(state)
        self._institution = InstitutionQuery(state, now_ticks=now_ticks)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                if component.component_type == RESOLUTION_COMPONENT:
                    actor = component.fields.get("actor_id")
                    level = component.fields.get("level", "lightweight")
                    rate = component.fields.get("rate_ticks", 50)
                    if isinstance(actor, str):
                        self._resolutions[EntityId(actor)] = (
                            str(level),
                            rate if isinstance(rate, int) else 50,
                        )
                elif component.component_type == SCHEDULER_RUN_COMPONENT:
                    self._runs.append(
                        {
                            "seed": _int_field(component.fields, "seed"),
                            "horizon": _int_field(component.fields, "horizon_ticks"),
                            "events": _int_field(component.fields, "events_submitted"),
                        }
                    )

    def level(self, actor_id: EntityId) -> PopulationLevel:
        value, _ = self._resolutions.get(actor_id, ("lightweight", 50))
        return value if value in ("focus", "lightweight", "duty", "aggregate") else "lightweight"  # type: ignore[return-value]

    def rate_ticks(self, actor_id: EntityId) -> int:
        _, rate = self._resolutions.get(actor_id, ("lightweight", 50))
        return rate

    def schedulable_actors(self) -> tuple[EntityId, ...]:
        return tuple(
            sorted(
                (a for a in self._resolutions if self._resolutions[a][0] != "aggregate"),
                key=lambda a: a.value,
            )
        )

    def pending_duties(self, actor_id: EntityId) -> tuple[object, ...]:
        return self._institution.due_duties(actor_id)

    def scheduler_runs(self) -> tuple[dict[str, int], ...]:
        return tuple(self._runs)


def build_initial_events(
    query: PopulationQuery,
    config: SchedulerConfig,
    start_ticks: int,
    seq_start: int = 0,
) -> tuple[SchedulerEvent, ...]:
    """Initial deterministic event set from population resolutions."""
    events: list[SchedulerEvent] = []
    seq = seq_start
    for actor in query.schedulable_actors():
        level = query.level(actor)
        rate = query.rate_ticks(actor)
        action = "scheduler.rest"
        priority = 5 if level == "focus" else 3
        due = start_ticks + rate
        events.append(
            SchedulerEvent(due_ticks=due, priority=priority, actor_id=actor, action=action, seq=seq)
        )
        seq += 1
    return tuple(events)


def _int_field(fields: Mapping[str, object], key: str, default: int = 0) -> int:
    value = fields.get(key, default)
    return value if isinstance(value, int) and not isinstance(value, bool) else default
