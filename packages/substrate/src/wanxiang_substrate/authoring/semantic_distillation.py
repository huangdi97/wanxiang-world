"""Bounded semantic distillation through the existing provider router."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.authoring.providers import ProviderProposal, ProviderRouter
from wanxiang_substrate.candidates.envelope import VALID_KINDS, CandidateEnvelope
from wanxiang_substrate.parsing.segment import Segment
from wanxiang_substrate.sources.errors import (
    SemanticProviderRequired,
    SemanticProviderSchemaError,
)


@dataclass(frozen=True, slots=True)
class DistillationStats:
    """Auditable bounded-batch progress, including retry/error information."""

    segment_count: int = 0
    batch_count: int = 0
    completed_batches: int = 0
    provider_calls: int = 0
    retries: int = 0
    candidate_count: int = 0
    provider_id: str = ""
    stage_errors: tuple[str, ...] = ()

    def checkpoint(self) -> dict[str, str]:
        return {
            "segments": str(self.segment_count),
            "batches": str(self.batch_count),
            "completed_batches": str(self.completed_batches),
            "provider_calls": str(self.provider_calls),
            "retries": str(self.retries),
            "candidates": str(self.candidate_count),
            "provider_id": self.provider_id,
            "stage_errors": "|".join(self.stage_errors),
        }


@dataclass(frozen=True, slots=True)
class DistillationResult:
    candidates: tuple[CandidateEnvelope, ...]
    stats: DistillationStats


class SemanticDistillationService:
    """Dispatch parsed segments to one configured semantic provider in batches."""

    def __init__(
        self,
        providers: ProviderRouter,
        *,
        batch_size: int = 24,
        retry_limit: int = 2,
    ) -> None:
        if batch_size <= 0 or retry_limit < 0:
            raise ValueError("batch_size must be positive and retry_limit cannot be negative")
        self._providers = providers
        self._batch_size = batch_size
        self._retry_limit = retry_limit

    @property
    def batch_size(self) -> int:
        return self._batch_size

    def run(
        self,
        segments: tuple[Segment, ...],
        *,
        source_id: str,
        private_source: bool,
    ) -> DistillationResult:
        capability = self._providers.select(
            "semantic",
            private_source=private_source,
            require_deterministic=True,
            source_refs=(source_id,),
        )
        batches = tuple(
            segments[index : index + self._batch_size]
            for index in range(0, len(segments), self._batch_size)
        )
        stats = DistillationStats(
            segment_count=len(segments),
            batch_count=len(batches),
            provider_id=capability.provider_id,
        )
        candidates: list[CandidateEnvelope] = []
        errors: list[str] = []
        for batch_index, batch in enumerate(batches):
            payload = json.dumps(
                [{"locator": item.locator.to_string(), "text": item.text} for item in batch],
                ensure_ascii=False,
                separators=(",", ":"),
            )
            refs = tuple(item.locator.to_string() for item in batch)
            completed = False
            for attempt in range(self._retry_limit + 1):
                try:
                    proposals = self._providers.propose("semantic", refs, payload)
                    converted = self._convert(proposals, refs, capability.provider_id)
                    candidates.extend(converted)
                    stats = DistillationStats(
                        segment_count=stats.segment_count,
                        batch_count=stats.batch_count,
                        completed_batches=stats.completed_batches + 1,
                        provider_calls=stats.provider_calls + 1,
                        retries=stats.retries + attempt,
                        candidate_count=len(candidates),
                        provider_id=stats.provider_id,
                        stage_errors=tuple(errors),
                    )
                    completed = True
                    break
                except (SemanticProviderSchemaError, ValueError, TypeError) as exc:
                    if attempt >= self._retry_limit:
                        errors.append(f"batch_{batch_index}:{type(exc).__name__}:{exc}")
                    stats = DistillationStats(
                        segment_count=stats.segment_count,
                        batch_count=stats.batch_count,
                        completed_batches=stats.completed_batches,
                        provider_calls=stats.provider_calls + 1,
                        retries=stats.retries + 1,
                        candidate_count=len(candidates),
                        provider_id=stats.provider_id,
                        stage_errors=tuple(errors),
                    )
            if not completed:
                raise SemanticProviderSchemaError(
                    f"semantic batch {batch_index} failed after {self._retry_limit + 1} attempts",
                    details=stats.checkpoint(),
                )
        return DistillationResult(tuple(candidates), stats)

    def require_available(self, *, source_id: str) -> None:
        if self._providers.capability("semantic") is None:
            raise SemanticProviderRequired(
                f"SEMANTIC_PROVIDER_REQUIRED: configure a semantic provider for {source_id}",
                details={"source_id": source_id},
            )

    @staticmethod
    def _convert(
        proposals: tuple[ProviderProposal, ...], refs: tuple[str, ...], provider_id: str
    ) -> tuple[CandidateEnvelope, ...]:
        converted: list[CandidateEnvelope] = []
        allowed = set(refs)
        for proposal in proposals:
            source_refs = proposal.source_refs
            payload = dict(proposal.payload)
            kind = payload.pop("candidate_kind", "")
            schema_version = payload.get("schema_version", "")
            if (
                kind not in VALID_KINDS
                or not schema_version
                or not source_refs
                or not set(source_refs).issubset(allowed)
            ):
                raise SemanticProviderSchemaError(
                    "semantic provider candidate schema or locator provenance is invalid"
                )
            proposal_id = proposal.proposal_id
            confidence = proposal.confidence
            if not proposal_id or not 0.0 <= confidence <= 1.0:
                raise SemanticProviderSchemaError(
                    "semantic provider candidate confidence/id is invalid"
                )
            digest = hashlib.sha256(f"{provider_id}:{proposal_id}".encode()).hexdigest()[:20]
            converted.append(
                CandidateEnvelope(
                    candidate_id=f"cand_semantic_{digest}",
                    kind=kind,  # type: ignore[arg-type]
                    origin_pass="semantic_distillation",
                    payload=tuple(sorted((str(key), str(value)) for key, value in payload.items())),
                    confidence=confidence,
                    source_refs=source_refs,
                    evidence_refs=source_refs,
                    distiller_version=1,
                    provider=provider_id,
                )
            )
        return tuple(converted)


__all__ = ["DistillationResult", "DistillationStats", "SemanticDistillationService"]
