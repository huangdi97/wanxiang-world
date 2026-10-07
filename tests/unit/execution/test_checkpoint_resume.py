"""R7 execution checkpoint/resume qualification."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from wanxiang_execution import (
    CheckpointedProcessRunner,
    ExecutionPolicy,
    ExecutionRequest,
    FileExecutionCheckpointStore,
    LocalProcessProvider,
)
from wanxiang_execution.errors import ExecutionError


class _CountingProcessProvider(LocalProcessProvider):
    def __init__(self) -> None:
        self.calls = 0

    def run(self, request: ExecutionRequest, workspace_dir: Path):  # type: ignore[no-untyped-def]
        self.calls += 1
        return super().run(request, workspace_dir)


def _request(execution_id: str, value: str = "hello") -> ExecutionRequest:
    return ExecutionRequest(
        execution_id=execution_id,
        capability_id="cap.r7.resume",
        capability_version="1.0.0",
        command=(sys.executable, "-c", f"print({value!r})"),
        input_refs=("sha256:input",),
        policy=ExecutionPolicy.default_untrusted(),
    )


def test_completed_request_fast_forwards_without_reexecution(tmp_path: Path) -> None:
    provider = _CountingProcessProvider()
    store = FileExecutionCheckpointStore(tmp_path / "checkpoints")
    runner = CheckpointedProcessRunner(provider, store)
    request = _request("resume-same")

    first = runner.run(request, tmp_path / "work")
    second = runner.run(request, tmp_path / "work")

    assert provider.calls == 1
    assert first.stdout_text == "hello\n"
    assert second.stdout_text == first.stdout_text
    assert first.trace.snapshot_ref is not None
    assert first.trace.resume_ref is None
    assert second.trace.snapshot_ref == first.trace.snapshot_ref
    assert second.trace.resume_ref == first.trace.snapshot_ref
    assert second.observation["resumed"] is True
    assert second.observation["proposal_only"] is True


def test_request_drift_does_not_reuse_checkpoint(tmp_path: Path) -> None:
    provider = _CountingProcessProvider()
    store = FileExecutionCheckpointStore(tmp_path / "checkpoints")
    runner = CheckpointedProcessRunner(provider, store)

    first = runner.run(_request("resume-drift", "first"), tmp_path / "work")
    second = runner.run(_request("resume-drift", "second"), tmp_path / "work")

    assert provider.calls == 2
    assert first.stdout_text == "first\n"
    assert second.stdout_text == "second\n"
    assert first.trace.snapshot_ref != second.trace.snapshot_ref


def test_corrupt_checkpoint_blob_fails_closed(tmp_path: Path) -> None:
    provider = _CountingProcessProvider()
    root = tmp_path / "checkpoints"
    store = FileExecutionCheckpointStore(root)
    runner = CheckpointedProcessRunner(provider, store)
    request = _request("resume-corrupt")
    first = runner.run(request, tmp_path / "work")
    assert first.trace.snapshot_ref is not None

    checkpoint_id = first.trace.snapshot_ref.split(":", 1)[1]
    payload = json.loads((root / "checkpoints" / f"{checkpoint_id}.json").read_text())
    stdout_blob = str(payload["stdout_blob"])
    (root / "blobs" / stdout_blob).write_text("tampered", encoding="utf-8")

    with pytest.raises(ExecutionError, match="blob digest mismatch"):
        runner.run(request, tmp_path / "work")
    assert provider.calls == 1
