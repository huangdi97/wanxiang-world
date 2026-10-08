"""Worldness integrity signals and gate thresholds (M81)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorldnessIntegrity:
    """Measured integrity signals used by calibration, not endpoint status."""

    identity_integrity: float = 1.0
    temporal_consistency: float = 1.0
    spatial_consistency: float = 1.0
    causal_consistency: float = 1.0
    epistemic_isolation: float = 1.0
    object_consistency: float = 1.0
    uncertainty_honesty: float = 1.0
    replay_consistency: float = 1.0
    violations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        values = (
            self.identity_integrity,
            self.temporal_consistency,
            self.spatial_consistency,
            self.causal_consistency,
            self.epistemic_isolation,
            self.object_consistency,
            self.uncertainty_honesty,
            self.replay_consistency,
        )
        if any(not 0.0 <= value <= 1.0 for value in values):
            raise ValueError("worldness integrity values must be within [0,1]")


@dataclass(frozen=True, slots=True)
class WorldnessThresholds:
    """Separate preview, publish, and living-ready policy thresholds."""

    preview_min: float = 0.50
    publish_min: float = 0.75
    living_min: float = 0.90
    publish_dimension_min: float = 0.60
    living_dimension_min: float = 0.75

    def __post_init__(self) -> None:
        values = (
            self.preview_min,
            self.publish_min,
            self.living_min,
            self.publish_dimension_min,
            self.living_dimension_min,
        )
        if any(not 0.0 <= value <= 1.0 for value in values):
            raise ValueError("worldness thresholds must be within [0,1]")


@dataclass(frozen=True, slots=True)
class WorldnessGates:
    """Gate decisions kept distinct so endpoint success cannot imply living-ready."""

    previewable: bool
    publishable: bool
    living_ready: bool


VIOLATION_DIMENSIONS: dict[str, tuple[str, ...]] = {
    "teleportation": ("spatial", "causal_action"),
    "secret_leakage": ("epistemic_isolation",),
    "duplicate_object": ("object_persistence",),
    "temporal_reversal": ("temporal", "causal_action"),
    "unsupported_fact": ("evidence_traceability", "uncertainty"),
    "replay_mismatch": ("branch_replay_readiness",),
    "identity_split": ("identity",),
    "identity_merge_corruption": ("identity",),
}


DEFAULT_WORLDNESS_THRESHOLDS = WorldnessThresholds()

__all__ = [
    "DEFAULT_WORLDNESS_THRESHOLDS",
    "VIOLATION_DIMENSIONS",
    "WorldnessGates",
    "WorldnessIntegrity",
    "WorldnessThresholds",
]
