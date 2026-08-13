"""Source record, claim candidate and rights value objects (G04B).

Source payloads are data, never system/prompt instructions: consumers must read
them through the gate which separates content from any executable/prompt
channel.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

ReviewStage = Literal["E0", "E1", "E2", "E3", "E4", "E5"]
# E0 received, E1 rights verified, E2 content reviewed, E3 approved,
# E4 rejected, E5 superseded.

STAGE_ORDER = ("E0", "E1", "E2", "E3", "E4", "E5")
CANONICAL_ELIGIBLE_STAGES = ("E3",)
MAX_PAYLOAD_BYTES = 64 * 1024


@dataclass(frozen=True, slots=True)
class RightsEnvelope:
    """Rights/policy decision attached to a source."""

    owner: str
    usage: str
    approved: bool
    policy_version: int = 1
    reviewer: str = "system"

    def __post_init__(self) -> None:
        if not self.owner or not self.usage:
            raise ContractError("rights envelope requires owner and usage")
        if self.policy_version <= 0:
            raise ContractError("policy_version must be positive")


@dataclass(frozen=True, slots=True)
class SourceRecord:
    """Immutable source identity: id + content hash, with review state."""

    source_id: str
    kind: str
    content_hash: str
    content_ref: str
    stage: ReviewStage = "E0"
    rights: RightsEnvelope | None = None
    payload: str = ""
    provenance: str = ""

    def __post_init__(self) -> None:
        if not self.source_id or len(self.source_id) > 64:
            raise ContractError("source_id must be non-empty and <= 64 chars")
        if self.kind not in ("text", "yaml", "json", "markdown"):
            raise ContractError(f"unsupported source kind {self.kind!r}")
        if not self.content_hash or len(self.content_hash) != 64:
            raise ContractError("content_hash must be a sha256 hex digest")
        if len(self.payload.encode("utf-8")) > MAX_PAYLOAD_BYTES:
            raise ContractError("source payload exceeds size limit")

    def canonical_eligible(self) -> bool:
        return self.stage in CANONICAL_ELIGIBLE_STAGES and self.rights is not None

    def can_transition_to(self, next_stage: ReviewStage) -> bool:
        if self.stage in ("E4", "E5"):
            return False
        order = {stage: index for index, stage in enumerate(STAGE_ORDER)}
        return order[next_stage] > order[self.stage]


def payload_hash(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class EvidenceLink:
    """Link between a claim candidate and a source."""

    claim_id: str
    source_id: str
    role: Literal["supports", "contradicts"]
    weight: float = 1.0

    def __post_init__(self) -> None:
        if self.role not in ("supports", "contradicts"):
            raise ContractError(f"invalid evidence role {self.role!r}")
        if not (0.0 <= self.weight <= 1.0):
            raise ContractError("evidence weight must be within [0,1]")


@dataclass(frozen=True, slots=True)
class ClaimCandidate:
    """A claim with provenance; conflicting candidates are never overwritten."""

    claim_id: str
    proposition: str
    source_ids: tuple[str, ...] = ()
    status: Literal["pending", "eligible", "rejected"] = "pending"
    evidence_links: tuple[EvidenceLink, ...] = ()

    def __post_init__(self) -> None:
        if not self.claim_id or not self.proposition:
            raise ContractError("claim requires id and proposition")
        if self.status not in ("pending", "eligible", "rejected"):
            raise ContractError(f"invalid claim status {self.status!r}")

    def with_status(self, status: Literal["pending", "eligible", "rejected"]) -> ClaimCandidate:
        return ClaimCandidate(
            claim_id=self.claim_id,
            proposition=self.proposition,
            source_ids=self.source_ids,
            status=status,
            evidence_links=self.evidence_links,
        )


def canonical_json(record: SourceRecord) -> str:
    """Stable serialization used for auditing decisions."""
    return json.dumps(
        {
            "source_id": record.source_id,
            "kind": record.kind,
            "content_hash": record.content_hash,
            "content_ref": record.content_ref,
            "stage": record.stage,
            "rights_approved": record.rights.approved if record.rights else False,
            "policy_version": record.rights.policy_version if record.rights else 0,
            "provenance": record.provenance,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
