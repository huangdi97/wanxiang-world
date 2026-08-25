"""Quality and generalization evidence that remains outside Canon."""

from wanxiang_substrate.quality.semantic_benchmark import (
    GoldAssertion,
    GoldSet,
    MetricResult,
    SamplingManifest,
    SemanticQualityReport,
    evaluate_gold_set,
    sample_candidates,
)
from wanxiang_substrate.quality.worldness_calibration import (
    CalibrationCase,
    WorldnessCalibrationReport,
    run_worldness_calibration,
)

__all__ = [
    "CalibrationCase",
    "GoldAssertion",
    "GoldSet",
    "MetricResult",
    "SamplingManifest",
    "SemanticQualityReport",
    "WorldnessCalibrationReport",
    "evaluate_gold_set",
    "run_worldness_calibration",
    "sample_candidates",
]
