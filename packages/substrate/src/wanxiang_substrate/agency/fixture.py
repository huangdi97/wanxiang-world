"""Synthetic organization fixture (explicitly synthetic).

A small club with a commander (issuer) and two members (receivers) with actor
state, used to test the order lifecycle and organization views.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.agency.components import actor_state_component
from wanxiang_substrate.institution.components import membership_component, role_component
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_org")
CLUB = EntityId("club")
ROLE_OFFICER = EntityId("role_officer")
COMMANDER = EntityId("commander")
SOLDIER_A = EntityId("soldier_a")
SOLDIER_B = EntityId("soldier_b")


def organization_delta() -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(
                entity_id=ROLE_OFFICER,
                entity_type="institution.role",
                components=(role_component(ROLE_OFFICER, "officer", ("issue_order",)),),
            ),
            EntityCreate(
                entity_id=EntityId("membership_commander"),
                entity_type="institution.membership",
                components=(
                    membership_component(
                        EntityId("membership_commander"), COMMANDER, ROLE_OFFICER, CLUB, 0, 100_000
                    ),
                ),
            ),
            EntityCreate(
                entity_id=COMMANDER,
                entity_type="person",
                components=(
                    actor_state_component(
                        COMMANDER, active=True, controller_policy="deterministic"
                    ),
                ),
            ),
            EntityCreate(
                entity_id=SOLDIER_A,
                entity_type="person",
                components=(
                    actor_state_component(
                        SOLDIER_A, active=True, controller_policy="deterministic"
                    ),
                ),
            ),
            EntityCreate(
                entity_id=SOLDIER_B,
                entity_type="person",
                components=(
                    actor_state_component(
                        SOLDIER_B, active=True, controller_policy="deterministic"
                    ),
                ),
            ),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"organization": organization_delta}


def build_organization_fixture_commands(
    branch_id: BranchId,
    start_revision: int = 0,
    command_id: str = "cmd_organization",
    instance_id: WorldInstanceId | None = None,
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the organization fixture."""
    from wanxiang_substrate.agency.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance_id or INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "organization", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
