"""Multi-simulator federation & co-simulation research (G19H, experimental).

Heterogeneous simulators produce PROPOSED deltas only; nothing is committed to
canonical world state by this research. A multi-rate scheduler coordinates
time deterministically, conflicts are resolved EXPLICITLY (never by "fastest
simulator wins"), validity envelopes/assumptions persist, and a failed
simulator is isolated from the others.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ValidityEnvelope:
    min_step: float
    max_step: float
    max_horizon: float


@dataclass(frozen=True, slots=True)
class SimDelta:
    simulator_id: str
    model_id: str
    model_version: str
    time: float
    values: tuple[tuple[str, float], ...]
    validity: ValidityEnvelope
    provenance: str = ""
    proposed: bool = True


class SimulatorAdapter(Protocol):
    simulator_id: str
    model_id: str
    model_version: str
    step_size: float
    validity: ValidityEnvelope

    def step(self, time: float) -> SimDelta: ...


class TickSimulator:
    """Fast, coarse deterministic simulator (large step, wide envelope)."""

    simulator_id = "tick"
    model_id = "tick_model"
    model_version = "1.0"
    step_size = 1.0
    validity = ValidityEnvelope(min_step=1.0, max_step=1.0, max_horizon=10.0)

    def step(self, time: float) -> SimDelta:
        return SimDelta(
            simulator_id=self.simulator_id,
            model_id=self.model_id,
            model_version=self.model_version,
            time=time,
            values=(("position", time * 2.0),),
            validity=self.validity,
            provenance="tick:v1",
        )


class PreciseSimulator:
    """Slow, precise deterministic simulator (small step, tight envelope)."""

    simulator_id = "precise"
    model_id = "precise_model"
    model_version = "1.0"
    step_size = 0.5
    validity = ValidityEnvelope(min_step=0.5, max_step=0.5, max_horizon=2.0)

    def step(self, time: float) -> SimDelta:
        return SimDelta(
            simulator_id=self.simulator_id,
            model_id=self.model_id,
            model_version=self.model_version,
            time=time,
            values=(("position", time * 2.0 + 0.1),),
            validity=self.validity,
            provenance="precise:v1",
        )


class FlakySimulator(TickSimulator):
    """Tick simulator that fails from a given time onward (partial failure)."""

    simulator_id = "flaky"

    def __init__(self, fail_from: float) -> None:
        self._fail_from = fail_from

    def step(self, time: float) -> SimDelta:
        if time >= self._fail_from:
            raise RuntimeError("simulator crashed")
        return super().step(time)


@dataclass(frozen=True, slots=True)
class FederationCheckpoint:
    now: float
    horizon: float
    next_due: tuple[tuple[str, float], ...]
    deltas: tuple[SimDelta, ...]
    failed: tuple[tuple[str, str], ...]
    coordination_steps: int

    def digest(self) -> str:
        canonical = json.dumps(
            {
                "now": self.now,
                "horizon": self.horizon,
                "next_due": sorted((k, v) for k, v in self.next_due),
                "deltas": [
                    {
                        "simulator_id": d.simulator_id,
                        "time": d.time,
                        "values": sorted(d.values),
                    }
                    for d in self.deltas
                ],
                "failed": sorted(self.failed),
                "coordination_steps": self.coordination_steps,
            },
            sort_keys=True,
        )
        return hashlib.sha256(canonical.encode()).hexdigest()


class FederationScheduler:
    """Multi-rate scheduler: advances only simulators whose due time is reached."""

    def __init__(self, adapters: Sequence[SimulatorAdapter], horizon: float) -> None:
        self._adapters = tuple(adapters)
        self._horizon = horizon
        self._next_due: dict[str, float] = {a.simulator_id: 0.0 for a in self._adapters}
        self._now = 0.0
        self._deltas: list[SimDelta] = []
        self._failed: dict[str, str] = {}
        self._coordination_steps = 0

    def run(self) -> tuple[SimDelta, ...]:
        while True:
            due = [t for t in self._next_due.values() if t <= self._horizon]
            if not due:
                break
            now = min(due)
            self._now = now
            self._coordination_steps += 1
            for adapter in self._adapters:
                if self._next_due[adapter.simulator_id] != now:
                    continue
                try:
                    delta = adapter.step(now)
                except Exception as exc:  # isolate failed simulator; others continue
                    self._failed[adapter.simulator_id] = str(exc)
                    self._next_due[adapter.simulator_id] = float("inf")
                    continue
                self._deltas.append(delta)
                self._next_due[adapter.simulator_id] = now + adapter.step_size
        return tuple(self._deltas)

    def checkpoint(self) -> FederationCheckpoint:
        return FederationCheckpoint(
            now=self._now,
            horizon=self._horizon,
            next_due=tuple(sorted(self._next_due.items())),
            deltas=tuple(self._deltas),
            failed=tuple(sorted(self._failed.items())),
            coordination_steps=self._coordination_steps,
        )

    def restore(self, checkpoint: FederationCheckpoint) -> None:
        self._now = checkpoint.now
        self._horizon = checkpoint.horizon
        self._next_due = dict(checkpoint.next_due)
        self._deltas = list(checkpoint.deltas)
        self._failed = dict(checkpoint.failed)
        self._coordination_steps = checkpoint.coordination_steps

    def assumptions(self) -> tuple[tuple[str, ValidityEnvelope], ...]:
        return tuple((a.simulator_id, a.validity) for a in self._adapters)

    def failed(self) -> tuple[tuple[str, str], ...]:
        return tuple(sorted(self._failed.items()))

    @property
    def coordination_steps(self) -> int:
        return self._coordination_steps


@dataclass(frozen=True, slots=True)
class Resolution:
    time: float
    accepted: SimDelta | None
    rejected: tuple[SimDelta, ...]
    unresolved: tuple[SimDelta, ...]
    reason: str


class ConflictResolver:
    """Explicit conflict adjudication; never implicit fastest-wins."""

    def __init__(self, precedence: Mapping[str, int] | None = None) -> None:
        self._precedence = dict(precedence) if precedence is not None else {}

    def resolve(self, deltas: Sequence[SimDelta]) -> tuple[Resolution, ...]:
        by_time: dict[float, list[SimDelta]] = {}
        for delta in deltas:
            by_time.setdefault(delta.time, []).append(delta)
        resolutions: list[Resolution] = []
        for time in sorted(by_time):
            group = tuple(by_time[time])
            if len(group) == 1:
                resolutions.append(Resolution(time, group[0], (), (), "single"))
                continue
            precedence = [self._precedence.get(d.model_id, 0) for d in group]
            top_index = max(range(len(group)), key=lambda i: precedence[i])
            top = group[top_index]
            ties = [
                d
                for d in group
                if self._precedence.get(d.model_id, 0) == self._precedence.get(top.model_id, 0)
            ]
            if len(ties) > 1:
                resolutions.append(
                    Resolution(time, None, (), tuple(group), "unresolved:no-precedence")
                )
            else:
                resolutions.append(
                    Resolution(
                        time,
                        top,
                        tuple(d for i, d in enumerate(group) if i != top_index),
                        (),
                        "explicit-precedence",
                    )
                )
        return tuple(resolutions)


@dataclass(frozen=True, slots=True)
class CommitProposal:
    deltas: tuple[SimDelta, ...]
    unresolved: tuple[SimDelta, ...]
    ready: bool


class FederationCoordinator:
    """Runs the federation and produces an explicit commit proposal (never commits)."""

    def __init__(self, scheduler: FederationScheduler, resolver: ConflictResolver) -> None:
        self._scheduler = scheduler
        self._resolver = resolver

    def run(self) -> CommitProposal:
        deltas = self._scheduler.run()
        resolutions = self._resolver.resolve(deltas)
        accepted = tuple(r.accepted for r in resolutions if r.accepted is not None)
        unresolved = tuple(d for r in resolutions for d in r.unresolved)
        return CommitProposal(deltas=accepted, unresolved=unresolved, ready=not unresolved)
