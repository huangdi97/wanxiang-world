"""Runtime protocols used by living-world evaluation."""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchId, BranchRevision
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.preview.runtime import PreviewRuntimePort


class LivingRuntimePort(PreviewRuntimePort, Protocol):
    """Runtime operations needed to produce living-world evidence."""

    def create_checkpoint(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> SnapshotMetadata: ...

    def create_branch(
        self,
        instance_id: WorldInstanceId,
        parent_branch_id: BranchId,
        *,
        fork_revision: BranchRevision | None = None,
    ) -> object: ...

    def events(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> tuple[CommittedEvent, ...]: ...


class ReplayState(Protocol):
    state: InMemoryCanonicalState


class BranchResult(Protocol):
    branch_id: BranchId


__all__ = ["BranchResult", "LivingRuntimePort", "ReplayState"]
