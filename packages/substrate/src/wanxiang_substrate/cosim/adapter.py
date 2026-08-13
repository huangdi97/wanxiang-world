"""SimulationAdapter contract + deterministic fake simulators (G11A).

Adapters receive world slices/snapshots and ONLY emit events and proposed
deltas; they never own commit authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.event import CommittedEvent
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.cosim.errors import AdapterContractError


class SimulationAdapter(Protocol):
    """The full SimulationAdapter contract."""

    def initialize(self, world_slice: object) -> None: ...
    def ingest_state(self, snapshot: InMemoryCanonicalState) -> None: ...
    def advance(self, t0: int, t1: int) -> None: ...
    def emit_events(self) -> tuple[CommittedEvent, ...]: ...
    def emit_proposed_deltas(self) -> tuple[ProposedWorldDelta, ...]: ...
    def checkpoint(self) -> object: ...
    def restore(self, checkpoint: object) -> None: ...
    def describe_assumptions(self) -> tuple[str, ...]: ...
    def describe_validity_envelope(self) -> str: ...


@dataclass(frozen=True, slots=True)
class FakeSimulatorState:
    """Serializable state of a fake simulator (checkpoint/restore)."""

    name: str
    t: int
    value: int
    events_emitted: int


class FakeSimulator:
    """Deterministic fake simulator at a fixed tick rate."""

    def __init__(
        self,
        name: str,
        *,
        rate_ticks: int = 1,
        growth: int = 1,
        assumptions: tuple[str, ...] = ("flat terrain", "no weather"),
    ) -> None:
        if rate_ticks <= 0:
            raise ValueError("rate_ticks must be positive")
        self._name = name
        self._rate_ticks = rate_ticks
        self._growth = growth
        self._assumptions = assumptions
        self._t = 0
        self._value = 0
        self._events_emitted = 0
        self._initialized = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def current_t(self) -> int:
        return self._t

    def initialize(self, world_slice: object) -> None:
        self._initialized = True

    def ingest_state(self, snapshot: InMemoryCanonicalState) -> None:
        # The simulator reads state; it never mutates it.
        self._value = snapshot.revision.value % 10

    def advance(self, t0: int, t1: int) -> None:
        if not self._initialized:
            raise AdapterContractError("adapter must be initialized before advance")
        if t1 < t0:
            raise AdapterContractError("advance requires t1 >= t0")
        if (t1 - t0) % self._rate_ticks != 0:
            raise AdapterContractError(
                f"{self._name} steps at rate {self._rate_ticks}; got {t0}->{t1}"
            )
        steps = (t1 - t0) // self._rate_ticks
        self._value += self._growth * steps
        self._events_emitted += steps
        self._t = t1

    def emit_events(self) -> tuple[CommittedEvent, ...]:
        # Deterministic simulators may emit zero events; deltas carry effects.
        return ()

    def emit_proposed_deltas(self) -> tuple[ProposedWorldDelta, ...]:
        if self._events_emitted == 0:
            return ()
        # A proposed delta is data; the orchestrator/authority decides commit.
        return ()

    def checkpoint(self) -> FakeSimulatorState:
        return FakeSimulatorState(
            name=self._name,
            t=self._t,
            value=self._value,
            events_emitted=self._events_emitted,
        )

    def restore(self, checkpoint: object) -> None:
        state = checkpoint
        if not isinstance(state, FakeSimulatorState):
            raise AdapterContractError("invalid checkpoint payload")
        self._t = state.t
        self._value = state.value
        self._events_emitted = state.events_emitted
        self._initialized = True

    def describe_assumptions(self) -> tuple[str, ...]:
        return self._assumptions

    def describe_validity_envelope(self) -> str:
        return f"valid for rate {self._rate_ticks}; deterministic given same steps"
