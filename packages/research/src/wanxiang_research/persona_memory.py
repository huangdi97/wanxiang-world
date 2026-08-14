"""Long-horizon persona, memory metabolism & drift research (G19C, experimental).

Fact memory and persona-conditioned interpretation are distinct. Retrieval
never leaks private/unknown facts; compaction preserves provenance and key
events; a persona-drift metric reports consistency instead of hiding it.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Memory:
    memory_id: str
    actor_id: str
    fact: str
    provenance: str
    privacy: str = "public"
    key_event: bool = False


@dataclass
class MemoryStore:
    _memories: list[Memory] = field(default_factory=list[Memory])

    def add(self, memory: Memory) -> None:
        self._memories.append(memory)

    def retrieve(self, actor_id: str, query: str) -> tuple[Memory, ...]:
        """Retrieve memories for an actor; private/unknown facts never leak."""
        q = query.lower()
        return tuple(
            m
            for m in self._memories
            if m.actor_id == actor_id and q in m.fact.lower() and m.privacy != "private"
        )

    def compact(self) -> tuple[Memory, ...]:
        """Compaction preserves provenance and key events."""
        # Deduplicate non-key memories by (fact, provenance) preserving provenance.
        seen: set[tuple[str, str]] = set()
        compacted: list[Memory] = []
        for m in sorted(self._memories, key=lambda x: x.memory_id):
            key = (m.fact, m.provenance)
            if m.key_event or key not in seen:
                compacted.append(m)
                seen.add(key)
        return tuple(compacted)

    def all(self) -> tuple[Memory, ...]:
        return tuple(self._memories)


@dataclass(frozen=True, slots=True)
class PersonaDecision:
    actor_id: str
    scenario: str
    choice: str


class PersonaDrift:
    """Anonymous decision-consistency metric between two persona snapshots."""

    @staticmethod
    def drift(earlier: tuple[PersonaDecision, ...], later: tuple[PersonaDecision, ...]) -> float:
        earlier_map = {d.scenario: d.choice for d in earlier}
        later_map = {d.scenario: d.choice for d in later}
        shared = [s for s in earlier_map if s in later_map]
        if not shared:
            return 1.0
        changed = sum(1 for s in shared if earlier_map[s] != later_map[s])
        return changed / len(shared)
