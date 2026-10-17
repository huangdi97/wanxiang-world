"""Entry, resume, leave, and raw observation helpers for PlayableService.

These helpers read canonical state through the injected runtime and persist
only playable session bookkeeping. They never mutate canonical world state.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wanxiang_domain.errors import NotFound
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.state import state_to_primitive

from wanxiang_substrate.playable.experience import EntryMode
from wanxiang_substrate.playable.service_session import _owned_instance, _save_instance
from wanxiang_substrate.playable.service_support import instance_dict
from wanxiang_substrate.playable.store import ExperienceInstanceRecord
from wanxiang_substrate.preview import instantiate_preview

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _enter(
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
    mode: str,
    session_id: str,
    character_id: str = "",
) -> dict[str, object]:
    service.plaza.require_access(profile_id, viewer_id)
    package = service._packages.get(profile_id)
    experience = service._experiences.get(profile_id)
    install = service._installs.get(profile_id)
    if package is None or experience is None or install is None:
        raise NotFound(f"playable package {profile_id!r} not found")
    world = instantiate_preview(service.runtime, package, install)
    receipt = service.entry.enter(
        experience,
        viewer_id=viewer_id,
        instance_id=world.instance_id.value,
        branch_id=world.branch_id.value,
        session_id=session_id,
        mode=cast(EntryMode, mode),
        character_id=character_id,
    )
    _save_instance(service, receipt, viewer_id, world.branch_id.value, updated_seq=1)
    return _observe(service, receipt.instance_id, viewer_id)


def _continue_instance(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
) -> dict[str, object]:
    record = _owned_instance(service, instance_id, viewer_id)
    profile = service.plaza.require_access(record.profile_id, viewer_id)
    experience = service._experiences.get(profile.profile_id)
    if experience is None:
        raise NotFound(f"experience {profile.profile_id!r} not found")
    next_session = f"resume_{record.instance_id}_{record.updated_seq + 1}"
    receipt = service.entry.enter(
        experience,
        viewer_id=viewer_id,
        instance_id=record.instance_id,
        branch_id=record.branch_id,
        session_id=next_session,
        mode=cast(EntryMode, record.mode),
        character_id=record.actor_id,
    )
    _save_instance(
        service,
        receipt,
        viewer_id,
        record.branch_id,
        updated_seq=record.updated_seq + 1,
    )
    return _observe(service, instance_id, viewer_id)


def _leave(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
) -> dict[str, object]:
    record = _owned_instance(service, instance_id, viewer_id)
    if record.session_id:
        service.entry.leave(record.session_id)
    state = service.runtime.current_state(
        WorldInstanceId(record.instance_id), BranchId(record.branch_id)
    )
    service.store.save_instance(
        ExperienceInstanceRecord(
            record.instance_id,
            record.profile_id,
            record.owner_id,
            record.branch_id,
            mode=record.mode,
            actor_id=record.actor_id,
            last_revision=state.revision.value,
            updated_seq=record.updated_seq + 1,
        )
    )
    return {"instance_id": instance_id, "status": "left", "revision": state.revision.value}


def _observe(
    service: PlayableService,
    instance_id: str,
    viewer_id: str,
) -> dict[str, object]:
    record = _owned_instance(service, instance_id, viewer_id)
    state = service.runtime.current_state(
        WorldInstanceId(record.instance_id), BranchId(record.branch_id)
    )
    return {
        "instance": instance_dict(record),
        "state": state_to_primitive(state),
        "state_hash": state.semantic_hash(),
        "revision": state.revision.value,
    }
