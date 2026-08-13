"""Source registry & source gate substrate (G04B)."""

from wanxiang_substrate.sources.errors import (
    DuplicateSource,
    InvalidTransition,
    MaliciousSource,
    RightsDenied,
    SourceError,
    SourceNotApproved,
    SourceNotFound,
)
from wanxiang_substrate.sources.fixture import (
    approved_source,
    conflicting_claims,
    conflicting_sources,
    malicious_source,
    rejected_source,
)
from wanxiang_substrate.sources.gate import GateDecision, SourceGate
from wanxiang_substrate.sources.model import (
    ClaimCandidate,
    EvidenceLink,
    RightsEnvelope,
    SourceRecord,
    payload_hash,
)
from wanxiang_substrate.sources.policy import SourcePolicy
from wanxiang_substrate.sources.registry import AuditEntry, SourceRegistry

__all__ = [
    "AuditEntry",
    "ClaimCandidate",
    "DuplicateSource",
    "EvidenceLink",
    "GateDecision",
    "InvalidTransition",
    "MaliciousSource",
    "RightsDenied",
    "RightsEnvelope",
    "SourceError",
    "SourceGate",
    "SourceNotApproved",
    "SourceNotFound",
    "SourcePolicy",
    "SourceRecord",
    "SourceRegistry",
    "approved_source",
    "conflicting_claims",
    "conflicting_sources",
    "malicious_source",
    "payload_hash",
    "rejected_source",
]
