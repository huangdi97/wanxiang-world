"""Synthetic calendar fixture (explicitly synthetic, spans day boundaries).

A world clock at tick 0, two actors, a recurring guard duty (daily), a
one-shot deadline and a morning appointment — deterministic scheduling tests.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.temporal.components import (
    CLOCK_ENTITY,
    appointment_component,
    clock_component,
    deadline_component,
    recurring_component,
)

INSTANCE = WorldInstanceId("wld_calendar")
DAY = 100  # one synthetic day = 100 ticks

ACTOR_A = EntityId("actor_a")
ACTOR_B = EntityId("actor_b")
APPT_MORNING = EntityId("appt_a_morning")
DEADLINE_REPORT = EntityId("deadline_report")
RECUR_GUARD = EntityId("recur_guard_duty")


def calendar_delta() -> ProposedWorldDelta:
    """Creation delta: clock at 0, actors, recurring duty, deadline, appointment."""
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(entity_id=ACTOR_A, entity_type="person", components=()),
            EntityCreate(entity_id=ACTOR_B, entity_type="person", components=()),
            EntityCreate(
                entity_id=RECUR_GUARD,
                entity_type="temporal.recurring",
                components=(
                    recurring_component(
                        RECUR_GUARD, "guard_duty", anchor_ticks=DAY, interval_ticks=DAY
                    ),
                ),
            ),
            EntityCreate(
                entity_id=DEADLINE_REPORT,
                entity_type="temporal.deadline",
                components=(deadline_component(DEADLINE_REPORT, ACTOR_A, due_ticks=2 * DAY),),
            ),
            EntityCreate(
                entity_id=APPT_MORNING,
                entity_type="temporal.appointment",
                components=(
                    appointment_component(
                        APPT_MORNING,
                        ACTOR_A,
                        "morning_meeting",
                        start_ticks=DAY + 10,
                        end_ticks=DAY + 20,
                    ),
                ),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"calendar": calendar_delta}


def build_calendar_fixture_commands(
    branch_id: BranchId, start_revision: int = 0, command_id: str = "cmd_calendar"
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the calendar fixture."""
    from wanxiang_substrate.temporal.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "calendar", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
