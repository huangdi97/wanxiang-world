"""Worldness evaluation and candidate-only repair loops (M66)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from wanxiang_substrate.authoring.worldness_policy import WorldnessGates, WorldnessIntegrity
from wanxiang_substrate.authoring.worldness_scoring import assess_worldness
from wanxiang_substrate.authoring.worldness_support import (
    WORLDNESS_DIMENSIONS,
    BoundedSimulation,
    BranchIsolationProof,
    DeterminismEnvelope,
    FailureLocalizer,
    FailureLocation,
    SimulationStep,
    SimulationTrace,
    WorldnessDimensionEvidence,
    WorldnessInput,
    WorldnessScore,
    determinism_envelope,
    prove_branch_isolation,
)


@dataclass(frozen=True, slots=True)
class RepairCandidate:
    repair_id: str
    dimension: str
    action: str
    source_refs: tuple[str, ...]
    confidence: float
    applied: bool = False
    target: str = ""


@dataclass(frozen=True, slots=True)
class RecompileCycle:
    round_number: int
    input_revision: int
    output_revision: int | None
    candidate_ids: tuple[str, ...]
    committed: bool = False


@dataclass(frozen=True, slots=True)
class RepairRun:
    rounds: int
    scores: tuple[WorldnessScore, ...]
    candidates: tuple[RepairCandidate, ...]
    converged: bool
    locations: tuple[FailureLocation, ...] = ()
    traces: tuple[SimulationTrace, ...] = ()
    cycles: tuple[RecompileCycle, ...] = ()


class WorldnessEvaluator:
    """Scores observable reference evidence, not subjective human realism."""

    def evaluate(self, value: WorldnessInput, *, threshold: float = 0.6) -> WorldnessScore:
        return assess_worldness(value, threshold=threshold)


class RepairLoop:
    """Runs bounded candidate-only repair/recompile/evaluation cycles."""

    def run(
        self,
        value: WorldnessInput,
        *,
        rounds: int = 2,
        recompile: Callable[[WorldnessInput, tuple[RepairCandidate, ...], int], WorldnessInput]
        | None = None,
    ) -> RepairRun:
        limit = min(max(rounds, 1), 7)
        evaluator = WorldnessEvaluator()
        simulator = BoundedSimulation()
        localizer = FailureLocalizer()
        current = value
        scores: list[WorldnessScore] = []
        traces: list[SimulationTrace] = []
        locations: list[FailureLocation] = []
        candidates: list[RepairCandidate] = []
        cycles: list[RecompileCycle] = []
        for number in range(1, limit + 1):
            score = evaluator.evaluate(current)
            scores.append(score)
            traces.append(simulator.run(current, branch_id=f"repair_{number}"))
            if score.passed:
                break
            found = localizer.locate(score, current)
            locations.extend(found)
            proposals = tuple(
                RepairCandidate(
                    repair_id=f"repair_{number}_{item.dimension}",
                    dimension=item.dimension,
                    action=f"rebuild_{item.target.replace(' ', '_')}",
                    source_refs=item.source_refs,
                    confidence=0.4,
                    target=f"{item.layer}:{item.target}",
                )
                for item in found
            )
            candidates.extend(proposals)
            input_revision = current.draft_revision
            output_revision: int | None = None
            if recompile is not None and number < limit:
                next_value = recompile(current, proposals, number)
                output_revision = next_value.draft_revision
                current = next_value
            cycles.append(
                RecompileCycle(
                    number,
                    input_revision,
                    output_revision,
                    tuple(item.repair_id for item in proposals),
                )
            )
            if recompile is None or number >= limit:
                break
        return RepairRun(
            rounds=limit,
            scores=tuple(scores),
            candidates=tuple(candidates),
            converged=scores[-1].passed,
            locations=tuple(locations),
            traces=tuple(traces),
            cycles=tuple(cycles),
        )


__all__ = [
    "WORLDNESS_DIMENSIONS",
    "BoundedSimulation",
    "BranchIsolationProof",
    "DeterminismEnvelope",
    "FailureLocalizer",
    "FailureLocation",
    "RepairCandidate",
    "RepairLoop",
    "RepairRun",
    "RecompileCycle",
    "SimulationStep",
    "SimulationTrace",
    "WorldnessEvaluator",
    "WorldnessDimensionEvidence",
    "WorldnessGates",
    "WorldnessIntegrity",
    "WorldnessInput",
    "WorldnessScore",
    "determinism_envelope",
    "prove_branch_isolation",
]
