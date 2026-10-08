"""Import/Authoring job model (G54E).

A Job is the unified execution unit for the Source->LivingWorld pipeline:
created idempotently, progressed through stages, checkpointed at stage
boundaries, resumable after interruption, and terminal once done/failed/
cancelled. Jobs never mutate sources or canon; they only carry progress.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

JobKind = Literal["import", "authoring"]
JobStatus = Literal["created", "running", "done", "failed", "cancelled"]
VALID_STATUSES = ("created", "running", "done", "failed", "cancelled")
TERMINAL_STATUSES = ("done", "failed", "cancelled")
# Ordered pipeline stages for the unified import/authoring job.
JOB_STAGES = (
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
)


@dataclass(frozen=True, slots=True)
class Job:
    """Immutable job record; progress lives in checkpoints, not here."""

    job_id: str
    kind: JobKind
    source_refs: tuple[str, ...]
    version: str
    status: JobStatus = "created"
    stage: str = "registered"
    created_by: str = "system"
    error: str = ""

    def __post_init__(self) -> None:
        if not self.job_id or len(self.job_id) > 64:
            raise ContractError("job_id must be non-empty and <= 64 chars")
        if self.kind not in ("import", "authoring"):
            raise ContractError(f"invalid job kind {self.kind!r}")
        if self.status not in VALID_STATUSES:
            raise ContractError(f"invalid job status {self.status!r}")
        if self.stage not in JOB_STAGES:
            raise ContractError(f"invalid job stage {self.stage!r}")

    @property
    def terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES


@dataclass(frozen=True, slots=True)
class JobCheckpoint:
    """A validated checkpoint: stage + JSON-serializable progress payload."""

    job_id: str
    stage: str
    payload: tuple[tuple[str, str], ...]
    checkpoint_version: int = 1

    def __post_init__(self) -> None:
        if not self.job_id:
            raise ContractError("checkpoint requires job_id")
        if self.stage not in JOB_STAGES:
            raise ContractError(f"invalid checkpoint stage {self.stage!r}")
        if self.checkpoint_version <= 0:
            raise ContractError("checkpoint_version must be positive")

    def to_dict(self) -> dict[str, object]:
        return {
            "job_id": self.job_id,
            "stage": self.stage,
            "payload": dict(self.payload),
            "checkpoint_version": self.checkpoint_version,
        }
