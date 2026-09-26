"""Append-only outbox semantics for irreversible external effects."""

from __future__ import annotations

from pathlib import Path

import pytest
from wanxiang_execution import (
    ATTEMPT_MARKER_STATUS,
    STATUS_AMBIGUOUS,
    STATUS_APPLIED,
    STATUS_DUPLICATE_SUPPRESSED,
    STATUS_FAILED,
    ExternalEffectIntent,
    ExternalEffectResult,
    Outbox,
    OutboxError,
    OutboxExecutor,
)


def _intent(intent_id: str = "intent_1", idempotency_key: str = "key_1") -> ExternalEffectIntent:
    return ExternalEffectIntent(
        intent_id=intent_id,
        worldline_id="wld_test",
        target="mail.example",
        operation="send_email",
        payload_digest="sha256:abc",
        idempotency_key=idempotency_key,
        requested_by="tester",
    )


class _ScriptedHandler:
    """Test handler that returns scripted statuses and counts calls."""

    handler_id = "test-handler"

    def __init__(self, *statuses: str) -> None:
        self.statuses = list(statuses) or [STATUS_APPLIED]
        self.calls: list[ExternalEffectIntent] = []

    def apply(self, intent: ExternalEffectIntent) -> ExternalEffectResult:
        self.calls.append(intent)
        index = min(len(self.calls) - 1, len(self.statuses) - 1)
        status = self.statuses[index]
        return ExternalEffectResult(
            intent_id=intent.intent_id,
            idempotency_key=intent.idempotency_key,
            status=status,
            external_ref="ext-1" if status == STATUS_APPLIED else None,
            detail=f"scripted {status}",
        )


@pytest.mark.unit
def test_appended_intents_survive_reopening_in_order(tmp_path: Path) -> None:
    path = tmp_path / "outbox.jsonl"
    first = _intent("intent_1", "key_1")
    second = _intent("intent_2", "key_2")

    outbox = Outbox(path)
    outbox.append(first)
    outbox.append(second)

    reopened = Outbox(path)
    assert reopened.intents() == (first, second)
    assert len(path.read_text(encoding="utf-8").splitlines()) == 2


@pytest.mark.unit
def test_duplicate_idempotency_key_calls_handler_once(tmp_path: Path) -> None:
    outbox = Outbox(tmp_path / "outbox.jsonl")
    intent = _intent()
    outbox.append(intent)
    handler = _ScriptedHandler()
    executor = OutboxExecutor(outbox, handler)

    first = executor.execute(intent)
    second = executor.execute(intent)

    assert first.status == STATUS_APPLIED
    assert second.status == STATUS_DUPLICATE_SUPPRESSED
    assert second.external_ref == first.external_ref
    assert len(handler.calls) == 1
    assert executor.pending() == ()


@pytest.mark.unit
def test_ambiguous_result_is_not_retried_and_is_listed(tmp_path: Path) -> None:
    outbox = Outbox(tmp_path / "outbox.jsonl")
    intent = _intent()
    outbox.append(intent)
    handler = _ScriptedHandler(STATUS_AMBIGUOUS)
    executor = OutboxExecutor(outbox, handler)

    first = executor.execute(intent)
    second = executor.execute(intent)

    assert first.status == STATUS_AMBIGUOUS
    assert second.status == STATUS_AMBIGUOUS
    assert len(handler.calls) == 1
    assert executor.ambiguous() == (intent,)
    assert executor.pending() == (intent,)


@pytest.mark.unit
def test_reconcile_records_resolution_and_clears_pending(tmp_path: Path) -> None:
    outbox = Outbox(tmp_path / "outbox.jsonl")
    intent = _intent()
    outbox.append(intent)
    executor = OutboxExecutor(outbox, _ScriptedHandler(STATUS_AMBIGUOUS))
    executor.execute(intent)

    resolution = executor.reconcile(
        intent.intent_id, STATUS_APPLIED, "ext-42", "operator confirmed delivery"
    )

    assert resolution.status == STATUS_APPLIED
    assert resolution.external_ref == "ext-42"
    assert executor.pending() == ()
    assert executor.ambiguous() == ()
    attempts = [record for record in outbox.attempts() if record.intent_id == intent.intent_id]
    assert attempts[-1].status == STATUS_APPLIED


@pytest.mark.unit
def test_reconcile_unknown_intent_raises(tmp_path: Path) -> None:
    executor = OutboxExecutor(Outbox(tmp_path / "outbox.jsonl"), _ScriptedHandler())

    with pytest.raises(OutboxError):
        executor.reconcile("intent_missing", STATUS_APPLIED, None, "unknown intent")


@pytest.mark.unit
def test_failing_handler_retries_record_every_attempt(tmp_path: Path) -> None:
    outbox = Outbox(tmp_path / "outbox.jsonl")
    intent = _intent()
    outbox.append(intent)
    handler = _ScriptedHandler(STATUS_FAILED)
    executor = OutboxExecutor(outbox, handler, max_attempts=3)

    result = executor.execute(intent)

    assert result.status == STATUS_FAILED
    assert len(handler.calls) == 3
    records = [record for record in outbox.attempts() if record.idempotency_key == "key_1"]
    markers = [record for record in records if record.status == ATTEMPT_MARKER_STATUS]
    results = [record for record in records if record.status == STATUS_FAILED]
    assert len(markers) == 3
    assert len(results) == 3

    again = executor.execute(intent)
    assert again.status == STATUS_FAILED
    assert len(handler.calls) == 3


@pytest.mark.unit
def test_attempt_marker_is_recorded_before_handler_runs(tmp_path: Path) -> None:
    outbox = Outbox(tmp_path / "outbox.jsonl")
    intent = _intent()
    outbox.append(intent)
    marker_seen_before_result: list[bool] = []

    class _ProbingHandler:
        handler_id = "probe-handler"

        def apply(self, intent: ExternalEffectIntent) -> ExternalEffectResult:
            marker_seen_before_result.append(
                any(
                    record.status == ATTEMPT_MARKER_STATUS and record.attempt_no == 1
                    for record in outbox.attempts()
                )
            )
            return ExternalEffectResult(
                intent_id=intent.intent_id,
                idempotency_key=intent.idempotency_key,
                status=STATUS_APPLIED,
                external_ref="ext-1",
                detail="probed",
            )

    result = OutboxExecutor(outbox, _ProbingHandler()).execute(intent)

    assert result.status == STATUS_APPLIED
    assert marker_seen_before_result == [True]


@pytest.mark.unit
def test_intent_requires_non_empty_fields() -> None:
    with pytest.raises(OutboxError) as excinfo:
        ExternalEffectIntent(
            intent_id="",
            worldline_id="wld_test",
            target="mail.example",
            operation="send_email",
            payload_digest="sha256:abc",
            idempotency_key="key_1",
        )
    assert "intent_id" in str(excinfo.value)
