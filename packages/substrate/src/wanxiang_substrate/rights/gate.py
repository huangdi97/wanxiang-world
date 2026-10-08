"""Rights gate for model/display/export/package inclusion (G58C).

Extends the G04B SourceGate rights check with scope-aware decisions:
model use, display, export, and package inclusion each require rights approval
per the source's RightsEnvelope; no scope is auto-approved.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.sources.errors import RightsDenied
from wanxiang_substrate.sources.model import SourceRecord

RightsScope = Literal["model", "display", "export", "package"]
VALID_SCOPES = ("model", "display", "export", "package")


@dataclass(frozen=True, slots=True)
class RightsDecision:
    source_id: str
    scope: RightsScope
    allowed: bool
    reason: str

    @property
    def ok(self) -> bool:
        return self.allowed


class RightsGate:
    """Scope-aware rights decisions (reuses SourceRecord rights)."""

    def require(self, record: SourceRecord, scope: RightsScope) -> None:
        decision = self.decide(record, scope)
        if not decision.ok:
            raise RightsDenied(decision.reason)

    def decide(self, record: SourceRecord, scope: RightsScope) -> RightsDecision:
        if scope not in VALID_SCOPES:
            raise RightsDenied(f"unknown rights scope {scope!r}")
        rights = record.rights
        if rights is None:
            return RightsDecision(record.source_id, scope, False, "source has no rights envelope")
        if not rights.approved:
            return RightsDecision(record.source_id, scope, False, "rights not approved")
        if scope == "package" and "package" not in rights.usage:
            return RightsDecision(
                record.source_id,
                scope,
                False,
                f"rights usage {rights.usage!r} does not permit package inclusion",
            )
        return RightsDecision(record.source_id, scope, True, "rights approved")
