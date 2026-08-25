"""Measured Worldness scoring and separate release gates (M81)."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_substrate.authoring.worldness_policy import (
    DEFAULT_WORLDNESS_THRESHOLDS,
    VIOLATION_DIMENSIONS,
    WorldnessGates,
)
from wanxiang_substrate.authoring.worldness_support import (
    WorldnessDimensionEvidence,
    WorldnessInput,
    WorldnessScore,
)


def assess_worldness(value: WorldnessInput, *, threshold: float = 0.6) -> WorldnessScore:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be within [0,1]")
    thresholds = replace(
        DEFAULT_WORLDNESS_THRESHOLDS,
        publish_dimension_min=max(DEFAULT_WORLDNESS_THRESHOLDS.publish_dimension_min, threshold),
    )
    entities = min(1.0, value.entity_count / 2)
    events = min(1.0, value.event_count / 2)
    relations = min(1.0, value.relation_count)
    places = min(1.0, value.place_count) if value.place_count else relations
    sources = min(1.0, value.source_count)
    integrity = value.integrity
    evidence = min(value.evidence_coverage, sources)
    action = (
        events * integrity.causal_consistency
        if not value.action_committed
        else (events * integrity.causal_consistency if value.action_evidence_refs else 0.0)
    )
    measurements = (
        ("persistence", entities, f"entity_count={value.entity_count}", ("draft.entities",)),
        (
            "identity",
            entities * integrity.identity_integrity,
            f"identity_count={value.entity_count};integrity={integrity.identity_integrity:.3f}",
            ("draft.entities",),
        ),
        (
            "temporal",
            events * integrity.temporal_consistency,
            f"event_count={value.event_count};consistency={integrity.temporal_consistency:.3f}",
            ("draft.events",),
        ),
        (
            "spatial",
            places * integrity.spatial_consistency,
            f"place_count={value.place_count};relation_count={value.relation_count}",
            ("draft.places", "draft.relations"),
        ),
        (
            "causal_action",
            action,
            f"action_committed={value.action_committed};action_evidence={len(value.action_evidence_refs)}",
            ("runtime.commit", "draft.events"),
        ),
        (
            "epistemic_isolation",
            (1.0 - value.uncertainty) * integrity.epistemic_isolation,
            f"uncertainty={value.uncertainty:.3f};isolation={integrity.epistemic_isolation:.3f}",
            ("draft.uncertainty", "runtime.perception"),
        ),
        (
            "object_persistence",
            min(1.0, value.object_count) * integrity.object_consistency
            if value.object_required
            else 1.0,
            f"object_count={value.object_count};required={value.object_required}",
            ("draft.objects",),
        ),
        (
            "evidence_traceability",
            evidence,
            f"evidence_coverage={value.evidence_coverage:.3f};source_count={value.source_count}",
            value.source_refs,
        ),
        (
            "uncertainty",
            (1.0 - value.uncertainty) * integrity.uncertainty_honesty,
            f"uncertainty={value.uncertainty:.3f};honesty={integrity.uncertainty_honesty:.3f}",
            ("draft.uncertainty",),
        ),
        (
            "branch_replay_readiness",
            (1.0 if value.branch_isolated and value.replay_equal else 0.0)
            * integrity.replay_consistency,
            f"branch_isolated={value.branch_isolated};replay_equal={value.replay_equal}",
            ("runtime.branch", "runtime.replay"),
        ),
    )
    scores = {name: score for name, score, _measurement, _refs in measurements}
    for violation in integrity.violations:
        for dimension in VIOLATION_DIMENSIONS.get(violation, ("evidence_traceability",)):
            if dimension in scores:
                scores[dimension] = 0.0
    ordered_measurements = tuple(
        (name, scores[name], measurement, refs) for name, _score, measurement, refs in measurements
    )
    dimensions = (
        ("persistence", entities),
        ("causality", events * integrity.causal_consistency),
        ("epistemic", (1.0 - value.uncertainty) * integrity.epistemic_isolation),
        ("spatial", relations * integrity.spatial_consistency),
        ("consequence", events * integrity.causal_consistency),
        ("autonomy", entities * integrity.identity_integrity),
        ("branch_isolation", 1.0 if value.branch_isolated else 0.0),
        ("replayability", 1.0 if value.replay_equal else 0.0),
        ("provenance", evidence),
        ("uncertainty", (1.0 - value.uncertainty) * integrity.uncertainty_honesty),
    )
    for violation in integrity.violations:
        for dimension in VIOLATION_DIMENSIONS.get(violation, ()):
            if dimension in scores:
                dimensions = _zero_legacy_dimension(dimensions, dimension)
    overall = sum(score for _name, score in dimensions) / len(dimensions)
    evidence_rows = tuple(
        WorldnessDimensionEvidence(
            name=name,
            measurement=measurement,
            score=score,
            evidence=tuple(refs),
            failure="" if score >= threshold else f"score {score:.3f} below {threshold:.3f}",
            remediation="" if score >= threshold else f"repair {name} from its evidence refs",
        )
        for name, score, measurement, refs in ordered_measurements
    )
    minimum = min(score for _name, score, _measurement, _refs in ordered_measurements)
    previewable = overall >= thresholds.preview_min
    publishable = (
        overall >= thresholds.publish_min
        and minimum >= thresholds.publish_dimension_min
        and not integrity.violations
    )
    living_ready = (
        overall >= thresholds.living_min
        and minimum >= thresholds.living_dimension_min
        and value.branch_isolated
        and value.replay_equal
        and not integrity.violations
    )
    gates = WorldnessGates(previewable, publishable, living_ready)
    return WorldnessScore(
        dimensions,
        overall,
        gates.living_ready,
        evidence_rows,
        gates,
        integrity.violations,
    )


def _zero_legacy_dimension(
    dimensions: tuple[tuple[str, float], ...], evidence_name: str
) -> tuple[tuple[str, float], ...]:
    aliases = {
        "temporal": "causality",
        "spatial": "spatial",
        "causal_action": "causality",
        "epistemic_isolation": "epistemic",
        "object_persistence": "persistence",
        "evidence_traceability": "provenance",
        "uncertainty": "uncertainty",
        "branch_replay_readiness": "replayability",
        "identity": "autonomy",
    }
    target = aliases.get(evidence_name, evidence_name)
    return tuple((name, 0.0 if name == target else score) for name, score in dimensions)


__all__ = ["assess_worldness"]
