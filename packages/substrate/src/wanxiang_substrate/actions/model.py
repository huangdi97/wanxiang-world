"""Pure action/affordance value objects (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

ParamType = Literal["str", "int", "float", "bool"]


@dataclass(frozen=True, slots=True)
class ParameterSpec:
    name: str
    type: ParamType
    required: bool = True

    def __post_init__(self) -> None:
        if not self.name:
            raise ContractError("parameter name must be non-empty")
        if self.type not in ("str", "int", "float", "bool"):
            raise ContractError(f"invalid parameter type {self.type!r}")


@dataclass(frozen=True, slots=True)
class ActionDefinition:
    action_type: str
    version: int
    parameters: tuple[ParameterSpec, ...]
    permission: str | None = None
    resource_cost: int | None = None
    requires_actor: bool = True
    description: str = ""

    def __post_init__(self) -> None:
        if not self.action_type:
            raise ContractError("action_type must be non-empty")
        if self.version <= 0:
            raise ContractError("action version must be positive")

    def parameter(self, name: str) -> ParameterSpec | None:
        for spec in self.parameters:
            if spec.name == name:
                return spec
        return None


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str

    def to_primitive(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


@dataclass(frozen=True, slots=True)
class ValidationResult:
    ok: bool
    issues: tuple[ValidationIssue, ...] = ()

    @classmethod
    def success(cls) -> ValidationResult:
        return cls(ok=True)

    @classmethod
    def failure(cls, issues: tuple[ValidationIssue, ...]) -> ValidationResult:
        return cls(ok=False, issues=issues)
