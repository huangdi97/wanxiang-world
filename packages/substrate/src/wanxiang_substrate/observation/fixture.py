"""Synthetic confidential-letter / overheard-message fixture (explicitly synthetic).

A house (hall + kitchen, open door) with observers, plus a sealed confidential
letter held by a messenger. Used to prove perspective isolation: custody does
not reveal payload content, and only actors in perception range observe events.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.material.components import (
    custody_component,
    info_payload_component,
    item_component,
)
from wanxiang_substrate.spatial.components import (
    place_component,
    portal_component,
    position_component,
)
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_obs")
HALL = EntityId("hall")
KITCHEN = EntityId("kitchen")
ALICE = EntityId("alice")
BOB = EntityId("bob")
LETTER = EntityId("letter_confidential")
MESSENGER = EntityId("messenger")
PAYLOAD = EntityId(f"payload_{LETTER.value}")


def confidential_delta() -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(
                entity_id=HALL,
                entity_type="spatial.place",
                components=(place_component(EntityId("house"), "hall", capacity=8),),
            ),
            EntityCreate(
                entity_id=KITCHEN,
                entity_type="spatial.place",
                components=(place_component(EntityId("house"), "kitchen", capacity=4),),
            ),
            EntityCreate(
                entity_id=EntityId("door_hk"),
                entity_type="spatial.portal",
                components=(portal_component(HALL, KITCHEN, state="open"),),
            ),
            EntityCreate(
                entity_id=ALICE,
                entity_type="person",
                components=(position_component(ALICE, HALL),),
            ),
            EntityCreate(
                entity_id=BOB,
                entity_type="person",
                components=(position_component(BOB, KITCHEN),),
            ),
            EntityCreate(
                entity_id=MESSENGER,
                entity_type="person",
                components=(position_component(MESSENGER, HALL),),
            ),
            EntityCreate(
                entity_id=LETTER,
                entity_type="material.item",
                components=(
                    item_component(LETTER, "letter"),
                    custody_component(LETTER, MESSENGER),
                ),
            ),
            EntityCreate(
                entity_id=PAYLOAD,
                entity_type="material.info_payload",
                components=(
                    info_payload_component(LETTER, "ref://confidential/body", state="sealed"),
                ),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"confidential": confidential_delta}


def build_confidential_fixture_commands(
    branch_id: BranchId,
    start_revision: int = 0,
    command_id: str = "cmd_confidential",
    instance_id: WorldInstanceId | None = None,
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the confidential fixture."""
    from wanxiang_substrate.observation.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance_id or INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "confidential", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
