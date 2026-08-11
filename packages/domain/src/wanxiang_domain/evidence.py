"""Foundational Claim/Evidence references.

A source is not automatically a fact: claims carry a status and reference
evidence. Full Source Registry/compiler review arrives in P4; only the
first-class references are introduced here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import ClaimId, EvidenceId, WorldInstanceId
from wanxiang_domain.versions import SchemaVersion

CLAIM_STATUSES = frozenset({"proposed", "confirmed", "disputed", "rejected"})


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    evidence_id: EvidenceId
    source_kind: str
    source_version: SchemaVersion | None = None


@dataclass(frozen=True, slots=True)
class ClaimRef:
    claim_id: ClaimId
    schema_version: SchemaVersion
    status: str = "proposed"
    instance_id: WorldInstanceId | None = None
    evidence: tuple[EvidenceRef, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.status not in CLAIM_STATUSES:
            raise ContractError(
                f"invalid claim status {self.status!r}; expected one of {sorted(CLAIM_STATUSES)}"
            )
