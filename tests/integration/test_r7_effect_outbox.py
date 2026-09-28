"""R7 Gate E: the external-effect outbox as a real cross-process reference path.

These tests start ``scripts/r7_effect_sink.py`` as a real subprocess on an
ephemeral localhost port and drive the genuine ``HttpEffectHandler`` against it,
so the durable outbox, the duplicate-suppression policy and the out-of-process
effect provider are exercised together end to end.
"""

from __future__ import annotations

import contextlib
import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Generator
from pathlib import Path
from typing import cast

import pytest
from wanxiang_execution import (
    STATUS_AMBIGUOUS,
    STATUS_APPLIED,
    STATUS_DUPLICATE_SUPPRESSED,
    STATUS_FAILED,
    EffectObservation,
    ExternalEffectIntent,
    ExternalEffectResult,
    HttpEffectHandler,
    Outbox,
    OutboxError,
    OutboxExecutor,
    observe_effect,
)

ROOT = Path(__file__).resolve().parents[2]
SINK_SCRIPT = ROOT / "scripts" / "r7_effect_sink.py"
HEALTH_TIMEOUT_SECONDS = 10.0
HEALTH_POLL_SECONDS = 0.05


def _sink_skip_reason() -> str | None:
    """Return a machine-checkable skip reason when the sink cannot run here."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.bind(("127.0.0.1", 0))
    except OSError:
        return "skip: localhost TCP socket bind unavailable; r7 effect sink cannot start"
    if not SINK_SCRIPT.is_file():
        return f"skip: r7 effect sink script missing at {SINK_SCRIPT}"
    try:
        completed = subprocess.run(
            [sys.executable, "-c", "import sys; sys.exit(0)"],
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return "skip: subprocess spawn unavailable; r7 effect sink cannot start"
    if completed.returncode != 0:
        return "skip: subprocess spawn returned non-zero; r7 effect sink cannot start"
    return None


_SKIP_REASON = _sink_skip_reason()
pytestmark = pytest.mark.skipif(_SKIP_REASON is not None, reason=_SKIP_REASON or "")


def _as_object(value: object) -> dict[str, object]:
    """Narrow a decoded JSON value to a string-keyed object."""
    if not isinstance(value, dict):
        raise AssertionError("expected a JSON object")
    return cast("dict[str, object]", value)


class _Sink:
    """A running reference effect sink subprocess."""

    def __init__(self, process: subprocess.Popen[str], port: int, journal: Path) -> None:
        self.process = process
        self.port = port
        self.journal = journal

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def rows(self) -> list[dict[str, object]]:
        """Read the raw journal rows from disk."""
        if not self.journal.is_file():
            return []
        return [
            _as_object(json.loads(line))
            for line in self.journal.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def applied_rows(self) -> list[dict[str, object]]:
        """Only the rows recording an applied effect."""
        return [row for row in self.rows() if row.get("status") == "applied"]

    def get_json(self, path: str) -> dict[str, object]:
        """GET a JSON object from the sink."""
        with urllib.request.urlopen(self.base_url + path, timeout=5) as response:
            payload = json.loads(response.read())
        return _as_object(payload)


class _DirectedHttpEffectHandler(HttpEffectHandler):
    """The real handler aimed at one sink failure endpoint.

    Request body, headers and response mapping are inherited unchanged; only the
    target path is redirected so the genuine handler can be driven against
    ``/effect/crash``, ``/effect/slow``, ``/effect/ambiguous`` and ``/effect/fail``.
    """

    def __init__(self, base_url: str, path: str, timeout_seconds: float = 5.0) -> None:
        super().__init__(base_url, timeout_seconds)
        self._apply_url = f"{base_url.rstrip('/')}{path}"


class _CountingHandler:
    """Delegate to a handler and count how many times ``apply`` was called."""

    handler_id = "test-counting-handler"

    def __init__(self, inner: HttpEffectHandler) -> None:
        self.inner = inner
        self.calls = 0

    def apply(self, intent: ExternalEffectIntent) -> ExternalEffectResult:
        self.calls += 1
        return self.inner.apply(intent)


@contextlib.contextmanager
def _start_sink(journal: Path) -> Generator[_Sink]:
    """Start the sink subprocess and always terminate it on exit."""
    process = subprocess.Popen(
        [sys.executable, str(SINK_SCRIPT), "--port", "0", "--journal", str(journal)],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout = process.stdout
        if stdout is None:
            raise AssertionError("sink subprocess has no stdout pipe")
        line = stdout.readline()
        if not line:
            stderr = process.stderr.read() if process.stderr is not None else ""
            raise AssertionError(f"sink did not start; stderr={stderr!r}")
        info = json.loads(line)
        sink = _Sink(process, int(info["port"]), journal)
        _await_health(sink)
        yield sink
    finally:
        _terminate(process)


def _await_health(sink: _Sink) -> None:
    deadline = time.monotonic() + HEALTH_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        if sink.process.poll() is not None:
            raise AssertionError(f"sink exited early with code {sink.process.poll()}")
        try:
            health = sink.get_json("/health")
        except (urllib.error.URLError, ConnectionError, OSError):
            time.sleep(HEALTH_POLL_SECONDS)
            continue
        if health.get("ok") is True:
            return
        time.sleep(HEALTH_POLL_SECONDS)
    raise AssertionError("sink did not become healthy in time")


def _terminate(process: subprocess.Popen[str]) -> None:
    if process.poll() is None:
        process.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=5)
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
    for stream in (process.stdout, process.stderr):
        if stream is not None:
            stream.close()


def _intent(intent_id: str = "intent_1", key: str = "key_1") -> ExternalEffectIntent:
    return ExternalEffectIntent(
        intent_id=intent_id,
        worldline_id="wld_r7",
        target="effect.example",
        operation="charge_card",
        payload_digest="sha256:deadbeef",
        idempotency_key=key,
        requested_by="r7-integration",
    )


def test_full_chain_from_intent_to_observation_applies_effect_once(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    with _start_sink(journal) as sink:
        intent = _intent()
        outbox = Outbox(outbox_path)
        outbox.append(intent)
        result = OutboxExecutor(outbox, HttpEffectHandler(sink.base_url)).execute(intent)
        observation = observe_effect(intent, result)

        assert result.status == STATUS_APPLIED
        assert result.external_ref == f"effect:{intent.idempotency_key}"
        assert len(sink.applied_rows()) == 1

        assert isinstance(observation, EffectObservation)
        assert observation.status == STATUS_APPLIED
        assert observation.worldline_id == intent.worldline_id
        assert observation.requires_manual_reconciliation is False
        assert observation.digest() == observe_effect(intent, result).digest()

        # Proposal-only: the observation holds no path to canonical history.
        assert not any(hasattr(observation, name) for name in ("append", "commit", "record_event"))


def test_duplicate_delivery_applies_effect_exactly_once(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    with _start_sink(journal) as sink:
        intent = _intent()
        Outbox(outbox_path).append(intent)
        first = OutboxExecutor(Outbox(outbox_path), HttpEffectHandler(sink.base_url)).execute(
            intent
        )
        rebuilt = OutboxExecutor(Outbox(outbox_path), HttpEffectHandler(sink.base_url))
        second = rebuilt.execute(intent)

        assert first.status == STATUS_APPLIED
        assert second.status == STATUS_DUPLICATE_SUPPRESSED
        assert len(sink.applied_rows()) == 1


def test_crash_before_answer_is_ambiguous_and_not_resent_after_restart(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    intent = _intent()
    Outbox(outbox_path).append(intent)

    with _start_sink(journal) as sink:
        crash = _DirectedHttpEffectHandler(sink.base_url, "/effect/crash")
        result = OutboxExecutor(Outbox(outbox_path), crash).execute(intent)
        observation = observe_effect(intent, result)

        assert result.status == STATUS_AMBIGUOUS
        assert observation.requires_manual_reconciliation is True
        assert len(sink.applied_rows()) == 1

    with _start_sink(journal) as restarted:
        executor = OutboxExecutor(
            Outbox(outbox_path), _DirectedHttpEffectHandler(restarted.base_url, "/effect")
        )
        again = executor.execute(intent)

        assert again.status == STATUS_AMBIGUOUS
        assert executor.ambiguous() == (intent,)
        assert len(restarted.applied_rows()) == 1


def test_slow_endpoint_times_out_to_ambiguous_without_retry(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    with _start_sink(journal) as sink:
        intent = _intent()
        Outbox(outbox_path).append(intent)
        slow = _CountingHandler(
            _DirectedHttpEffectHandler(sink.base_url, "/effect/slow", timeout_seconds=1.0)
        )
        executor = OutboxExecutor(Outbox(outbox_path), slow, max_attempts=3)
        result = executor.execute(intent)
        observation = observe_effect(intent, result)

        assert result.status == STATUS_AMBIGUOUS
        assert observation.requires_manual_reconciliation is True
        assert slow.calls == 1
        assert sink.applied_rows() == []

        again = executor.execute(intent)
        assert again.status == STATUS_AMBIGUOUS
        assert slow.calls == 1


def test_ambiguous_response_requires_explicit_reconciliation(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    with _start_sink(journal) as sink:
        intent = _intent()
        Outbox(outbox_path).append(intent)
        handler = _DirectedHttpEffectHandler(sink.base_url, "/effect/ambiguous")
        executor = OutboxExecutor(Outbox(outbox_path), handler)
        result = executor.execute(intent)

        assert result.status == STATUS_AMBIGUOUS
        assert observe_effect(intent, result).requires_manual_reconciliation is True
        assert len(sink.applied_rows()) == 1

        with pytest.raises(OutboxError):
            executor.reconcile(intent.intent_id, STATUS_APPLIED, None, "   ")
        with pytest.raises(OutboxError):
            executor.reconcile(intent.intent_id, STATUS_AMBIGUOUS, None, "still unsure")

        resolution = executor.reconcile(
            intent.intent_id, STATUS_APPLIED, "ext-9", "operator confirmed delivery"
        )
        assert resolution.status == STATUS_APPLIED
        assert resolution.external_ref == "ext-9"
        assert executor.pending() == ()
        assert executor.ambiguous() == ()


def test_new_executor_over_same_journal_reconstructs_state(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    applied_intent = _intent("intent_ok", "key_ok")
    ambiguous_intent = _intent("intent_amb", "key_amb")

    with _start_sink(journal) as sink:
        store = Outbox(outbox_path)
        store.append(applied_intent)
        store.append(ambiguous_intent)
        OutboxExecutor(Outbox(outbox_path), HttpEffectHandler(sink.base_url)).execute(
            applied_intent
        )
        OutboxExecutor(
            Outbox(outbox_path),
            _DirectedHttpEffectHandler(sink.base_url, "/effect/ambiguous"),
        ).execute(ambiguous_intent)

    reopened = OutboxExecutor(Outbox(outbox_path), HttpEffectHandler("http://127.0.0.1:1"))
    assert reopened.pending() == (ambiguous_intent,)
    assert reopened.ambiguous() == (ambiguous_intent,)
    assert applied_intent not in reopened.pending()


def test_server_error_is_failed_and_retryable_within_budget(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    with _start_sink(journal) as sink:
        intent = _intent()
        Outbox(outbox_path).append(intent)
        counting = _CountingHandler(_DirectedHttpEffectHandler(sink.base_url, "/effect/fail"))
        executor = OutboxExecutor(Outbox(outbox_path), counting, max_attempts=3)
        result = executor.execute(intent)

        assert result.status == STATUS_FAILED
        assert counting.calls == 3
        assert sink.applied_rows() == []

        again = executor.execute(intent)
        assert again.status == STATUS_FAILED
        assert counting.calls == 3


def test_request_and_journal_carry_identifiers_only(tmp_path: Path) -> None:
    journal = tmp_path / "sink.jsonl"
    outbox_path = tmp_path / "outbox.jsonl"
    payload_secret = "SECRET-CARD-4111"
    with _start_sink(journal) as sink:
        intent = _intent()
        Outbox(outbox_path).append(intent)
        OutboxExecutor(Outbox(outbox_path), HttpEffectHandler(sink.base_url)).execute(intent)

        rows = sink.applied_rows()
        assert len(rows) == 1
        assert set(rows[0]) == {"status", "key", "intentId", "operation", "at"}
        assert rows[0]["key"] == intent.idempotency_key
        assert rows[0]["intentId"] == intent.intent_id
        assert rows[0]["operation"] == intent.operation
        journal_text = journal.read_text(encoding="utf-8")
        assert payload_secret not in journal_text
        assert intent.payload_digest not in journal_text
        outbox_text = outbox_path.read_text(encoding="utf-8")
        assert intent.payload_digest in outbox_text
        assert payload_secret not in outbox_text
