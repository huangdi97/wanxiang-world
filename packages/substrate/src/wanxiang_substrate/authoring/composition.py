"""Domain composition and sandbox gap packs (M63)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.domains.capability import DomainRegistry
from wanxiang_substrate.domains.resolver import DomainDependencyResolver


@dataclass(frozen=True, slots=True)
class DomainComposition:
    composition_id: str
    domain_versions: tuple[tuple[str, str], ...]
    dependency_order: tuple[str, ...]
    dependency_lock: tuple[str, ...]
    gaps: tuple[str, ...]
    fingerprint: str
    candidate_only: bool = True


@dataclass(frozen=True, slots=True)
class DomainGapPack:
    gap_id: str
    domain_id: str
    missing_capabilities: tuple[str, ...]
    sandbox_only: bool = True


@dataclass(frozen=True, slots=True)
class DomainFingerprint:
    """Explainable source signal fingerprint used only for domain inference."""

    candidate_kinds: tuple[str, ...]
    signals: tuple[str, ...]
    fingerprint: str


@dataclass(frozen=True, slots=True)
class DomainCapabilityCandidate:
    """Proposal for a missing domain capability; never an activated domain."""

    candidate_id: str
    domain_id: str
    capability: str
    reason: str
    source_refs: tuple[str, ...]
    confidence: float
    sandbox_only: bool = True


@dataclass(frozen=True, slots=True)
class GapPackScaffold:
    gap_id: str
    domain_id: str
    capability_candidates: tuple[DomainCapabilityCandidate, ...]
    sandbox_only: bool = True


@dataclass(frozen=True, slots=True)
class DomainValidationResult:
    candidate_id: str
    passed: bool
    violations: tuple[str, ...]
    validation_hash: str


@dataclass(frozen=True, slots=True)
class CrossWorldReuseDecision:
    candidate_id: str
    target_world_id: str
    reusable: bool
    reason: str


def compose_domains(
    registry: DomainRegistry,
    selected: tuple[str, ...],
    *,
    composition_id: str = "composition_1",
) -> DomainComposition:
    resolution = DomainDependencyResolver().resolve(registry, selected)
    versions = tuple(
        sorted(
            (domain_id, registry.require(domain_id).version)
            for domain_id in resolution.selected
            if registry.get(domain_id)
        )
    )
    payload = {"versions": versions, "order": resolution.order, "conflicts": resolution.conflicts}
    fingerprint = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return DomainComposition(
        composition_id=composition_id,
        domain_versions=versions,
        dependency_order=resolution.order,
        dependency_lock=resolution.order,
        gaps=resolution.conflicts,
        fingerprint=fingerprint,
    )


def make_gap_pack(
    composition: DomainComposition, registry: DomainRegistry
) -> tuple[DomainGapPack, ...]:
    packs: list[DomainGapPack] = []
    for domain_id, _version in composition.domain_versions:
        domain = registry.require(domain_id)
        if not domain.actions or not domain.rules:
            missing = tuple(
                item
                for item, present in (
                    ("actions", bool(domain.actions)),
                    ("rules", bool(domain.rules)),
                )
                if not present
            )
            packs.append(DomainGapPack(f"gap_{domain_id}", domain_id, missing))
    return tuple(packs)


def fingerprint_domain_signals(candidates: tuple[CandidateEnvelope, ...]) -> DomainFingerprint:
    """Create a deterministic explainability record from candidate evidence."""
    kinds = tuple(sorted({candidate.kind for candidate in candidates}))
    values = " ".join(
        value.lower() for candidate in candidates for value in candidate.fields.values()
    )
    signals = tuple(
        sorted(
            signal
            for signal, markers in {
                "family": ("gedcom", "family", "genealogy"),
                "spatial": ("place", "garden", "city", "topology"),
                "normative": ("rule", "norm", "penalty", "institution"),
                "epistemic": ("secret", "believe", "knows"),
                "temporal": ("date", "year", "arrival", "birth"),
            }.items()
            if signal in kinds or any(marker in values for marker in markers)
        )
    )
    payload = {"kinds": kinds, "signals": signals}
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return DomainFingerprint(kinds, signals, digest)


def make_capability_candidates(
    gap_packs: tuple[DomainGapPack, ...],
    *,
    source_refs: tuple[str, ...] = (),
) -> tuple[GapPackScaffold, ...]:
    scaffolds: list[GapPackScaffold] = []
    for gap in gap_packs:
        candidates = tuple(
            DomainCapabilityCandidate(
                candidate_id=f"domain_cap_{gap.domain_id}_{capability}",
                domain_id=gap.domain_id,
                capability=capability,
                reason=f"gap pack {gap.gap_id} is missing {capability}",
                source_refs=source_refs,
                confidence=0.0,
            )
            for capability in gap.missing_capabilities
        )
        scaffolds.append(GapPackScaffold(gap.gap_id, gap.domain_id, candidates))
    return tuple(scaffolds)


class DomainValidationSandbox:
    """Pure validation sandbox; it does not claim OS isolation or mutate registry."""

    def validate(
        self, candidate: DomainCapabilityCandidate, registry: DomainRegistry
    ) -> DomainValidationResult:
        violations: list[str] = []
        domain = registry.get(candidate.domain_id)
        if domain is None:
            violations.append(f"unknown domain {candidate.domain_id!r}")
        elif candidate.capability not in domain.provides:
            violations.append(f"capability {candidate.capability!r} is not declared")
        if not candidate.sandbox_only:
            violations.append("candidate is not marked sandbox_only")
        payload = {
            "candidate": candidate.candidate_id,
            "domain": candidate.domain_id,
            "capability": candidate.capability,
            "violations": violations,
        }
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return DomainValidationResult(
            candidate.candidate_id, not violations, tuple(violations), digest
        )


def check_cross_world_reuse(
    candidate: DomainCapabilityCandidate,
    *,
    target_world_id: str,
    consented_source_ids: tuple[str, ...],
) -> CrossWorldReuseDecision:
    """Require explicit source consent before reusing a domain proposal."""
    if not target_world_id:
        return CrossWorldReuseDecision(
            candidate.candidate_id, target_world_id, False, "target world required"
        )
    source_ids = {ref.split("#", 1)[0] for ref in candidate.source_refs}
    allowed = bool(source_ids) and source_ids.issubset(set(consented_source_ids))
    return CrossWorldReuseDecision(
        candidate.candidate_id,
        target_world_id,
        allowed,
        "explicit source consent" if allowed else "source consent is missing",
    )
