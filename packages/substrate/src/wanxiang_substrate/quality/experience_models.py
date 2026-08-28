"""Versioned, evidence-linked Experience Quality records (M97)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from math import isfinite
from typing import Literal, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

EXPERIENCE_QUALITY_SCHEMA = "wanxiang.v5.5.experience-quality.v1"
QUALITY_DIMENSIONS = (
    "Agency",
    "Coherence",
    "CharacterConsistency",
    "ConsequenceVisibility",
    "NarrativeStateAlignment",
    "GoalClarity",
    "WorldReactivity",
    "MemoryQuality",
    "ContinuationQuality",
    "NoveltyRepetition",
)
MeasurementMethod = Literal["invariant_metric", "behavioral_trace", "human_rating", "model_judge"]
MeasurementStatus = Literal["measured", "missing", "not_applicable"]
WorldFamily = Literal["source", "prompt"]
HumanDataStatus = Literal["missing", "provided", "not_required"]
ScientificValidity = Literal["not_assessed", "external_review_required"]


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or any(char.isspace() for char in value):
        raise ContractError(f"{name} must be a non-empty opaque reference")
    return value


def _ref_tuple(values: Sequence[object], name: str) -> tuple[str, ...]:
    result = tuple(_text(value, f"{name} item") for value in values)
    if len(set(result)) != len(result):
        raise ContractError(f"{name} must not contain duplicates")
    return tuple(sorted(result))


@dataclass(frozen=True, slots=True)
class ExperienceMeasurement:
    """One normalized [0,1] measurement and its evidence method."""

    method: MeasurementMethod
    status: MeasurementStatus
    value: float | None = None
    evidence_refs: tuple[str, ...] = ()
    sample_size: int = 0
    scale: str = "normalized_0_1"
    note: str = ""

    def __post_init__(self) -> None:
        if self.method not in {
            "invariant_metric",
            "behavioral_trace",
            "human_rating",
            "model_judge",
        }:
            raise ContractError(f"unsupported ExperienceQuality method {self.method!r}")
        if self.status not in {"measured", "missing", "not_applicable"}:
            raise ContractError(f"unsupported ExperienceQuality status {self.status!r}")
        if not self.scale.strip() or any(char in self.scale for char in "\r\n"):
            raise ContractError("measurement scale must be a single non-empty line")
        if self.note and (len(self.note) > 256 or any(char in self.note for char in "\r\n")):
            raise ContractError("measurement note must be at most 256 single-line characters")
        object.__setattr__(self, "evidence_refs", _ref_tuple(self.evidence_refs, "evidence_refs"))
        if self.status == "measured":
            if self.value is None or not isfinite(self.value) or not 0.0 <= self.value <= 1.0:
                raise ContractError("measured quality value must be finite and within [0,1]")
            if self.sample_size < 1 or not self.evidence_refs:
                raise ContractError("measured quality requires sample_size and evidence_refs")
        elif self.value is not None or self.sample_size != 0:
            raise ContractError("missing or not-applicable quality data cannot carry a value")

    def to_dict(self) -> dict[str, object]:
        return {
            "method": self.method,
            "status": self.status,
            "value": self.value,
            "evidence_refs": list(self.evidence_refs),
            "sample_size": self.sample_size,
            "scale": self.scale,
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class ExperienceDimension:
    """A quality dimension with explicit measured and missing methods."""

    name: str
    measurements: tuple[ExperienceMeasurement, ...]

    def __post_init__(self) -> None:
        if self.name not in QUALITY_DIMENSIONS:
            raise ContractError(f"unknown ExperienceQuality dimension {self.name!r}")
        if not self.measurements:
            raise ContractError("ExperienceQuality dimension requires a measurement")
        methods = tuple(item.method for item in self.measurements)
        if len(set(methods)) != len(methods):
            raise ContractError("ExperienceQuality measurement methods must be unique")

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "measurements": [item.to_dict() for item in self.measurements],
        }


@dataclass(frozen=True, slots=True)
class ExperienceQualityRun:
    """Sanitized per-run quality evidence; canonical state remains referenced."""

    run_id: str
    scenario_id: str
    world_family: WorldFamily
    world_ref: str
    package_ref: str
    scenario_version: str
    build_sha: str
    seed: int
    action_script: tuple[str, ...]
    event_refs: tuple[str, ...]
    state_refs: tuple[str, ...]
    replay_refs: tuple[str, ...]
    dimensions: tuple[ExperienceDimension, ...]
    worldness_ref: str
    scientific_validity: ScientificValidity = "not_assessed"
    human_status: HumanDataStatus = "missing"
    missing_data: tuple[str, ...] = ()
    schema: str = EXPERIENCE_QUALITY_SCHEMA
    sanitized: bool = True
    content_hash: str = ""

    def __post_init__(self) -> None:
        for name in (
            "run_id",
            "scenario_id",
            "world_ref",
            "package_ref",
            "scenario_version",
            "build_sha",
            "worldness_ref",
        ):
            _text(getattr(self, name), name)
        if self.schema != EXPERIENCE_QUALITY_SCHEMA:
            raise ContractError(f"unsupported ExperienceQuality schema {self.schema!r}")
        if type(self.seed) is not int:
            raise ContractError("ExperienceQuality seed must be an integer")
        if self.world_family not in {"source", "prompt"}:
            raise ContractError(f"unsupported world family {self.world_family!r}")
        if self.scientific_validity not in {"not_assessed", "external_review_required"}:
            raise ContractError("invalid scientific validity status")
        if self.human_status not in {"missing", "provided", "not_required"}:
            raise ContractError("invalid human data status")
        if not self.sanitized:
            raise ContractError("ExperienceQualityRun must be sanitized")
        object.__setattr__(self, "action_script", _ref_tuple(self.action_script, "action_script"))
        for name in ("event_refs", "state_refs", "replay_refs", "missing_data"):
            object.__setattr__(self, name, _ref_tuple(getattr(self, name), name))
        names = tuple(item.name for item in self.dimensions)
        if set(names) != set(QUALITY_DIMENSIONS) or len(names) != len(QUALITY_DIMENSIONS):
            raise ContractError("ExperienceQuality run must cover every required dimension once")
        if self.human_status == "missing" and not self.missing_data:
            raise ContractError("missing human data requires explicit missing_data fields")
        if self.content_hash and (
            len(self.content_hash) != 64
            or any(char not in "0123456789abcdef" for char in self.content_hash)
        ):
            raise ContractError("content_hash must be a lowercase SHA-256 digest")

    def canonical_payload(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "run_id": self.run_id,
            "scenario_id": self.scenario_id,
            "world_family": self.world_family,
            "world_ref": self.world_ref,
            "package_ref": self.package_ref,
            "scenario_version": self.scenario_version,
            "build_sha": self.build_sha,
            "seed": self.seed,
            "action_script": list(self.action_script),
            "event_refs": list(self.event_refs),
            "state_refs": list(self.state_refs),
            "replay_refs": list(self.replay_refs),
            "dimensions": [item.to_dict() for item in self.dimensions],
            "worldness_ref": self.worldness_ref,
            "scientific_validity": self.scientific_validity,
            "human_status": self.human_status,
            "missing_data": list(self.missing_data),
            "sanitized": self.sanitized,
        }

    def compute_hash(self) -> str:
        return semantic_sha256(self.canonical_payload())

    def with_hash(self) -> ExperienceQualityRun:
        return replace(self, content_hash=self.compute_hash())

    def verify_hash(self) -> bool:
        return bool(self.content_hash) and self.content_hash == self.compute_hash()

    def to_dict(self) -> dict[str, object]:
        payload = self.canonical_payload()
        payload["content_hash"] = self.content_hash
        return payload


def measurement_from_dict(data: Mapping[str, object]) -> ExperienceMeasurement:
    method = data.get("method")
    status = data.get("status")
    if method not in {"invariant_metric", "behavioral_trace", "human_rating", "model_judge"}:
        raise ContractError("invalid measurement method")
    if status not in {"measured", "missing", "not_applicable"}:
        raise ContractError("invalid measurement status")
    value = data.get("value")
    if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool)):
        raise ContractError("measurement value must be numeric or null")
    refs = data.get("evidence_refs", ())
    if not isinstance(refs, (list, tuple)):
        raise ContractError("evidence_refs must be a list")
    raw_refs = cast(list[object] | tuple[object, ...], refs)
    raw_sample_size = data.get("sample_size", 0)
    if not isinstance(raw_sample_size, int) or isinstance(raw_sample_size, bool):
        raise ContractError("sample_size must be an integer")
    return ExperienceMeasurement(
        cast(MeasurementMethod, method),
        cast(MeasurementStatus, status),
        float(value) if value is not None else None,
        tuple(str(item) for item in raw_refs),
        raw_sample_size,
        str(data.get("scale", "normalized_0_1")),
        str(data.get("note", "")),
    )


__all__ = [
    "EXPERIENCE_QUALITY_SCHEMA",
    "QUALITY_DIMENSIONS",
    "ExperienceDimension",
    "ExperienceMeasurement",
    "ExperienceQualityRun",
    "HumanDataStatus",
    "MeasurementMethod",
    "MeasurementStatus",
    "ScientificValidity",
    "WorldFamily",
    "measurement_from_dict",
]
