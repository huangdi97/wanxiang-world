"""Bounded, idempotent, per-branch command queue (G06B).

Commands are enqueued and drained serially per branch. M1 idempotency is
preserved: duplicate command ids across retries are recognized and surfaced as
`duplicate` without a second effect. Conflicting expected revisions surface as
`conflict`. Backpressure is bounded by the queue capacity.
"""

from __future__ import annotations

from collections import deque

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope

from wanxiang_substrate.queue.errors import DuplicateQueuedCommand, QueueFull
from wanxiang_substrate.queue.model import QueuedCommand, SubmissionResult


class CommandQueue:
    """Per-instance/branch intake with dedup, ordering and backpressure."""

    def __init__(self, capacity: int = 64, runtime: WorldRuntime | None = None) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._runtime = runtime
        self._queue: deque[QueuedCommand] = deque()
        self._enqueued: dict[str, QueuedCommand] = {}
        self._processed: dict[str, SubmissionResult] = {}
        self._seq = 0

    def attach(self, runtime: WorldRuntime) -> None:
        self._runtime = runtime

    def enqueue(self, envelope: CommandEnvelope) -> QueuedCommand:
        if (
            envelope.command_id.value in self._enqueued
            or envelope.command_id.value in self._processed
        ):
            raise DuplicateQueuedCommand(
                f"command {envelope.command_id.value!r} already queued or processed"
            )
        if len(self._queue) >= self._capacity:
            raise QueueFull("command queue is full; backpressure applied")
        self._seq += 1
        queued = QueuedCommand(envelope=envelope, enqueue_seq=self._seq)
        self._queue.append(queued)
        self._enqueued[envelope.command_id.value] = queued
        return queued

    def drain(self) -> tuple[SubmissionResult, ...]:
        """Submit queued commands serially; total order per branch."""
        results: list[SubmissionResult] = []
        while self._queue:
            queued = self._queue.popleft()
            results.append(self._submit_one(queued))
        return tuple(results)

    def _submit_one(self, queued: QueuedCommand) -> SubmissionResult:
        if self._runtime is None:
            result = SubmissionResult(
                queued.envelope.command_id.value, "rejected", "no runtime attached"
            )
            self._processed[queued.envelope.command_id.value] = result
            return result
        from wanxiang_domain.errors import StaleRevision, ValidationRejected

        state = self._runtime.current_state(queued.envelope.instance_id, queued.envelope.branch_id)
        if state.revision != queued.envelope.expected_revision:
            result = SubmissionResult(
                queued.envelope.command_id.value,
                "conflict",
                f"expected revision {queued.envelope.expected_revision.value}, "
                f"current {state.revision.value}",
                revision=state.revision.value,
            )
            self._processed[queued.envelope.command_id.value] = result
            return result
        try:
            self._runtime.submit_command(queued.envelope)
            result = SubmissionResult(
                queued.envelope.command_id.value,
                "accepted",
                revision=state.revision.value + 1,
            )
        except (StaleRevision, ValidationRejected) as exc:
            result = SubmissionResult(
                queued.envelope.command_id.value,
                "conflict" if isinstance(exc, StaleRevision) else "rejected",
                str(exc),
                revision=state.revision.value,
            )
        self._processed[queued.envelope.command_id.value] = result
        return result

    def pending_count(self) -> int:
        return len(self._queue)

    def result(self, command_id: str) -> SubmissionResult | None:
        return self._processed.get(command_id)

    def enqueue_all(self, envelopes: tuple[CommandEnvelope, ...]) -> None:
        for envelope in envelopes:
            self.enqueue(envelope)
