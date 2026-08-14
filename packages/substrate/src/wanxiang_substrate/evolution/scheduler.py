"""Multi-scale evolution scheduler (G32B).

Reuses the scheduler idea: different scales (actor / relation / group /
institution / world) evaluate on different cadences. No full scan every tick ?
only the entities/windows whose cadence is due are activated, using modular
arithmetic, so long runs grow linearly (never exponentially).
"""

from __future__ import annotations

from dataclasses import dataclass

EVOLUTION_SCALES: tuple[str, ...] = (
    "actor",
    "relation",
    "group",
    "institution",
    "world",
)


@dataclass(frozen=True, slots=True)
class EvolutionCadence:
    """Evaluation cadence per scale (ticks between evaluations)."""

    actor: int = 1
    relation: int = 5
    group: int = 10
    institution: int = 30
    world: int = 100

    def __post_init__(self) -> None:
        for name, value in (
            ("actor", self.actor),
            ("relation", self.relation),
            ("group", self.group),
            ("institution", self.institution),
            ("world", self.world),
        ):
            if value < 1:
                raise ValueError(f"cadence {name} must be >= 1")

    def cadence_for(self, scale: str) -> int:
        return getattr(self, scale)


class EvolutionScheduler:
    """Deterministic multi-scale activation scheduler (no full scans)."""

    def __init__(self, cadence: EvolutionCadence | None = None, seed: int = 0) -> None:
        self._cadence = cadence or EvolutionCadence()
        self._seed = seed

    @property
    def cadence(self) -> EvolutionCadence:
        return self._cadence

    def due_scales(self, tick: int) -> tuple[str, ...]:
        """Scales due at a tick (modular activation, no full scan)."""
        if tick <= 0:
            return ()
        # seed only offsets the world-scale phase; actor/relation/etc. stay fixed.
        offset = self._seed % self._cadence.world
        due: list[str] = []
        for scale in EVOLUTION_SCALES:
            cadence = self._cadence.cadence_for(scale)
            if scale == "world":
                if (tick + offset) % cadence == 0:
                    due.append(scale)
            elif tick % cadence == 0:
                due.append(scale)
        return tuple(due)

    def activations_at(self, tick: int) -> int:
        return len(self.due_scales(tick))

    def total_activations(self, up_to_tick: int) -> int:
        """Total activations across ticks ? linear, not exponential."""
        total = 0
        for tick in range(1, up_to_tick + 1):
            total += self.activations_at(tick)
        return total

    def bounded_window(self, tick: int, window: int = 64) -> tuple[str, ...]:
        """Only the affected window is activated (entities are not all scanned)."""
        due = self.due_scales(tick)
        if not due:
            return ()
        # Deterministic subset of the due scales limited to the window.
        return tuple(due[:window])
