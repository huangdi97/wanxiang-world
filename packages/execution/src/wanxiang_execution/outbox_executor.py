"""Duplicate-suppression policy for the irreversible-external-effect outbox.

This module owns "what happens when an irreversible effect is executed more
than once": the append-only store in `outbox.py` records, and this executor
decides whether the handler may run again. Once an idempotency key reached
STATUS_APPLIED the handler is never called again; an ambiguous attempt is never
retried automatically and needs explicit reconciliation.

INVARIANT: an external result never writes canonical state. It becomes an
observation/proposal for the authority to decide on.
"""

from __future__ import annotations

from wanxiang_execution.errors import OutboxError
from wanxiang_execution.outbox import Outbox
from wanxiang_execution.outbox_records import (
    ATTEMPT_MARKER_STATUS,
    RECONCILABLE_STATUSES,
    RESOLVED_STATUSES,
    STATUS_AMBIGUOUS,
    STATUS_APPLIED,
    STATUS_DUPLICATE_SUPPRESSED,
    STATUS_FAILED,
    ExternalEffectAttempt,
    ExternalEffectHandler,
    ExternalEffectIntent,
    ExternalEffectResult,
)


class OutboxExecutor:
    """Execute external-effect intents through one handler, biased against duplicates.

    `execute` retries a failed handler up to ``max_attempts`` times within one
    call and records every attempt; a later call cannot exceed the recorded
    attempt budget.
    """

    def __init__(
        self, outbox: Outbox, handler: ExternalEffectHandler, max_attempts: int = 3
    ) -> None:
        """Wire the executor to its durable store and its external handler.

        Args:
            outbox: Append-only store the intents were appended to.
            handler: Boundary adapter that applies the effect.
            max_attempts: Retry budget per idempotency key.

        Raises:
            OutboxError: If max_attempts is less than 1.
        """
        if max_attempts < 1:
            raise OutboxError(f"max_attempts must be at least 1: got {max_attempts}")
        self._outbox = outbox
        self._handler = handler
        self._max_attempts = max_attempts

    def execute(self, intent: ExternalEffectIntent) -> ExternalEffectResult:
        """Attempt one external effect, biased against duplicate execution.

        Args:
            intent: Intent previously appended to the outbox.

        Returns:
            The handler result, or a duplicate-suppressed / ambiguous / failed
            result derived from the append-only record.

        Raises:
            OutboxError: If the intent is not recorded in the outbox.
        """
        self._require_recorded(intent)
        records = self._records_for_key(intent.idempotency_key)
        latest = records[-1] if records else None
        if latest is not None:
            if latest.status == STATUS_APPLIED:
                return _duplicate_result(intent, latest)
            if latest.status == ATTEMPT_MARKER_STATUS:
                return self._record_unknown_outcome(intent, latest)
            if latest.status == STATUS_AMBIGUOUS:
                return _ambiguous_result(intent, latest)
        remaining = self._max_attempts - sum(
            1 for record in records if record.status == ATTEMPT_MARKER_STATUS
        )
        if remaining <= 0:
            return self._exhausted_result(intent, records)
        return self._attempt_until_settled(intent, remaining, records)

    def pending(self) -> tuple[ExternalEffectIntent, ...]:
        """Intents whose latest attempt is neither applied nor duplicate-suppressed."""
        latest = _latest_attempts(self._outbox.attempts())
        pending: list[ExternalEffectIntent] = []
        for intent in self._outbox.intents():
            attempt = latest.get(intent.intent_id)
            if attempt is None or attempt.status not in RESOLVED_STATUSES:
                pending.append(intent)
        return tuple(pending)

    def ambiguous(self) -> tuple[ExternalEffectIntent, ...]:
        """Intents whose latest attempt is ambiguous and needs reconciliation."""
        latest = _latest_attempts(self._outbox.attempts())
        ambiguous: list[ExternalEffectIntent] = []
        for intent in self._outbox.intents():
            attempt = latest.get(intent.intent_id)
            if attempt is not None and attempt.status == STATUS_AMBIGUOUS:
                ambiguous.append(intent)
        return tuple(ambiguous)

    def reconcile(
        self,
        intent_id: str,
        resolved_status: str,
        external_ref: str | None,
        detail: str,
    ) -> ExternalEffectResult:
        """Record a manual resolution for one intent as another attempt.

        Args:
            intent_id: Intent being reconciled.
            resolved_status: STATUS_APPLIED or STATUS_FAILED.
            external_ref: External reference observed during reconciliation.
            detail: Human-readable resolution note; required for audit.

        Returns:
            The recorded resolution result.

        Raises:
            OutboxError: If the intent is unknown, the status is not a valid
                resolution, or the detail is empty.
        """
        intent = self._find_intent(intent_id)
        if resolved_status not in RECONCILABLE_STATUSES:
            raise OutboxError(
                f"resolved_status must be one of {sorted(RECONCILABLE_STATUSES)}: "
                f"got {resolved_status!r}"
            )
        if not detail.strip():
            raise OutboxError("reconciliation detail must be non-empty")
        attempts = [record for record in self._outbox.attempts() if record.intent_id == intent_id]
        attempt_no = max((record.attempt_no for record in attempts), default=0) + 1
        result = ExternalEffectResult(
            intent_id=intent_id,
            idempotency_key=intent.idempotency_key,
            status=resolved_status,
            external_ref=external_ref,
            detail=detail,
        )
        self._outbox.record_attempt(intent, result, attempt_no)
        return result

    def _attempt_until_settled(
        self, intent: ExternalEffectIntent, remaining: int, records: list[ExternalEffectAttempt]
    ) -> ExternalEffectResult:
        next_attempt_no = max((record.attempt_no for record in records), default=0) + 1
        last_result: ExternalEffectResult | None = None
        for offset in range(remaining):
            attempt_no = next_attempt_no + offset
            self._outbox.record_attempt_marker(intent, attempt_no)
            result = self._handler.apply(intent)
            self._outbox.record_attempt(intent, result, attempt_no)
            if result.status != STATUS_FAILED:
                return result
            last_result = result
        if last_result is None:
            raise OutboxError(f"no attempt was performed for intent_id={intent.intent_id!r}")
        return last_result

    def _record_unknown_outcome(
        self, intent: ExternalEffectIntent, marker: ExternalEffectAttempt
    ) -> ExternalEffectResult:
        # SAFETY: an attempt without a recorded result may or may not have been
        # applied; an irreversible effect is never retried on uncertainty.
        result = ExternalEffectResult(
            intent_id=intent.intent_id,
            idempotency_key=intent.idempotency_key,
            status=STATUS_AMBIGUOUS,
            external_ref=None,
            detail=f"attempt {marker.attempt_no} has no recorded result; reconciliation required",
        )
        self._outbox.record_attempt(intent, result, marker.attempt_no)
        return result

    def _exhausted_result(
        self, intent: ExternalEffectIntent, records: list[ExternalEffectAttempt]
    ) -> ExternalEffectResult:
        last = records[-1]
        return ExternalEffectResult(
            intent_id=intent.intent_id,
            idempotency_key=intent.idempotency_key,
            status=STATUS_FAILED,
            external_ref=last.external_ref,
            detail=(
                f"retry budget of {self._max_attempts} attempts exhausted; "
                f"last attempt {last.attempt_no} recorded {last.status!r}"
            ),
        )

    def _require_recorded(self, intent: ExternalEffectIntent) -> None:
        if not any(existing.intent_id == intent.intent_id for existing in self._outbox.intents()):
            raise OutboxError(
                f"intent_id={intent.intent_id!r} is not recorded in the outbox; append it first"
            )

    def _records_for_key(self, idempotency_key: str) -> list[ExternalEffectAttempt]:
        return [
            record
            for record in self._outbox.attempts()
            if record.idempotency_key == idempotency_key
        ]

    def _find_intent(self, intent_id: str) -> ExternalEffectIntent:
        for intent in self._outbox.intents():
            if intent.intent_id == intent_id:
                return intent
        raise OutboxError(f"cannot reconcile unknown intent_id={intent_id!r}")


def _duplicate_result(
    intent: ExternalEffectIntent, applied: ExternalEffectAttempt
) -> ExternalEffectResult:
    return ExternalEffectResult(
        intent_id=intent.intent_id,
        idempotency_key=intent.idempotency_key,
        status=STATUS_DUPLICATE_SUPPRESSED,
        external_ref=applied.external_ref,
        detail=f"idempotency_key={intent.idempotency_key!r} already applied; handler not called",
    )


def _ambiguous_result(
    intent: ExternalEffectIntent, latest: ExternalEffectAttempt
) -> ExternalEffectResult:
    return ExternalEffectResult(
        intent_id=intent.intent_id,
        idempotency_key=intent.idempotency_key,
        status=STATUS_AMBIGUOUS,
        external_ref=latest.external_ref,
        detail=(
            f"attempt {latest.attempt_no} is ambiguous and is never retried automatically; "
            "reconciliation required"
        ),
    )


def _latest_attempts(
    attempts: tuple[ExternalEffectAttempt, ...],
) -> dict[str, ExternalEffectAttempt]:
    latest: dict[str, ExternalEffectAttempt] = {}
    for attempt in attempts:
        latest[attempt.intent_id] = attempt
    return latest
