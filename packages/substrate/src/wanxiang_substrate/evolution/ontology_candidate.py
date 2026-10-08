"""Strict culture/ontology candidate derivation from long-window evidence (G94F)."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

from wanxiang_domain.errors import ContractError, PermissionDenied

from wanxiang_substrate.evolution.institution_promotion import (
    APPROVERS,
    InstitutionCandidate,
)
from wanxiang_substrate.evolution.norm_candidate_model import NormCandidate
from wanxiang_substrate.evolution.ontology_law import OntologyCandidate


@dataclass(frozen=True, slots=True)
class OntologyCandidatePolicy:
    """High-threshold policy for shared culture/ontology evidence."""

    minimum_norm_candidates: int = 3
    minimum_cross_windows: int = 3
    minimum_windows_per_norm: int = 2
    minimum_total_observed_windows: int = 6
    minimum_support: float = 0.9
    maximum_exception_rate: float = 0.1
    minimum_confidence: float = 0.9
    minimum_stability: float = 0.85
    maximum_complexity: float = 0.4
    minimum_interpretability: float = 0.9

    def __post_init__(self) -> None:
        for name, value in (
            ("minimum norm candidates", self.minimum_norm_candidates),
            ("minimum cross windows", self.minimum_cross_windows),
            ("minimum windows per norm", self.minimum_windows_per_norm),
            ("minimum total observed windows", self.minimum_total_observed_windows),
        ):
            if type(value) is not int or value < 2:
                raise ContractError(f"{name} must be an integer of at least two")
        for name, value in (
            ("minimum support", self.minimum_support),
            ("maximum exception rate", self.maximum_exception_rate),
            ("minimum confidence", self.minimum_confidence),
            ("minimum stability", self.minimum_stability),
            ("maximum complexity", self.maximum_complexity),
            ("minimum interpretability", self.minimum_interpretability),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ContractError(f"{name} must be within [0, 1]")
        if self.minimum_total_observed_windows < self.minimum_cross_windows:
            raise ContractError("total observed windows cannot be below cross-window floor")

    def to_dict(self) -> dict[str, object]:
        return {
            "minimum_norm_candidates": self.minimum_norm_candidates,
            "minimum_cross_windows": self.minimum_cross_windows,
            "minimum_windows_per_norm": self.minimum_windows_per_norm,
            "minimum_total_observed_windows": self.minimum_total_observed_windows,
            "minimum_support": self.minimum_support,
            "maximum_exception_rate": self.maximum_exception_rate,
            "minimum_confidence": self.minimum_confidence,
            "minimum_stability": self.minimum_stability,
            "maximum_complexity": self.maximum_complexity,
            "minimum_interpretability": self.minimum_interpretability,
        }


def _validate_windows(windows: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    if not windows or len(set(windows)) != len(windows):
        raise ContractError("ontology candidate requires unique cross-window evidence")
    for start, end in windows:
        if isinstance(start, bool) or isinstance(end, bool) or start < 0 or end <= start:
            raise ContractError("ontology evidence windows must be non-empty")
    return tuple(sorted(windows))


def _window_indexes(
    norms: tuple[NormCandidate, ...], windows: tuple[tuple[int, int], ...]
) -> set[int]:
    return {
        index
        for norm in norms
        for index, (start, end) in enumerate(windows)
        if start <= norm.created_at <= end
    }


def create_ontology_candidate(
    norm_candidates: tuple[NormCandidate, ...],
    *,
    candidate_id: str,
    concept: str,
    evidence_windows: tuple[tuple[int, int], ...],
    institution_candidates: tuple[InstitutionCandidate, ...] = (),
    policy: OntologyCandidatePolicy | None = None,
    scope: str = "world",
) -> OntologyCandidate:
    """Derive a high-level candidate without changing the Constitution or Canon."""
    policy = policy or OntologyCandidatePolicy()
    norms = tuple(norm_candidates)
    if not candidate_id.strip() or not concept.strip():
        raise ContractError("ontology candidate requires id and concept")
    if len(norms) < policy.minimum_norm_candidates:
        raise ContractError("ontology candidate requires more independent norm evidence")
    norm_ids = tuple(norm.candidate_id for norm in norms)
    if len(set(norm_ids)) != len(norm_ids):
        raise ContractError("ontology candidate requires unique norm evidence")
    windows = _validate_windows(evidence_windows)
    occupied = _window_indexes(norms, windows)
    if len(occupied) < policy.minimum_cross_windows:
        raise ContractError("ontology evidence does not span enough distinct windows")
    if any(norm.observed_window_count < policy.minimum_windows_per_norm for norm in norms):
        raise ContractError("each norm must retain multi-window evidence")
    if sum(norm.observed_window_count for norm in norms) < policy.minimum_total_observed_windows:
        raise ContractError("ontology evidence has too few observed windows")

    keys = {norm.pattern_key for norm in norms}
    support = min(norm.support_ratio for norm in norms)
    exception_rate = max(norm.exception_rate for norm in norms)
    confidence = min(norm.confidence for norm in norms)
    stability = min(
        min(norm.support_ratio, norm.confidence, 1.0 - norm.exception_rate) for norm in norms
    )
    complexity = round(len(keys) / len(norms), 6)
    interpretability = round(
        sum(bool(norm.detection_id and norm.scope_ref and norm.source_event_refs) for norm in norms)
        / len(norms),
        6,
    )
    if support < policy.minimum_support:
        raise ContractError("ontology support does not meet the strict threshold")
    if exception_rate > policy.maximum_exception_rate:
        raise ContractError("ontology exception rate exceeds the strict threshold")
    if confidence < policy.minimum_confidence or stability < policy.minimum_stability:
        raise ContractError("ontology confidence or stability does not meet the strict threshold")
    if complexity > policy.maximum_complexity:
        raise ContractError("ontology pattern complexity exceeds the strict threshold")
    if interpretability < policy.minimum_interpretability:
        raise ContractError("ontology evidence is not sufficiently interpretable")

    institutions = tuple(institution_candidates)
    institution_ids = tuple(item.candidate_id for item in institutions)
    if len(set(institution_ids)) != len(institution_ids):
        raise ContractError("ontology candidate requires unique institution evidence")
    if any(not item.approved for item in institutions):
        raise PermissionDenied("ontology candidate cannot consume an unreviewed institution")
    evidence_refs = tuple(
        sorted(
            {ref for norm in norms for ref in norm.source_event_refs + norm.exception_event_refs}
            | {ref for item in institutions for ref in item.evidence}
        )
    )
    provenance_refs = tuple(
        sorted(
            {ref for norm in norms for ref in (norm.detection_id, norm.scope_ref)}
            | set(evidence_refs)
        )
    )
    return OntologyCandidate(
        candidate_id=candidate_id,
        concept=concept,
        scope=scope,
        stability=round(stability, 6),
        complexity=complexity,
        interpretability=interpretability,
        evidence_refs=evidence_refs,
        evidence_windows=windows,
        norm_refs=tuple(sorted(norm_ids)),
        institution_refs=tuple(sorted(institution_ids)),
        provenance_refs=provenance_refs,
        approved=False,
        reviewed_by=None,
    )


def review_ontology_candidate(
    candidate: OntologyCandidate,
    *,
    reviewer: str,
    approved: bool,
) -> OntologyCandidate:
    """Record a human/policy decision; this helper never commits ontology."""
    if reviewer not in APPROVERS:
        raise PermissionDenied(f"reviewer {reviewer!r} is not authorized")
    if approved and (
        not candidate.evidence_refs or not candidate.evidence_windows or not candidate.norm_refs
    ):
        raise ContractError("evidence-backed ontology candidate is incomplete")
    return replace(candidate, approved=approved, reviewed_by=reviewer)
