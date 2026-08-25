"""No-API Source -> WorldDraft pipeline (M58-M61, M71-M78)."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from typing import cast

from wanxiang_substrate.assets.storage import InMemoryObjectStore
from wanxiang_substrate.authoring.draft_builder import build_pipeline_build
from wanxiang_substrate.authoring.model import PipelineBuild
from wanxiang_substrate.authoring.pipeline_support import default_domain_registry, distiller_dag
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.semantic_distillation import (
    DistillationResult,
    DistillationStats,
    SemanticDistillationService,
)
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.domains.capability import DomainRegistry
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, Segment, build_segments
from wanxiang_substrate.sources.adapter import AdapterRegistry, IngestResult, SourceInspection
from wanxiang_substrate.sources.asset import AssetAdapter
from wanxiang_substrate.sources.blob import SourceBlobStore
from wanxiang_substrate.sources.book import BookAdapter
from wanxiang_substrate.sources.errors import (
    ContentHashMismatch,
    RightsDenied,
    SemanticProviderRequired,
    ZeroCoverage,
)
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.sources.security import IngestSecurityGate
from wanxiang_substrate.sources.structured import StructuredAdapter


def _merge_stats(
    total: DistillationStats, current: DistillationStats, count: int
) -> DistillationStats:
    return DistillationStats(
        segment_count=total.segment_count + current.segment_count,
        batch_count=total.batch_count + current.batch_count,
        completed_batches=total.completed_batches + current.completed_batches,
        provider_calls=total.provider_calls + current.provider_calls,
        retries=total.retries + current.retries,
        candidate_count=count,
        provider_id=current.provider_id or total.provider_id,
        stage_errors=total.stage_errors + current.stage_errors,
    )


class SourceToDraftPipeline:
    """Build a revisioned Forge draft from one or more registered sources."""

    def __init__(
        self,
        *,
        domains: DomainRegistry | None = None,
        blob_loader: Callable[[SourceRecord], bytes | None] | None = None,
        security_gate: IngestSecurityGate | None = None,
        providers: ProviderRouter | None = None,
    ) -> None:
        self._adapters = AdapterRegistry(
            (
                BookAdapter(),
                StructuredAdapter(),
                AssetAdapter(SourceBlobStore(InMemoryObjectStore())),
            )
        )
        self._gate = SourceGate()
        self._blob_loader = blob_loader
        self._security = security_gate or IngestSecurityGate()
        self._domains = domains or default_domain_registry()
        self._dag = distiller_dag()
        self._parser = StructureParser()
        self._providers = providers or ProviderRouter()
        self._semantic = SemanticDistillationService(self._providers)

    def run(
        self,
        records: tuple[SourceRecord, ...],
        *,
        draft_id: str,
        use_semantic_provider: bool = False,
    ) -> PipelineBuild:
        if not records:
            raise ValueError("authoring requires at least one source")
        candidates: list[CandidateEnvelope] = []
        segments: list[Segment] = []
        diagnostics: list[str] = []
        parsed_nodes = 0
        semantic_candidates = 0
        distillation = DistillationStats()
        for record in sorted(records, key=lambda item: item.source_id):
            result, inspection = self._ingest(record)
            parsed = self._parser.parse(
                result,
                source_id=record.source_id,
                version=record.version,
                content_hash=record.content_hash,
            )
            parsed_nodes += max(0, len(parsed.nodes) - 1)
            source_segments = build_segments(
                parsed, fmt=cast(LocatorFormat, result.detected_format)
            )
            segments.extend(source_segments)
            candidates.extend(self._dag.run(source_segments, source_id=record.source_id))
            if use_semantic_provider:
                distilled = self._distill(record, source_segments, parsed_nodes, len(segments))
                candidates.extend(distilled.candidates)
                semantic_candidates += len(distilled.candidates)
                distillation = _merge_stats(distillation, distilled.stats, len(candidates))
            else:
                batch_count = (
                    len(source_segments) + self._semantic.batch_size - 1
                ) // self._semantic.batch_size
                distillation = DistillationStats(
                    segment_count=len(segments),
                    batch_count=distillation.batch_count + batch_count,
                    completed_batches=0,
                    candidate_count=len(candidates),
                )
            diagnostics.extend(item.message for item in parsed.diagnostics)
            if not inspection.ok:
                diagnostics.append(f"source {record.source_id} inspection requires capability")
        if use_semantic_provider and semantic_candidates == 0 and not candidates:
            raise ZeroCoverage(
                "ZERO_COVERAGE: configured semantic provider returned no candidates",
                details=self._progress_details(parsed_nodes, segments, distillation),
            )
        private_eligible_sources = any(
            record.access != "public" and record.canonical_eligible() for record in records
        )
        if not use_semantic_provider and not candidates and private_eligible_sources:
            raise SemanticProviderRequired(
                "SEMANTIC_PROVIDER_REQUIRED: deterministic baseline found no candidates",
                details=self._progress_details(parsed_nodes, segments, distillation),
            )
        return build_pipeline_build(
            records,
            draft_id=draft_id,
            candidates=tuple(candidates),
            segments=tuple(segments),
            diagnostics=tuple(diagnostics),
            parsed_nodes=parsed_nodes,
            distillation=distillation,
            domains=self._domains,
        )

    def _ingest(self, record: SourceRecord) -> tuple[IngestResult, SourceInspection]:
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
        return adapter.ingest(record, raw), inspection

    def _distill(
        self,
        record: SourceRecord,
        segments: tuple[Segment, ...],
        parsed_nodes: int,
        all_segments: int,
    ) -> DistillationResult:
        capability = self._providers.capability("semantic")
        batch_count = (len(segments) + self._semantic.batch_size - 1) // self._semantic.batch_size
        if capability is None:
            raise SemanticProviderRequired(
                f"SEMANTIC_PROVIDER_REQUIRED: configure a semantic provider for {record.source_id}",
                details={
                    "source_id": record.source_id,
                    "parsed_nodes": str(parsed_nodes),
                    "segments": str(all_segments),
                    "batches": str(batch_count),
                },
            )
        if (
            record.access != "public"
            and not capability.private_safe
            and not (
                record.rights is not None and record.rights.allows("external_model_processing")
            )
        ):
            raise RightsDenied(
                "external semantic processing is not allowed for this source",
                details={
                    "source_id": record.source_id,
                    "gate": "external_model_processing",
                    "provider_id": capability.provider_id,
                },
            )
        return self._semantic.run(
            segments,
            source_id=record.source_id,
            private_source=record.access != "public",
        )

    @staticmethod
    def _progress_details(
        parsed_nodes: int, segments: list[Segment], distillation: DistillationStats
    ) -> dict[str, str]:
        return {
            "parsed_nodes": str(parsed_nodes),
            "segments": str(len(segments)),
            "batches": str(distillation.batch_count),
        }


__all__ = ["SourceToDraftPipeline"]
