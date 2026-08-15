"""Canonical Replay / Soft Canon / Living Open strategies (G36G).

Three world-run policies: canonical_replay (facts locked to canon), soft_canon
(facts may drift but an attractor pulls toward canon under conditions), and
living_open (full freedom, baseline comparison reports divergence). Canon locks
are immutable: a locked fact rejects mutation. Open branches compare against a
baseline hash. Pure; no write path.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

WorldStrategy = Literal["canonical_replay", "soft_canon", "living_open"]
VALID_STRATEGIES = ("canonical_replay", "soft_canon", "living_open")


@dataclass(frozen=True, slots=True)
class StrategyConfig:
    """One run policy: strategy + canon lock depth + soft attractor + baseline."""

    strategy: WorldStrategy
    canon_lock_depth: int = 0
    soft_attractor: str | None = None
    branch_baseline_ref: str | None = None

    def __post_init__(self) -> None:
        if self.strategy not in VALID_STRATEGIES:
            raise ContractError(f"invalid strategy {self.strategy!r}")
        if self.canon_lock_depth < 0:
            raise ContractError("canon_lock_depth must be non-negative")


def strategy_for(name: WorldStrategy, *, baseline_ref: str | None = None) -> StrategyConfig:
    """Resolve the three strategy policy configs."""
    if name == "canonical_replay":
        return StrategyConfig(
            strategy="canonical_replay", canon_lock_depth=1, branch_baseline_ref=baseline_ref
        )
    if name == "soft_canon":
        return StrategyConfig(
            strategy="soft_canon",
            canon_lock_depth=0,
            soft_attractor="canon",
            branch_baseline_ref=baseline_ref,
        )
    return StrategyConfig(
        strategy="living_open", canon_lock_depth=0, branch_baseline_ref=baseline_ref
    )


class CanonLocks:
    """Immutable canon-lock set: a locked fact key rejects mutation."""

    def __init__(self, locked: tuple[str, ...] = ()) -> None:
        self._locked = frozenset(locked)

    def lock(self, fact_key: str) -> CanonLocks:
        if not fact_key:
            raise ContractError("fact key must be non-empty")
        return CanonLocks(tuple(sorted(set(self._locked) | {fact_key})))

    def is_locked(self, fact_key: str) -> bool:
        return fact_key in self._locked

    def assert_mutable(self, fact_key: str) -> None:
        if self.is_locked(fact_key):
            from wanxiang_substrate.ledger.errors import CanonLocked

            raise CanonLocked(f"canon fact {fact_key!r} is locked; mutation rejected")


@dataclass(frozen=True, slots=True)
class BaselineComparison:
    """Comparison of a branch state against a frozen baseline."""

    matches: bool
    baseline_hash: str
    current_hash: str
    revision_delta: int

    @property
    def diverged(self) -> bool:
        return not self.matches


def compare_to_baseline(
    *,
    baseline_hash: str,
    current_hash: str,
    current_revision: int,
    baseline_revision: int,
) -> BaselineComparison:
    """Open-branch baseline comparison (canonical replay must match)."""
    if not baseline_hash:
        raise ContractError("baseline hash must be non-empty")
    return BaselineComparison(
        matches=baseline_hash == current_hash,
        baseline_hash=baseline_hash,
        current_hash=current_hash,
        revision_delta=current_revision - baseline_revision,
    )


@dataclass(frozen=True, slots=True)
class SoftAttractor:
    """A soft-canon pull toward a target when a condition holds."""

    target: str
    condition: Callable[[], bool] | None = None

    def pull(self, current: str, strength: float = 0.5) -> float:
        """Deterministic attraction score: 1.0 when already at target."""
        if current == self.target:
            return 1.0
        if self.condition is not None and not self.condition():
            return 0.0
        if not (0.0 <= strength <= 1.0):
            raise ContractError("strength must be within [0,1]")
        return strength
