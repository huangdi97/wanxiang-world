"""Evidence ledger for accelerated 24h/7d long-horizon qualifications."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_runtime.state import InMemoryCanonicalState

HorizonLabel = Literal["24h", "7d", "30d"]


@dataclass(frozen=True, slots=True)
class HorizonSample:
    """One measured checkpoint from a real or explicitly reference runtime."""

    label: HorizonLabel
    target_tick: int
    observed_tick: int
    actor_ids: tuple[str, ...]
    event_count: int
    checkpoint_count: int
    storage_bytes: int
    replay_hash: str
    recovery_hash: str

    def __post_init__(self) -> None:
        if self.target_tick < 1 or self.observed_tick != self.target_tick:
            raise ContractError("horizon sample tick did not reach the target")
        if not self.actor_ids or len(self.actor_ids) != len(set(self.actor_ids)):
            raise ContractError("horizon sample requires unique actor ids")
        if min(self.event_count, self.checkpoint_count, self.storage_bytes) < 0:
            raise ContractError("horizon sample metrics cannot be negative")
        if not self.replay_hash or not self.recovery_hash:
            raise ContractError("horizon sample replay hashes must be non-empty")

    @property
    def replay_recovery_equal(self) -> bool:
        return self.replay_hash == self.recovery_hash


@dataclass(frozen=True, slots=True)
class HorizonQualificationReport:
    run_id: str
    samples: tuple[HorizonSample, ...]
    replay_recovery_equal: bool
    multiple_actor_evidence: bool
    storage_bytes_growth: int

    @property
    def qualified(self) -> bool:
        labels = {sample.label for sample in self.samples}
        return (
            {"24h", "7d"}.issubset(labels)
            and self.replay_recovery_equal
            and self.multiple_actor_evidence
            and self.storage_bytes_growth >= 0
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "qualified": self.qualified,
            "replay_recovery_equal": self.replay_recovery_equal,
            "multiple_actor_evidence": self.multiple_actor_evidence,
            "storage_bytes_growth": self.storage_bytes_growth,
            "samples": [
                {
                    "label": sample.label,
                    "target_tick": sample.target_tick,
                    "observed_tick": sample.observed_tick,
                    "actor_count": len(sample.actor_ids),
                    "event_count": sample.event_count,
                    "checkpoint_count": sample.checkpoint_count,
                    "storage_bytes": sample.storage_bytes,
                    "replay_recovery_equal": sample.replay_recovery_equal,
                }
                for sample in self.samples
            ],
        }


@dataclass(slots=True)
class HorizonQualification:
    """Monotonic metric collector; it never claims scientific validity."""

    run_id: str
    _samples: list[HorizonSample] = field(default_factory=list[HorizonSample])

    def record(self, sample: HorizonSample) -> None:
        if self._samples and sample.target_tick <= self._samples[-1].target_tick:
            raise ContractError("horizon samples must advance monotonically")
        if any(existing.label == sample.label for existing in self._samples):
            raise ContractError(f"duplicate horizon label {sample.label!r}")
        if self._samples and sample.event_count < self._samples[-1].event_count:
            raise ContractError("event count cannot regress across horizon samples")
        self._samples.append(sample)

    def finish(self) -> HorizonQualificationReport:
        if not self._samples:
            raise ContractError("qualification needs at least one horizon sample")
        first = self._samples[0]
        last = self._samples[-1]
        return HorizonQualificationReport(
            run_id=self.run_id,
            samples=tuple(self._samples),
            replay_recovery_equal=all(item.replay_recovery_equal for item in self._samples),
            multiple_actor_evidence=len(set(last.actor_ids)) >= 2,
            storage_bytes_growth=last.storage_bytes - first.storage_bytes,
        )


def state_storage_bytes(state: InMemoryCanonicalState) -> int:
    """Measure serialized state projection size without persisting a second state."""
    from wanxiang_runtime.state import state_to_primitive

    return len(json.dumps(state_to_primitive(state), sort_keys=True).encode("utf-8"))


__all__ = [
    "HorizonLabel",
    "HorizonQualification",
    "HorizonQualificationReport",
    "HorizonSample",
    "state_storage_bytes",
]
