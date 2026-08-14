"""Actor Capability / Persona evolution separation (G32C).

A learned skill must never silently rewrite a persona. Capability deltas (reuse
CapabilityDelta) change the actor's capability state; only an explicit
PersonaDelta changes the persona. The tracker records a provenance chain
(trajectory) so long-term persona change is always traceable to events.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.capability.model import (
    CAPABILITY_MAX_LEVEL,
    CONFIDENCE_MAX,
    MASTERY_MAX,
    CapabilityDelta,
    CapabilityState,
)

TrajectoryKind = Literal["capability", "persona"]


@dataclass(frozen=True, slots=True)
class PersonaDelta:
    """An explicit, reasoned persona change (never implied by skill gain)."""

    actor_id: EntityId
    trait: str
    to_value: str
    rationale: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.trait or not self.rationale:
            raise ContractError("persona delta requires a trait and rationale")


@dataclass(frozen=True, slots=True)
class TrajectoryEntry:
    """One provenance record in the actor's evolution trajectory."""

    seq: int
    kind: TrajectoryKind
    detail: str
    provenance_ref: str


@dataclass(frozen=True, slots=True)
class ActorEvolutionState:
    """Separated capability + persona state with trajectory provenance."""

    actor_id: EntityId
    capabilities: tuple[CapabilityState, ...] = ()
    persona: tuple[tuple[str, str], ...] = ()
    trajectory: tuple[TrajectoryEntry, ...] = ()

    def capability_hash(self) -> str:
        payload = {
            c.capability: {
                "level": c.level,
                "mastery": c.mastery,
                "confidence": c.confidence,
            }
            for c in self.capabilities
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def persona_hash(self) -> str:
        payload = dict(self.persona)
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def trait(self, name: str) -> str | None:
        for trait, value in self.persona:
            if trait == name:
                return value
        return None


class ActorEvolutionTracker:
    """Keeps capability and persona strictly separated, with provenance."""

    def __init__(self, actor_id: EntityId, seed: int = 0) -> None:
        self._actor_id = actor_id
        self._seed = seed
        self._state = ActorEvolutionState(actor_id=actor_id)

    @property
    def state(self) -> ActorEvolutionState:
        return self._state

    def apply_capability(
        self, delta: CapabilityDelta, provenance_ref: str = "cap://learn"
    ) -> ActorEvolutionState:
        if delta.actor_id != self._actor_id:
            raise ContractError("capability delta targets a different actor")
        caps = {c.capability: c for c in self._state.capabilities}
        current = caps.get(delta.capability)
        base_level = current.level if current is not None else 0
        base_mastery = current.mastery if current is not None else 0.0
        base_confidence = current.confidence if current is not None else 0.0
        base_evidence = current.evidence_refs if current is not None else ()
        updated = CapabilityState(
            actor_id=delta.actor_id,
            capability=delta.capability,
            level=min(CAPABILITY_MAX_LEVEL, max(0, base_level + delta.level_delta)),
            mastery=min(MASTERY_MAX, max(0.0, base_mastery + delta.mastery_delta)),
            confidence=min(CONFIDENCE_MAX, max(0.0, base_confidence + delta.confidence_delta)),
            evidence_refs=base_evidence + delta.evidence_refs,
        )
        caps[delta.capability] = updated
        entry = TrajectoryEntry(
            seq=len(self._state.trajectory) + 1,
            kind="capability",
            detail=delta.capability,
            provenance_ref=provenance_ref,
        )
        self._state = ActorEvolutionState(
            actor_id=self._actor_id,
            capabilities=tuple(sorted(caps.values(), key=lambda c: c.capability)),
            persona=self._state.persona,
            trajectory=self._state.trajectory + (entry,),
        )
        return self._state

    def apply_persona(
        self, delta: PersonaDelta, provenance_ref: str = "persona://explicit"
    ) -> ActorEvolutionState:
        if delta.actor_id != self._actor_id:
            raise ContractError("persona delta targets a different actor")
        traits = dict(self._state.persona)
        traits[delta.trait] = delta.to_value
        entry = TrajectoryEntry(
            seq=len(self._state.trajectory) + 1,
            kind="persona",
            detail=f"{delta.trait}={delta.to_value}",
            provenance_ref=provenance_ref,
        )
        self._state = ActorEvolutionState(
            actor_id=self._actor_id,
            capabilities=self._state.capabilities,
            persona=tuple(sorted(traits.items())),
            trajectory=self._state.trajectory + (entry,),
        )
        return self._state
