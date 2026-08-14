"""World Semantic ISA - minimal typed semantic instructions (G30D).

The ISA is a thin reduction layer: eight instructions that business actions /
the compiler / domain use cases reduce to. It is NOT a parallel command bus and
NOT a giant interpreter: data instructions reduce to existing deltas
(ProposedWorldDelta), control instructions map to existing use cases (commit
boundary, fork, promotion pipeline).

Instructions:
  DECLARE   -> EntityCreate delta (declare a distinction)
  ASSERT    -> RelationCreate delta (assert a relation/fact)
  RETRACT   -> EntityDelete / RelationDelete delta
  PROPOSE   -> ProposedWorldDelta (a proposal envelope)
  VALIDATE  -> resolver/validator + kernel invariants
  COMMIT    -> CommitAuthority (single mutation boundary)
  FORK      -> fork_branch (branch/lineage semantics, one history model)
  PROMOTE   -> promotion pipeline (candidate promotion, later Goals)

Business actions (e.g. create_entity, transfer_resource) remain at the upper
layer; the ISA is the reduction target they compile to.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Literal, cast

from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    ProposedWorldDelta,
    RelationCreate,
    RelationDelete,
)
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId, RelationId

ISA_VERSION = 1
ISA_SUPPORTED_VERSIONS: tuple[int, ...] = (ISA_VERSION,)

WorldIsaInstruction = Literal[
    "DECLARE",
    "ASSERT",
    "RETRACT",
    "PROPOSE",
    "VALIDATE",
    "COMMIT",
    "FORK",
    "PROMOTE",
]

ISA_INSTRUCTIONS: tuple[WorldIsaInstruction, ...] = (
    "DECLARE",
    "ASSERT",
    "RETRACT",
    "PROPOSE",
    "VALIDATE",
    "COMMIT",
    "FORK",
    "PROMOTE",
)


@dataclass(frozen=True, slots=True)
class WorldIsaOp:
    """A discriminated semantic instruction (typed payload)."""

    op: WorldIsaInstruction
    version: int = ISA_VERSION
    payload: dict[str, object] = field(default_factory=dict[str, object])

    def __post_init__(self) -> None:
        if self.op not in ISA_INSTRUCTIONS:
            raise ContractError(f"unknown ISA instruction {self.op!r}")
        if self.version not in ISA_SUPPORTED_VERSIONS:
            raise ContractError(
                f"unsupported ISA version {self.version}; supported {ISA_SUPPORTED_VERSIONS}"
            )

    def to_primitive(self) -> dict[str, object]:
        return {"op": self.op, "version": self.version, "payload": dict(self.payload or {})}


def isa_op_from_primitive(data: dict[str, object]) -> WorldIsaOp:
    """Deserialize an ISA op; unknown versions/ops fail explicitly."""
    op = data.get("op")
    version = data.get("version")
    if not isinstance(op, str) or op not in ISA_INSTRUCTIONS:
        raise ContractError(f"invalid ISA op {op!r}")
    if not isinstance(version, int) or version not in ISA_SUPPORTED_VERSIONS:
        raise ContractError(f"unsupported ISA version {version!r}")
    raw_payload = data.get("payload")
    payload: dict[str, object] = {}
    if isinstance(raw_payload, dict):
        payload = dict(cast(Mapping[str, object], raw_payload))
    return WorldIsaOp(op=op, version=version, payload=payload)


def reduce_isa_to_delta(op: WorldIsaOp) -> ProposedWorldDelta | None:
    """Reduce data instructions to a delta (None for control instructions).

    Control instructions (VALIDATE/COMMIT/FORK/PROMOTE) map to existing use
    cases executed outside this module; they carry no delta payload here.
    """
    if op.op == "DECLARE":
        entity_id = EntityId(str(op.payload.get("entity_id")))
        entity_type = str(op.payload.get("entity_type", "thing"))
        return ProposedWorldDelta(
            operations=(EntityCreate(entity_id=entity_id, entity_type=entity_type),)
        )
    if op.op == "ASSERT":
        relation_id = RelationId(str(op.payload.get("relation_id")))
        relation_type = str(op.payload.get("relation_type", "relates_to"))
        source_id = EntityId(str(op.payload.get("source_id")))
        target_id = EntityId(str(op.payload.get("target_id")))
        return ProposedWorldDelta(
            operations=(
                RelationCreate(
                    relation_id=relation_id,
                    relation_type=relation_type,
                    source_id=source_id,
                    target_id=target_id,
                ),
            )
        )
    if op.op == "RETRACT":
        entity_id = op.payload.get("entity_id")
        if entity_id is not None:
            return ProposedWorldDelta(
                operations=(EntityDelete(entity_id=EntityId(str(entity_id))),)
            )
        relation_id = op.payload.get("relation_id")
        if relation_id is not None:
            return ProposedWorldDelta(
                operations=(RelationDelete(relation_id=RelationId(str(relation_id))),)
            )
        raise ContractError("RETRACT requires entity_id or relation_id")
    if op.op == "PROPOSE":
        raw_delta = op.payload.get("delta")
        if not isinstance(raw_delta, dict):
            raise ContractError("PROPOSE requires a delta payload")
        from wanxiang_domain.serialization import delta_from_primitive

        return delta_from_primitive(cast(dict[str, object], raw_delta))
    return None
