"""Session persistence helpers for PlayableService."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_domain.errors import NotFound
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.entry import EntryReceipt
from wanxiang_substrate.playable.store import ExperienceInstanceRecord

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _save_instance(
    service: PlayableService,
    receipt: EntryReceipt,
    owner_id: str,
    branch_id: str,
    *,
    updated_seq: int,
) -> None:
    state = service.runtime.current_state(
        WorldInstanceId(receipt.instance_id), BranchId(branch_id)
    )
    service.store._save_instance(
        ExperienceInstanceRecord(
            receipt.instance_id,
            receipt.profile_id,
            owner_id,
            branch_id,
            mode=receipt.mode,
            actor_id=receipt.actor_id,
            session_id=receipt.session_id,
            lease_id=receipt.lease_id,
            last_revision=state.revision.value,
            updated_seq=updated_seq,
        )
    )


def _owned_instance(
    service: PlayableService,
    instance_id: str,
    viewer_id: str,
) -> ExperienceInstanceRecord:
    record = service.store.get_instance(instance_id)
    if record.owner_id != viewer_id:
        raise NotFound(f"playable instance {instance_id!r} not found")
    return record
