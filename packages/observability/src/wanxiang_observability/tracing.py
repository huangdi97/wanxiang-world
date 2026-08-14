"""Lightweight OpenTelemetry-compatible observability (G16E).

Provides a no-op-by-default tracing/metrics facade with an in-memory exporter
for local diagnostics. Spans correlate world/branch/command/commit IDs and
never include private memory or source secrets. No commercial backend is
required; a local collector can consume the exported records.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Span:
    """A recorded operational span (no sensitive payloads)."""

    trace_id: str
    world_id: str
    branch_id: str
    command_id: str
    stage: str
    status: str
    latency_ms: float
    error_code: str = ""


@dataclass
class Metrics:
    """Simple counters/gauges for failure and saturation signals."""

    counters: dict[str, int] = field(default_factory=dict[str, int])
    gauges: dict[str, int] = field(default_factory=dict[str, int])

    def increment(self, name: str, by: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + by

    def set_gauge(self, name: str, value: int) -> None:
        self.gauges[name] = value


class Observability:
    """No-op-by-default facade with an in-memory exporter for diagnostics."""

    def __init__(self) -> None:
        self._spans: list[Span] = []
        self.metrics = Metrics()

    def record_span(
        self,
        *,
        trace_id: str,
        world_id: str = "",
        branch_id: str = "",
        command_id: str = "",
        stage: str,
        status: str,
        latency_ms: float = 0.0,
        error_code: str = "",
    ) -> None:
        self._spans.append(
            Span(
                trace_id=trace_id,
                world_id=world_id,
                branch_id=branch_id,
                command_id=command_id,
                stage=stage,
                status=status,
                latency_ms=latency_ms,
                error_code=error_code,
            )
        )

    def spans(self) -> tuple[Span, ...]:
        return tuple(self._spans)

    def trace(self, trace_id: str) -> tuple[Span, ...]:
        return tuple(s for s in self._spans if s.trace_id == trace_id)


def now_ms() -> float:
    return time.perf_counter() * 1000.0
