"""Deterministic multi-source candidate fusion (M61/M64)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.sources.model import SourceRecord


@dataclass(frozen=True, slots=True)
class FusionResult:
    """Fused candidates retain every input and expose conflicts explicitly."""

    candidates: tuple[CandidateEnvelope, ...]
    conflict_ids: tuple[str, ...]
    provenance: tuple[tuple[str, tuple[str, ...]], ...]
    alignments: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = ()


@dataclass(frozen=True, slots=True)
class SourceFamily:
    """Edition/version family; source bytes remain separate and immutable."""

    family_id: str
    source_ids: tuple[str, ...]
    versions: tuple[tuple[str, str], ...]
    alignment_confidence: float
    roles: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class ProvenanceGraph:
    """Claim/candidate/source edges used by review and audit surfaces."""

    edges: tuple[tuple[str, str, str], ...]


@dataclass(frozen=True, slots=True)
class IncrementalFusion:
    """Supplemental-source result with affected keys and reused candidates."""

    result: FusionResult
    affected_keys: tuple[str, ...]
    reused_candidate_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RightsDecision:
    """Rights-compatible candidate view; denied candidates are never hidden."""

    included: tuple[CandidateEnvelope, ...]
    excluded_candidate_ids: tuple[str, ...]
    blocked_source_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DissentPolicy:
    """Explicit conflict policy; dissent is preserved by default."""

    policy_id: str = "preserve_dissent"
    choose_winner: bool = False
    require_review: bool = True
    preferred_source_ids: tuple[str, ...] = ()
    minimum_reliability: float = 0.0

    def rank(
        self, candidate: CandidateEnvelope, records: tuple[SourceRecord, ...]
    ) -> tuple[float, str]:
        source_ids = {ref.split("#", 1)[0] for ref in candidate.source_refs}
        reliability = max(
            (record.reliability for record in records if record.source_id in source_ids),
            default=0.0,
        )
        preferred = 1.0 if source_ids.intersection(self.preferred_source_ids) else 0.0
        return preferred + reliability, candidate.candidate_id


@dataclass(frozen=True, slots=True)
class ConflictWorkbench:
    """Review view over conflicts without deleting candidate alternatives."""

    conflict_ids: tuple[str, ...]
    alternatives: tuple[tuple[str, tuple[str, ...]], ...]
    policy: DissentPolicy
    impact: tuple[tuple[str, int], ...] = ()


def build_source_family(
    records: tuple[tuple[str, str, str], ...],
    *,
    roles: tuple[tuple[str, str], ...] = (),
) -> SourceFamily:
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
        roles=tuple(sorted(roles)),
    )


def build_source_family_from_records(
    family_id: str,
    records: tuple[SourceRecord, ...],
    *,
    roles: tuple[tuple[str, str], ...] = (),
) -> SourceFamily:
    """Build a family from immutable registry records without copying bytes."""
    return build_source_family(
        tuple((family_id, record.source_id, record.version) for record in records),
        roles=roles,
    )


def build_provenance_graph(candidates: tuple[CandidateEnvelope, ...]) -> ProvenanceGraph:
    edges: list[tuple[str, str, str]] = []
    for candidate in candidates:
        edges.extend(
            (candidate.candidate_id, source_ref, "evidence") for source_ref in candidate.source_refs
        )
        fields = candidate.fields
        for relation in ("supports", "contradicts", "refines", "derived_from"):
            targets = fields.get(relation, "")
            edges.extend(
                (candidate.candidate_id, target.strip(), relation)
                for target in targets.replace(";", ",").split(",")
                if target.strip()
            )
    edges.sort()
    return ProvenanceGraph(tuple(edges))


def open_conflict_workbench(
    result: FusionResult, *, policy: DissentPolicy | None = None
) -> ConflictWorkbench:
    alternatives: list[tuple[str, tuple[str, ...]]] = []
    impact: list[tuple[str, int]] = []
    for conflict_id in result.conflict_ids:
        candidate_ids = tuple(
            candidate.candidate_id
            for candidate in result.candidates
            if conflict_id.endswith(_digest(*_key(candidate)))
        )
        alternatives.append((conflict_id, candidate_ids))
        impact.append((conflict_id, len(candidate_ids)))
    return ConflictWorkbench(
        result.conflict_ids, tuple(alternatives), policy or DissentPolicy(), tuple(impact)
    )


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
    alignments: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = []
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
        source_ids = tuple(
            sorted({ref.split("#", 1)[0] for item in batch for ref in item.source_refs})
        )
        if len(source_ids) > 1:
            alignments.append(
                (f"{key[0]}:{key[1]}", tuple(item.candidate_id for item in batch), source_ids)
            )
    return FusionResult(
        tuple(ordered), tuple(sorted(conflicts)), tuple(provenance), tuple(alignments)
    )


def incremental_fuse(
    previous: FusionResult, supplemental: tuple[CandidateEnvelope, ...]
) -> IncrementalFusion:
    """Fuse a supplemental source while reporting affected semantic keys."""
    previous_ids = {candidate.candidate_id for candidate in previous.candidates}
    supplemental_keys = set(map(_key, supplemental))
    affected = tuple(sorted({f"{kind}:{value}" for kind, value in map(_key, supplemental)}))
    result = fuse_candidates(previous.candidates + supplemental)
    reused = tuple(
        sorted(
            candidate.candidate_id
            for candidate in result.candidates
            if candidate.candidate_id in previous_ids and _key(candidate) not in supplemental_keys
        )
    )
    return IncrementalFusion(result, affected, reused)


def apply_rights_policy(
    candidates: tuple[CandidateEnvelope, ...], records: tuple[SourceRecord, ...]
) -> RightsDecision:
    """Return only candidates whose source records are canonically eligible."""
    by_id = {record.source_id: record for record in records}
    included: list[CandidateEnvelope] = []
    excluded: list[str] = []
    blocked_sources: set[str] = set()
    for candidate in candidates:
        source_ids = {ref.split("#", 1)[0] for ref in candidate.source_refs}
        allowed = bool(source_ids) and all(
            source_id in by_id and by_id[source_id].canonical_eligible() for source_id in source_ids
        )
        if allowed:
            included.append(candidate)
        else:
            excluded.append(candidate.candidate_id)
            blocked_sources.update(source_ids - set(by_id))
            blocked_sources.update(
                source_id
                for source_id in source_ids
                if source_id in by_id and not by_id[source_id].canonical_eligible()
            )
    return RightsDecision(tuple(included), tuple(sorted(excluded)), tuple(sorted(blocked_sources)))
