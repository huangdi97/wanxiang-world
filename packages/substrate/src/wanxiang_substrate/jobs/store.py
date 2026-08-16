"""Import/Authoring job store with idempotency + checkpoints (G54E).

Job creation is idempotent on (kind, source_refs, version): re-creating the
same logical job returns the existing record, so duplicate command retries
never duplicate effects. Checkpoints are published atomically and must be
stage-monotonic; status transitions are validated and history is append-only.
"""

from __future__ import annotations

from wanxiang_substrate.jobs.errors import (
    CorruptJobCheckpoint,
    DuplicateJob,
    InvalidJobTransition,
    JobNotFound,
)
from wanxiang_substrate.jobs.model import (
    JOB_STAGES,
    TERMINAL_STATUSES,
    Job,
    JobCheckpoint,
    JobKind,
    JobStatus,
)

_VALID_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "created": ("running", "cancelled", "failed"),
    "running": ("done", "failed", "cancelled"),
    "done": (),
    "failed": (),
    "cancelled": (),
}


class JobStore:
    """In-memory job store; single owner of job identity and checkpoints."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._by_fingerprint: dict[tuple[object, ...], str] = {}
        self._checkpoints: dict[str, tuple[JobCheckpoint, ...]] = {}
        self._history: dict[str, tuple[str, ...]] = {}

    def create(
        self,
        job_id: str,
        kind: JobKind,
        source_refs: tuple[str, ...],
        version: str,
        created_by: str = "system",
    ) -> Job:
        fingerprint = (kind, tuple(source_refs), version)
        existing_id = self._by_fingerprint.get(fingerprint)
        if existing_id is not None:
            return self.require(existing_id)
        if job_id in self._jobs:
            raise DuplicateJob(f"job {job_id!r} already registered")
        job = Job(
            job_id=job_id,
            kind=kind,
            source_refs=tuple(source_refs),
            version=version,
            created_by=created_by,
        )
        self._jobs[job_id] = job
        self._by_fingerprint[fingerprint] = job_id
        self._history[job_id] = ("created",)
        return job

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def require(self, job_id: str) -> Job:
        job = self.get(job_id)
        if job is None:
            raise JobNotFound(f"job {job_id!r} not found")
        return job

    def transition(self, job_id: str, status: JobStatus, *, error: str = "") -> Job:
        job = self.require(job_id)
        if status not in _VALID_TRANSITIONS[job.status]:
            raise InvalidJobTransition(f"job {job_id!r} cannot move from {job.status} to {status}")
        if status in TERMINAL_STATUSES and not error and status == "failed":
            raise InvalidJobTransition("failed job requires an error message")
        updated = Job(
            job_id=job.job_id,
            kind=job.kind,
            source_refs=job.source_refs,
            version=job.version,
            status=status,
            stage=job.stage,
            created_by=job.created_by,
            error=error,
        )
        self._jobs[job_id] = updated
        self._history[job_id] = self._history[job_id] + (status,)
        return updated

    def save_checkpoint(self, checkpoint: JobCheckpoint) -> JobCheckpoint:
        job = self.require(checkpoint.job_id)
        if job.status != "running":
            raise InvalidJobTransition(
                f"checkpoint requires running job; {checkpoint.job_id!r} is {job.status}"
            )
        self._validate_payload(checkpoint)
        history = self._checkpoints.setdefault(checkpoint.job_id, ())
        latest = history[-1] if history else None
        if latest is not None and JOB_STAGES.index(checkpoint.stage) < JOB_STAGES.index(job.stage):
            raise InvalidJobTransition(
                f"checkpoint stage {checkpoint.stage} regresses job stage {job.stage}"
            )
        # Atomic publish: the record becomes visible only after all validation.
        self._checkpoints[checkpoint.job_id] = history + (checkpoint,)
        self._jobs[checkpoint.job_id] = Job(
            job_id=job.job_id,
            kind=job.kind,
            source_refs=job.source_refs,
            version=job.version,
            status=job.status,
            stage=checkpoint.stage,
            created_by=job.created_by,
            error=job.error,
        )
        return checkpoint

    def load_checkpoint(self, job_id: str) -> JobCheckpoint | None:
        self.require(job_id)
        history = self._checkpoints.get(job_id, ())
        return history[-1] if history else None

    def checkpoint_history(self, job_id: str) -> tuple[JobCheckpoint, ...]:
        self.require(job_id)
        return self._checkpoints.get(job_id, ())

    def history(self, job_id: str) -> tuple[str, ...]:
        self.require(job_id)
        return self._history[job_id]

    def _validate_payload(self, checkpoint: JobCheckpoint) -> None:
        import json

        try:
            json.dumps(checkpoint.to_dict())
        except (TypeError, ValueError) as exc:
            raise CorruptJobCheckpoint(
                f"checkpoint payload for {checkpoint.job_id!r} is not JSON-safe"
            ) from exc
