"""Multi-rate event-driven co-simulation orchestrator (G11B).

Simulators register with rates; stepping is deterministic (sorted by name at
each synchronized tick); proposal arbitration resolves conflicts explicitly by
a deterministic rule; checkpoint/recovery restores simulator state.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.cosim.adapter import FakeSimulator
from wanxiang_substrate.cosim.errors import OrchestrationError


@dataclass(frozen=True, slots=True)
class SimRegistration:
    name: str
    rate_ticks: int
    next_wakeup: int


@dataclass(frozen=True, slots=True)
class ArbitrationResult:
    """Explicit adjudication of competing simulator proposals."""

    winner: str | None
    rejected: tuple[str, ...]
    conflict: bool


class CoSimOrchestrator:
    """Deterministic multi-rate orchestrator over fake simulators."""

    def __init__(self) -> None:
        self.simulators: dict[str, FakeSimulator] = {}
        self._registrations: dict[str, SimRegistration] = {}
        self._now = 0
        self._checkpoint_log: list[object] = []

    def register(self, simulator: FakeSimulator, rate_ticks: int) -> None:
        if rate_ticks <= 0:
            raise OrchestrationError("rate must be positive")
        if simulator.name in self._registrations:
            raise OrchestrationError(f"simulator {simulator.name!r} already registered")
        simulator.initialize({})
        self.simulators[simulator.name] = simulator
        self._registrations[simulator.name] = SimRegistration(
            name=simulator.name, rate_ticks=rate_ticks, next_wakeup=rate_ticks
        )

    def step_to(self, target_ticks: int) -> int:
        """Advance all simulators to a synchronized target (deterministic)."""
        if target_ticks < self._now:
            raise OrchestrationError("cannot step backwards")
        for name in sorted(self._registrations):
            reg = self._registrations[name]
            sim = self.simulators[name]
            if target_ticks % reg.rate_ticks == 0 and target_ticks > sim.current_t:
                sim.advance(sim.current_t, target_ticks)
            reg = SimRegistration(
                name=name, rate_ticks=reg.rate_ticks, next_wakeup=target_ticks + reg.rate_ticks
            )
            self._registrations[name] = reg
        self._now = target_ticks
        return self._now

    def next_wakeup(self) -> int:
        return min(reg.next_wakeup for reg in self._registrations.values())

    def advance_one_barrier(self) -> int:
        """Advance to the next synchronization barrier (lowest wakeup)."""
        target = self.next_wakeup()
        return self.step_to(target)

    def checkpoint(self) -> tuple[object, ...]:
        # The orchestrator clock is part of the checkpoint so restore+continue
        # realigns barriers instead of stepping backwards or mis-stepping.
        snap = (self._now,) + tuple(
            self.simulators[name].checkpoint() for name in sorted(self.simulators)
        )
        self._checkpoint_log.append(snap)
        return snap

    def restore(self, checkpoint: tuple[object, ...]) -> None:
        names = sorted(self.simulators)
        if len(checkpoint) != len(names) + 1:
            raise OrchestrationError("checkpoint length mismatch")
        now = checkpoint[0]
        if not isinstance(now, int):
            raise OrchestrationError("checkpoint clock must be an integer")
        self._now = now
        for name, payload in zip(names, checkpoint[1:], strict=True):
            self.simulators[name].restore(payload)

    def arbitrate(self, proposals: dict[str, object]) -> ArbitrationResult:
        """Adjudicate conflicting simulator proposals deterministically."""
        if not proposals:
            return ArbitrationResult(winner=None, rejected=(), conflict=False)
        winner = min(proposals)
        rejected = tuple(p for p in sorted(proposals) if p != winner)
        return ArbitrationResult(
            winner=winner,
            rejected=rejected,
            conflict=len(proposals) > 1,
        )
