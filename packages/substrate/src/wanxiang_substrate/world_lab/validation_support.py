"""Shared parsers and constants for the G95G validation contracts."""

from __future__ import annotations

from collections.abc import Sequence
from math import isfinite
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.authoring.worldness_support import WORLDNESS_DIMENSIONS
from wanxiang_substrate.world_lab.registry_support import ref, sequence

VALIDATION_SCHEMA_VERSION = 1
ValidationLevel = Literal["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7"]
ValidationStatus = Literal["pass", "fail", "unknown", "blocked"]
VALIDATION_LEVELS: tuple[ValidationLevel, ...] = (
    "V0",
    "V1",
    "V2",
    "V3",
    "V4",
    "V5",
    "V6",
    "V7",
)
_LEVEL_SET = frozenset(VALIDATION_LEVELS)
_STATUS_SET = frozenset({"pass", "fail", "unknown", "blocked"})
_WORLDNESS_SET = frozenset(WORLDNESS_DIMENSIONS)
LEVEL_NAMES = {
    "V0": "Structural Validity",
    "V1": "Source Fidelity",
    "V2": "Behavioral Validity",
    "V3": "Mechanism Validity",
    "V4": "Macro Validity",
    "V5": "Long-Horizon Stability",
    "V6": "Counterfactual Validity",
    "V7": "External Calibration",
}
DEFAULT_WORLDNESS_MAPPING: tuple[tuple[ValidationLevel, tuple[str, ...]], ...] = (
    ("V0", ("persistence", "provenance", "replayability")),
    ("V1", ("provenance", "uncertainty")),
    ("V2", ("causality", "consequence", "replayability")),
    ("V3", ("causality", "epistemic")),
    ("V4", ("consequence", "autonomy")),
    ("V5", ("persistence", "replayability", "uncertainty")),
    ("V6", ("branch_isolation", "replayability")),
    ("V7", ("provenance", "uncertainty")),
)


def level(value: object, name: str = "level") -> ValidationLevel:
    if not isinstance(value, str) or value not in _LEVEL_SET:
        raise ContractError(f"unsupported {name} {value!r}")
    return value


def status(value: object) -> ValidationStatus:
    if not isinstance(value, str) or value not in _STATUS_SET:
        raise ContractError(f"unsupported validation status {value!r}")
    return cast(ValidationStatus, value)


def reason(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError("validation reason must be non-empty text")
    if "\n" in value or "\r" in value or len(value) > 512:
        raise ContractError("validation reason must be one line of <=512 characters")
    return value


def refs(values: Sequence[object], name: str) -> tuple[str, ...]:
    result = tuple(ref(value, f"{name} item") for value in values)
    if len(result) != len(set(result)):
        raise ContractError(f"{name} must not contain duplicates")
    return tuple(sorted(result))


def measurements(values: Sequence[object]) -> tuple[tuple[str, float], ...]:
    result: list[tuple[str, float]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError("validation measurements must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError("validation measurements must be pairs")
        key, value = ref(pair[0], "measurement key"), pair[1]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ContractError("validation measurement values must be finite numbers")
        result.append((key, float(value)))
    if len(result) != len({key for key, _value in result}):
        raise ContractError("validation measurement keys must be unique")
    return tuple(sorted(result))


def optional_score(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ContractError("validation score must be a finite number")
    if not 0.0 <= value <= 1.0:
        raise ContractError("validation score must be within [0,1]")
    return float(value)


def worldness_mapping(
    values: Sequence[object],
) -> tuple[tuple[ValidationLevel, tuple[str, ...]], ...]:
    found: dict[ValidationLevel, tuple[str, ...]] = {}
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError("worldness mapping items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError("worldness mapping items must be pairs")
        code = level(pair[0], "worldness mapping level")
        dimensions = tuple(
            ref(value, "worldness dimension") for value in sequence(pair[1], "worldness dimensions")
        )
        if not dimensions or len(dimensions) != len(set(dimensions)):
            raise ContractError("worldness mapping dimensions must be non-empty and unique")
        if not set(dimensions).issubset(_WORLDNESS_SET):
            raise ContractError("worldness mapping contains an unknown Worldness dimension")
        if code in found:
            raise ContractError("worldness mapping levels must be unique")
        found[code] = tuple(sorted(dimensions))
    if set(found) != set(VALIDATION_LEVELS):
        raise ContractError("worldness mapping must cover V0-V7 exactly")
    return tuple((code, found[code]) for code in VALIDATION_LEVELS)


__all__ = [
    "DEFAULT_WORLDNESS_MAPPING",
    "LEVEL_NAMES",
    "VALIDATION_LEVELS",
    "VALIDATION_SCHEMA_VERSION",
    "ValidationLevel",
    "ValidationStatus",
]
