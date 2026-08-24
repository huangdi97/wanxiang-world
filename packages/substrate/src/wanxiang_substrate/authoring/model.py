"""Typed authoring pipeline records shared by API, CLI, and reference tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.authoring.semantic import SemanticAnalysis
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.parsing.segment import Segment

PipelineStage = Literal[
    "registered",
    "parsed",
    "segmented",
    "distilled",
    "fused",
    "reviewed",
    "drafted",
    "compiled",
    "previewed",
    "published",
]


@dataclass(frozen=True, slots=True)
class PipelineBuild:
    """Non-canonical build output with source/candidate provenance."""

    draft: WorldDraft
    candidates: tuple[CandidateEnvelope, ...]
    segments: tuple[Segment, ...]
    diagnostics: tuple[str, ...]
    conflicts: tuple[str, ...]
    selected_domains: tuple[str, ...]
    semantic_analysis: SemanticAnalysis | None = None

    @property
    def candidate_ids(self) -> tuple[str, ...]:
        return tuple(candidate.candidate_id for candidate in self.candidates)


@dataclass(frozen=True, slots=True)
class AuthoringSnapshot:
    """Transport-neutral status snapshot; it contains no canonical state."""

    job_id: str
    status: str
    stage: str
    source_ids: tuple[str, ...]
    draft_id: str | None = None
    package_id: str | None = None
    preview_id: str | None = None
    candidate_count: int = 0
    conflict_count: int = 0
    error: str = ""
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "job_id": self.job_id,
            "status": self.status,
            "stage": self.stage,
            "source_ids": list(self.source_ids),
            "draft_id": self.draft_id,
            "package_id": self.package_id,
            "preview_id": self.preview_id,
            "candidate_count": self.candidate_count,
            "conflict_count": self.conflict_count,
            "error": self.error,
            "diagnostics": list(self.diagnostics),
        }
