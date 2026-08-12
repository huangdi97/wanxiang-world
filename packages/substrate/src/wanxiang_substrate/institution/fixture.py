"""Synthetic household/club fixture (explicitly synthetic).

A club with a restricted room: only members with the `enter.<room>` permission
may enter. A steward holds a delegated duty; roles are time-scoped.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.institution.components import (
    duty_component,
    membership_component,
    permission_component,
    role_component,
)
from wanxiang_substrate.spatial.components import place_component, portal_component
from wanxiang_substrate.spatial.fixture import HALL, REGION
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_club")
CLUB = EntityId("club")
ROLE_MEMBER = EntityId("role_member")
ROOM = EntityId("study")
ALICE = EntityId("alice")
BOB = EntityId("bob")
MEM_ALICE = EntityId("membership_alice")
PERM_ALICE = EntityId("permission_alice")
DUTY_STEWARD = EntityId("duty_steward")


def institution_delta() -> ProposedWorldDelta:
    """Club with a role, time-scoped membership, restricted room, duty."""
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(entity_id=CLUB, entity_type="institution.club", components=()),
            EntityCreate(
                entity_id=ROLE_MEMBER,
                entity_type="institution.role",
                components=(role_component(ROLE_MEMBER, "member", ("enter.study", "read")),),
            ),
            EntityCreate(
                entity_id=MEM_ALICE,
                entity_type="institution.membership",
                components=(
                    membership_component(
                        MEM_ALICE, ALICE, ROLE_MEMBER, CLUB, start_ticks=0, end_ticks=1000
                    ),
                ),
            ),
            EntityCreate(
                entity_id=PERM_ALICE,
                entity_type="institution.permission",
                components=(
                    permission_component(
                        PERM_ALICE,
                        ALICE,
                        "enter.study",
                        "study",
                        CLUB,
                        start_ticks=0,
                        end_ticks=1000,
                    ),
                ),
            ),
            EntityCreate(
                entity_id=DUTY_STEWARD,
                entity_type="institution.duty",
                components=(duty_component(DUTY_STEWARD, ALICE, "steward_rounds", due_ticks=500),),
            ),
            EntityCreate(
                entity_id=ROOM,
                entity_type="spatial.place",
                components=(place_component(REGION, "study", capacity=4, privacy="restricted"),),
            ),
            EntityCreate(
                entity_id=EntityId("door_hall_study"),
                entity_type="spatial.portal",
                components=(portal_component(HALL, ROOM, state="open", label="hall-study"),),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"club": institution_delta}


def build_institution_fixture_commands(
    branch_id: BranchId,
    start_revision: int = 0,
    command_id: str = "cmd_club",
    instance_id: WorldInstanceId | None = None,
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the club fixture."""
    from wanxiang_substrate.institution.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance_id or INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "club", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
