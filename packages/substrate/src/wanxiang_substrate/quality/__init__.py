"""Quality and generalization evidence that remains outside Canon."""

from wanxiang_substrate.quality.experience_models import (
    EXPERIENCE_QUALITY_SCHEMA,
    QUALITY_DIMENSIONS,
    ExperienceDimension,
    ExperienceMeasurement,
    ExperienceQualityRun,
    measurement_from_dict,
)
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
    "EXPERIENCE_QUALITY_SCHEMA",
    "QUALITY_DIMENSIONS",
    "GoldAssertion",
    "GoldSet",
    "MetricResult",
    "SamplingManifest",
    "SemanticQualityReport",
    "WorldnessCalibrationReport",
    "ExperienceDimension",
    "ExperienceMeasurement",
    "ExperienceQualityRun",
    "evaluate_gold_set",
    "measurement_from_dict",
    "run_worldness_calibration",
    "sample_candidates",
]
