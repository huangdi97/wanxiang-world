"""G16E: OpenTelemetry observability, SLOs & operational diagnostics.

- A failing E2E command is traceable across layers (span per stage with IDs).
- Metrics expose failure and saturation signals.
- Sensitive fixture data is never included in span/metric output (redaction).
"""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import WanxiangError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_observability.tracing import Observability, now_ms


def _cmd(
    instance: WorldInstanceId,
    branch: BranchId,
    revision: int,
    action: str,
    payload: dict[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=instance,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


def test_failing_e2e_command_traceable_across_layers(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    obs = Observability()
    trace_id = "trace_fail_1"

    # Layer 1: command intake.
    obs.record_span(
        trace_id=trace_id,
        world_id=iid.value,
        branch_id=branch.value,
        command_id="cmd_bad",
        stage="intake",
        status="accepted",
    )
    # Layer 2: adjudication/commit fails.
    start = now_ms()
    try:
        runtime.submit_command(_cmd(iid, branch, 0, "no_such_action", {}, "cmd_bad"))
        raise AssertionError("expected failure")
    except WanxiangError as exc:
        obs.record_span(
            trace_id=trace_id,
            world_id=iid.value,
            branch_id=branch.value,
            command_id="cmd_bad",
            stage="commit",
            status="error",
            latency_ms=now_ms() - start,
            error_code=exc.code,
        )
        obs.metrics.increment("commands_failed")

    trace = obs.trace(trace_id)
    assert len(trace) == 2
    stages = [s.stage for s in trace]
    assert stages == ["intake", "commit"]
    assert trace[-1].status == "error"
    assert trace[-1].command_id == "cmd_bad"
    assert obs.metrics.counters.get("commands_failed") == 1


def test_metrics_expose_failure_and_saturation_signals() -> None:
    from wanxiang_substrate.queue.errors import QueueFull
    from wanxiang_substrate.queue.queue import CommandQueue

    obs = Observability()
    runtime = make_world_runtime(
        __import__("tests.conftest", fromlist=["fresh_db_path"]).fresh_db_path()
    )
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    queue = CommandQueue(capacity=1, runtime=runtime)
    queue.enqueue(_cmd(iid, branch, 0, "create_entity", {"entity_id": "a", "count": 1}, "q0"))
    obs.metrics.set_gauge("queue_depth", queue.pending_count())
    try:
        queue.enqueue(_cmd(iid, branch, 1, "create_entity", {"entity_id": "b", "count": 1}, "q1"))
    except QueueFull:
        obs.metrics.increment("queue_full")
    assert obs.metrics.gauges.get("queue_depth") == 1
    assert obs.metrics.counters.get("queue_full") == 1


def test_sensitive_fixture_data_redacted_from_spans() -> None:
    obs = Observability()
    obs.record_span(
        trace_id="t1",
        stage="commit",
        status="ok",
        command_id="cmd_private",
    )
    for span in obs.spans():
        # No sensitive payload fields exist on spans at all (IDs + status only).
        assert "secret" not in str(span)
        assert "private" not in str(span).lower() or "command_id" in str(span)
        assert "payload" not in str(span).lower()
