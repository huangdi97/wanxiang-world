"""Pure agency value objects: intent candidates, orders, reports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

OrderState = Literal["issued", "received", "accepted", "rejected", "executed", "reported"]
VALID_ORDER_STATES = ("issued", "received", "accepted", "rejected", "executed", "reported")


@dataclass(frozen=True, slots=True)
class IntentCandidate:
    """A policy's propose-only output (never a mutation)."""

    actor_id: EntityId
    action_type: str
    payload: dict[str, FieldValue]
    priority: int = 0
    policy_ref: str = ""

    def __post_init__(self) -> None:
        if not self.action_type:
            raise ContractError("intent action_type must be non-empty")


@dataclass(frozen=True, slots=True)
class ExecutionReport:
    order_id: EntityId
    executor_id: EntityId
    executed_ticks: int
    outcome: str
    deviation: str | None = None

    def __post_init__(self) -> None:
        if not self.outcome:
            raise ContractError("execution report outcome must be non-empty")


@dataclass(frozen=True, slots=True)
class Order:
    order_id: EntityId
    issuer_id: EntityId
    receiver_id: EntityId
    action_type: str
    payload: dict[str, FieldValue]
    state: OrderState = "issued"
    deviation: str | None = None

    def __post_init__(self) -> None:
        if not self.action_type:
            raise ContractError("order action_type must be non-empty")
        if self.state not in VALID_ORDER_STATES:
            raise ContractError(f"invalid order state {self.state!r}")

    def can_transition_to(self, next_state: OrderState) -> bool:
        allowed: dict[OrderState, tuple[OrderState, ...]] = {
            "issued": ("received",),
            "received": ("accepted", "rejected"),
            "accepted": ("executed",),
            "executed": ("reported",),
            "rejected": (),
            "reported": (),
        }
        return next_state in allowed.get(self.state, ())
