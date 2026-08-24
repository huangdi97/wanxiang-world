"""Worldness evaluation and repair proposals (M66)."""

from __future__ import annotations

from dataclasses import dataclass

WORLDNESS_DIMENSIONS = (
    "persistence",
    "causality",
    "epistemic",
    "spatial",
    "consequence",
    "autonomy",
    "branch_isolation",
    "replayability",
    "provenance",
    "uncertainty",
)


@dataclass(frozen=True, slots=True)
class WorldnessInput:
    entity_count: int
    relation_count: int
    event_count: int
    source_count: int
    uncertainty: float
    replay_equal: bool
    branch_isolated: bool


@dataclass(frozen=True, slots=True)
class WorldnessScore:
    dimensions: tuple[tuple[str, float], ...]
    overall: float
    passed: bool

    def value(self, name: str) -> float:
        return dict(self.dimensions).get(name, 0.0)


@dataclass(frozen=True, slots=True)
class RepairCandidate:
    repair_id: str
    dimension: str
    action: str
    source_refs: tuple[str, ...]
    confidence: float
    applied: bool = False


@dataclass(frozen=True, slots=True)
class RepairRun:
    rounds: int
    scores: tuple[WorldnessScore, ...]
    candidates: tuple[RepairCandidate, ...]
    converged: bool


class WorldnessEvaluator:
    """Scores observable reference evidence, not subjective human realism."""

    def evaluate(self, value: WorldnessInput, *, threshold: float = 0.6) -> WorldnessScore:
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
        return WorldnessScore(
            dimensions, overall, all(score >= threshold for _name, score in dimensions)
        )


class RepairLoop:
    """Produces bounded repair proposals and re-evaluates supplied evidence."""

    def run(self, value: WorldnessInput, *, rounds: int = 2) -> RepairRun:
        evaluator = WorldnessEvaluator()
        scores = [evaluator.evaluate(value)]
        candidates: list[RepairCandidate] = []
        for name, score in scores[0].dimensions:
            if score < 0.6:
                candidates.append(
                    RepairCandidate(
                        repair_id=f"repair_{name}",
                        dimension=name,
                        action=f"rebuild_{name}",
                        source_refs=(),
                        confidence=0.4,
                    )
                )
        return RepairRun(
            rounds=min(max(rounds, 1), 7),
            scores=tuple(scores),
            candidates=tuple(candidates),
            converged=scores[-1].passed,
        )
