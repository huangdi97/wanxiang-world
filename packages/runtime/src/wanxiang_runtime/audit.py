"""Structured audit/trace records for canonical commits.

Audit data is emitted separately from domain state; it is not part of the
canonical semantic hash.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import (
    ActorId,
    BranchId,
    CommandId,
    CorrelationId,
    EventId,
    TraceId,
    WorldInstanceId,
)
from wanxiang_domain.time import CommitTimestamp, WorldTime
from wanxiang_domain.versions import RuntimeVersion
from wanxiang_domain.world_commit import DELTA_SCHEMA_VERSION, WorldCommitKind


@dataclass(frozen=True, slots=True)
class AuditRecord:
    trace_id: TraceId
    command_id: CommandId
    event_id: EventId
    instance_id: WorldInstanceId
    branch_id: BranchId
    revision: BranchRevision
    rule_version: RuntimeVersion
    world_time: WorldTime
    actor_id: ActorId | None = None
    correlation_id: CorrelationId | None = None
    commit_timestamp: CommitTimestamp | None = None
    kind: WorldCommitKind = "state"
    delta_schema_version: int = DELTA_SCHEMA_VERSION
