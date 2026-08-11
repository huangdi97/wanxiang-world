"""Command/ActionIntent envelope.

A Command is a proposal: it never mutates canonical state by itself. It carries
idempotency/causation/correlation metadata required by the commit contract.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, CorrelationId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import SchemaVersion


@dataclass(frozen=True, slots=True)
class CommandEnvelope:
    command_id: CommandId
    instance_id: WorldInstanceId
    branch_id: BranchId
    expected_revision: BranchRevision
    action_type: str
    payload: Mapping[str, FieldValue] = field(default_factory=dict[str, FieldValue])
    actor_id: ActorId | None = None
    causation_id: CommandId | None = None
    correlation_id: CorrelationId | None = None
    world_time: WorldTime | None = None
    schema_version: SchemaVersion = SchemaVersion(1)

    def __post_init__(self) -> None:
        if not self.action_type:
            raise ContractError("action_type must be a non-empty string")
