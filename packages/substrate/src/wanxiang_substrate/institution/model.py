"""Pure institution/authority value objects and invariants (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

DutyState = Literal["pending", "done", "overdue"]


@dataclass(frozen=True, slots=True)
class Role:
    role_id: EntityId
    name: str
    permissions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise ContractError("role name must be non-empty")

    def grants(self, permission: str) -> bool:
        return permission in self.permissions


@dataclass(frozen=True, slots=True)
class Membership:
    membership_id: EntityId
    actor_id: EntityId
    role_id: EntityId
    institution_id: EntityId
    start_ticks: int
    end_ticks: int | None = None

    def __post_init__(self) -> None:
        if self.start_ticks < 0:
            raise ContractError("membership start ticks must be non-negative")
        if self.end_ticks is not None and self.end_ticks < self.start_ticks:
            raise ContractError("membership end ticks must not precede start")

    def is_active_at(self, ticks: int) -> bool:
        return ticks >= self.start_ticks and (self.end_ticks is None or ticks <= self.end_ticks)


@dataclass(frozen=True, slots=True)
class PermissionDecision:
    allow: bool
    permission: str
    target: str
    rule_refs: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class Duty:
    duty_id: EntityId
    actor_id: EntityId
    duty_type: str
    due_ticks: int
    state: DutyState = "pending"

    def __post_init__(self) -> None:
        if self.due_ticks < 0:
            raise ContractError("duty due ticks must be non-negative")
        if not self.duty_type:
            raise ContractError("duty type must be non-empty")


@dataclass(frozen=True, slots=True)
class DelegatedPermission:
    permission_id: EntityId
    actor_id: EntityId
    permission: str
    target: str
    granter_id: EntityId
    start_ticks: int
    end_ticks: int | None = None

    def is_active_at(self, ticks: int) -> bool:
        return ticks >= self.start_ticks and (self.end_ticks is None or ticks <= self.end_ticks)
