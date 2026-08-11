"""World time vs wall-clock commit time.

World time is a deterministic, monotonic, non-negative tick counter owned by the
world. Commit timestamps are wall-clock and explicitly NON-semantic: they must
never participate in canonical ordering or semantic hashing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from wanxiang_domain.errors import ContractError


def _validate_ticks(value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ContractError(f"WorldTime ticks must be a non-negative integer, got {value!r}")


@dataclass(frozen=True, slots=True)
class WorldTime:
    """Deterministic world time in integer ticks (monotonic per branch)."""

    ticks: int

    def __post_init__(self) -> None:
        _validate_ticks(self.ticks)

    def __str__(self) -> str:
        return str(self.ticks)


@dataclass(frozen=True, slots=True)
class CommitTimestamp:
    """Wall-clock commit timestamp. Non-semantic: excluded from canonical hash."""

    utc: datetime

    def __post_init__(self) -> None:
        if self.utc.tzinfo is None:
            object.__setattr__(self, "utc", self.utc.replace(tzinfo=UTC))

    @classmethod
    def now(cls) -> CommitTimestamp:
        return cls(datetime.now(UTC))

    @classmethod
    def from_isoformat(cls, value: str) -> CommitTimestamp:
        return cls(datetime.fromisoformat(value))
