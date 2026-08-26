"""Shared metadata and deterministic encoding for typed evolution records."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import ClassVar, Literal, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.ids import EntityId

EVOLUTION_DELTA_SCHEMA_VERSION = 1
EvolutionDeltaKind = Literal[
    "state", "belief", "relationship", "capability", "persona", "organization"
]
EvolutionOrigin = Literal[
    "world_event",
    "belief_evidence",
    "relationship_event",
    "capability_evidence",
    "persona_review",
    "organization_event",
]
type PrimitiveValue = str | int | float | bool | None
BeliefOperation = Literal["support", "contradict", "refine", "unknown"]
BeliefStance = Literal["supported", "contested", "unknown"]
OrganizationLifecycle = Literal["formed", "joined", "left", "role_changed", "dissolved"]


def text(value: str, field: str) -> None:
    if type(value) is not str or not value.strip():
        raise ContractError(f"{field} must be non-empty")


def refs(values: tuple[str, ...], field: str) -> None:
    if any(type(value) is not str or not value.strip() for value in values):
        raise ContractError(f"{field} cannot contain blank refs")
    if len(set(values)) != len(values):
        raise ContractError(f"{field} must be unique")


def level(value: float, field: str, *, low: float = 0.0, high: float = 1.0) -> None:
    if type(value) not in (int, float):
        raise ContractError(f"{field} must be numeric")
    if not low <= float(value) <= high:
        raise ContractError(f"{field} must be within [{low}, {high}]")


@dataclass(frozen=True, slots=True)
class EvolutionProvenance:
    """Evidence lineage attached to every evolution proposal."""

    origin_ref: str
    source_refs: tuple[str, ...] = ()
    event_refs: tuple[str, ...] = ()
    producer: str = "substrate"

    def __post_init__(self) -> None:
        text(self.origin_ref, "origin_ref")
        text(self.producer, "producer")
        refs(self.source_refs, "source_refs")
        refs(self.event_refs, "event_refs")

    def to_dict(self) -> dict[str, object]:
        return {
            "origin_ref": self.origin_ref,
            "source_refs": list(self.source_refs),
            "event_refs": list(self.event_refs),
            "producer": self.producer,
        }


@dataclass(frozen=True, slots=True)
class DeltaRecord:
    """Common identity behavior; every concrete payload stays explicitly typed."""

    kind: ClassVar[EvolutionDeltaKind]

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {}
        for item in fields(self):
            value = getattr(self, item.name)
            if isinstance(value, EntityId):
                result[item.name] = value.value
            elif isinstance(value, EvolutionProvenance):
                result[item.name] = value.to_dict()
            elif isinstance(value, tuple):
                result[item.name] = list(cast(tuple[object, ...], value))
            else:
                result[item.name] = value
        result["kind"] = self.kind
        return result

    def fingerprint(self) -> str:
        return semantic_sha256(self.to_dict())


def common_checks(
    delta_id: str,
    schema_version: int,
    version: int,
    provenance: EvolutionProvenance,
) -> None:
    text(delta_id, "delta_id")
    if schema_version != EVOLUTION_DELTA_SCHEMA_VERSION:
        raise ContractError(
            f"unsupported evolution delta schema {schema_version}; "
            f"expected {EVOLUTION_DELTA_SCHEMA_VERSION}"
        )
    if type(schema_version) is not int:
        raise ContractError("evolution delta schema version must be an integer")
    if type(version) is not int or version < 1:
        raise ContractError("evolution delta version must be positive")
