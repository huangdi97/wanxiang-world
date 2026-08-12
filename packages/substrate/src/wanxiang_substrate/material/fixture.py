"""Synthetic letter/package scenario (explicitly synthetic).

Writer owns and seals a letter; a messenger holds it (custody) without reading;
the recipient reads it after receiving. Proves custody and information
separation. The payload lives on its own entity (`payload_<item>`), so custody
of the letter never equals knowledge of its content.
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
    ownership_component,
)

INSTANCE = WorldInstanceId("wld_package")
LETTER = EntityId("letter_1")
WRITER = EntityId("writer")
MESSENGER = EntityId("messenger")
RECIPIENT = EntityId("recipient")


def package_delta() -> ProposedWorldDelta:
    """Writer owns/seals the letter; messenger initially holds it (unread)."""
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=LETTER,
                entity_type="material.item",
                components=(
                    item_component(LETTER, "letter"),
                    custody_component(LETTER, MESSENGER),
                    ownership_component(LETTER, WRITER),
                ),
            ),
            EntityCreate(
                entity_id=EntityId(f"payload_{LETTER.value}"),
                entity_type="material.info_payload",
                components=(info_payload_component(LETTER, "ref://letter_1/body", state="sealed"),),
            ),
            EntityCreate(entity_id=WRITER, entity_type="person", components=()),
            EntityCreate(entity_id=MESSENGER, entity_type="person", components=()),
            EntityCreate(entity_id=RECIPIENT, entity_type="person", components=()),
        )
    )


FIXTURE_DELTAS: dict[str, Callable[[], ProposedWorldDelta]] = {"package": package_delta}


def build_package_fixture_commands(
    branch_id: BranchId, start_revision: int = 0, command_id: str = "cmd_package"
) -> tuple[CommandEnvelope, ...]:
    """One deterministic command that instantiates the package fixture."""
    from wanxiang_substrate.material.resolver import ACTION_INSTANTIATE

    return (
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=INSTANCE,
            branch_id=branch_id,
            expected_revision=BranchRevision(start_revision),
            action_type=ACTION_INSTANTIATE,
            payload={"fixture": "package", "version": 1},
            world_time=WorldTime(start_revision + 1),
        ),
    )
