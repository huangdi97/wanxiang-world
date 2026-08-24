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
class LifeArcCandidate:
    """Reversible phase/goal/belief observations for one identity."""

    subject: str
    phase: str
    goal: str
    belief: str
    evidence: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SpatialTopology:
    """Place containment/connectivity/access edges without invented geometry."""

    places: tuple[str, ...]
    edges: tuple[tuple[str, str, str], ...]
    unresolved_access: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ObjectBiography:
    """Candidate ownership/custody/location history for an object."""

    object_key: str
    observations: tuple[tuple[str, str, str, str], ...]


@dataclass(frozen=True, slots=True)
class InstitutionNorm:
    """Candidate institution/role/norm/consequence observations."""

    institution: str
    role: str
    norm: str
    consequence: str


@dataclass(frozen=True, slots=True)
class SemanticMetrics:
    """Benchmark metrics, not a claim of human-level understanding."""

    candidate_count: int
    identity_count: int
    temporal_count: int
    graph_edge_count: int
    evidence_coverage: float
    uncertainty: float
    unknown_count: int = 0
    conflict_count: int = 0
    precision_proxy: float = 0.0
    recall_proxy: float = 0.0
    calibration_error: float = 0.0


@dataclass(frozen=True, slots=True)
class SemanticAnalysis:
    identities: IdentityResolution
    temporal: TemporalNarrative
    graph: KnowledgeGraph
    metrics: SemanticMetrics
    life_arcs: tuple[LifeArcCandidate, ...] = ()
    spatial: SpatialTopology = SpatialTopology((), (), ())
    object_biographies: tuple[ObjectBiography, ...] = ()
    institution_norms: tuple[InstitutionNorm, ...] = ()


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
                _field(candidate, "mention", "display_name", default=candidate.candidate_id)
                for candidate in candidates
                if candidate.kind == "coreference"
            }
        )
        ordered_events = tuple(
            (
                _field(candidate, "event_type", "subject_xref", default="event"),
                _field(candidate, "date", default="unknown"),
            )
            for candidate in candidates
            if candidate.kind in ("event", "time")
        )
        events = tuple(sorted(ordered_events))
        unknown_time = tuple(sorted(event for event, date in events if date == "unknown"))
        known_dates = [date for _event, date in ordered_events if date != "unknown"]
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
        life_arcs = tuple(
            sorted(
                (
                    LifeArcCandidate(
                        subject=_field(
                            candidate, "subject", "subject_key", "identity_key", default="unknown"
                        ),
                        phase=_field(candidate, "phase", "stage", default="unknown"),
                        goal=_field(candidate, "goal", "objective"),
                        belief=_field(candidate, "belief", "statement"),
                        evidence=candidate.source_refs,
                    )
                    for candidate in candidates
                    if candidate.kind in ("life_arc", "character", "persona", "belief")
                ),
                key=lambda item: (item.subject, item.phase, item.goal, item.belief, item.evidence),
            )
        )
        topology_edges = tuple(
            sorted(
                (
                    _field(candidate, "source", "source_place", "from_place"),
                    _field(candidate, "target", "target_place", "to_place"),
                    _field(candidate, "relation", "relation_type", default=candidate.kind),
                )
                for candidate in candidates
                if candidate.kind
                in ("topology", "containment", "connectivity", "access", "place_relation")
                and _field(candidate, "source", "source_place", "from_place")
                and _field(candidate, "target", "target_place", "to_place")
            )
        )
        unresolved_access = tuple(
            sorted(
                candidate.candidate_id
                for candidate in candidates
                if candidate.kind == "access"
                and not _field(candidate, "target", "target_place", "to_place")
            )
        )
        object_histories: dict[str, list[tuple[str, str, str, str]]] = {}
        for candidate in candidates:
            if candidate.kind not in ("object", "ownership", "custody", "transfer", "object_event"):
                continue
            object_key = _field(candidate, "object_key", "object_id", "name", default="unknown")
            observation = (
                _field(candidate, "event", "event_type", default=candidate.kind),
                _field(candidate, "actor", "owner", "custodian", default="unknown"),
                _field(candidate, "location", "place", default="unknown"),
                _field(candidate, "date", default="unknown"),
            )
            object_histories.setdefault(object_key, []).append(observation)
        object_biographies = tuple(
            ObjectBiography(key, tuple(sorted(observations)))
            for key, observations in sorted(object_histories.items())
        )
        institution_norms = tuple(
            sorted(
                (
                    InstitutionNorm(
                        institution=_field(
                            candidate, "institution", "organization", "name", default="unknown"
                        ),
                        role=_field(candidate, "role", default="unknown"),
                        norm=_field(candidate, "norm", "rule", "statement", default="unknown"),
                        consequence=_field(candidate, "consequence", "penalty", default="unknown"),
                    )
                    for candidate in candidates
                    if candidate.kind in ("organization", "role", "rule", "norm", "institution")
                ),
                key=lambda item: (
                    item.institution,
                    item.role,
                    item.norm,
                    item.consequence,
                ),
            )
        )
        support = sum(1 for candidate in candidates if candidate.source_refs)
        coverage = support / len(candidates) if candidates else 0.0
        unknown_count = len(unresolved) + len(unknown_time) + len(unresolved_access)
        confidence = (
            sum(candidate.confidence for candidate in candidates) / len(candidates)
            if candidates
            else 0.0
        )
        precision_proxy = coverage
        recall_proxy = max(0.0, 1.0 - (unknown_count / max(1, len(nodes) + len(events))))
        calibration_error = abs(confidence - coverage)
        uncertainty = min(1.0, 0.05 + 0.1 * len(ordering_conflicts) + 0.02 * len(unresolved))
        metrics = SemanticMetrics(
            candidate_count=len(candidates),
            identity_count=len(identity_keys),
            temporal_count=len(events),
            graph_edge_count=len(edges),
            evidence_coverage=coverage,
            uncertainty=uncertainty,
            unknown_count=unknown_count,
            conflict_count=len(ordering_conflicts),
            precision_proxy=precision_proxy,
            recall_proxy=recall_proxy,
            calibration_error=calibration_error,
        )
        return SemanticAnalysis(
            IdentityResolution(tuple(identity_keys), tuple(aliases), tuple(unresolved)),
            TemporalNarrative(tuple(events), unknown_time, ordering_conflicts),
            KnowledgeGraph(nodes, tuple(edges), tuple(places), tuple(objects), tuple(institutions)),
            metrics,
            life_arcs,
            SpatialTopology(tuple(places), topology_edges, unresolved_access),
            object_biographies,
            institution_norms,
        )
