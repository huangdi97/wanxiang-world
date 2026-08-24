"""No-API Source -> WorldDraft pipeline (M58-M61)."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import replace
from typing import cast

from wanxiang_substrate.authoring.fusion import fuse_candidates
from wanxiang_substrate.authoring.model import PipelineBuild
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.distill import (
    CharacterKnowledgePass,
    DistillerDAG,
    EventTimeSpacePass,
    IdentityPass,
    ObjectRuleSkillPass,
    RelationOrganizationPass,
)
from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry
from wanxiang_substrate.domains.recommender import DomainRecommender
from wanxiang_substrate.domains.resolver import DomainDependencyResolver
from wanxiang_substrate.draft.coverage import CoverageAssessor
from wanxiang_substrate.draft.model import DraftStatus, WorldDraft
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, Segment, build_segments
from wanxiang_substrate.sources.adapter import AdapterRegistry
from wanxiang_substrate.sources.book import BookAdapter
from wanxiang_substrate.sources.errors import ContentHashMismatch
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.sources.security import IngestSecurityGate
from wanxiang_substrate.sources.structured import StructuredAdapter


def default_domain_registry() -> DomainRegistry:
    registry = DomainRegistry()
    for domain in (
        DomainCapability("family", "Family", "1.0.0", ("family", "genealogy")),
        DomainCapability(
            "narrative",
            "Narrative",
            "1.0.0",
            ("narrative", "character", "temporal"),
            requires=("family",),
        ),
        DomainCapability("household", "Household", "1.0.0", ("social", "norm", "institution")),
        DomainCapability("spatial", "Spatial", "1.0.0", ("spatial", "place", "topology")),
    ):
        registry.register(domain)
    return registry


def _dag() -> DistillerDAG:
    return DistillerDAG(
        (
            IdentityPass(),
            EventTimeSpacePass(),
            RelationOrganizationPass(),
            CharacterKnowledgePass(),
            ObjectRuleSkillPass(),
        )
    )


def _field(candidate: CandidateEnvelope, *names: str, default: str = "") -> str:
    fields = candidate.fields
    for name in names:
        if fields.get(name):
            return fields[name]
    return default


def _expand_domains(registry: DomainRegistry, selected: tuple[str, ...]) -> tuple[str, ...]:
    found = set(selected)
    changed = True
    while changed:
        changed = False
        for domain_id in tuple(found):
            domain = registry.get(domain_id)
            if domain is None:
                continue
            for required in domain.requires:
                if required not in found:
                    found.add(required)
                    changed = True
    return tuple(sorted(found))


class SourceToDraftPipeline:
    """Build a revisioned Forge draft from one or more registered sources."""

    def __init__(
        self,
        *,
        domains: DomainRegistry | None = None,
        blob_loader: Callable[[SourceRecord], bytes | None] | None = None,
        security_gate: IngestSecurityGate | None = None,
    ) -> None:
        self._adapters = AdapterRegistry((BookAdapter(), StructuredAdapter()))
        self._gate = SourceGate()
        self._blob_loader = blob_loader
        self._security = security_gate or IngestSecurityGate()
        self._domains = domains or default_domain_registry()
        self._dag = _dag()
        self._parser = StructureParser()

    def run(self, records: tuple[SourceRecord, ...], *, draft_id: str) -> PipelineBuild:
        if not records:
            raise ValueError("authoring requires at least one source")
        candidates: list[CandidateEnvelope] = []
        segments: list[Segment] = []
        diagnostics: list[str] = []
        for record in sorted(records, key=lambda item: item.source_id):
            content = self._gate.read_as_data(record)
            adapter = self._adapters.select(kind=record.kind)
            if adapter is None:
                raise ValueError(f"unsupported source kind {record.kind!r}")
            inspection = adapter.inspect(record)
            blob = self._blob_loader(record) if self._blob_loader is not None else None
            raw = content.encode("utf-8") if blob is None else blob
            if hashlib.sha256(raw).hexdigest() != record.content_hash:
                raise ContentHashMismatch(
                    f"source {record.source_id!r} bytes do not match content hash"
                )
            self._security.check_blob(raw, kind=record.kind)
            result = adapter.ingest(record, raw)
            parsed = self._parser.parse(
                result,
                source_id=record.source_id,
                version=record.version,
                content_hash=record.content_hash,
            )
            fmt = cast(LocatorFormat, result.detected_format)
            source_segments = build_segments(parsed, fmt=fmt)
            segments.extend(source_segments)
            candidates.extend(self._dag.run(source_segments, source_id=record.source_id))
            diagnostics.extend(
                parsed_diagnostic.message for parsed_diagnostic in parsed.diagnostics
            )
            if not inspection.ok:
                diagnostics.append(f"source {record.source_id} inspection requires capability")
        fusion = fuse_candidates(tuple(candidates))
        source_kind = (
            "gedcom" if any(record.kind == "gedcom" for record in records) else records[0].kind
        )
        recommendations = DomainRecommender().recommend(
            self._domains, source_kind=source_kind, candidates=fusion.candidates
        )
        selected = _expand_domains(
            self._domains, tuple(recommendation.domain_id for recommendation in recommendations[:2])
        )
        resolution = DomainDependencyResolver().resolve(self._domains, selected)
        domain_order = resolution.order if resolution.ok else selected
        entities = sorted(
            {
                (_field(candidate, "key", "identity_key"), _field(candidate, "display_name", "key"))
                for candidate in fusion.candidates
                if candidate.kind in ("identity", "character")
                and _field(candidate, "key", "identity_key")
            }
        )
        relations = sorted(
            (
                _field(candidate, "source_key", "subject_xref"),
                _field(candidate, "target_key", "object_key", default="unknown"),
                _field(candidate, "relation_type", default="related"),
            )
            for candidate in fusion.candidates
            if candidate.kind in ("relation", "membership")
            and _field(candidate, "source_key", "subject_xref")
        )
        places = sorted(
            {
                _field(candidate, "name")
                for candidate in fusion.candidates
                if candidate.kind == "place"
            }
        )
        events = sorted(
            {
                (
                    _field(candidate, "event_type", default="event"),
                    _field(candidate, "date", default="unknown"),
                )
                for candidate in fusion.candidates
                if candidate.kind in ("event", "time")
            }
        )
        objects = sorted(
            {
                _field(candidate, "name")
                for candidate in fusion.candidates
                if candidate.kind == "object"
            }
        )
        rules = sorted(
            {
                _field(candidate, "name")
                for candidate in fusion.candidates
                if candidate.kind in ("rule", "norm")
            }
        )
        skills = sorted(
            {
                _field(candidate, "name")
                for candidate in fusion.candidates
                if candidate.kind == "skill"
            }
        )
        knowledge = sorted(
            {
                _field(candidate, "boundary", "statement")
                for candidate in fusion.candidates
                if candidate.kind in ("knowledge_boundary", "belief")
            }
        )
        rights = tuple(record.source_id for record in records if not record.canonical_eligible())
        preliminary = WorldDraft(
            draft_id=draft_id,
            revision=1,
            status="FUSING",
            source_refs=tuple(sorted(record.source_id for record in records)),
            source_versions=tuple(sorted((record.source_id, record.version) for record in records)),
            constitution_ref="constitution:v1",
            selected_domains=domain_order,
            dependency_lock=domain_order,
            entities=tuple(entities),
            relations=tuple(relations),
            places=tuple(place for place in places if place),
            objects=tuple(item for item in objects if item),
            events=tuple(events),
            rules=tuple(item for item in rules if item),
            skills=tuple(item for item in skills if item),
            knowledge_boundaries=tuple(item for item in knowledge if item),
            completion_items=(),
            unresolved_conflicts=fusion.conflict_ids + resolution.conflicts,
            unresolved_rights=rights,
            coverage=0.0,
            uncertainty=0.0,
            quality=0.0,
            compiler_metadata={"pipeline": "reference", "candidates": str(len(fusion.candidates))},
        )
        coverage = CoverageAssessor().assess(preliminary, self._domains)
        completion = tuple(sorted(set(coverage.unknown)))
        uncertainty = min(1.0, 0.05 + 0.15 * len(fusion.conflict_ids) + 0.05 * len(completion))
        final_status = (
            "READY_TO_COMPILE"
            if not preliminary.unresolved_conflicts and not rights
            else "REVIEW_REQUIRED"
        )
        draft = replace(
            preliminary,
            status=cast(DraftStatus, final_status),
            completion_items=completion,
            coverage=coverage.coverage,
            uncertainty=uncertainty,
            quality=max(0.0, min(1.0, coverage.coverage - uncertainty)),
        )
        return PipelineBuild(
            draft=draft,
            candidates=fusion.candidates,
            segments=tuple(segments),
            diagnostics=tuple(diagnostics),
            conflicts=fusion.conflict_ids + resolution.conflicts,
            selected_domains=domain_order,
        )
