"""Worldness evaluation and candidate-only repair loops (M66)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

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
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be within [0,1]")
        enough_entities = min(1.0, value.entity_count / 2)
        enough_events = min(1.0, value.event_count / 2)
        enough_relations = min(1.0, value.relation_count / 1)
        enough_sources = min(1.0, value.source_count / 1)
        dimensions = (
            ("persistence", enough_entities),
            ("causality", enough_events),
            ("epistemic", 1.0 - value.uncertainty),
            ("spatial", enough_relations),
            ("consequence", enough_events),
            ("autonomy", enough_entities),
            ("branch_isolation", 1.0 if value.branch_isolated else 0.0),
            ("replayability", 1.0 if value.replay_equal else 0.0),
            ("provenance", enough_sources),
            ("uncertainty", 1.0 - value.uncertainty),
        )
        overall = sum(score for _name, score in dimensions) / len(dimensions)
        measurements = (
            (
                "persistence",
                enough_entities,
                f"entity_count={value.entity_count}",
                ("draft.entities",),
            ),
            (
                "identity",
                enough_entities,
                f"identity_count={value.entity_count}",
                ("draft.entities",),
            ),
            ("temporal", enough_events, f"event_count={value.event_count}", ("draft.events",)),
            (
                "spatial",
                min(1.0, value.place_count / 1) if value.place_count else enough_relations,
                f"place_count={value.place_count};relation_count={value.relation_count}",
                ("draft.places", "draft.relations"),
            ),
            (
                "causal_action",
                1.0 if value.action_committed and value.event_count else enough_events,
                f"action_committed={value.action_committed};event_count={value.event_count}",
                ("runtime.commit", "draft.events"),
            ),
            (
                "epistemic_isolation",
                1.0 - value.uncertainty,
                f"uncertainty={value.uncertainty:.3f}",
                ("draft.uncertainty", "runtime.perception"),
            ),
            (
                "object_persistence",
                min(1.0, value.object_count / 1) if value.object_required else 1.0,
                f"object_count={value.object_count};required={value.object_required}",
                ("draft.objects",),
            ),
            (
                "evidence_traceability",
                value.evidence_coverage,
                f"evidence_coverage={value.evidence_coverage:.3f}",
                value.source_refs,
            ),
            (
                "uncertainty",
                1.0 - value.uncertainty,
                f"uncertainty={value.uncertainty:.3f}",
                ("draft.uncertainty",),
            ),
            (
                "branch_replay_readiness",
                1.0 if value.branch_isolated and value.replay_equal else 0.0,
                f"branch_isolated={value.branch_isolated};replay_equal={value.replay_equal}",
                ("runtime.branch", "runtime.replay"),
            ),
        )
        evidence = tuple(
            WorldnessDimensionEvidence(
                name=name,
                measurement=measurement,
                score=score,
                evidence=tuple(refs),
                failure="" if score >= threshold else f"score {score:.3f} below {threshold:.3f}",
                remediation="" if score >= threshold else f"repair {name} from its evidence refs",
            )
            for name, score, measurement, refs in measurements
        )
        return WorldnessScore(
            dimensions,
            overall,
            all(score >= threshold for _name, score in dimensions)
            and all(item.score >= threshold for item in evidence),
            evidence,
        )


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
    "WorldnessInput",
    "WorldnessScore",
    "determinism_envelope",
    "prove_branch_isolation",
]
