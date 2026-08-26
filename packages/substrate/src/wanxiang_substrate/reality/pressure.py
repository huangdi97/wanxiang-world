"""Composable world-pressure profile (M88 / G91A).

Pressure is a Scenario/Domain capability.  This value object describes inputs
that a world may expose to actors; it is not canonical state, an actor goal, or
an instruction to the director.  The profile carries only versioned data and
provenance so callers can persist or compare it without adding a kernel type.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

PRESSURE_PROFILE_SCHEMA_VERSION: Final = 1
PRESSURE_DIMENSIONS: Final = (
    "scarcity",
    "goals",
    "private_information",
    "obligation",
    "authority",
    "reward",
    "sanction",
    "reputation",
    "time",
    "risk",
    "norm",
)


def _text(value: object, field: str, *, default: str = "") -> str:
    if value is None and default:
        return default
    if not isinstance(value, str) or not value:
        raise ContractError(f"{field} must be a non-empty string")
    return value


def _version(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ContractError(f"{field} must be a positive integer")
    return value


def _level(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{field} must be numeric")
    level = float(value)
    if not math.isfinite(level) or not 0.0 <= level <= 1.0:
        raise ContractError(f"{field} must be finite and within [0,1]")
    return level


def _refs(value: object, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ContractError(f"{field} must be a list of strings")
    items = cast(list[object] | tuple[object, ...], value)
    result = tuple(_text(item, field) for item in items)
    return tuple(dict.fromkeys(result))


@dataclass(frozen=True, slots=True)
class PressureProfile:
    """Schema-versioned pressure inputs for one Scenario/Domain context."""

    profile_id: str
    scenario_ref: str = "default-scenario"
    domain_ref: str = "default-domain"
    scarcity: float = 0.0
    goals: float = 0.0
    private_information: float = 0.0
    obligation: float = 0.0
    authority: float = 0.0
    reward: float = 0.0
    sanction: float = 0.0
    reputation: float = 0.0
    time: float = 0.0
    risk: float = 0.0
    norm: float = 0.0
    source_refs: tuple[str, ...] = ()
    schema_version: int = PRESSURE_PROFILE_SCHEMA_VERSION
    version: int = 1

    def __post_init__(self) -> None:
        _text(self.profile_id, "profile_id")
        _text(self.scenario_ref, "scenario_ref")
        _text(self.domain_ref, "domain_ref")
        if self.schema_version != PRESSURE_PROFILE_SCHEMA_VERSION:
            raise ContractError(
                f"unsupported pressure profile schema {self.schema_version}; "
                f"expected {PRESSURE_PROFILE_SCHEMA_VERSION}"
            )
        _version(self.version, "version")
        for dimension in PRESSURE_DIMENSIONS:
            _level(getattr(self, dimension), dimension)
        object.__setattr__(self, "source_refs", _refs(self.source_refs, "source_refs"))

    @property
    def goal_pressure(self) -> float:
        """Readable alias for integrations that call the dimension goal pressure."""

        return self.goals

    def dimensions(self) -> dict[str, float]:
        """Return a detached, stable map of all pressure dimensions."""

        return {dimension: float(getattr(self, dimension)) for dimension in PRESSURE_DIMENSIONS}

    def to_dict(self) -> dict[str, object]:
        """Serialize the profile without losing schema or provenance."""

        return {
            "profile_id": self.profile_id,
            "scenario_ref": self.scenario_ref,
            "domain_ref": self.domain_ref,
            "dimensions": self.dimensions(),
            "source_refs": list(self.source_refs),
            "schema_version": self.schema_version,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PressureProfile:
        """Read v1 and the flat v0 draft shape; always write the v1 shape."""

        raw_data: dict[str, object] = dict(data)
        raw_dimensions_value = raw_data.get("dimensions", raw_data)
        if not isinstance(raw_dimensions_value, Mapping):
            raise ContractError("pressure profile dimensions must be an object")
        raw_dimensions = cast(Mapping[str, object], raw_dimensions_value)
        values: dict[str, object] = {}
        for dimension in PRESSURE_DIMENSIONS:
            key = dimension
            if dimension == "goals" and key not in raw_dimensions:
                key = "goal_pressure"
            values[dimension] = raw_dimensions.get(key, 0.0)
        return cls(
            profile_id=_text(raw_data.get("profile_id"), "profile_id"),
            scenario_ref=_text(
                raw_data.get("scenario_ref"), "scenario_ref", default="default-scenario"
            ),
            domain_ref=_text(raw_data.get("domain_ref"), "domain_ref", default="default-domain"),
            **{
                dimension: _level(values[dimension], dimension) for dimension in PRESSURE_DIMENSIONS
            },
            source_refs=_refs(raw_data.get("source_refs"), "source_refs"),
            schema_version=PRESSURE_PROFILE_SCHEMA_VERSION,
            version=_version(raw_data.get("version", 1), "version"),
        )

    def fingerprint(self) -> str:
        """Return a deterministic content identity for evidence and comparisons."""

        return semantic_sha256(self.to_dict())

    def distance(self, other: PressureProfile) -> float:
        """Return normalized Manhattan distance across the shared dimensions."""

        return sum(
            abs(self_value - other_value)
            for self_value, other_value in zip(
                self.dimensions().values(), other.dimensions().values(), strict=True
            )
        ) / len(PRESSURE_DIMENSIONS)

    def without_pressure(self, *, profile_id: str | None = None) -> PressureProfile:
        """Create the matched zero-pressure comparison profile."""

        return PressureProfile(
            profile_id=profile_id or f"{self.profile_id}:baseline",
            scenario_ref=self.scenario_ref,
            domain_ref=self.domain_ref,
            source_refs=self.source_refs,
            schema_version=self.schema_version,
            version=self.version,
        )
