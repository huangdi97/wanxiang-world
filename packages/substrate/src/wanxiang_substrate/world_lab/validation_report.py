"""ValidationCheck and conservative ValidationReport contracts (G95G)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.registry_support import integer, ref, sequence
from wanxiang_substrate.world_lab.validation_support import (
    VALIDATION_LEVELS,
    VALIDATION_SCHEMA_VERSION,
    ValidationLevel,
    ValidationStatus,
    level,
    measurements,
    optional_score,
    reason,
    refs,
    status,
)


@dataclass(frozen=True, slots=True)
class ValidationCheck:
    """One explicit level result. No result is inferred from Worldness."""

    level: ValidationLevel
    status: ValidationStatus
    reason: str
    evidence_refs: tuple[str, ...] = ()
    score: float | None = None
    measurements: tuple[tuple[str, float], ...] = ()
    schema_version: int = VALIDATION_SCHEMA_VERSION

    def __post_init__(self) -> None:
        level(self.level)
        status(self.status)
        reason(self.reason)
        if self.schema_version != VALIDATION_SCHEMA_VERSION:
            raise ContractError("unsupported validation check schema")
        object.__setattr__(self, "evidence_refs", refs(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "score", optional_score(self.score))
        object.__setattr__(self, "measurements", measurements(self.measurements))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "level": self.level,
            "status": self.status,
            "reason": self.reason,
            "evidence_refs": list(self.evidence_refs),
            "score": self.score,
            "measurements": [list(item) for item in self.measurements],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ValidationCheck:
        return cls(
            level=level(data.get("level")),
            status=status(data.get("status")),
            reason=reason(data.get("reason")),
            evidence_refs=refs(
                sequence(data.get("evidence_refs", ()), "evidence_refs"), "evidence_refs"
            ),
            score=optional_score(data.get("score")),
            measurements=measurements(sequence(data.get("measurements", ()), "measurements")),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Independent V0-V7 report with conservative aggregate semantics."""

    profile_ref: str
    profile_version: int
    required_levels: tuple[ValidationLevel, ...]
    checks: tuple[ValidationCheck, ...]
    worldness_ref: str = ""
    worldness_independent: bool = True
    schema_version: int = VALIDATION_SCHEMA_VERSION
    overall_status: ValidationStatus = "unknown"

    def __post_init__(self) -> None:
        ref(self.profile_ref, "profile_ref")
        integer(self.profile_version, "profile_version", minimum=1)
        if self.schema_version != VALIDATION_SCHEMA_VERSION:
            raise ContractError("unsupported validation report schema")
        if self.worldness_ref:
            ref(self.worldness_ref, "worldness_ref")
        if self.worldness_independent is not True:
            raise ContractError("ValidationReport must remain independent of Worldness")
        levels = tuple(level(value, "required level") for value in self.required_levels)
        if set(levels) != set(VALIDATION_LEVELS) or len(levels) != len(VALIDATION_LEVELS):
            raise ContractError("validation report must require V0-V7 exactly")
        checks = tuple(self.checks)
        if len({check.level for check in checks}) != len(checks):
            raise ContractError("validation report levels must be unique")
        if any(check.level not in levels for check in checks):
            raise ContractError("validation report contains an unrequired level")
        ordered = tuple(sorted(checks, key=lambda check: VALIDATION_LEVELS.index(check.level)))
        object.__setattr__(self, "required_levels", VALIDATION_LEVELS)
        object.__setattr__(self, "checks", ordered)
        object.__setattr__(self, "overall_status", self._aggregate(ordered))

    @staticmethod
    def _aggregate(checks: tuple[ValidationCheck, ...]) -> ValidationStatus:
        statuses = {check.status for check in checks}
        if "fail" in statuses:
            return "fail"
        if "blocked" in statuses:
            return "blocked"
        if "unknown" in statuses or len(checks) != len(VALIDATION_LEVELS):
            return "unknown"
        return "pass"

    @property
    def complete(self) -> bool:
        return {check.level for check in self.checks} == set(self.required_levels)

    @property
    def accepted(self) -> bool:
        return self.complete and self.overall_status == "pass"

    @property
    def missing_levels(self) -> tuple[ValidationLevel, ...]:
        found = {check.level for check in self.checks}
        return tuple(level for level in self.required_levels if level not in found)

    @property
    def unknown_levels(self) -> tuple[ValidationLevel, ...]:
        return tuple(check.level for check in self.checks if check.status == "unknown")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "profile_ref": self.profile_ref,
            "profile_version": self.profile_version,
            "required_levels": list(self.required_levels),
            "checks": [check.to_dict() for check in self.checks],
            "worldness_ref": self.worldness_ref,
            "worldness_independent": self.worldness_independent,
            "overall_status": self.overall_status,
            "complete": self.complete,
            "accepted": self.accepted,
            "missing_levels": list(self.missing_levels),
            "unknown_levels": list(self.unknown_levels),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ValidationReport:
        raw_checks = sequence(data.get("checks", ()), "checks")
        checks: list[ValidationCheck] = []
        for item in raw_checks:
            if not isinstance(item, Mapping):
                raise ContractError("validation report checks must be mappings")
            checks.append(ValidationCheck.from_dict(cast(Mapping[str, object], item)))
        worldness_ref = data.get("worldness_ref", "")
        if not isinstance(worldness_ref, str):
            raise ContractError("worldness_ref must be text")
        independent = data.get("worldness_independent", True)
        if not isinstance(independent, bool):
            raise ContractError("worldness_independent must be boolean")
        return cls(
            profile_ref=ref(data.get("profile_ref"), "profile_ref"),
            profile_version=integer(data.get("profile_version"), "profile_version", minimum=1),
            required_levels=tuple(
                level(value, "required level")
                for value in sequence(data.get("required_levels", ()), "required_levels")
            ),
            checks=tuple(checks),
            worldness_ref=worldness_ref,
            worldness_independent=independent,
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


__all__ = ["ValidationCheck", "ValidationReport"]
