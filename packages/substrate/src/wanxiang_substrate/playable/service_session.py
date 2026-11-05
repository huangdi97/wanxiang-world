"""Session persistence helpers for PlayableService."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from wanxiang_domain.errors import NotFound
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.entry import EntryReceipt
from wanxiang_substrate.playable.service_support import _runtime_instance_id
from wanxiang_substrate.playable.store import ExperienceInstanceRecord

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _next_touch(service: PlayableService) -> int:
    """Monotonic save order shared by every worldline of the store.

    ``updated_seq`` is a touch counter, not a per-branch event count, so
    ``continue_last`` can resume the worldline the player actually used last.
    """
    return max((item.updated_seq for item in service.store.list_instances()), default=0) + 1


def _save_instance(
    service: PlayableService,
    receipt: EntryReceipt,
    record: ExperienceInstanceRecord,
) -> ExperienceInstanceRecord:
    state = service.runtime.current_state(
        WorldInstanceId(_runtime_instance_id(record)),
        BranchId(record.branch_id),
    )
    updated = replace(
        record,
        mode=receipt.mode,
        actor_id=receipt.actor_id or record.actor_id,
        session_id=receipt.session_id,
        lease_id=receipt.lease_id,
        last_revision=state.revision.value,
        updated_seq=_next_touch(service),
    )
    service.store.save_instance(updated)
    return updated


def _owned_instance(
    service: PlayableService,
    instance_id: str,
    viewer_id: str,
) -> ExperienceInstanceRecord:
    record = service.store.get_instance_for(instance_id, viewer_id)
    if record is None:
        raise NotFound(f"playable instance {instance_id!r} not found")
    return record
