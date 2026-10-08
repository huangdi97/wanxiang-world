"""Independent V0-V7 validation orchestration (G95G)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.validation_models import (
    VALIDATION_LEVELS,
    ValidationCheck,
    ValidationProfile,
    ValidationReport,
)


class ValidationStack:
    """Assemble explicit validation evidence without deriving pass from Worldness."""

    def evaluate(
        self,
        profile: ValidationProfile,
        checks: Mapping[str, ValidationCheck] | Sequence[ValidationCheck] = (),
        *,
        worldness_ref: str = "",
    ) -> ValidationReport:
        normalized = self._normalize_checks(checks)
        by_level = {check.level: check for check in normalized}
        filled = tuple(
            by_level.get(
                level,
                ValidationCheck(
                    level=level,
                    status="unknown",
                    reason="no validation evidence supplied",
                ),
            )
            for level in profile.required_levels
        )
        return ValidationReport(
            profile_ref=profile.profile_id,
            profile_version=profile.version,
            required_levels=profile.required_levels,
            checks=filled,
            worldness_ref=worldness_ref,
        )

    def api_report(self, profile: ValidationProfile, report: ValidationReport) -> dict[str, object]:
        if report.profile_ref != profile.profile_id or report.profile_version != profile.version:
            raise ContractError("validation report does not match the supplied profile")
        return {"profile": profile.to_dict(), "report": report.to_dict()}

    @staticmethod
    def _normalize_checks(
        checks: Mapping[str, ValidationCheck] | Sequence[ValidationCheck],
    ) -> tuple[ValidationCheck, ...]:
        if isinstance(checks, Mapping):
            values: list[ValidationCheck] = []
            for raw_level, check in checks.items():
                raw_level_value = _level_key(raw_level)
                raw_check = _check(check)
                if raw_check.level != raw_level_value:
                    raise ContractError("validation mapping key does not match its check")
                values.append(raw_check)
        else:
            values = []
            for item in checks:
                values.append(_check(item))
        if len({check.level for check in values}) != len(values):
            raise ContractError("validation checks must contain each level at most once")
        return tuple(values)


def _level_key(value: object) -> str:
    if not isinstance(value, str) or value not in VALIDATION_LEVELS:
        raise ContractError(f"unsupported validation level key {value!r}")
    return value


def _check(value: object) -> ValidationCheck:
    if not isinstance(value, ValidationCheck):
        raise ContractError("validation checks must be ValidationCheck records")
    return value


__all__ = ["ValidationStack"]
