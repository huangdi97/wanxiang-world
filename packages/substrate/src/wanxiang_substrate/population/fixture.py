"""Synthetic micro-town fixture for the autonomous scheduler (explicitly synthetic).

Two focus residents with body conditions + population resolutions, and a guard
duty actor with a recurring duty + a world clock. The scheduler advances this
town without user input.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.body.components import condition_component
from wanxiang_substrate.institution.components import duty_component
from wanxiang_substrate.population.components import resolution_component
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_town")
DAY = 100
RESIDENT_A = EntityId("resident_a")
RESIDENT_B = EntityId("resident_b")
GUARD = EntityId("guard")
DUTY_GUARD = EntityId("duty_guard")


def town_delta() -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(
                entity_id=RESIDENT_A,
                entity_type="person",
                components=(
                    condition_component(health=100, energy=90, sleep=80, mobility=100),
                    resolution_component(RESIDENT_A, "focus", rate_ticks=20),
                ),
            ),
            EntityCreate(
                entity_id=RESIDENT_B,
                entity_type="person",
                components=(
                    condition_component(health=100, energy=85, sleep=75, mobility=100),
                    resolution_component(RESIDENT_B, "lightweight", rate_ticks=50),
                ),
            ),
            EntityCreate(
                entity_id=GUARD,
                entity_type="person",
                components=(
                    condition_component(health=100, energy=80, sleep=70, mobility=100),
                    resolution_component(GUARD, "duty", rate_ticks=25),
                ),
            ),
            EntityCreate(
                entity_id=DUTY_GUARD,
                entity_type="institution.duty",
                components=(duty_component(DUTY_GUARD, GUARD, "guard_rounds", due_ticks=DAY),),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"town": town_delta}


def build_town_fixture_commands(
    branch_id: BranchId,
    start_revision: int = 0,
    command_id: str = "cmd_town",
    instance_id: WorldInstanceId | None = None,
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the micro-town fixture."""
    from wanxiang_substrate.population.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance_id or INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "town", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
