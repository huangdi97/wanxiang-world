"""Ground a Player character that has no canonical entity in its world.

The entity is created through the existing runtime commit path using the
preview entity resolver: this is a canonical event, not a visual projection or
a direct state write. Used only when an API client enters with an explicit
character id that the source package did not declare.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.preview import PREVIEW_CREATE_ENTITY, instantiate_preview

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def ground_missing_actor(
    service: PlayableService,
    profile_id: str,
    character_id: str,
    *,
    viewer_id: str,
) -> bool:
    """Create the character's actor entity if it is not already canonical."""

    if not character_id:
        return False
    service.plaza.require_access(profile_id, viewer_id)
    package = service._packages.get(profile_id)
    install = service._installs.get(profile_id)
    experience = service._experiences.get(profile_id)
    if package is None or install is None or experience is None:
        return False
    if not experience.supports_entry("embodiment"):
        return False
    character = service.store.get_character(character_id)
    if character.owner_id != viewer_id:
        return False
    world = instantiate_preview(service.runtime, package, install)
    instance_id = WorldInstanceId(world.instance_id.value)
    branch_id = BranchId(world.branch_id.value)
    state = service.runtime.current_state(instance_id, branch_id)
    if state.entity(EntityId(character_id)) is not None:
        return False
    command = CommandEnvelope(
        command_id=CommandId.generate(),
        instance_id=instance_id,
        branch_id=branch_id,
        expected_revision=BranchRevision(state.revision.value),
        action_type=PREVIEW_CREATE_ENTITY,
        payload={
            "entity_id": character_id,
            "display_name": character.display_name,
            "entity_type": "actor",
        },
        world_time=WorldTime(state.revision.value + 1),
    )
    service.runtime.submit_command(command)
    return True
