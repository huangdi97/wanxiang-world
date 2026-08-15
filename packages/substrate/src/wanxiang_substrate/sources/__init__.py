"""Source registry & source gate substrate (G04B)."""

from wanxiang_substrate.sources.canon import (
    CanonClaim,
    CanonCompiler,
    CompiledCanon,
    ScenarioPoint,
    scenario_at,
)
from wanxiang_substrate.sources.character import (
    CharacterCanon,
    CharacterDistiller,
    CharacterFact,
    FactKind,
    FactScope,
    KnowledgeBoundary,
    RelationClaim,
)
from wanxiang_substrate.sources.entity_distill import (
    DistilledEntities,
    EntityCandidate,
    EntityConnection,
    EntityDistiller,
    EntityMention,
    EntityReviewDecision,
    EntityReviewGate,
)
from wanxiang_substrate.sources.errors import (
    DuplicateSource,
    InvalidTransition,
    MaliciousSource,
    RightsDenied,
    SourceError,
    SourceNotApproved,
    SourceNotFound,
)
from wanxiang_substrate.sources.evidence import AUTHORIZED_REVIEWERS, evidence_ok
from wanxiang_substrate.sources.fixture import (
    approved_source,
    conflicting_claims,
    conflicting_sources,
    malicious_source,
    rejected_source,
)
from wanxiang_substrate.sources.gate import GateDecision, SourceGate
from wanxiang_substrate.sources.identity import (
    AliasClaim,
    IdentityCandidate,
    IdentityDistiller,
    IdentityReviewDecision,
    IdentityReviewGate,
    identity_to_claim,
)
from wanxiang_substrate.sources.locator import (
    SourceLocator,
    locator_stable_hash,
    segment_source,
    source_slice,
)
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
    "CharacterCanon",
    "CharacterDistiller",
    "CharacterFact",
    "FactKind",
    "FactScope",
    "KnowledgeBoundary",
    "RelationClaim",
    "CanonClaim",
    "CanonCompiler",
    "CompiledCanon",
    "ScenarioPoint",
    "scenario_at",
    "AUTHORIZED_REVIEWERS",
    "DistilledEntities",
    "EntityCandidate",
    "EntityConnection",
    "EntityDistiller",
    "EntityMention",
    "EntityReviewDecision",
    "EntityReviewGate",
    "evidence_ok",
    "ClaimCandidate",
    "DuplicateSource",
    "EvidenceLink",
    "GateDecision",
    "AliasClaim",
    "IdentityCandidate",
    "IdentityDistiller",
    "IdentityReviewDecision",
    "IdentityReviewGate",
    "identity_to_claim",
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
    "SourceLocator",
    "locator_stable_hash",
    "segment_source",
    "source_slice",
]
