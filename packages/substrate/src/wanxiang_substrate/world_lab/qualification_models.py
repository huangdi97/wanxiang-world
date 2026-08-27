"""Sanitized M92 laboratory qualification records (G95H)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.registry_support import integer, ref, sequence

QUALIFICATION_SCHEMA_VERSION = 1
QualificationStatus = Literal["pass", "fail", "unknown"]
_STATUSES = frozenset({"pass", "fail", "unknown"})


def _status(value: object) -> QualificationStatus:
    if not isinstance(value, str) or value not in _STATUSES:
        raise ContractError(f"unsupported qualification status {value!r}")
    return cast(QualificationStatus, value)


def _refs(values: tuple[str, ...], name: str) -> tuple[str, ...]:
    result = tuple(ref(value, f"{name} item") for value in values)
    if len(result) != len(set(result)):
        raise ContractError(f"{name} must not contain duplicates")
    return tuple(sorted(result))


@dataclass(frozen=True, slots=True)
class QualificationCheck:
    """One explicit M92 evidence condition."""

    name: str
    status: QualificationStatus
    reason: str
    evidence_refs: tuple[str, ...] = ()
    schema_version: int = QUALIFICATION_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.name, "qualification check name")
        _status(self.status)
        if not self.reason.strip() or "\n" in self.reason or "\r" in self.reason:
            raise ContractError("qualification check reason must be one-line text")
        integer(self.schema_version, "schema_version", minimum=1)
        if self.schema_version != QUALIFICATION_SCHEMA_VERSION:
            raise ContractError("unsupported qualification check schema")
        object.__setattr__(self, "evidence_refs", _refs(self.evidence_refs, "evidence_refs"))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "status": self.status,
            "reason": self.reason,
            "evidence_refs": list(self.evidence_refs),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> QualificationCheck:
        status = _status(data.get("status"))
        reason = data.get("reason")
        if not isinstance(reason, str):
            raise ContractError("qualification reason must be text")
        raw_refs = sequence(data.get("evidence_refs", ()), "evidence_refs")
        refs = tuple(ref(value, "evidence_refs item") for value in raw_refs)
        return cls(
            name=ref(data.get("name"), "qualification check name"),
            status=status,
            reason=reason,
            evidence_refs=refs,
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class LabQualification:
    """Cross-artifact M92 result; it is evidence, never canonical state."""

    qualification_id: str
    experiment_ref: str
    source_profile: str
    validation_profile_ref: str
    batch_ref: str
    worldline_refs: tuple[str, ...]
    artifact_refs: tuple[str, ...]
    intervention_refs: tuple[str, ...]
    comparison_ref: str
    checks: tuple[QualificationCheck, ...]
    schema_version: int = QUALIFICATION_SCHEMA_VERSION
    overall_status: QualificationStatus = "unknown"

    def __post_init__(self) -> None:
        for name in (
            "qualification_id",
            "experiment_ref",
            "source_profile",
            "validation_profile_ref",
            "batch_ref",
            "comparison_ref",
        ):
            ref(getattr(self, name), name)
        if self.schema_version != QUALIFICATION_SCHEMA_VERSION:
            raise ContractError("unsupported lab qualification schema")
        object.__setattr__(self, "worldline_refs", _refs(self.worldline_refs, "worldline_refs"))
        object.__setattr__(self, "artifact_refs", _refs(self.artifact_refs, "artifact_refs"))
        object.__setattr__(
            self, "intervention_refs", _refs(self.intervention_refs, "intervention_refs")
        )
        if len({check.name for check in self.checks}) != len(self.checks):
            raise ContractError("qualification check names must be unique")
        ordered = tuple(sorted(self.checks, key=lambda check: check.name))
        object.__setattr__(self, "checks", ordered)
        object.__setattr__(self, "overall_status", self._aggregate(ordered))

    @staticmethod
    def _aggregate(checks: tuple[QualificationCheck, ...]) -> QualificationStatus:
        statuses = {check.status for check in checks}
        if "fail" in statuses:
            return "fail"
        if "unknown" in statuses or not checks:
            return "unknown"
        return "pass"

    @property
    def qualified(self) -> bool:
        return self.overall_status == "pass"

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "qualification_id": self.qualification_id,
            "experiment_ref": self.experiment_ref,
            "source_profile": self.source_profile,
            "validation_profile_ref": self.validation_profile_ref,
            "batch_ref": self.batch_ref,
            "worldline_refs": list(self.worldline_refs),
            "artifact_refs": list(self.artifact_refs),
            "intervention_refs": list(self.intervention_refs),
            "comparison_ref": self.comparison_ref,
            "checks": [check.to_dict() for check in self.checks],
            "overall_status": self.overall_status,
            "qualified": self.qualified,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> LabQualification:
        raw_checks = sequence(data.get("checks", ()), "checks")
        checks: list[QualificationCheck] = []
        for item in raw_checks:
            if not isinstance(item, Mapping):
                raise ContractError("qualification checks must be mappings")
            checks.append(QualificationCheck.from_dict(cast(Mapping[str, object], item)))
        return cls(
            qualification_id=ref(data.get("qualification_id"), "qualification_id"),
            experiment_ref=ref(data.get("experiment_ref"), "experiment_ref"),
            source_profile=ref(data.get("source_profile"), "source_profile"),
            validation_profile_ref=ref(
                data.get("validation_profile_ref"), "validation_profile_ref"
            ),
            batch_ref=ref(data.get("batch_ref"), "batch_ref"),
            worldline_refs=tuple(
                ref(value, "worldline_refs item")
                for value in sequence(data.get("worldline_refs", ()), "worldline_refs")
            ),
            artifact_refs=tuple(
                ref(value, "artifact_refs item")
                for value in sequence(data.get("artifact_refs", ()), "artifact_refs")
            ),
            intervention_refs=tuple(
                ref(value, "intervention_refs item")
                for value in sequence(data.get("intervention_refs", ()), "intervention_refs")
            ),
            comparison_ref=ref(data.get("comparison_ref"), "comparison_ref"),
            checks=tuple(checks),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


__all__ = [
    "LabQualification",
    "QUALIFICATION_SCHEMA_VERSION",
    "QualificationCheck",
    "QualificationStatus",
]
