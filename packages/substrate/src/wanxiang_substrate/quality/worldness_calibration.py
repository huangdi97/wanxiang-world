"""Adversarial Worldness calibration (M81/G84A-G84F)."""

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_substrate.authoring.worldness import WorldnessEvaluator, WorldnessInput
from wanxiang_substrate.authoring.worldness_support import WorldnessIntegrity, WorldnessScore


@dataclass(frozen=True, slots=True)
class CalibrationCase:
    name: str
    broken: WorldnessInput
    repair: WorldnessInput
    violated_dimensions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class WorldnessCalibrationReport:
    baseline: WorldnessScore
    cases: tuple[tuple[str, WorldnessScore, WorldnessScore], ...]
    minimum_score_drop: float
    anti_gaming_passed: bool
    threshold_policy_passed: bool
    passed: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "baseline": _score(self.baseline),
            "cases": {
                name: {"broken": _score(broken), "repair": _score(repair)}
                for name, broken, repair in self.cases
            },
            "minimum_score_drop": self.minimum_score_drop,
            "anti_gaming_passed": self.anti_gaming_passed,
            "threshold_policy_passed": self.threshold_policy_passed,
            "passed": self.passed,
        }


def run_worldness_calibration() -> WorldnessCalibrationReport:
    evaluator = WorldnessEvaluator()
    baseline_input = _baseline()
    baseline = evaluator.evaluate(baseline_input)
    cases = tuple(_cases(baseline_input))
    scored = tuple(
        (case.name, evaluator.evaluate(case.broken), evaluator.evaluate(case.repair))
        for case in cases
    )
    drops = tuple(baseline.overall - broken.overall for _name, broken, _repair in scored)
    anti_gaming = evaluator.evaluate(
        replace(baseline_input, action_committed=True, action_evidence_refs=())
    )
    medium = evaluator.evaluate(
        WorldnessInput(
            1,
            1,
            1,
            1,
            0.1,
            replay_equal=True,
            branch_isolated=True,
            place_count=1,
        )
    )
    threshold_policy = (
        medium.gates.previewable and not medium.gates.publishable and not medium.gates.living_ready
    )
    minimum_drop = min(drops) if drops else 0.0
    all_cases = all(
        broken.overall < baseline.overall
        and not broken.gates.living_ready
        and repair.gates.living_ready
        for _name, broken, repair in scored
    )
    passed = (
        baseline.gates.living_ready
        and all_cases
        and minimum_drop >= 0.08
        and anti_gaming.gates.living_ready is False
        and threshold_policy
    )
    return WorldnessCalibrationReport(
        baseline,
        scored,
        minimum_drop,
        anti_gaming.gates.living_ready is False,
        threshold_policy,
        passed,
    )


def _baseline() -> WorldnessInput:
    return WorldnessInput(
        entity_count=4,
        relation_count=3,
        event_count=4,
        source_count=2,
        uncertainty=0.08,
        replay_equal=True,
        branch_isolated=True,
        draft_id="calibration_baseline",
        draft_revision=1,
        source_refs=("source:anonymous#record/1", "source:anonymous#record/2"),
        domain_refs=("narrative", "spatial"),
        package_id="package:calibration",
        provider_ids=("reference",),
        seed=84,
        place_count=2,
        object_count=2,
        object_required=True,
        evidence_coverage=0.96,
        action_committed=True,
        action_evidence_refs=("runtime.commit", "runtime.replay"),
    )


def _cases(base: WorldnessInput) -> tuple[CalibrationCase, ...]:
    return (
        CalibrationCase(
            "teleportation",
            replace(
                base,
                integrity=WorldnessIntegrity(
                    spatial_consistency=0.0, violations=("teleportation",)
                ),
            ),
            base,
            ("spatial",),
        ),
        CalibrationCase(
            "secret_leakage",
            replace(
                base,
                integrity=WorldnessIntegrity(
                    epistemic_isolation=0.0, violations=("secret_leakage",)
                ),
            ),
            base,
            ("epistemic_isolation",),
        ),
        CalibrationCase(
            "duplicate_object",
            replace(
                base,
                integrity=WorldnessIntegrity(
                    object_consistency=0.0, violations=("duplicate_object",)
                ),
            ),
            base,
            ("object_persistence",),
        ),
        CalibrationCase(
            "temporal_reversal",
            replace(
                base,
                integrity=WorldnessIntegrity(
                    temporal_consistency=0.0, violations=("temporal_reversal",)
                ),
            ),
            base,
            ("temporal",),
        ),
        CalibrationCase(
            "unsupported_fact",
            replace(
                base,
                evidence_coverage=0.0,
                integrity=WorldnessIntegrity(
                    uncertainty_honesty=0.0, violations=("unsupported_fact",)
                ),
            ),
            base,
            ("evidence_traceability", "uncertainty"),
        ),
        CalibrationCase(
            "replay_mismatch",
            replace(
                base,
                replay_equal=False,
                integrity=WorldnessIntegrity(
                    replay_consistency=0.0, violations=("replay_mismatch",)
                ),
            ),
            base,
            ("branch_replay_readiness",),
        ),
        CalibrationCase(
            "identity_corruption",
            replace(
                base,
                integrity=WorldnessIntegrity(
                    identity_integrity=0.0, violations=("identity_split",)
                ),
            ),
            base,
            ("identity",),
        ),
    )


def _score(score: WorldnessScore) -> dict[str, object]:
    return {
        "overall": score.overall,
        "passed": score.passed,
        "dimensions": dict(score.dimensions),
        "gates": {
            "previewable": score.gates.previewable,
            "publishable": score.gates.publishable,
            "living_ready": score.gates.living_ready,
        },
        "violations": list(score.violations),
    }


__all__ = ["CalibrationCase", "WorldnessCalibrationReport", "run_worldness_calibration"]
