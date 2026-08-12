"""Synthetic multi-room house fixture (explicitly synthetic, no real content).

The fixture is a deterministic world definition applied through the
`spatial.instantiate` resolver (which still flows through Commit Authority).
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.spatial.components import (
    access_key_component,
    place_component,
    portal_component,
    position_component,
    region_component,
)

INSTANCE = WorldInstanceId("wld_house")
REGION = EntityId("house")
HALL = EntityId("hall")
KITCHEN = EntityId("kitchen")
GARDEN = EntityId("garden")
DOOR_HK = EntityId("door_hall_kitchen")
DOOR_HG = EntityId("door_hall_garden")
KEY = EntityId("house_key")
ALICE = EntityId("alice")
BOB = EntityId("bob")
NO_KEY = EntityId("no_key")


def house_delta() -> ProposedWorldDelta:
    """Creation delta for the synthetic house (region, places, portals, actors)."""
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=REGION,
                entity_type="spatial.region",
                components=(region_component("house"),),
            ),
            EntityCreate(
                entity_id=HALL,
                entity_type="spatial.place",
                components=(place_component(REGION, "hall", capacity=4),),
            ),
            EntityCreate(
                entity_id=KITCHEN,
                entity_type="spatial.place",
                components=(place_component(REGION, "kitchen", capacity=2),),
            ),
            EntityCreate(
                entity_id=GARDEN,
                entity_type="spatial.place",
                components=(place_component(REGION, "garden", capacity=8),),
            ),
            EntityCreate(
                entity_id=DOOR_HK,
                entity_type="spatial.portal",
                components=(portal_component(HALL, KITCHEN, state="open", label="hall-kitchen"),),
            ),
            EntityCreate(
                entity_id=DOOR_HG,
                entity_type="spatial.portal",
                components=(
                    portal_component(
                        HALL, GARDEN, state="locked", locked_key=KEY, label="hall-garden"
                    ),
                ),
            ),
            EntityCreate(
                entity_id=KEY,
                entity_type="spatial.key",
                components=(),
            ),
            EntityCreate(
                entity_id=ALICE,
                entity_type="person",
                components=(position_component(ALICE, HALL),),
            ),
            EntityCreate(
                entity_id=BOB,
                entity_type="person",
                components=(position_component(BOB, KITCHEN), access_key_component(KEY)),
            ),
            EntityCreate(
                entity_id=NO_KEY,
                entity_type="person",
                components=(position_component(NO_KEY, HALL),),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"house": house_delta}


def build_house_fixture_commands(
    branch_id: BranchId,
    start_revision: int = 0,
    command_id: str = "cmd_house",
    instance_id: WorldInstanceId | None = None,
) -> tuple[CommandEnvelope, ...]:
    """Return a single deterministic command that instantiates the house fixture."""
    from wanxiang_substrate.spatial.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance_id or INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "house", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
