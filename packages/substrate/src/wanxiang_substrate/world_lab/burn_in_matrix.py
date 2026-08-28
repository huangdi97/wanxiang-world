"""Versioned M98 burn-in run matrix (G101A).

The matrix is an experiment definition only. It does not own a world, event
history, branch, or commit authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Literal, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

M98_MATRIX_SCHEMA = "wanxiang.v5.5.m98-burn-in-matrix.v1"
BurnInHorizon = Literal["30d", "90d"]
PolicyProfile = Literal["baseline", "conservative"]
PressureProfile = Literal["low", "high", "baseline", "stress"]


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or any(char.isspace() for char in value):
        raise ContractError(f"{name} must be a non-empty opaque reference")
    return value


@dataclass(frozen=True, slots=True)
class BurnInRunSpec:
    """One declared, reproducible worldline row."""

    run_id: str
    horizon: BurnInHorizon
    seed: int
    policy_profile: PolicyProfile
    pressure_profile: PressureProfile

    def __post_init__(self) -> None:
        _text(self.run_id, "run_id")
        if self.horizon not in ("30d", "90d"):
            raise ContractError("unsupported burn-in horizon")
        if type(self.seed) is not int or self.seed < 1:
            raise ContractError("burn-in seed must be a positive integer")
        if self.policy_profile not in ("baseline", "conservative"):
            raise ContractError("unsupported policy profile")
        if self.pressure_profile not in ("low", "high", "baseline", "stress"):
            raise ContractError("unsupported pressure profile")
        if self.horizon == "30d" and self.pressure_profile not in ("low", "high"):
            raise ContractError("30d rows require low/high pressure profiles")
        if self.horizon == "90d" and self.pressure_profile not in ("baseline", "stress"):
            raise ContractError("90d rows require baseline/stress pressure profiles")
        if self.horizon == "90d" and self.policy_profile != "baseline":
            raise ContractError("90d rows use the declared baseline policy")

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "horizon": self.horizon,
            "seed": self.seed,
            "policy_profile": self.policy_profile,
            "pressure_profile": self.pressure_profile,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> BurnInRunSpec:
        horizon = data.get("horizon")
        policy = data.get("policy_profile")
        pressure = data.get("pressure_profile")
        if not isinstance(horizon, str) or horizon not in ("30d", "90d"):
            raise ContractError("invalid burn-in horizon")
        if not isinstance(policy, str) or policy not in ("baseline", "conservative"):
            raise ContractError("invalid burn-in policy")
        if not isinstance(pressure, str) or pressure not in (
            "low",
            "high",
            "baseline",
            "stress",
        ):
            raise ContractError("invalid burn-in pressure")
        seed = data.get("seed")
        if type(seed) is not int:
            raise ContractError("invalid burn-in seed")
        return cls(
            run_id=_text(data.get("run_id"), "run_id"),
            horizon=horizon,
            seed=seed,
            policy_profile=policy,
            pressure_profile=pressure,
        )


@dataclass(frozen=True, slots=True)
class BurnInMatrix:
    """Complete M98 declaration with a verifiable content hash."""

    matrix_id: str
    world_package_ref: str
    scenario_ref: str
    rows: tuple[BurnInRunSpec, ...]
    schema: str = M98_MATRIX_SCHEMA
    content_hash: str = ""

    def __post_init__(self) -> None:
        _text(self.matrix_id, "matrix_id")
        _text(self.world_package_ref, "world_package_ref")
        _text(self.scenario_ref, "scenario_ref")
        if self.schema != M98_MATRIX_SCHEMA:
            raise ContractError("unsupported M98 matrix schema")
        if not self.rows:
            raise ContractError("M98 matrix requires rows")
        ids = tuple(row.run_id for row in self.rows)
        if len(ids) != len(set(ids)):
            raise ContractError("M98 matrix run ids must be unique")
        self._validate_shape()
        if self.content_hash and (
            len(self.content_hash) != 64
            or any(char not in "0123456789abcdef" for char in self.content_hash)
        ):
            raise ContractError("matrix content_hash must be lowercase SHA-256")

    def _validate_shape(self) -> None:
        thirty = tuple(row for row in self.rows if row.horizon == "30d")
        ninety = tuple(row for row in self.rows if row.horizon == "90d")
        if len(thirty) != 12 or len(ninety) != 6:
            raise ContractError("M98 matrix must contain 12 30d and 6 90d rows")
        if {(row.seed, row.policy_profile, row.pressure_profile) for row in thirty} != {
            (seed, policy, pressure)
            for seed in (9801, 9802, 9803)
            for policy in ("baseline", "conservative")
            for pressure in ("low", "high")
        }:
            raise ContractError("30d M98 matrix does not cover the declared factorial")
        if {(row.seed, row.policy_profile, row.pressure_profile) for row in ninety} != {
            (seed, "baseline", pressure)
            for seed in (9811, 9812, 9813)
            for pressure in ("baseline", "stress")
        }:
            raise ContractError("90d M98 matrix does not cover the declared subset")

    def canonical_payload(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "matrix_id": self.matrix_id,
            "world_package_ref": self.world_package_ref,
            "scenario_ref": self.scenario_ref,
            "rows": [row.to_dict() for row in self.rows],
        }

    def compute_hash(self) -> str:
        return semantic_sha256(self.canonical_payload())

    def with_hash(self) -> BurnInMatrix:
        return replace(self, content_hash=self.compute_hash())

    def verify_hash(self) -> bool:
        return bool(self.content_hash) and self.content_hash == self.compute_hash()

    def to_dict(self) -> dict[str, object]:
        payload = self.canonical_payload()
        payload["content_hash"] = self.content_hash
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> BurnInMatrix:
        schema = data.get("schema")
        rows_value = data.get("rows")
        if schema != M98_MATRIX_SCHEMA or not isinstance(rows_value, list):
            raise ContractError("invalid M98 matrix export")
        rows: list[object] = cast(list[object], rows_value)
        parsed = tuple(
            BurnInRunSpec.from_dict(cast(Mapping[str, object], item))
            for item in rows
            if isinstance(item, Mapping)
        )
        if len(parsed) != len(rows):
            raise ContractError("M98 matrix rows must be objects")
        matrix = cls(
            matrix_id=_text(data.get("matrix_id"), "matrix_id"),
            world_package_ref=_text(data.get("world_package_ref"), "world_package_ref"),
            scenario_ref=_text(data.get("scenario_ref"), "scenario_ref"),
            rows=parsed,
            schema=cast(str, schema),
            content_hash=_text(data.get("content_hash"), "content_hash"),
        )
        if not matrix.verify_hash():
            raise ContractError("M98 matrix content hash does not verify")
        return matrix


def stable_m98_matrix() -> BurnInMatrix:
    """Return the frozen 18-row Stable certification matrix."""
    rows = [
        BurnInRunSpec(
            run_id=f"m98-30d-s{seed}-{policy}-{pressure}",
            horizon="30d",
            seed=seed,
            policy_profile=policy,
            pressure_profile=pressure,
        )
        for seed in (9801, 9802, 9803)
        for policy in ("baseline", "conservative")
        for pressure in ("low", "high")
    ]
    rows.extend(
        BurnInRunSpec(
            run_id=f"m98-90d-s{seed}-{pressure}",
            horizon="90d",
            seed=seed,
            policy_profile="baseline",
            pressure_profile=pressure,
        )
        for seed in (9811, 9812, 9813)
        for pressure in ("baseline", "stress")
    )
    return BurnInMatrix(
        matrix_id="matrix:m98:stable-burn-in:v1",
        world_package_ref="qualification:m98:creator-owned-synthetic-source:v1",
        scenario_ref="scenario:m98:standard-burn-in:v1",
        rows=tuple(rows),
    ).with_hash()


__all__ = [
    "BurnInHorizon",
    "BurnInMatrix",
    "BurnInRunSpec",
    "M98_MATRIX_SCHEMA",
    "PolicyProfile",
    "PressureProfile",
    "stable_m98_matrix",
]
