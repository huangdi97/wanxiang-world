"""Synthetic condition fixture (explicitly synthetic).

One healthy actor and one fatigued actor (energy below threshold), used to prove
body condition can block an otherwise valid action.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.body.components import condition_component
from wanxiang_substrate.spatial.components import position_component
from wanxiang_substrate.spatial.fixture import HALL

INSTANCE = WorldInstanceId("wld_body")
HEALTHY = EntityId("healthy")
TIRED = EntityId("tired")


def body_delta() -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=HEALTHY,
                entity_type="person",
                components=(
                    condition_component(health=100, energy=90, sleep=90, mobility=100),
                    position_component(HEALTHY, HALL),
                ),
            ),
            EntityCreate(
                entity_id=TIRED,
                entity_type="person",
                components=(
                    condition_component(health=100, energy=10, sleep=80, mobility=100),
                    position_component(TIRED, HALL),
                ),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"body": body_delta}


def build_condition_fixture_commands(
    branch_id: BranchId,
    start_revision: int = 0,
    command_id: str = "cmd_body",
    instance_id: WorldInstanceId | None = None,
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the body fixture."""
    from wanxiang_substrate.body.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance_id or INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "body", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
