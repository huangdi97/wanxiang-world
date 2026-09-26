"""Trace digests, environment hashing and the not-history invariant."""

from __future__ import annotations

import pytest
from wanxiang_execution import (
    EXIT_STATUS_COMPLETED,
    ExecutionClass,
    ExecutionTrace,
    TrustLevel,
    environment_hash,
    trace_digest,
)
from wanxiang_execution import trace as trace_module


def _make_trace(exit_code: int = 0) -> ExecutionTrace:
    return ExecutionTrace(
        execution_id="exec_trace_1",
        capability_id="cap_trace",
        capability_version="1.0.0",
        provider_id="execution-local-process",
        provider_version="1.0.0",
        execution_class=ExecutionClass.PROCESS,
        trust=TrustLevel.UNTRUSTED,
        environment_hash="a" * 64,
        input_refs=("in-digest",),
        commands=(("python", "-c", "pass"),),
        output_refs=("out-digest",),
        exit_status=EXIT_STATUS_COMPLETED,
        exit_code=exit_code,
        wall_ms=5,
        stdout_bytes=0,
        stderr_bytes=0,
        stdout_digest="b" * 64,
        stderr_digest="c" * 64,
        snapshot_ref=None,
        resume_ref=None,
        isolation={
            "process": "enforced",
            "filesystem_scratch": "enforced",
            "environment": "scrubbed",
            "network": "not_enforced",
            "memory": "not_enforced",
        },
    )


@pytest.mark.unit
def test_trace_digest_is_stable_across_identical_constructions() -> None:
    assert _make_trace() == _make_trace()
    assert trace_digest(_make_trace()) == trace_digest(_make_trace())


@pytest.mark.unit
def test_trace_digest_changes_when_a_field_changes() -> None:
    assert trace_digest(_make_trace(exit_code=0)) != trace_digest(_make_trace(exit_code=1))


@pytest.mark.unit
def test_environment_hash_is_order_insensitive_and_value_sensitive() -> None:
    base = environment_hash({"ALPHA": "1", "BETA": "2"})
    assert environment_hash({"BETA": "2", "ALPHA": "1"}) == base
    assert environment_hash({"ALPHA": "1", "BETA": "3"}) != base


@pytest.mark.unit
def test_trace_module_documents_that_a_trace_is_not_world_history() -> None:
    module_doc = " ".join((trace_module.__doc__ or "").split())
    class_doc = " ".join((ExecutionTrace.__doc__ or "").split())
    assert "NOT world history" in module_doc
    assert "can never be appended to canonical history" in module_doc
    assert "can never be appended to canonical history" in class_doc
