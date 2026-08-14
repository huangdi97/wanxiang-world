"""Deterministic multi-rate autonomous scheduler (G02F).

The scheduler advances world time and submits commands through the M1 Commit
Authority without any user input. Given the same initial snapshot + seed +
config, it reproduces the same event sequence and final canonical hash.

Revision tracking is incremental (no full replay per event) so long horizons
run in bounded time.
"""

from __future__ import annotations

import heapq
from collections.abc import Mapping
from contextlib import suppress

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import WanxiangError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.population.errors import SchedulerBudgetExceeded
from wanxiang_substrate.population.model import (
    SchedulerConfig,
    SchedulerEvent,
    SchedulerRunResult,
)
from wanxiang_substrate.population.query import PopulationQuery, build_initial_events
from wanxiang_substrate.runtime_port import WorldRuntimePort
from wanxiang_substrate.temporal.query import TemporalQuery

ACTION_ADVANCE = "temporal.advance"
ACTION_REST = "body.rest"
ACTION_COMPLETE_DUTY = "institution.complete_duty"


class AutonomousScheduler:
    """Advances a deterministic world autonomously to a horizon."""

    def __init__(
        self,
        runtime: WorldRuntimePort,
        seed: int,
        config: SchedulerConfig | None = None,
    ) -> None:
        self._runtime = runtime
        self._seed = seed
        self._config = config or SchedulerConfig()

    def run(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        horizon_ticks: int,
        run_id: str = "sched_run",
    ) -> SchedulerRunResult:
        state = self._runtime.current_state(instance_id, branch_id)
        now = TemporalQuery(state).now()
        query = PopulationQuery(state, now_ticks=now)
        events: list[SchedulerEvent] = list(build_initial_events(query, self._config, now))
        heapq.heapify(events)
        current_revision = state.revision.value
        pending_duties = _initial_duties(state)
        completed_duties: set[str] = set()
        submitted = 0
        rejected = 0
        seq = 0
        tick_counts: dict[int, int] = {}

        while events:
            next_event = events[0]
            if next_event.due_ticks > horizon_ticks:
                break
            if next_event.due_ticks > now:
                self._submit(
                    instance_id,
                    branch_id,
                    current_revision,
                    ACTION_ADVANCE,
                    {"ticks": next_event.due_ticks - now},
                    now,
                    seq,
                )
                current_revision += 1
                now = next_event.due_ticks

            event = heapq.heappop(events)
            if event.due_ticks != now:
                continue
            tick_counts[now] = tick_counts.get(now, 0) + 1
            if tick_counts[now] > self._config.max_events_per_tick:
                raise SchedulerBudgetExceeded(
                    f"more than {self._config.max_events_per_tick} events due at tick {now}"
                )
            if submitted >= self._config.total_event_budget:
                raise SchedulerBudgetExceeded(
                    f"total scheduler event budget {self._config.total_event_budget} exceeded"
                )

            action, payload = _resolve_action(event.actor_id, pending_duties, completed_duties)
            try:
                self._submit(
                    instance_id,
                    branch_id,
                    current_revision,
                    action,
                    payload,
                    now,
                    seq,
                )
                submitted += 1
                current_revision += 1
                if action == ACTION_COMPLETE_DUTY:
                    duty_id = payload.get("duty_id")
                    if isinstance(duty_id, str):
                        completed_duties.add(duty_id)
            except WanxiangError:
                # A proposed scheduler action that the world rejects is not an
                # error in the world: it simply does not commit. Track it so
                # rejections are observable instead of silently dropped.
                rejected += 1
            seq += 1

            if event.action == "scheduler.rest":
                rate = query.rate_ticks(event.actor_id)
                heapq.heappush(
                    events,
                    SchedulerEvent(
                        due_ticks=now + rate,
                        priority=event.priority,
                        actor_id=event.actor_id,
                        action=event.action,
                        seq=seq,
                    ),
                )

        # Record the scheduler run as committed canonical state (deterministic restore).
        # Best-effort by design: the run result is returned regardless; this marker
        # must never block the deterministic run from completing.
        with suppress(WanxiangError):
            self._submit(
                instance_id,
                branch_id,
                current_revision,
                "population.record_run",
                {
                    "run_id": run_id,
                    "seed": self._seed,
                    "horizon_ticks": horizon_ticks,
                    "events_submitted": submitted,
                },
                now,
                seq,
            )
        final = self._runtime.current_state(instance_id, branch_id)
        return SchedulerRunResult(
            run_id=run_id,
            seed=self._seed,
            events_submitted=submitted,
            final_hash=final.semantic_hash(),
            ticks_advanced=now,
            queue_stats={"peak_tick_events": max(tick_counts.values()) if tick_counts else 0},
            rejected_events=rejected,
        )

    def _submit(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        expected_revision: int,
        action: str,
        payload: Mapping[str, FieldValue],
        ticks: int,
        seq: int,
    ) -> None:
        self._runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(
                    f"sched_{expected_revision}_{action.replace('.', '_')}_{ticks}_{seq}"
                ),
                instance_id=instance_id,
                branch_id=branch_id,
                expected_revision=BranchRevision(expected_revision),
                action_type=action,
                payload=dict(payload),
                world_time=WorldTime(ticks),
            )
        )


def _initial_duties(state: InMemoryCanonicalState) -> dict[EntityId, str]:
    """Map schedulable actor -> first due duty id at start (deterministic)."""
    from wanxiang_substrate.institution.query import InstitutionQuery

    now = TemporalQuery(state).now()
    query = InstitutionQuery(state, now_ticks=now)
    result: dict[EntityId, str] = {}
    for actor in _all_actors(state):
        duties = query.due_duties(actor)
        if duties:
            first = sorted(duties, key=lambda d: (d.due_ticks, d.duty_id.value))[0]
            result[actor] = first.duty_id.value
    return result


def _all_actors(state: InMemoryCanonicalState) -> tuple[EntityId, ...]:
    return tuple(sorted((e.entity_id for e in state.entities()), key=lambda e: e.value))


def _resolve_action(
    actor_id: EntityId,
    pending_duties: Mapping[EntityId, str],
    completed_duties: set[str],
) -> tuple[str, Mapping[str, FieldValue]]:
    duty_id = pending_duties.get(actor_id)
    if duty_id is not None and duty_id not in completed_duties:
        return ACTION_COMPLETE_DUTY, {"duty_id": duty_id}
    return ACTION_REST, {"actor_id": actor_id.value, "ticks": 5}
