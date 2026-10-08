"""Pure belief/memory value objects and epistemic invariants."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

MemoryKind = Literal["observation", "interpretation", "belief", "reflection"]
BeliefStatus = Literal["active", "corrected", "superseded", "forgotten"]
BeliefStance = Literal["supported", "contested", "unknown"]


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
    source_perception_refs: tuple[str, ...] = ()
    decay_rate: float = 0.0
    reinforcement_count: int = 0
    last_reinforced_ticks: int | None = None

    def __post_init__(self) -> None:
        if not self.content_ref:
            raise ContractError("memory content_ref must be non-empty")
        if not (0.0 <= self.salience <= 1.0):
            raise ContractError("salience must be in [0, 1]")
        if self.kind not in ("observation", "interpretation", "belief", "reflection"):
            raise ContractError(f"invalid memory kind {self.kind!r}")
        if any(not ref.strip() for ref in self.source_perception_refs):
            raise ContractError("memory perception refs cannot be blank")
        if len(set(self.source_perception_refs)) != len(self.source_perception_refs):
            raise ContractError("memory perception refs must be unique")
        if not 0.0 <= self.decay_rate <= 1.0:
            raise ContractError("memory decay_rate must be in [0, 1]")
        if self.reinforcement_count < 0:
            raise ContractError("memory reinforcement_count cannot be negative")
        if self.last_reinforced_ticks is not None and self.last_reinforced_ticks < self.at_ticks:
            raise ContractError("memory reinforcement time cannot precede observation time")

    @property
    def perception_refs(self) -> tuple[str, ...]:
        """All source perception refs, including the v1 compatibility field."""
        refs = list(self.source_perception_refs)
        if self.source_obs_ref and self.source_obs_ref not in refs:
            refs.insert(0, self.source_obs_ref)
        return tuple(refs)

    def effective_salience(self, now_ticks: int) -> float:
        """Read-only decay hook; it never changes the stored memory."""
        if now_ticks < self.at_ticks:
            raise ContractError("memory query time cannot precede observation time")
        elapsed = now_ticks - self.at_ticks
        return round(self.salience * ((1.0 - self.decay_rate) ** elapsed), 6)

    def decayed(self, now_ticks: int) -> MemoryRecord:
        """Return a projection with decay applied, retaining the source record."""
        return replace(self, salience=self.effective_salience(now_ticks))

    def reinforce(
        self, at_ticks: int, *, amount: float = 0.1, perception_ref: str | None = None
    ) -> MemoryRecord:
        """Return a new record with explicit reinforcement lineage."""
        if at_ticks < self.at_ticks:
            raise ContractError("reinforcement time cannot precede observation time")
        if not 0.0 < amount <= 1.0:
            raise ContractError("reinforcement amount must be in (0, 1]")
        refs = self.source_perception_refs
        if perception_ref:
            refs = refs if perception_ref in refs else refs + (perception_ref,)
        return replace(
            self,
            salience=min(1.0, self.salience + amount),
            source_perception_refs=refs,
            reinforcement_count=self.reinforcement_count + 1,
            last_reinforced_ticks=at_ticks,
        )


# Product vocabulary for callers that distinguish episodic memory from the
# observation event that originally produced it.
EpistemicMemory = MemoryRecord


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
    stance: BeliefStance = "unknown"

    def __post_init__(self) -> None:
        if not self.proposition:
            raise ContractError("belief proposition must be non-empty")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("belief confidence must be in [0, 1]")
        if self.status not in ("active", "corrected", "superseded", "forgotten"):
            raise ContractError(f"invalid belief status {self.status!r}")
        if self.stance not in ("supported", "contested", "unknown"):
            raise ContractError(f"invalid belief stance {self.stance!r}")

    @property
    def is_world_truth(self) -> bool:
        """Belief assertions are always actor projections, never world truth."""
        return False
