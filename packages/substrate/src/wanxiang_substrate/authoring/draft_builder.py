"""Candidate fusion and WorldDraft assembly for the authoring pipeline."""

from __future__ import annotations

from dataclasses import replace
from typing import cast

from wanxiang_substrate.authoring.fusion import FusionResult, fuse_candidates
from wanxiang_substrate.authoring.model import PipelineBuild
from wanxiang_substrate.authoring.pipeline_support import expand_domains, field
from wanxiang_substrate.authoring.semantic import SemanticAnalyzer
from wanxiang_substrate.authoring.semantic_distillation import DistillationStats
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.domains.capability import DomainRegistry
from wanxiang_substrate.domains.recommender import DomainRecommender
from wanxiang_substrate.domains.resolver import DomainDependencyResolver
from wanxiang_substrate.draft.coverage import CoverageAssessor
from wanxiang_substrate.draft.model import DraftStatus, WorldDraft
from wanxiang_substrate.parsing.segment import Segment
from wanxiang_substrate.sources.model import SourceRecord


def _entities(fusion: FusionResult) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            {
                (field(candidate, "key", "identity_key"), field(candidate, "display_name", "key"))
                for candidate in fusion.candidates
                if candidate.kind in ("identity", "character")
                and field(candidate, "key", "identity_key")
            }
        )
    )


def _relations(fusion: FusionResult) -> tuple[tuple[str, str, str], ...]:
    by_xref = {
        field(candidate, "xref"): field(candidate, "key")
        for candidate in fusion.candidates
        if candidate.kind == "identity" and field(candidate, "xref") and field(candidate, "key")
    }
    return tuple(
        sorted(
            (
                by_xref.get(
                    field(candidate, "source_key", "subject_xref"),
                    field(candidate, "source_key", "subject_xref"),
                ),
                by_xref.get(
                    field(candidate, "target_key", "object_key", default="unknown"),
                    field(candidate, "target_key", "object_key", default="unknown"),
                ),
                field(candidate, "relation_type", default="related"),
            )
            for candidate in fusion.candidates
            if candidate.kind in ("relation", "membership")
            and field(candidate, "source_key", "subject_xref")
        )
    )


def _names(fusion: FusionResult, kind: str) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                field(candidate, "name")
                for candidate in fusion.candidates
                if candidate.kind == kind and field(candidate, "name")
            }
        )
    )


def build_pipeline_build(
    records: tuple[SourceRecord, ...],
    *,
    draft_id: str,
    candidates: tuple[CandidateEnvelope, ...],
    segments: tuple[Segment, ...],
    diagnostics: tuple[str, ...],
    parsed_nodes: int,
    distillation: DistillationStats,
    domains: DomainRegistry,
) -> PipelineBuild:
    fusion = fuse_candidates(candidates)
    semantic = SemanticAnalyzer().analyze(fusion.candidates)
    source_kind = (
        "gedcom" if any(record.kind == "gedcom" for record in records) else records[0].kind
    )
    recommendations = DomainRecommender().recommend(
        domains, source_kind=source_kind, candidates=fusion.candidates
    )
    selected = expand_domains(domains, tuple(item.domain_id for item in recommendations[:2]))
    resolution = DomainDependencyResolver().resolve(domains, selected)
    domain_order = resolution.order if resolution.ok else selected
    events = tuple(
        sorted(
            {
                (
                    field(candidate, "event_type", default="event"),
                    field(candidate, "date", default="unknown"),
                )
                for candidate in fusion.candidates
                if candidate.kind in ("event", "time")
            }
        )
    )
    rules = _names(fusion, "rule") + _names(fusion, "norm")
    skills = _names(fusion, "skill")
    knowledge = tuple(
        sorted(
            {
                field(candidate, "boundary", "statement")
                for candidate in fusion.candidates
                if candidate.kind in ("knowledge_boundary", "belief")
                and field(candidate, "boundary", "statement")
            }
        )
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
        entities=_entities(fusion),
        relations=_relations(fusion),
        places=_names(fusion, "place"),
        objects=_names(fusion, "object"),
        events=events,
        rules=tuple(sorted({item for item in rules if item})),
        skills=skills,
        knowledge_boundaries=knowledge,
        unresolved_conflicts=fusion.conflict_ids + resolution.conflicts,
        unresolved_rights=rights,
        compiler_metadata={
            "pipeline": "reference",
            "candidates": str(len(fusion.candidates)),
            "semantic_identities": str(semantic.metrics.identity_count),
            "semantic_events": str(semantic.metrics.temporal_count),
            "semantic_edges": str(semantic.metrics.graph_edge_count),
            "parsed_nodes": str(parsed_nodes),
            "segments": str(len(segments)),
            "batches": str(distillation.batch_count),
            "provider_id": distillation.provider_id,
        },
    )
    coverage = CoverageAssessor().assess(preliminary, domains)
    completion = tuple(sorted(set(coverage.unknown)))
    uncertainty = min(1.0, 0.05 + 0.15 * len(fusion.conflict_ids) + 0.05 * len(completion))
    ready = not preliminary.unresolved_conflicts and not rights and coverage.coverage > 0.0
    draft = replace(
        preliminary,
        status=cast(DraftStatus, "READY_TO_COMPILE" if ready else "COMPLETION_REQUIRED"),
        completion_items=completion,
        coverage=coverage.coverage,
        uncertainty=uncertainty,
        quality=max(0.0, min(1.0, coverage.coverage - uncertainty)),
    )
    return PipelineBuild(
        draft=draft,
        candidates=fusion.candidates,
        segments=segments,
        diagnostics=diagnostics,
        conflicts=fusion.conflict_ids + resolution.conflicts,
        selected_domains=domain_order,
        semantic_analysis=semantic,
        distillation=DistillationStats(
            segment_count=len(segments),
            batch_count=distillation.batch_count,
            completed_batches=distillation.completed_batches,
            provider_calls=distillation.provider_calls,
            retries=distillation.retries,
            candidate_count=len(fusion.candidates),
            provider_id=distillation.provider_id,
            stage_errors=distillation.stage_errors,
        ),
    )


__all__ = ["build_pipeline_build"]
