"""Norm-to-institution candidate derivation and explicit review (G94E)."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_domain.errors import ContractError, PermissionDenied

from wanxiang_substrate.evolution.institution_promotion import (
    APPROVERS,
    InstitutionCandidate,
)
from wanxiang_substrate.evolution.norm_candidate_model import NormCandidate


def create_institution_candidate(
    norm: NormCandidate,
    *,
    candidate_id: str,
    role_refs: tuple[str, ...],
    resource_refs: tuple[str, ...],
    process_refs: tuple[str, ...],
) -> InstitutionCandidate:
    """Derive a structured institution candidate without activating its rule."""
    for label, refs in (
        ("role", role_refs),
        ("resource", resource_refs),
        ("process", process_refs),
    ):
        if not refs or len(set(refs)) != len(refs) or any(not ref.strip() for ref in refs):
            raise ContractError(f"institution candidate requires unique {label} refs")
    evidence = tuple(dict.fromkeys(norm.source_event_refs + norm.exception_event_refs))
    stability = round(min(norm.support_ratio, norm.confidence, 1.0 - norm.exception_rate), 6)
    return InstitutionCandidate(
        candidate_id=candidate_id,
        rule=norm.pattern_key,
        evidence=evidence,
        origin=f"norm:{norm.candidate_id}",
        stability_score=stability,
        role_refs=tuple(sorted(role_refs)),
        resource_refs=tuple(sorted(resource_refs)),
        process_refs=tuple(sorted(process_refs)),
        provenance_refs=tuple(
            dict.fromkeys((norm.detection_id, norm.scope_ref) + norm.source_event_refs)
        ),
    )


def review_institution_candidate(
    candidate: InstitutionCandidate,
    *,
    reviewer: str,
    approved: bool,
) -> InstitutionCandidate:
    """Record an explicit review decision; this function never commits a law."""
    if reviewer not in APPROVERS:
        raise PermissionDenied(f"reviewer {reviewer!r} is not authorized")
    if approved and (
        not candidate.role_refs or not candidate.resource_refs or not candidate.process_refs
    ):
        raise ContractError("structured institution candidate is incomplete")
    return replace(candidate, approved=approved, reviewed_by=reviewer)
