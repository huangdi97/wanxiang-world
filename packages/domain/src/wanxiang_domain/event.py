"""CommittedEvent envelope (append-only, replayable)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
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
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class CommittedEvent:
    """An immutable, ordered record of a committed canonical mutation.

    `commit_timestamp` and `trace_id` are audit fields and are excluded from
    canonical semantic hashing.
    """

    event_id: EventId
    instance_id: WorldInstanceId
    branch_id: BranchId
    event_seq: EventSeq
    revision: BranchRevision
    schema_version: SchemaVersion
    command_id: CommandId
    delta: ProposedWorldDelta
    world_time: WorldTime
    rule_version: RuntimeVersion
    actor_id: ActorId | None = None
    causation_id: CommandId | None = None
    correlation_id: CorrelationId | None = None
    trace_id: TraceId | None = None
    commit_timestamp: CommitTimestamp | None = None
