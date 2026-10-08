"""G54E: unified Import/Authoring job checkpoint/resume/idempotency (M51)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.jobs.errors import (
    DuplicateJob,
    InvalidJobTransition,
    JobNotFound,
)
from wanxiang_substrate.jobs.model import JobCheckpoint
from wanxiang_substrate.jobs.service import JobService
from wanxiang_substrate.jobs.store import JobStore


@pytest.fixture()
def service() -> JobService:
    return JobService(JobStore())


@pytest.mark.unit
def test_create_is_idempotent_by_fingerprint(service: JobService) -> None:
    first = service.create("job_1", "import", ("src_a",), "v1")
    second = service.create("job_1", "import", ("src_a",), "v1")
    assert first.job_id == second.job_id
    assert second.status == "created"
    # Same logical job; store holds exactly one record.
    assert service.status("job_1").version == "v1"


@pytest.mark.unit
def test_changed_source_version_creates_new_job(service: JobService) -> None:
    first = service.create("job_1", "import", ("src_a",), "v1")
    second = service.create("job_2", "import", ("src_a",), "v2")
    assert first.job_id != second.job_id


@pytest.mark.unit
def test_duplicate_job_id_rejected(service: JobService) -> None:
    service.create("job_1", "import", ("src_a",), "v1")
    with pytest.raises(DuplicateJob):
        service.create("job_1", "import", ("src_b",), "v1")


@pytest.mark.unit
def test_checkpoint_roundtrip_and_resume(service: JobService) -> None:
    service.create("job_1", "authoring", ("src_a",), "v1")
    service.start("job_1")
    service.checkpoint("job_1", "distilled", {"entities": "12"})
    job, checkpoint = service.resume("job_1")
    assert job.status == "running"
    assert checkpoint is not None
    assert checkpoint.stage == "distilled"
    assert dict(checkpoint.payload) == {"entities": "12"}


@pytest.mark.unit
def test_resume_done_job_is_noop(service: JobService) -> None:
    service.create("job_1", "import", ("src_a",), "v1")
    service.start("job_1")
    service.checkpoint("job_1", "previewed", {"ok": "1"})
    service.finish("job_1")
    job, checkpoint = service.resume("job_1")
    assert job.status == "done"
    assert checkpoint is not None and checkpoint.stage == "previewed"


@pytest.mark.unit
def test_checkpoint_stage_monotonic(service: JobService) -> None:
    service.create("job_1", "import", ("src_a",), "v1")
    service.start("job_1")
    service.checkpoint("job_1", "distilled", {"a": "1"})
    with pytest.raises(InvalidJobTransition):
        service.checkpoint("job_1", "parsed", {"a": "1"})


@pytest.mark.unit
def test_terminal_job_cannot_transition(service: JobService) -> None:
    service.create("job_1", "import", ("src_a",), "v1")
    service.start("job_1")
    service.finish("job_1")
    with pytest.raises(InvalidJobTransition):
        service.start("job_1")


@pytest.mark.unit
def test_failed_job_requires_error(service: JobService) -> None:
    service.create("job_1", "import", ("src_a",), "v1")
    service.start("job_1")
    with pytest.raises(InvalidJobTransition):
        service.fail("job_1", "")
    job = service.fail("job_1", "parse error")
    assert job.status == "failed"
    assert job.error == "parse error"


@pytest.mark.unit
def test_corrupt_checkpoint_rejected(service: JobService) -> None:
    from wanxiang_domain.errors import ContractError

    service.create("job_1", "import", ("src_a",), "v1")
    service.start("job_1")
    # Invalid checkpoint version / unknown stage are corrupt and rejected.
    with pytest.raises(ContractError):
        JobCheckpoint(job_id="job_1", stage="parsed", payload=(("k", "v"),), checkpoint_version=0)
    with pytest.raises(ContractError):
        JobCheckpoint(job_id="job_1", stage="not_a_stage", payload=())
    # Checkpoint on a non-running job is rejected by the store.
    service2 = JobService(JobStore())
    service2.create("job_2", "import", ("src_a",), "v1")
    with pytest.raises(InvalidJobTransition):
        service2.checkpoint("job_2", "parsed", {"k": "v"})


@pytest.mark.unit
def test_missing_job_raises(service: JobService) -> None:
    with pytest.raises(JobNotFound):
        service.status("missing")


@pytest.mark.unit
def test_history_is_append_only(service: JobService) -> None:
    service.create("job_1", "import", ("src_a",), "v1")
    service.start("job_1")
    service.finish("job_1")
    assert service.history("job_1") == ("created", "running", "done")
