"""Candidate transport serialization shared by draft and review views."""

from __future__ import annotations

from wanxiang_substrate.candidates.envelope import CandidateEnvelope


def candidate_to_dict(candidate: CandidateEnvelope) -> dict[str, object]:
    return {
        "candidate_id": candidate.candidate_id,
        "kind": candidate.kind,
        "confidence": candidate.confidence,
        "status": candidate.status,
        "origin_pass": candidate.origin_pass,
        "distiller_version": candidate.distiller_version,
        "provider": candidate.provider,
        "source_refs": list(candidate.source_refs),
        "evidence_refs": list(candidate.evidence_refs),
        "payload": dict(candidate.payload),
    }
