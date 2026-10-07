"""Wanxiang Capability Foundry (R7 Artifact2Capability slice).

Turns an external artifact into a verified, self-describing capability package:
providers propose candidates, a reference provider is honest and LLM-free, the
execution fabric verifies declared cases as real subprocesses, and a registry
admits only fully-verified packages. Nothing here can mutate canonical world
state; the foundry is proposal-side only.
"""

from wanxiang_foundry.candidate import ArtifactKind, ArtifactRef, CapabilityCandidate
from wanxiang_foundry.digest import canonical_sha256, is_hex_digest
from wanxiang_foundry.errors import (
    ArtifactError,
    CandidateError,
    FoundryError,
    InvocationError,
    RegistryError,
    VerificationError,
)
from wanxiang_foundry.fabric_runner import run_cases
from wanxiang_foundry.invocation import CapabilityOutcome, CapabilityRequest, invoke
from wanxiang_foundry.marketplace import (
    CapabilityDiscoveryQuery,
    CapabilityMarketplaceListing,
    VerifiedCapabilityMarketplace,
)
from wanxiang_foundry.levels import (
    AUTOMATION_MAX_PROMOTION,
    KnowledgeLevel,
    PromotionLevel,
    is_automation_grantable,
)
from wanxiang_foundry.package import (
    CapabilityPackage,
    OutputClass,
    RuntimeRequirement,
    Validity,
    WorldEffect,
)
from wanxiang_foundry.provenance import (
    ProvenanceLayer,
    ProvenanceRecord,
    provenance_digest,
)
from wanxiang_foundry.provider import Artifact2CapabilityProvider, ProviderRegistry
from wanxiang_foundry.reference_provider import RuleBasedFoundryProvider
from wanxiang_foundry.registry import PromotionGrant, VerifiedCapabilityRegistry
from wanxiang_foundry.verification import (
    CaseKind,
    CaseResult,
    FailureLayer,
    VerificationCase,
    VerificationReport,
    verify,
)

__version__ = "0.1.0"

__all__ = [
    "AUTOMATION_MAX_PROMOTION",
    "Artifact2CapabilityProvider",
    "ArtifactError",
    "ArtifactKind",
    "ArtifactRef",
    "CandidateError",
    "CapabilityCandidate",
    "CapabilityDiscoveryQuery",
    "CapabilityMarketplaceListing",
    "CapabilityOutcome",
    "CapabilityPackage",
    "CapabilityRequest",
    "CaseKind",
    "CaseResult",
    "FailureLayer",
    "FoundryError",
    "InvocationError",
    "KnowledgeLevel",
    "OutputClass",
    "PromotionGrant",
    "PromotionLevel",
    "ProvenanceLayer",
    "ProvenanceRecord",
    "ProviderRegistry",
    "RegistryError",
    "RuleBasedFoundryProvider",
    "RuntimeRequirement",
    "Validity",
    "VerificationCase",
    "VerificationError",
    "VerificationReport",
    "VerifiedCapabilityMarketplace",
    "VerifiedCapabilityRegistry",
    "WorldEffect",
    "canonical_sha256",
    "invoke",
    "is_automation_grantable",
    "is_hex_digest",
    "provenance_digest",
    "run_cases",
    "verify",
]
