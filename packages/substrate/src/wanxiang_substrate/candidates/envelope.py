"""Unified CandidateEnvelope (G57A).

One candidate shell across all distillation passes and providers: candidate
kind, origin pass, confidence, source refs, evidence refs, distiller version,
payload, status, provider. Converges the earlier pattern-specific
CandidateEnvelope (evolution/distillation) into the shared Forge candidate
fabric; candidates never enter Canon without review.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

CandidateKind = Literal[
    "identity",
    "alias",
    "coreference",
    "event",
    "time",
    "place",
    "relation",
    "role",
    "membership",
    "organization",
    "character",
    "life_arc",
    "goal",
    "belief",
    "knowledge_boundary",
    "object",
    "rule",
    "norm",
    "skill",
    "affordance",
    "ontology",
    "scenario",
]
VALID_KINDS = (
    "identity",
    "alias",
    "coreference",
    "event",
    "time",
    "place",
    "relation",
    "role",
    "membership",
    "organization",
    "character",
    "life_arc",
    "goal",
    "belief",
    "knowledge_boundary",
    "object",
    "rule",
    "norm",
    "skill",
    "affordance",
    "ontology",
    "scenario",
)
CandidateStatus = Literal["pending", "eligible", "rejected"]
VALID_STATUSES = ("pending", "eligible", "rejected")


@dataclass(frozen=True, slots=True)
class CandidateEnvelope:
    """A distillation candidate with full provenance; never Canon."""

    candidate_id: str
    kind: CandidateKind
    origin_pass: str
    payload: tuple[tuple[str, str], ...]
    confidence: float
    source_refs: tuple[str, ...]
    distiller_version: int
    evidence_refs: tuple[str, ...] = ()
    status: CandidateStatus = "pending"
    provider: str = "deterministic"

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.origin_pass:
            raise ContractError("candidate requires id and origin pass")
        if self.kind not in VALID_KINDS:
            raise ContractError(f"invalid candidate kind {self.kind!r}")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("confidence must be within [0,1]")
        if self.distiller_version <= 0:
            raise ContractError("distiller_version must be positive")
        if self.status not in VALID_STATUSES:
            raise ContractError(f"invalid candidate status {self.status!r}")

    @property
    def fields(self) -> dict[str, str]:
        return dict(self.payload)

    def compute_hash(self) -> str:
        payload = json.dumps(
            {
                "candidate_id": self.candidate_id,
                "kind": self.kind,
                "origin_pass": self.origin_pass,
                "payload": dict(self.payload),
                "confidence": self.confidence,
                "source_refs": sorted(self.source_refs),
                "evidence_refs": sorted(self.evidence_refs),
                "distiller_version": self.distiller_version,
                "provider": self.provider,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_status(self, status: CandidateStatus) -> CandidateEnvelope:
        return CandidateEnvelope(
            candidate_id=self.candidate_id,
            kind=self.kind,
            origin_pass=self.origin_pass,
            payload=self.payload,
            confidence=self.confidence,
            source_refs=self.source_refs,
            distiller_version=self.distiller_version,
            evidence_refs=self.evidence_refs,
            status=status,
            provider=self.provider,
        )
