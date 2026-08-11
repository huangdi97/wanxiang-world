"""Foundational RightsEnvelope/decision seam.

Full rights policy arrives later; this establishes the decision object so
callers never scatter boolean is_allowed checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.ids import ActorId
from wanxiang_domain.versions import SchemaVersion

RightsDecision = Literal["allow", "deny"]


@dataclass(frozen=True, slots=True)
class RightsEnvelope:
    actor_id: ActorId | None
    permission: str
    policy_version: SchemaVersion
    decision: RightsDecision
    reason: str | None = None
