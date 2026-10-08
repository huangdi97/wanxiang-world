"""World/actor/provider cost admission, alerts, and graceful backpressure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.long_horizon.lod import SimulationLevel

BudgetScope = Literal["world", "actor", "provider"]
AdmissionStatus = Literal["accepted", "degraded", "deferred", "rejected"]
BackpressureAction = Literal["allow", "defer", "reject"]


@dataclass(frozen=True, slots=True)
class BudgetKey:
    scope: BudgetScope
    ref: str

    def __post_init__(self) -> None:
        if self.scope not in ("world", "actor", "provider") or not self.ref:
            raise ContractError("budget key scope/ref is invalid")


@dataclass(frozen=True, slots=True)
class CostLimit:
    max_calls: int = 0
    max_tokens: int = 0
    max_time_ms: int = 0
    max_storage_bytes: int = 0

    def __post_init__(self) -> None:
        for name in ("max_calls", "max_tokens", "max_time_ms", "max_storage_bytes"):
            if getattr(self, name) < 0:
                raise ContractError(f"{name} must be non-negative")


@dataclass(frozen=True, slots=True)
class CostUsage:
    calls: int = 0
    tokens: int = 0
    time_ms: int = 0
    storage_bytes: int = 0

    def __post_init__(self) -> None:
        for name in ("calls", "tokens", "time_ms", "storage_bytes"):
            if getattr(self, name) < 0:
                raise ContractError(f"{name} must be non-negative")

    def plus(self, other: CostUsage) -> CostUsage:
        return CostUsage(
            calls=self.calls + other.calls,
            tokens=self.tokens + other.tokens,
            time_ms=self.time_ms + other.time_ms,
            storage_bytes=self.storage_bytes + other.storage_bytes,
        )


@dataclass(frozen=True, slots=True)
class BudgetAlert:
    key: BudgetKey
    metric: str
    ratio: float
    severity: Literal["warning", "exhausted"]


@dataclass(frozen=True, slots=True)
class BackpressurePolicy:
    soft_queue_limit: int = 8
    hard_queue_limit: int = 16

    def __post_init__(self) -> None:
        if self.soft_queue_limit < 0 or self.hard_queue_limit <= self.soft_queue_limit:
            raise ContractError("backpressure limits must be ordered and non-negative")

    def decide(self, queue_depth: int) -> BackpressureAction:
        if queue_depth < 0:
            raise ContractError("queue_depth must be non-negative")
        if queue_depth >= self.hard_queue_limit:
            return "reject"
        if queue_depth >= self.soft_queue_limit:
            return "defer"
        return "allow"


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    status: AdmissionStatus
    requested_lod: SimulationLevel
    recommended_lod: SimulationLevel | None
    reason: str
    alerts: tuple[BudgetAlert, ...] = ()


@dataclass(slots=True)
class CostBudgetLedger:
    """Atomic multi-scope admission ledger; no state or command mutation."""

    alert_ratio: float = 0.80
    backpressure: BackpressurePolicy = field(default_factory=BackpressurePolicy)
    _limits: dict[BudgetKey, CostLimit] = field(
        init=False, default_factory=dict[BudgetKey, CostLimit]
    )
    _usage: dict[BudgetKey, CostUsage] = field(
        init=False, default_factory=dict[BudgetKey, CostUsage]
    )

    def __post_init__(self) -> None:
        if not 0.0 < self.alert_ratio <= 1.0:
            raise ContractError("alert_ratio must be in (0, 1]")

    def register(self, key: BudgetKey, limit: CostLimit) -> None:
        if key in self._limits:
            raise ContractError(f"budget key {key.scope}:{key.ref} already registered")
        self._limits[key] = limit
        self._usage[key] = CostUsage()

    def usage(self, key: BudgetKey) -> CostUsage:
        self._require(key)
        return self._usage[key]

    def remaining(self, key: BudgetKey) -> CostUsage:
        limit = self._require(key)
        used = self._usage[key]
        return CostUsage(
            calls=limit.max_calls - used.calls,
            tokens=limit.max_tokens - used.tokens,
            time_ms=limit.max_time_ms - used.time_ms,
            storage_bytes=limit.max_storage_bytes - used.storage_bytes,
        )

    def admit(
        self,
        keys: tuple[BudgetKey, ...],
        request: CostUsage,
        *,
        requested_lod: SimulationLevel,
        queue_depth: int = 0,
    ) -> AdmissionDecision:
        if not keys or len(keys) != len(set(keys)):
            raise ContractError("admission requires unique non-empty budget keys")
        for key in keys:
            self._require(key)
        pressure = self.backpressure.decide(queue_depth)
        if pressure == "reject":
            return AdmissionDecision("rejected", requested_lod, None, "hard_backpressure")
        if pressure == "defer":
            return AdmissionDecision("deferred", requested_lod, None, "soft_backpressure")
        if not all(self._fits(key, request) for key in keys):
            recommendation = _next_level(requested_lod)
            if recommendation is not None:
                return AdmissionDecision(
                    "degraded",
                    requested_lod,
                    recommendation,
                    "budget_exhausted;retry_at_lower_lod",
                )
            return AdmissionDecision("rejected", requested_lod, None, "budget_exhausted")
        for key in keys:
            self._usage[key] = self._usage[key].plus(request)
        alerts = tuple(alert for key in keys for alert in self._alerts(key))
        return AdmissionDecision("accepted", requested_lod, requested_lod, "admitted", alerts)

    def _require(self, key: BudgetKey) -> CostLimit:
        limit = self._limits.get(key)
        if limit is None:
            raise ContractError(f"unregistered budget key {key.scope}:{key.ref}")
        return limit

    def _fits(self, key: BudgetKey, request: CostUsage) -> bool:
        limit = self._limits[key]
        used = self._usage[key]
        next_usage = used.plus(request)
        return (
            next_usage.calls <= limit.max_calls
            and next_usage.tokens <= limit.max_tokens
            and next_usage.time_ms <= limit.max_time_ms
            and next_usage.storage_bytes <= limit.max_storage_bytes
        )

    def _alerts(self, key: BudgetKey) -> tuple[BudgetAlert, ...]:
        limit = self._limits[key]
        used = self._usage[key]
        values = (
            ("calls", used.calls, limit.max_calls),
            ("tokens", used.tokens, limit.max_tokens),
            ("time_ms", used.time_ms, limit.max_time_ms),
            ("storage_bytes", used.storage_bytes, limit.max_storage_bytes),
        )
        alerts: list[BudgetAlert] = []
        for metric, amount, maximum in values:
            ratio = amount / maximum if maximum else (1.0 if amount else 0.0)
            if ratio >= self.alert_ratio:
                alerts.append(
                    BudgetAlert(
                        key,
                        metric,
                        ratio,
                        "exhausted" if ratio >= 1.0 else "warning",
                    )
                )
        return tuple(alerts)


def _next_level(level: SimulationLevel) -> SimulationLevel | None:
    levels: tuple[SimulationLevel, ...] = ("L0", "L1", "L2", "L3", "L4")
    index = levels.index(level)
    return levels[index + 1] if index + 1 < len(levels) else None


__all__ = [
    "AdmissionDecision",
    "AdmissionStatus",
    "BackpressurePolicy",
    "BudgetAlert",
    "BudgetKey",
    "BudgetScope",
    "CostLimit",
    "CostUsage",
    "CostBudgetLedger",
]
