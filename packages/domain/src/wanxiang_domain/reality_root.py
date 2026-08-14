"""Reality Root semantic contract (G30A).

The Reality Root is the semantic bedrock of every world. It is expressed ONLY
with the existing core types ? no second state kernel, event store, or commit
authority is created here. This module provides:

- `REALITY_ROOT_SEMANTICS` ? documentation table mapping the five primitives
  (Distinction, Relation, Transition, Commitment, History) onto existing
  contracts;
- `RealityRootContract` ? documentation-level Protocol spelling out the
  vocabulary any world runtime realizes through the existing machinery
  (CommitAuthority, ReplayEngine, StateReader / WorldRuntimePort).

Explicitly, the Reality Root contains NO physical / magical / domain rules:
spatial, temporal, body, institution, item, and world-specific semantics live in
Runtime / Forge / World content, never here.

Invariants (tested in tests/unit/domain/test_reality_root.py):
1. Distinction  -> EntityId + EntityState (identity).
2. Relation     -> RelationId + RelationState (typed link between distinctions).
3. Transition   -> ProposedWorldDelta realized as a CommittedEvent.
4. Commitment   -> CommitRequest through the single CommitAuthority boundary.
5. History      -> append-only committed stream, deterministically replayable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.entity import EntityState, RelationState
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, EntityId, RelationId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class SemanticMapping:
    """Documentation record: one Reality Root primitive -> existing contracts."""

    name: str
    meaning: str
    mapped_to: tuple[str, ...]
    no_domain_rules: bool = True


REALITY_ROOT_SEMANTICS: tuple[SemanticMapping, ...] = (
    SemanticMapping(
        "Distinction",
        "naming and separating one thing from the world (identity)",
        ("EntityId", "EntityState"),
    ),
    SemanticMapping(
        "Relation",
        "a typed link between two distinctions",
        ("RelationId", "RelationState"),
    ),
    SemanticMapping(
        "Transition",
        "an atomic change proposal realized as a committed event",
        ("ProposedWorldDelta", "CommittedEvent"),
    ),
    SemanticMapping(
        "Commitment",
        "the single mutation boundary every change must pass",
        ("CommitRequest", "CommitAuthority"),
    ),
    SemanticMapping(
        "History",
        "append-only committed stream, rebuildable by replay",
        ("CommittedEvent", "ReplayEngine"),
    ),
)


class RealityRootContract(Protocol):
    """Documentation-level contract: the five primitives on existing types.

    A concrete world runtime realizes this vocabulary through the existing core
    machinery (CommitAuthority / ReplayEngine / StateReader / WorldRuntimePort).
    No Reality Root implementation stores state or domain rules of its own.
    """

    def distinguish(
        self, entity_id: EntityId, entity_type: str, schema_version: SchemaVersion
    ) -> EntityState: ...

    def relate(
        self,
        relation_id: RelationId,
        relation_type: str,
        source_id: EntityId,
        target_id: EntityId,
    ) -> RelationState: ...

    def transition(
        self,
        delta: ProposedWorldDelta,
        *,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
    ) -> CommittedEvent: ...

    def commit(
        self,
        delta: ProposedWorldDelta,
        *,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        expected_revision: BranchRevision,
        world_time: WorldTime,
        rule_version: RuntimeVersion,
        schema_version: SchemaVersion,
    ) -> CommittedEvent: ...

    def history(
        self, instance_id: WorldInstanceId, branch_id: BranchId
    ) -> tuple[CommittedEvent, ...]: ...
