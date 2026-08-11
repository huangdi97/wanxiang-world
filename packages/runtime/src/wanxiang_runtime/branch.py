"""Branch model, fork and repository (in-memory)."""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.errors import NotFound, ValidationRejected
from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata, BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_runtime.state import InMemoryCanonicalState


class BranchRepository(Protocol):
    def save(self, metadata: BranchMetadata) -> None: ...

    def get(self, branch_id: BranchId) -> BranchMetadata: ...

    def list(self, instance_id: WorldInstanceId) -> tuple[BranchMetadata, ...]: ...


class InMemoryBranchRepository:
    """Stores branch metadata keyed by branch id (instance-aware)."""

    def __init__(self) -> None:
        self._branches: dict[BranchId, BranchMetadata] = {}

    def save(self, metadata: BranchMetadata) -> None:
        self._branches[metadata.branch_id] = metadata

    def get(self, branch_id: BranchId) -> BranchMetadata:
        branch = self._branches.get(branch_id)
        if branch is None:
            raise NotFound(f"branch {branch_id.value} not found")
        return branch

    def list(self, instance_id: WorldInstanceId) -> tuple[BranchMetadata, ...]:
        return tuple(
            branch
            for branch in sorted(self._branches.values(), key=lambda b: b.branch_id.value)
            if branch.instance_id == instance_id
        )


def fork_branch(
    parent: BranchMetadata,
    state: InMemoryCanonicalState,
    *,
    fork_revision: BranchRevision,
    fork_event_seq: EventSeq,
    snapshot_ref: str,
    branch_id: BranchId | None = None,
) -> BranchMetadata:
    """Create a child branch metadata with explicit ancestry.

    The child starts at `fork_revision`; its writes never mutate the parent
    event stream (enforced by the event store's per-branch keys).
    """
    if fork_revision.value > state.revision.value:
        raise ValidationRejected(
            f"cannot fork at revision {fork_revision.value} beyond head {state.revision.value}"
        )
    return BranchMetadata(
        branch_id=branch_id or BranchId.generate(),
        instance_id=parent.instance_id,
        ancestry=BranchAncestry(
            parent_branch_id=parent.branch_id,
            fork_revision=fork_revision,
            fork_event_seq=fork_event_seq,
            fork_snapshot_ref=snapshot_ref,
        ),
        schema_version=parent.schema_version,
        rule_version=parent.rule_version,
        snapshot_ref=snapshot_ref,
    )
