"""Evolution telemetry & privacy rights (G32G).

A minimal authorized data plane for cross-world learning: telemetry is
metadata / hash / aggregate by default; sensitive actor trajectories are gated
by retention + rights; consent/rights policy is opt-in. Unauthorized world data
never enters a cross-world dataset, and revocation removes it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import PermissionDenied

TelemetryKind = Literal["metadata", "hash", "aggregate", "trajectory"]


@dataclass(frozen=True, slots=True)
class TelemetryEnvelope:
    """One telemetry record with consent/rights metadata."""

    envelope_id: str
    world_ref: str
    kind: TelemetryKind
    metric: str
    value_hash: str = ""
    consent: bool = False
    rights_ref: str = "platform-default"
    retention_days: int = 0
    aggregate: int = 0

    def __post_init__(self) -> None:
        if not self.envelope_id or not self.world_ref or not self.metric:
            raise ValueError("telemetry envelope requires id, world_ref and metric")
        if self.kind not in ("metadata", "hash", "aggregate", "trajectory"):
            raise ValueError(f"unknown telemetry kind {self.kind!r}")


class TelemetryPolicy:
    """Opt-in / consent / rights policy for telemetry eligibility."""

    @staticmethod
    def eligible(envelope: TelemetryEnvelope) -> bool:
        if not envelope.consent:
            return False  # opt-in required
        if envelope.kind == "trajectory":
            # Sensitive trajectories require explicit rights + retention.
            if envelope.rights_ref == "platform-default":
                return False
            if envelope.retention_days <= 0:
                return False
        return True

    @staticmethod
    def require_eligible(envelope: TelemetryEnvelope) -> None:
        if not TelemetryPolicy.eligible(envelope):
            raise PermissionDenied(
                f"telemetry {envelope.envelope_id!r} is not eligible (consent/rights/retention)"
            )


class CrossWorldDataset:
    """Authorized cross-world telemetry dataset (opt-in, revocable)."""

    def __init__(self) -> None:
        self._envelopes: dict[str, TelemetryEnvelope] = {}

    def add(self, envelope: TelemetryEnvelope) -> TelemetryEnvelope:
        TelemetryPolicy.require_eligible(envelope)
        self._envelopes[envelope.envelope_id] = envelope
        return envelope

    def get(self, envelope_id: str) -> TelemetryEnvelope | None:
        return self._envelopes.get(envelope_id)

    def entries(self) -> tuple[TelemetryEnvelope, ...]:
        return tuple(sorted(self._envelopes.values(), key=lambda e: e.envelope_id))

    def revoke_world(self, world_ref: str) -> int:
        """Revocation policy: remove every envelope from a world."""
        removed = [eid for eid, e in self._envelopes.items() if e.world_ref == world_ref]
        for eid in removed:
            self._envelopes.pop(eid)
        return len(removed)

    def count(self) -> int:
        return len(self._envelopes)
