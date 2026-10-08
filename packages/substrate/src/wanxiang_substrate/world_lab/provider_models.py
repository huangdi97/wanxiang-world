"""Versioned multi-provider assignment and sanitized run evidence (G95E)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.world_lab.registry_support import (
    integer,
    names,
    parameters,
    ref,
    sequence,
)

PROVIDER_SCHEMA_VERSION = 1
AssignmentMode = Literal["homogeneous", "round_robin", "explicit"]
_ASSIGNMENT_MODES: frozenset[str] = frozenset({"homogeneous", "round_robin", "explicit"})


def _ordered_refs(values: Sequence[object], name: str) -> tuple[str, ...]:
    result = tuple(ref(value, f"{name} item") for value in values)
    if len(result) != len(set(result)):
        raise ContractError(f"{name} must not contain duplicates")
    return result


def _version(value: object, name: str) -> str:
    return ref(value, name)


@dataclass(frozen=True, slots=True)
class ProviderAssignmentPolicy:
    """Immutable, deterministic provider assignment for one population."""

    policy_id: str
    version: int
    mode: AssignmentMode
    provider_ids: tuple[str, ...]
    explicit_assignments: tuple[tuple[str, str], ...] = ()
    schema_version: int = PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.policy_id, "policy_id")
        integer(self.version, "version", minimum=1)
        if self.mode not in _ASSIGNMENT_MODES:
            raise ContractError(f"unsupported provider assignment mode {self.mode!r}")
        if self.schema_version != PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported provider assignment policy schema")
        providers = names(self.provider_ids, "provider_ids")
        if not providers:
            raise ContractError("provider assignment policy requires providers")
        if self.mode == "homogeneous" and len(providers) != 1:
            raise ContractError("homogeneous policy requires exactly one provider")
        assignments = _pairs(self.explicit_assignments, "explicit_assignments")
        if self.mode != "explicit" and assignments:
            raise ContractError("only explicit policy may declare member assignments")
        if any(provider not in providers for _member, provider in assignments):
            raise ContractError("explicit assignment references an unknown provider")
        object.__setattr__(self, "provider_ids", providers)
        object.__setattr__(self, "explicit_assignments", assignments)

    def assign(self, member_refs: Sequence[str]) -> tuple[ProviderAssignment, ...]:
        """Resolve every member without randomness or provider-side state."""
        members = _ordered_refs(member_refs, "member_refs")
        if not members:
            raise ContractError("provider assignment requires a non-empty population")
        explicit = dict(self.explicit_assignments)
        assignments: list[ProviderAssignment] = []
        for index, member_ref in enumerate(members):
            if self.mode == "homogeneous":
                provider_id = self.provider_ids[0]
            elif self.mode == "round_robin":
                provider_id = self.provider_ids[index % len(self.provider_ids)]
            else:
                provider_id = explicit.get(member_ref, "")
                if not provider_id:
                    raise ContractError(f"explicit policy has no provider for {member_ref!r}")
            assignments.append(
                ProviderAssignment(
                    member_ref=member_ref,
                    provider_id=provider_id,
                    policy_id=self.policy_id,
                    policy_version=self.version,
                )
            )
        return tuple(assignments)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "policy_id": self.policy_id,
            "version": self.version,
            "mode": self.mode,
            "provider_ids": list(self.provider_ids),
            "explicit_assignments": [list(item) for item in self.explicit_assignments],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ProviderAssignmentPolicy:
        mode = data.get("mode")
        if not isinstance(mode, str) or mode not in _ASSIGNMENT_MODES:
            raise ContractError("invalid provider assignment mode")
        return cls(
            policy_id=ref(data.get("policy_id"), "policy_id"),
            version=integer(data.get("version"), "version", minimum=1),
            mode=cast(AssignmentMode, mode),
            provider_ids=names(
                sequence(data.get("provider_ids", ()), "provider_ids"), "provider_ids"
            ),
            explicit_assignments=_pairs(
                sequence(data.get("explicit_assignments", ()), "explicit_assignments"),
                "explicit_assignments",
            ),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class ProviderAssignment:
    """Resolved member-to-provider mapping carried into a provider invocation."""

    member_ref: str
    provider_id: str
    policy_id: str
    policy_version: int

    def __post_init__(self) -> None:
        ref(self.member_ref, "member_ref")
        ref(self.provider_id, "provider_id")
        ref(self.policy_id, "policy_id")
        integer(self.policy_version, "policy_version", minimum=1)


@dataclass(frozen=True, slots=True)
class ProviderRunInput:
    """Same world input sent to every assigned provider; payload is never exported."""

    run_id: str
    world_package_ref: str
    world_package_version: str
    scenario_ref: str
    scenario_version: str
    source_refs: tuple[str, ...]
    population_refs: tuple[str, ...]
    seed: int
    parameters: tuple[tuple[str, object], ...]
    payload: str
    private_source: bool = False
    control_timestamp: str = ""
    schema_version: int = PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in (
            "run_id",
            "world_package_ref",
            "scenario_ref",
        ):
            ref(getattr(self, name), name)
        for name in ("world_package_version", "scenario_version"):
            _version(getattr(self, name), name)
        if type(self.seed) is not int:
            raise ContractError("seed must be an integer")
        if type(self.payload) is not str or not self.payload:
            raise ContractError("provider run input requires a payload")
        if type(self.private_source) is not bool:
            raise ContractError("private_source must be boolean")
        if not self.control_timestamp:
            raise ContractError("provider run input requires a control timestamp")
        if self.schema_version != PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported provider run input schema")
        object.__setattr__(self, "source_refs", _ordered_refs(self.source_refs, "source_refs"))
        object.__setattr__(
            self,
            "population_refs",
            _ordered_refs(self.population_refs, "population_refs"),
        )
        object.__setattr__(self, "parameters", parameters(self.parameters, "parameters"))

    @property
    def input_hash(self) -> str:
        return semantic_sha256(
            {
                "schema_version": self.schema_version,
                "world_package_ref": self.world_package_ref,
                "world_package_version": self.world_package_version,
                "scenario_ref": self.scenario_ref,
                "scenario_version": self.scenario_version,
                "source_refs": self.source_refs,
                "population_refs": self.population_refs,
                "seed": self.seed,
                "parameters": self.parameters,
                "payload": self.payload,
                "private_source": self.private_source,
            }
        )

    def to_dict(self) -> dict[str, object]:
        """Export references and a digest only; never export source payload."""
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "world_package_ref": self.world_package_ref,
            "world_package_version": self.world_package_version,
            "scenario_ref": self.scenario_ref,
            "scenario_version": self.scenario_version,
            "source_refs": list(self.source_refs),
            "population_refs": list(self.population_refs),
            "seed": self.seed,
            "parameters": [list(item) for item in self.parameters],
            "input_hash": self.input_hash,
            "private_source": self.private_source,
            "payload_redacted": True,
        }


def _pairs(values: Sequence[object], name: str) -> tuple[tuple[str, str], ...]:
    result: list[tuple[str, str]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError(f"{name} items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError(f"{name} items must be pairs")
        result.append((ref(pair[0], f"{name} member"), ref(pair[1], f"{name} provider")))
    if len({member for member, _provider in result}) != len(result):
        raise ContractError(f"{name} members must be unique")
    return tuple(sorted(result))


__all__ = [
    "AssignmentMode",
    "PROVIDER_SCHEMA_VERSION",
    "ProviderAssignment",
    "ProviderAssignmentPolicy",
    "ProviderRunInput",
]
