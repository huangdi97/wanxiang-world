"""Synthetic rumor -> correction epistemic fixture (explicitly synthetic).

An actor holds a low-confidence rumor belief, then receives a higher-confidence
correction. Both are retained; the correction links to the superseded belief.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.epistemic.components import (
    belief_component,
    memory_component,
)

INSTANCE = WorldInstanceId("wld_rumor")
ACTOR = EntityId("villager")
MEM_RUMOR = EntityId("memory_rumor")
MEM_CORRECTION = EntityId("memory_correction")
BELIEF_RUMOR = EntityId("belief_rumor")


def rumor_delta() -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(entity_id=ACTOR, entity_type="person", components=()),
            EntityCreate(
                entity_id=MEM_RUMOR,
                entity_type="epistemic.memory",
                components=(
                    memory_component(
                        MEM_RUMOR, ACTOR, "observation", "ref://rumor", at_ticks=10, salience=0.4
                    ),
                ),
            ),
            EntityCreate(
                entity_id=MEM_CORRECTION,
                entity_type="epistemic.memory",
                components=(
                    memory_component(
                        MEM_CORRECTION,
                        ACTOR,
                        "observation",
                        "ref://correction",
                        at_ticks=30,
                        salience=0.9,
                    ),
                ),
            ),
            EntityCreate(
                entity_id=BELIEF_RUMOR,
                entity_type="epistemic.belief",
                components=(
                    belief_component(
                        BELIEF_RUMOR,
                        ACTOR,
                        "treasure_is_in_the_cellar",
                        confidence=0.3,
                        at_ticks=10,
                        source_ref="ref://rumor",
                    ),
                ),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"rumor": rumor_delta}


def build_rumor_fixture_commands(
    branch_id: BranchId,
    start_revision: int = 0,
    command_id: str = "cmd_rumor",
    instance_id: WorldInstanceId | None = None,
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the rumor fixture."""
    from wanxiang_substrate.epistemic.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance_id or INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "rumor", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
