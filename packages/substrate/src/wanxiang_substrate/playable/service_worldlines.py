"""Player worldline list: branches of one runtime instance with product handles.

Only records owned by the viewer are listed. The canonical branch metadata is
read-only; the view exposes no event ids, hashes, or storage refs.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.service_session import _owned_instance
from wanxiang_substrate.playable.service_support import _runtime_instance_id
from wanxiang_substrate.playable.store import ExperienceInstanceRecord

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _belongs(record: ExperienceInstanceRecord, runtime_id: str) -> bool:
    return (record.runtime_instance_id or record.instance_id) == runtime_id


def _branch_metadata(
    service: PlayableService,
    runtime_id: str,
) -> tuple[int, dict[str, int]]:
    count = 0
    revisions: dict[str, int] = {}
    for branch in service.runtime.worldline_branches(WorldInstanceId(runtime_id)):
        branch_id = getattr(branch, "branch_id", None)
        if not isinstance(branch_id, BranchId):
            continue
        count += 1
        ancestry = getattr(branch, "ancestry", None)
        fork_revision = getattr(ancestry, "fork_revision", None)
        if isinstance(fork_revision, BranchRevision):
            revisions[branch_id.value] = fork_revision.value
    return count, revisions


def _worldlines(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
) -> dict[str, object]:
    """List the viewer's worldline handles for the instance's runtime branch set."""

    record = _owned_instance(service, instance_id, viewer_id)
    service.plaza.require_access(record.profile_id, viewer_id)
    runtime_id = _runtime_instance_id(record)
    branch_count, fork_revisions = _branch_metadata(service, runtime_id)
    records = [item for item in service.store.list_instances() if _belongs(item, runtime_id)]
    records.sort(
        key=lambda item: (
            fork_revisions.get(item.branch_id) is not None,
            fork_revisions.get(item.branch_id) or 0,
            item.instance_id,
        )
    )
    world_instance = WorldInstanceId(runtime_id)
    cards: list[dict[str, object]] = []
    for item in records:
        branch = BranchId(item.branch_id)
        events = tuple(service.runtime.worldline_events(world_instance, branch))
        state = service.runtime.current_state(world_instance, branch)
        cards.append(
            {
                "instance_id": item.instance_id,
                "branch_id": item.branch_id,
                "current": item.instance_id == instance_id,
                "active_session": bool(item.session_id),
                "mode": item.mode,
                "revision": state.revision.value,
                "world_time": events[-1].world_time.ticks if events else 0,
                "forked_from_revision": fork_revisions.get(item.branch_id),
            }
        )
    return {
        "instance_id": instance_id,
        "branches": branch_count,
        "worldlines": cards,
    }
