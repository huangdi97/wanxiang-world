"""Compatibility exports for the G95G validation model contracts."""

from wanxiang_substrate.world_lab.validation_profile import ValidationProfile
from wanxiang_substrate.world_lab.validation_report import ValidationCheck, ValidationReport
from wanxiang_substrate.world_lab.validation_support import (
    DEFAULT_WORLDNESS_MAPPING,
    VALIDATION_LEVELS,
    VALIDATION_SCHEMA_VERSION,
    ValidationLevel,
    ValidationStatus,
)

__all__ = [
    "DEFAULT_WORLDNESS_MAPPING",
    "VALIDATION_LEVELS",
    "VALIDATION_SCHEMA_VERSION",
    "ValidationCheck",
    "ValidationLevel",
    "ValidationProfile",
    "ValidationReport",
    "ValidationStatus",
]
