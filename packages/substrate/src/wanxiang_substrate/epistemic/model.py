"""Pure belief/memory value objects and epistemic invariants."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

MemoryKind = Literal["observation", "interpretation", "belief"]
BeliefStatus = Literal["active", "corrected", "superseded", "forgotten"]


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    """An actor-local memory record (never canonical truth)."""

    memory_id: EntityId
    actor_id: EntityId
    kind: MemoryKind
    content_ref: str
    at_ticks: int
    salience: float = 0.5
    source_obs_ref: str | None = None
    forgotten: bool = False

    def __post_init__(self) -> None:
        if not self.content_ref:
            raise ContractError("memory content_ref must be non-empty")
        if not (0.0 <= self.salience <= 1.0):
            raise ContractError("salience must be in [0, 1]")
        if self.kind not in ("observation", "interpretation", "belief"):
            raise ContractError(f"invalid memory kind {self.kind!r}")


@dataclass(frozen=True, slots=True)
class BeliefAssertion:
    """An actor belief with confidence, source and correction lineage."""

    belief_id: EntityId
    actor_id: EntityId
    proposition: str
    confidence: float
    at_ticks: int
    source_ref: str | None = None
    status: BeliefStatus = "active"
    supersedes: EntityId | None = None
    corrected_by: EntityId | None = None

    def __post_init__(self) -> None:
        if not self.proposition:
            raise ContractError("belief proposition must be non-empty")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("belief confidence must be in [0, 1]")
        if self.status not in ("active", "corrected", "superseded", "forgotten"):
            raise ContractError(f"invalid belief status {self.status!r}")
