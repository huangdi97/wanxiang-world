"""Versioned ValidationProfile v1 contract (G95G)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.registry_support import integer, ref, sequence
from wanxiang_substrate.world_lab.validation_support import (
    DEFAULT_WORLDNESS_MAPPING,
    LEVEL_NAMES,
    VALIDATION_LEVELS,
    VALIDATION_SCHEMA_VERSION,
    ValidationLevel,
    level,
    worldness_mapping,
)


@dataclass(frozen=True, slots=True)
class ValidationProfile:
    """Version-pinned validation contract; it does not score or mutate worlds."""

    profile_id: str
    version: int
    required_levels: tuple[ValidationLevel, ...] = VALIDATION_LEVELS
    worldness_mapping: tuple[tuple[ValidationLevel, tuple[str, ...]], ...] = (
        DEFAULT_WORLDNESS_MAPPING
    )
    schema_version: int = VALIDATION_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.profile_id, "profile_id")
        integer(self.version, "profile version", minimum=1)
        if self.schema_version != VALIDATION_SCHEMA_VERSION:
            raise ContractError("unsupported validation profile schema")
        levels = tuple(level(value, "required level") for value in self.required_levels)
        if set(levels) != set(VALIDATION_LEVELS) or len(levels) != len(VALIDATION_LEVELS):
            raise ContractError("ValidationProfile must require V0-V7 exactly")
        object.__setattr__(self, "required_levels", VALIDATION_LEVELS)
        object.__setattr__(self, "worldness_mapping", worldness_mapping(self.worldness_mapping))

    def mapping_for(self, validation_level: ValidationLevel) -> tuple[str, ...]:
        return dict(self.worldness_mapping)[level(validation_level)]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "version": self.version,
            "required_levels": list(self.required_levels),
            "level_names": {code: LEVEL_NAMES[code] for code in self.required_levels},
            "worldness_mapping": [
                [code, list(dimensions)] for code, dimensions in self.worldness_mapping
            ],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ValidationProfile:
        return cls(
            profile_id=ref(data.get("profile_id"), "profile_id"),
            version=integer(data.get("version"), "profile version", minimum=1),
            required_levels=tuple(
                level(value, "required level")
                for value in sequence(data.get("required_levels", ()), "required_levels")
            ),
            worldness_mapping=worldness_mapping(
                sequence(data.get("worldness_mapping", ()), "worldness_mapping")
            ),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


__all__ = ["ValidationProfile"]
