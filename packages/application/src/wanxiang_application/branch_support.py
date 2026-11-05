"""Branch-fork structure and worldline event projections.

Both helpers are read/structural: they never submit commands. ``fork_branch_at``
keeps the exact fork semantics previously embedded in ``WorldRuntime``.
"""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.errors import ContractError, ValidationRejected
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchMetadata, BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.branch import fork_branch
from wanxiang_runtime.canonical_write import CanonicalWriteLease
from wanxiang_runtime.snapshot import create_snapshot_metadata

from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.state_reader import StateReader

LeaseFactory = Callable[[BranchId, str], CanonicalWriteLease]


def fork_branch_at(
    persistence: PersistenceBundle,
    state_reader: StateReader,
    instance_id: WorldInstanceId,
    parent_branch_id: BranchId,
    *,
    fork_revision: BranchRevision | None,
    lease_for: LeaseFactory,
) -> BranchMetadata:
    """Fork ``parent_branch_id`` at a revision, persisting the fork baseline."""
    parent = persistence.branches.get(parent_branch_id)
    parent_state = state_reader.state_at(instance_id, parent_branch_id)
    revision = fork_revision or parent_state.revision
    if revision.value > parent_state.revision.value:
        raise ValidationRejected("cannot fork beyond the parent head")
    fork_events = [
        event
        for event in persistence.event_store.load(instance_id, parent_branch_id)
        if event.revision.value <= revision.value
    ]
    fork_event_seq = EventSeq(len(fork_events))
    snapshot_ref = f"mem://{parent_branch_id.value}/fork/{revision.value}"
    child = fork_branch(
        parent,
        parent_state,
        fork_revision=revision,
        fork_event_seq=fork_event_seq,
        snapshot_ref=snapshot_ref,
    )
    persistence.branches.save(child, lease=lease_for(child.branch_id, "create_branch"))
    # Persist a snapshot of the fork baseline so restore/replay is deterministic.
    fork_state = state_reader.state_at(instance_id, parent_branch_id, upto_seq=fork_event_seq)
    # The fork-baseline snapshot is keyed by the parent branch at the fork
    # revision (fork_state keeps the parent branch id), so it needs its own lease.
    persistence.snapshot_store.save(
        create_snapshot_metadata(fork_state, fork_event_seq, content_ref=snapshot_ref),
        fork_state,
        lease=lease_for(fork_state.branch_id, "create_branch_snapshot"),
    )
    return child


def worldline_events(
    persistence: PersistenceBundle,
    instance_id: WorldInstanceId,
    branch_id: BranchId,
) -> tuple[CommittedEvent, ...]:
    """Return inherited events plus the branch's own events, oldest first.

    Branch-local seq restarts at 1, so ancestry is cut by *revision*: every
    ancestor event at or below the fork revision belongs to the worldline.
    """
    branch = persistence.branches.get(branch_id)
    own = persistence.event_store.load(instance_id, branch_id)
    ancestry = branch.ancestry
    if ancestry.parent_branch_id is None or ancestry.fork_revision is None:
        return tuple(own)
    inherited = tuple(
        event
        for event in worldline_events(persistence, instance_id, ancestry.parent_branch_id)
        if event.revision.value <= ancestry.fork_revision.value
    )
    return inherited + tuple(own)


def _branch_chain(persistence: PersistenceBundle, branch_id: BranchId) -> list[BranchMetadata]:
    chain: list[BranchMetadata] = []
    meta = persistence.branches.get(branch_id)
    chain.append(meta)
    while meta.ancestry.parent_branch_id is not None:
        meta = persistence.branches.get(meta.ancestry.parent_branch_id)
        chain.append(meta)
    chain.reverse()
    return chain


def worldline_compare_point(
    persistence: PersistenceBundle,
    state_reader: StateReader,
    instance_id: WorldInstanceId,
    left_branch_id: BranchId,
    right_branch_id: BranchId,
) -> tuple[BranchId, int]:
    """Return the deepest shared (branch, revision) of two worldlines.

    Two sibling forks share history only up to the earlier fork revision; a
    branch compared with its own descendant shares the descendant's fork point
    (or the branch head when they are identical).
    """
    left_chain = _branch_chain(persistence, left_branch_id)
    right_chain = _branch_chain(persistence, right_branch_id)
    depth = 0
    for left, right in zip(left_chain, right_chain, strict=False):
        if left.branch_id != right.branch_id:
            break
        depth += 1
    if depth == 0:
        raise ContractError("worldlines do not share a branch ancestry")
    common = left_chain[depth - 1]
    if left_branch_id == right_branch_id:
        head = state_reader.state_at(instance_id, common.branch_id)
        return (common.branch_id, head.revision.value)

    def boundary(chain: list[BranchMetadata]) -> int:
        if len(chain) > depth:
            fork_revision = chain[depth].ancestry.fork_revision
            if fork_revision is not None:
                return fork_revision.value
        return state_reader.state_at(instance_id, common.branch_id).revision.value

    return (common.branch_id, min(boundary(left_chain), boundary(right_chain)))
