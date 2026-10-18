"""Worldline forks: expose a real Kernel branch as a separate Player handle.

A fork is structural canonical history (a child branch at the parent head). It
creates no event, never mutates the parent branch, and the forked Player record
stays a detached session until the player continues it.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.service_session import _next_touch, _owned_instance
from wanxiang_substrate.playable.service_support import _runtime_instance_id
from wanxiang_substrate.playable.store import ExperienceInstanceRecord

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _fork_worldline(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
) -> dict[str, object]:
    """Fork the owned branch at its current head and register a detached handle."""

    record = _owned_instance(service, instance_id, viewer_id)
    service.plaza.require_access(record.profile_id, viewer_id)
    if record.mode != "embodiment" or not record.actor_id:
        raise ContractError("only an embodied character can fork a worldline")
    runtime_id = _runtime_instance_id(record)
    parent_branch = BranchId(record.branch_id)
    head = service.runtime.current_state(WorldInstanceId(runtime_id), parent_branch)
    child = service.runtime.create_branch(
        WorldInstanceId(runtime_id),
        parent_branch,
        fork_revision=head.revision,
    )
    branch_id = getattr(child, "branch_id", None)
    if not isinstance(branch_id, BranchId):
        raise ValueError("runtime returned an invalid branch handle")
    handle = branch_id.value
    service.store.save_instance(
        ExperienceInstanceRecord(
            instance_id=handle,
            profile_id=record.profile_id,
            owner_id=record.owner_id,
            branch_id=handle,
            mode=record.mode,
            actor_id=record.actor_id,
            last_revision=head.revision.value,
            updated_seq=_next_touch(service),
            runtime_instance_id=runtime_id,
        )
    )
    return {
        "instance_id": handle,
        "branch_id": handle,
        "revision": head.revision.value,
        "parent_instance_id": instance_id,
    }
