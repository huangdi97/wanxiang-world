"""Checkpoint/resume for long parses (G56F).

Reuses the unified JobStore (G54E): a long parse is a job whose progress is
checkpointed at batch boundaries and published atomically; interruption
resumes from the latest checkpoint without redoing completed segments.
"""

from __future__ import annotations

from wanxiang_substrate.jobs.model import Job, JobCheckpoint
from wanxiang_substrate.jobs.service import JobService


class ParseCheckpointService:
    """Wraps JobService with parse-specific progress checkpoints."""

    def __init__(self, jobs: JobService) -> None:
        self._jobs = jobs

    def begin(self, source_id: str, version: str) -> Job:
        job = self._jobs.create(
            f"parse:{source_id}:{version}",
            "import",
            (source_id,),
            version,
        )
        return self._jobs.start(job.job_id)

    def checkpoint(
        self,
        job_id: str,
        *,
        parsed_batches: int,
        next_index: int,
        total_batches: int,
    ) -> JobCheckpoint:
        return self._jobs.checkpoint(
            job_id,
            "parsed",
            {
                "parsed_batches": str(parsed_batches),
                "next_index": str(next_index),
                "total_batches": str(total_batches),
            },
        )

    def resume(self, job_id: str) -> tuple[Job, dict[str, int] | None]:
        job, checkpoint = self._jobs.resume(job_id)
        if checkpoint is None:
            return job, None
        payload = dict(checkpoint.payload)
        return job, {
            "parsed_batches": int(payload.get("parsed_batches", "0")),
            "next_index": int(payload.get("next_index", "0")),
            "total_batches": int(payload.get("total_batches", "0")),
        }

    def complete(self, job_id: str) -> Job:
        return self._jobs.finish(job_id)

    def fail(self, job_id: str, error: str) -> Job:
        return self._jobs.fail(job_id, error)
