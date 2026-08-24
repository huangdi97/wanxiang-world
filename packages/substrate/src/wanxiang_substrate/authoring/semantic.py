"""Book-scale deterministic semantic analysis (M60)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.candidates.envelope import CandidateEnvelope


@dataclass(frozen=True, slots=True)
class IdentityResolution:
    """Reversible alias/coreference result; no destructive identity merge."""

    canonical_keys: tuple[str, ...]
    aliases: tuple[tuple[str, str], ...]
    unresolved_mentions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TemporalNarrative:
    """Ordered event/time view with explicit unknown dates."""

    events: tuple[tuple[str, str], ...]
    unknown_time: tuple[str, ...]
    ordering_conflicts: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class KnowledgeGraph:
    """Candidate graph preserving edges, places, objects, and institutions."""

    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str, str], ...]
    places: tuple[str, ...]
    objects: tuple[str, ...]
    institutions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SemanticMetrics:
    """Benchmark metrics, not a claim of human-level understanding."""

    candidate_count: int
    identity_count: int
    temporal_count: int
    graph_edge_count: int
    evidence_coverage: float
    uncertainty: float


@dataclass(frozen=True, slots=True)
class SemanticAnalysis:
    identities: IdentityResolution
    temporal: TemporalNarrative
    graph: KnowledgeGraph
    metrics: SemanticMetrics


def _field(candidate: CandidateEnvelope, *keys: str, default: str = "") -> str:
    fields = candidate.fields
    for key in keys:
        if fields.get(key):
            return fields[key]
    return default


class SemanticAnalyzer:
    """Runs shared long-range semantic views over candidate envelopes."""

    def analyze(self, candidates: tuple[CandidateEnvelope, ...]) -> SemanticAnalysis:
        identity_keys = sorted(
            {
                _field(candidate, "key", "identity_key")
                for candidate in candidates
                if candidate.kind == "identity" and _field(candidate, "key", "identity_key")
            }
        )
        aliases = sorted(
            (
                _field(candidate, "identity_key"),
                _field(candidate, "alias"),
            )
            for candidate in candidates
            if candidate.kind == "alias"
            and _field(candidate, "identity_key")
            and _field(candidate, "alias")
        )
        unresolved = sorted(
            {
                _field(candidate, "mention", "display_name")
                for candidate in candidates
                if candidate.kind == "coreference" and _field(candidate, "mention", "display_name")
            }
        )
        events = sorted(
            (
                _field(candidate, "event_type", "subject_xref", default="event"),
                _field(candidate, "date", default="unknown"),
            )
            for candidate in candidates
            if candidate.kind in ("event", "time")
        )
        unknown_time = tuple(sorted(event for event, date in events if date == "unknown"))
        known_dates = [date for _event, date in events if date != "unknown"]
        ordering_conflicts = (
            () if known_dates == sorted(known_dates) else ("event order differs from source order",)
        )
        edges = sorted(
            (
                _field(candidate, "source_key", "subject_xref"),
                _field(candidate, "target_key", "object_key", default="unknown"),
                _field(candidate, "relation_type", default="related"),
            )
            for candidate in candidates
            if candidate.kind in ("relation", "membership")
        )
        places = sorted(
            {
                _field(candidate, "name")
                for candidate in candidates
                if candidate.kind == "place" and _field(candidate, "name")
            }
        )
        objects = sorted(
            {
                _field(candidate, "name")
                for candidate in candidates
                if candidate.kind == "object" and _field(candidate, "name")
            }
        )
        institutions = sorted(
            {
                _field(candidate, "name", "organization")
                for candidate in candidates
                if candidate.kind in ("organization", "role")
                and _field(candidate, "name", "organization")
            }
        )
        nodes = tuple(sorted(set(identity_keys) | set(places) | set(objects) | set(institutions)))
        support = sum(1 for candidate in candidates if candidate.source_refs)
        coverage = support / len(candidates) if candidates else 0.0
        uncertainty = min(1.0, 0.05 + 0.1 * len(ordering_conflicts) + 0.02 * len(unresolved))
        metrics = SemanticMetrics(
            candidate_count=len(candidates),
            identity_count=len(identity_keys),
            temporal_count=len(events),
            graph_edge_count=len(edges),
            evidence_coverage=coverage,
            uncertainty=uncertainty,
        )
        return SemanticAnalysis(
            IdentityResolution(tuple(identity_keys), tuple(aliases), tuple(unresolved)),
            TemporalNarrative(tuple(events), unknown_time, ordering_conflicts),
            KnowledgeGraph(nodes, tuple(edges), tuple(places), tuple(objects), tuple(institutions)),
            metrics,
        )
