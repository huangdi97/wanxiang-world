"""Source Gate: decides canonical eligibility before any compilation (G04B).

The gate treats source payloads strictly as data: it can read a payload as
content, but never as system/prompt instructions, and it flags instruction-
injection attempts.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.sources.errors import MaliciousSource, RightsDenied, SourceNotApproved
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.sources.policy import SourcePolicy


@dataclass(frozen=True, slots=True)
class GateDecision:
    """Structured gate decision with provenance."""

    source_id: str
    allowed: bool
    reason: str
    policy_version: int
    reviewer: str = "source_gate"

    @property
    def ok(self) -> bool:
        return self.allowed


class SourceGate:
    """Pure decision engine: rights + review stage + injection scan."""

    def __init__(self, policy: SourcePolicy | None = None) -> None:
        self._policy = policy or SourcePolicy()

    def decide(self, record: SourceRecord) -> GateDecision:
        if self._is_malicious(record):
            return GateDecision(
                record.source_id,
                False,
                "malicious injection markers detected",
                self._policy.policy_version,
            )
        if self._policy.require_rights_approval and (
            record.rights is None or not record.rights.approved
        ):
            return GateDecision(
                record.source_id, False, "rights not approved", self._policy.policy_version
            )
        if not record.canonical_eligible():
            return GateDecision(
                record.source_id,
                False,
                f"source stage {record.stage} is not canonical-eligible",
                self._policy.policy_version,
            )
        return GateDecision(
            record.source_id,
            True,
            "approved for canonical compilation",
            self._policy.policy_version,
        )

    def require_compile(self, record: SourceRecord) -> None:
        decision = self.decide(record)
        if not decision.ok:
            if "malicious" in decision.reason:
                raise MaliciousSource(decision.reason)
            if "rights" in decision.reason:
                raise RightsDenied(decision.reason)
            raise SourceNotApproved(decision.reason)

    def read_as_data(self, record: SourceRecord) -> str:
        """Return source content as data only; never as instructions."""
        if self._is_malicious(record):
            raise MaliciousSource("refusing to surface injection payload")
        return record.payload

    def _is_malicious(self, record: SourceRecord) -> bool:
        lowered = record.payload.lower()
        return any(marker in lowered for marker in self._policy.malicious_markers)
