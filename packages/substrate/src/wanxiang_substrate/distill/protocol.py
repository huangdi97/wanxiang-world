"""Distiller protocol + pass DAG (G57B).

One distiller contract across all passes: deterministic reference passes are
always available (no API); optional model providers plug in later behind the
same boundary. Passes produce CandidateEnvelopes only; providers never own
Commit. The DAG runs passes in order and tags provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.parsing.segment import Segment


class Distiller(Protocol):
    """A distillation pass: segments -> candidate envelopes."""

    name: str
    version: int

    def distill(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
    ) -> tuple[CandidateEnvelope, ...]: ...


@dataclass(frozen=True, slots=True)
class DistillerDAG:
    """Ordered multi-pass distillation with provenance tagging."""

    passes: tuple[Distiller, ...]

    def run(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
    ) -> tuple[CandidateEnvelope, ...]:
        candidates: list[CandidateEnvelope] = []
        for distiller in self.passes:
            batch = distiller.distill(segments, source_id=source_id)
            candidates.extend(batch)
        return tuple(candidates)

    def pass_names(self) -> tuple[str, ...]:
        return tuple(distiller.name for distiller in self.passes)


class DistillerRegistry:
    """Registers passes and runs the full DAG."""

    def __init__(self) -> None:
        self._passes: list[Distiller] = []

    def register(self, distiller: Distiller) -> None:
        self._passes.append(distiller)

    def dag(self) -> DistillerDAG:
        return DistillerDAG(tuple(self._passes))

    def run(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
    ) -> tuple[CandidateEnvelope, ...]:
        return self.dag().run(segments, source_id=source_id)
