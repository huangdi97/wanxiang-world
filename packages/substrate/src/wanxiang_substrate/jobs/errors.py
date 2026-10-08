"""Import/Authoring job error taxonomy (G54E)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class JobError(WanxiangError):
    """Base error for import/authoring job failures."""

    code = "job_error"


class JobNotFound(JobError):
    code = "job_not_found"


class DuplicateJob(JobError):
    code = "duplicate_job"


class InvalidJobTransition(JobError):
    code = "invalid_job_transition"


class CorruptJobCheckpoint(JobError):
    code = "corrupt_job_checkpoint"
