"""G56E/G56F: Incremental parsing + checkpoint resume (M53)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.jobs.service import JobService
from wanxiang_substrate.jobs.store import JobStore
from wanxiang_substrate.parsing.checkpoint import ParseCheckpointService
from wanxiang_substrate.parsing.incremental import IncrementalParser, changed_segments
from wanxiang_substrate.sources.adapter import IngestResult


def _result(content: str, fmt: str = "text") -> IngestResult:
    return IngestResult(source_id="s1", kind=fmt, content=content, detected_format=fmt)


@pytest.mark.unit
def test_parse_is_cached_by_content() -> None:
    parser = IncrementalParser()
    first, cached1 = parser.parse(_result("# One\n\nbody"), source_id="s1", version="1")
    second, cached2 = parser.parse(_result("# One\n\nbody"), source_id="s1", version="1")
    assert cached1 is False
    assert cached2 is True
    assert first.document_id == second.document_id


@pytest.mark.unit
def test_changed_content_reparses() -> None:
    parser = IncrementalParser()
    _first, _ = parser.parse(_result("# One\n\nbody"), source_id="s1", version="1")
    changed, cached = parser.parse(_result("# One\n\nCHANGED"), source_id="s1", version="1")
    assert cached is False
    assert any("CHANGED" in n.text for n in changed.nodes)


@pytest.mark.unit
def test_version_change_invalidates() -> None:
    parser = IncrementalParser()
    first, _ = parser.parse(_result("# One\n\nbody"), source_id="s1", version="1")
    assert parser.invalidate("s1") >= 1
    second, cached = parser.parse(_result("# One\n\nbody"), source_id="s1", version="2")
    assert cached is False
    assert first.document_id != second.document_id


@pytest.mark.unit
def test_changed_segments_diff() -> None:
    parser = IncrementalParser()
    before, _ = parser.parse(_result("# One\n\nalpha"), source_id="s1", version="1")
    after, _ = parser.parse(_result("# One\n\nbeta"), source_id="s1", version="1")
    changed = changed_segments(before, after)
    assert changed  # at least the paragraph that changed


@pytest.mark.unit
def test_checkpoint_resume_roundtrip() -> None:
    service = ParseCheckpointService(JobService(JobStore()))
    job = service.begin("src_book", "v1")
    service.checkpoint(job.job_id, parsed_batches=3, next_index=4, total_batches=10)
    resumed_job, progress = service.resume(job.job_id)
    assert resumed_job.status == "running"
    assert progress == {"parsed_batches": 3, "next_index": 4, "total_batches": 10}


@pytest.mark.unit
def test_checkpoint_complete_and_fail() -> None:
    service = ParseCheckpointService(JobService(JobStore()))
    job = service.begin("src_book", "v1")
    service.checkpoint(job.job_id, parsed_batches=10, next_index=10, total_batches=10)
    done = service.complete(job.job_id)
    assert done.status == "done"
    service2 = ParseCheckpointService(JobService(JobStore()))
    job2 = service2.begin("src_book2", "v1")
    failed = service2.fail(job2.job_id, "parse crash")
    assert failed.status == "failed"
    assert failed.error == "parse crash"
