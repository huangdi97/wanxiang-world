"""External engine capability port with honest unavailable semantics (M93/G96F)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, Protocol, cast, runtime_checkable

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.registry_support import integer, names, ref, sequence

EXTERNAL_ENGINE_SCHEMA_VERSION = 1
ExternalEngineAvailability = Literal["available", "unavailable", "external_blocked"]
ExternalEngineKind = Literal["renderer", "physics", "visual", "unknown"]
_AVAILABILITIES = frozenset({"available", "unavailable", "external_blocked"})
_KINDS = frozenset({"renderer", "physics", "visual", "unknown"})


def _value(value: object, name: str, allowed: frozenset[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise ContractError(f"unsupported {name} {value!r}")
    return value


@dataclass(frozen=True, slots=True)
class ExternalEngineCapability:
    """Versioned discovery result; blocked is evidence, never a successful run."""

    engine_id: str
    engine_kind: ExternalEngineKind
    availability: ExternalEngineAvailability
    available: bool
    version: str = ""
    capabilities: tuple[str, ...] = ()
    deterministic: bool = False
    reason: str = ""
    schema_version: int = EXTERNAL_ENGINE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.engine_id, "engine_id")
        _value(self.engine_kind, "engine kind", _KINDS)
        status = _value(self.availability, "engine availability", _AVAILABILITIES)
        if type(self.available) is not bool or type(self.deterministic) is not bool:
            raise ContractError("engine availability and determinism must be boolean")
        if (status == "available") != self.available:
            raise ContractError("engine availability does not match available flag")
        if status == "available":
            ref(self.version, "engine version")
        elif self.version and any(char.isspace() for char in self.version):
            raise ContractError("engine version must not contain whitespace")
        if status != "available" and not self.reason.strip():
            raise ContractError("unavailable engine capability requires a reason")
        if "\n" in self.reason or "\r" in self.reason:
            raise ContractError("engine reason must be one-line text")
        if self.schema_version != EXTERNAL_ENGINE_SCHEMA_VERSION:
            raise ContractError("unsupported external engine capability schema")
        object.__setattr__(self, "capabilities", names(self.capabilities, "capabilities"))

    @property
    def external_blocked(self) -> bool:
        return self.availability == "external_blocked"

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "engine_id": self.engine_id,
            "engine_kind": self.engine_kind,
            "availability": self.availability,
            "available": self.available,
            "version": self.version,
            "capabilities": list(self.capabilities),
            "deterministic": self.deterministic,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ExternalEngineCapability:
        availability = _value(data.get("availability"), "engine availability", _AVAILABILITIES)
        kind = _value(data.get("engine_kind"), "engine kind", _KINDS)
        version = data.get("version", "")
        reason = data.get("reason", "")
        if not isinstance(version, str) or not isinstance(reason, str):
            raise ContractError("engine version and reason must be text")
        return cls(
            engine_id=ref(data.get("engine_id"), "engine_id"),
            engine_kind=cast(ExternalEngineKind, kind),
            availability=cast(ExternalEngineAvailability, availability),
            available=data.get("available"),  # type: ignore[arg-type]
            version=version,
            capabilities=tuple(
                ref(value, "capabilities item")
                for value in sequence(data.get("capabilities", ()), "capabilities")
            ),
            deterministic=data.get("deterministic", False),  # type: ignore[arg-type]
            reason=reason,
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@runtime_checkable
class ExternalEngineAdapter(Protocol):
    """Discovery-only port; execution adapters remain non-authoritative."""

    def discover(self) -> ExternalEngineCapability: ...


@dataclass(frozen=True, slots=True)
class BlockedExternalEngineAdapter:
    """Honest local diagnostic for an engine absent from the current environment."""

    engine_id: str
    engine_kind: ExternalEngineKind
    reason: str = "external engine runtime is not available in this environment"

    def __post_init__(self) -> None:
        ref(self.engine_id, "engine_id")
        _value(self.engine_kind, "engine kind", _KINDS)
        if not self.reason.strip() or "\n" in self.reason or "\r" in self.reason:
            raise ContractError("blocked engine reason must be non-empty one-line text")

    def discover(self) -> ExternalEngineCapability:
        return ExternalEngineCapability(
            engine_id=self.engine_id,
            engine_kind=self.engine_kind,
            availability="external_blocked",
            available=False,
            reason=self.reason,
        )


__all__ = [
    "BlockedExternalEngineAdapter",
    "EXTERNAL_ENGINE_SCHEMA_VERSION",
    "ExternalEngineAdapter",
    "ExternalEngineAvailability",
    "ExternalEngineCapability",
    "ExternalEngineKind",
]
