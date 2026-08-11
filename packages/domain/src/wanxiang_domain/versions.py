"""Schema and runtime version identifiers.

Every persisted/external contract carries a schema version. Versions are
non-negative integers; incompatible versions produce structured errors.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError


def _validate_non_negative(value: object, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ContractError(f"{name} must be a non-negative integer, got {value!r}")


@dataclass(frozen=True, slots=True)
class SchemaVersion:
    """Version of a persisted/external contract schema."""

    value: int

    def __post_init__(self) -> None:
        _validate_non_negative(self.value, "SchemaVersion")

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class RuntimeVersion:
    """Version of the authoritative runtime/rule implementation."""

    value: int

    def __post_init__(self) -> None:
        _validate_non_negative(self.value, "RuntimeVersion")


@dataclass(frozen=True, slots=True)
class PackageVersion:
    """Version of a domain/world package (definition-plane)."""

    value: int

    def __post_init__(self) -> None:
        _validate_non_negative(self.value, "PackageVersion")
