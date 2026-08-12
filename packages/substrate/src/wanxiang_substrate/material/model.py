"""Pure material value objects and invariants (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

ItemState = Literal["intact", "damaged", "consumed"]
DamageState = Literal["none", "damaged", "destroyed"]
PayloadState = Literal["sealed", "read"]


@dataclass(frozen=True, slots=True)
class MaterialItem:
    item_id: EntityId
    kind: str
    state: ItemState = "intact"

    def __post_init__(self) -> None:
        if not self.kind:
            raise ContractError("item kind must be non-empty")
        if self.state not in ("intact", "damaged", "consumed"):
            raise ContractError(f"invalid item state {self.state!r}")


@dataclass(frozen=True, slots=True)
class ContainerSpec:
    container_id: EntityId
    capacity: int
    accepts_kinds: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ContractError("container capacity must be positive")

    def accepts(self, kind: str) -> bool:
        return not self.accepts_kinds or kind in self.accepts_kinds


@dataclass(frozen=True, slots=True)
class Custody:
    item_id: EntityId
    custodian_id: EntityId


@dataclass(frozen=True, slots=True)
class Ownership:
    item_id: EntityId
    owner_id: EntityId


@dataclass(frozen=True, slots=True)
class Containment:
    item_id: EntityId
    container_id: EntityId


@dataclass(frozen=True, slots=True)
class InfoPayload:
    item_id: EntityId
    payload_ref: str
    state: PayloadState = "sealed"
    readers: tuple[EntityId, ...] = ()

    def __post_init__(self) -> None:
        if not self.payload_ref:
            raise ContractError("payload_ref must be non-empty")
        if self.state not in ("sealed", "read"):
            raise ContractError(f"invalid payload state {self.state!r}")
