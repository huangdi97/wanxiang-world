"""Wanxiang runtime: validate/resolve/commit/replay coordination."""

from wanxiang_runtime.audit import AuditRecord
from wanxiang_runtime.authority import (
    CommitAuthority,
    CommitRequest,
    CommitResult,
)
from wanxiang_runtime.branch import InMemoryBranchRepository, fork_branch
from wanxiang_runtime.diff import StateDiff, diff_states
from wanxiang_runtime.invariants import (
    INVARIANTS,
    check_delta_invariants,
)
from wanxiang_runtime.ports import EventAppendPort, EventStore, InMemoryEventStore
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.snapshot import (
    InMemorySnapshotStore,
    SnapshotStore,
    StoredSnapshot,
    create_snapshot_metadata,
)
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta

__version__ = "0.1.0"

__all__ = [
    "AuditRecord",
    "CommitAuthority",
    "CommitRequest",
    "CommitResult",
    "EventAppendPort",
    "EventStore",
    "INVARIANTS",
    "InMemoryBranchRepository",
    "InMemoryCanonicalState",
    "InMemoryEventStore",
    "InMemorySnapshotStore",
    "ReplayEngine",
    "ResolverRegistry",
    "SnapshotStore",
    "StateDiff",
    "StoredSnapshot",
    "apply_delta",
    "create_snapshot_metadata",
    "diff_states",
    "fork_branch",
    "check_delta_invariants",
]
