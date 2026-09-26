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
from wanxiang_runtime.isa_pipeline import IsaExecutionResult, PromotionUseCase, execute_isa
from wanxiang_runtime.ports import EventAppendPort, EventStore, InMemoryEventStore
from wanxiang_runtime.r7_agent_harness import JsonRpcAgentHarnessProvider
from wanxiang_runtime.r7_agent_harness_contract import (
    HARNESS_PROTOCOL,
    AgentDecision,
    AgentHarnessProvider,
    AgentProposal,
    HarnessConsequence,
    HarnessError,
    HarnessInfo,
    HarnessProtocolError,
    HarnessUnavailable,
    WorldObservation,
    parse_decision,
)
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
    "HARNESS_PROTOCOL",
    "AuditRecord",
    "AgentDecision",
    "AgentHarnessProvider",
    "AgentProposal",
    "CommitAuthority",
    "CommitRequest",
    "CommitResult",
    "EventAppendPort",
    "EventStore",
    "HarnessConsequence",
    "HarnessError",
    "HarnessInfo",
    "HarnessProtocolError",
    "HarnessUnavailable",
    "INVARIANTS",
    "InMemoryBranchRepository",
    "InMemoryCanonicalState",
    "InMemoryEventStore",
    "InMemorySnapshotStore",
    "IsaExecutionResult",
    "JsonRpcAgentHarnessProvider",
    "PromotionUseCase",
    "ReplayEngine",
    "ResolverRegistry",
    "SnapshotStore",
    "StateDiff",
    "StoredSnapshot",
    "WorldObservation",
    "apply_delta",
    "check_delta_invariants",
    "create_snapshot_metadata",
    "diff_states",
    "execute_isa",
    "fork_branch",
    "parse_decision",
]
