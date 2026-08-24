"""Deterministic multi-source candidate fusion (M61/M64)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.candidates.envelope import CandidateEnvelope


@dataclass(frozen=True, slots=True)
class FusionResult:
    """Fused candidates retain every input and expose conflicts explicitly."""

    candidates: tuple[CandidateEnvelope, ...]
    conflict_ids: tuple[str, ...]
    provenance: tuple[tuple[str, tuple[str, ...]], ...]


@dataclass(frozen=True, slots=True)
class SourceFamily:
    """Edition/version family; source bytes remain separate and immutable."""

    family_id: str
    source_ids: tuple[str, ...]
    versions: tuple[tuple[str, str], ...]
    alignment_confidence: float


@dataclass(frozen=True, slots=True)
class ProvenanceGraph:
    """Claim/candidate/source edges used by review and audit surfaces."""

    edges: tuple[tuple[str, str, str], ...]


@dataclass(frozen=True, slots=True)
class DissentPolicy:
    """Explicit conflict policy; dissent is preserved by default."""

    policy_id: str = "preserve_dissent"
    choose_winner: bool = False
    require_review: bool = True


@dataclass(frozen=True, slots=True)
class ConflictWorkbench:
    """Review view over conflicts without deleting candidate alternatives."""

    conflict_ids: tuple[str, ...]
    alternatives: tuple[tuple[str, tuple[str, ...]], ...]
    policy: DissentPolicy


def build_source_family(records: tuple[tuple[str, str, str], ...]) -> SourceFamily:
    """Align source ids by an explicit family id supplied by the caller."""
    if not records:
        raise ValueError("source family requires at least one record")
    family_id = records[0][0]
    versions = tuple(sorted((source_id, version) for _family, source_id, version in records))
    return SourceFamily(
        family_id=family_id,
        source_ids=tuple(source_id for source_id, _version in versions),
        versions=versions,
        alignment_confidence=1.0
        if len({family for family, _source, _version in records}) == 1
        else 0.0,
    )


def build_provenance_graph(candidates: tuple[CandidateEnvelope, ...]) -> ProvenanceGraph:
    edges = tuple(
        sorted(
            (candidate.candidate_id, source_ref, "evidence")
            for candidate in candidates
            for source_ref in candidate.source_refs
        )
    )
    return ProvenanceGraph(edges)


def open_conflict_workbench(
    result: FusionResult, *, policy: DissentPolicy | None = None
) -> ConflictWorkbench:
    alternatives: list[tuple[str, tuple[str, ...]]] = []
    for conflict_id in result.conflict_ids:
        alternatives.append(
            (
                conflict_id,
                tuple(
                    candidate.candidate_id
                    for candidate in result.candidates
                    if conflict_id.endswith(_digest(*_key(candidate)))
                ),
            )
        )
    return ConflictWorkbench(result.conflict_ids, tuple(alternatives), policy or DissentPolicy())


def _key(candidate: CandidateEnvelope) -> tuple[str, str]:
    fields = candidate.fields
    value = (
        fields.get("key")
        or fields.get("identity_key")
        or fields.get("name")
        or fields.get("date")
        or fields.get("event_type")
        or candidate.candidate_id
    )
    return candidate.kind, value


def _digest(kind: str, value: str) -> str:
    encoded = json.dumps([kind, value], ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:12]


def fuse_candidates(candidates: tuple[CandidateEnvelope, ...]) -> FusionResult:
    """Group by semantic key without overwriting dissenting candidates."""
    groups: dict[tuple[str, str], list[CandidateEnvelope]] = {}
    for candidate in candidates:
        groups.setdefault(_key(candidate), []).append(candidate)
    conflicts: list[str] = []
    provenance: list[tuple[str, tuple[str, ...]]] = []
    ordered: list[CandidateEnvelope] = []
    for key in sorted(groups):
        batch = sorted(groups[key], key=lambda item: item.candidate_id)
        payloads = {tuple(item.payload) for item in batch}
        if len(payloads) > 1 and len({ref for item in batch for ref in item.source_refs}) > 1:
            conflicts.append(f"conflict_{_digest(*key)}")
        ordered.extend(batch)
        provenance.append(
            (
                f"{key[0]}:{key[1]}",
                tuple(sorted({ref for item in batch for ref in item.source_refs})),
            )
        )
    return FusionResult(tuple(ordered), tuple(sorted(conflicts)), tuple(provenance))
