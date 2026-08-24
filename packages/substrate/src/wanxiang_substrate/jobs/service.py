"""Job service: idempotent create + checkpoint/resume lifecycle (G54E).

Resume semantics: a running job resumes from its latest checkpoint (crash
recovery never repeats completed stages); a done job resumes as a no-op; a
created job is started on first resume.
"""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_substrate.jobs.errors import InvalidJobTransition, JobNotFound
from wanxiang_substrate.jobs.model import Job, JobCheckpoint, JobKind
from wanxiang_substrate.jobs.store import JobStore


class JobService:
    """Unified import/authoring job lifecycle over a JobStore."""

    def __init__(self, store: JobStore) -> None:
        self._store = store

    def create(
        self,
        job_id: str,
        kind: JobKind,
        source_refs: tuple[str, ...],
        version: str,
        created_by: str = "system",
    ) -> Job:
        return self._store.create(job_id, kind, source_refs, version, created_by)

    def start(self, job_id: str) -> Job:
        job = self._store.require(job_id)
        if job.status == "running":
            return job
        return self._store.transition(job_id, "running")

    def checkpoint(self, job_id: str, stage: str, payload: Mapping[str, str]) -> JobCheckpoint:
        pairs = tuple(sorted((str(k), str(v)) for k, v in payload.items()))
        return self._store.save_checkpoint(JobCheckpoint(job_id=job_id, stage=stage, payload=pairs))

    def resume(self, job_id: str) -> tuple[Job, JobCheckpoint | None]:
        job = self._store.require(job_id)
        if job.status in ("created", "cancelled"):
            job = self.start(job_id)
        checkpoint = self._store.load_checkpoint(job_id)
        return job, checkpoint

    def finish(self, job_id: str) -> Job:
        job = self._store.require(job_id)
        if job.status == "done":
            return job
        if job.status != "running":
            raise InvalidJobTransition(f"cannot finish job {job_id!r} in state {job.status}")
        return self._store.transition(job_id, "done")

    def fail(self, job_id: str, error: str) -> Job:
        job = self._store.require(job_id)
        if job.status in ("done", "cancelled", "failed"):
            raise InvalidJobTransition(f"job {job_id!r} is already terminal")
        return self._store.transition(job_id, "failed", error=error)

    def cancel(self, job_id: str) -> Job:
        job = self._store.require(job_id)
        if job.status == "cancelled":
            return job
        if job.status == "done":
            raise InvalidJobTransition("cannot cancel a done job")
        return self._store.transition(job_id, "cancelled")

    def history(self, job_id: str) -> tuple[str, ...]:
        return self._store.history(job_id)

    def status(self, job_id: str) -> Job:
        try:
            return self._store.require(job_id)
        except JobNotFound:
            raise JobNotFound(f"job {job_id!r} not found") from None
