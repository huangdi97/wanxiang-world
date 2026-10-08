"""Record types for the irreversible-external-effect outbox.

The outbox is an append-only JSONL log of intents and attempts. This module
defines the record vocabulary; `outbox.py` owns the durable store and its JSON
codec, and `outbox_executor.py` owns the duplicate-suppression policy.

INVARIANT: an external effect result never writes canonical state. Records are
evidence and proposals for the authority to decide on, never world history.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_execution.errors import OutboxError

STATUS_APPLIED = "applied"
STATUS_DUPLICATE_SUPPRESSED = "duplicate_suppressed"
STATUS_AMBIGUOUS = "ambiguous"
STATUS_FAILED = "failed"

ATTEMPT_MARKER_STATUS = "attempting"

RECORD_TYPE_INTENT = "intent"
RECORD_TYPE_ATTEMPT = "attempt"

RESULT_STATUSES = frozenset(
    {STATUS_APPLIED, STATUS_DUPLICATE_SUPPRESSED, STATUS_AMBIGUOUS, STATUS_FAILED}
)
RESOLVED_STATUSES = frozenset({STATUS_APPLIED, STATUS_DUPLICATE_SUPPRESSED})
RECONCILABLE_STATUSES = frozenset({STATUS_APPLIED, STATUS_FAILED})


@dataclass(frozen=True, slots=True)
class ExternalEffectIntent:
    """One irreversible external effect the caller wants to happen.

    Attributes:
        intent_id: Unique id of this intent record.
        worldline_id: Worldline the effect belongs to.
        target: External system or resource being touched.
        operation: Operation to apply, e.g. ``"send_email"``.
        payload_digest: Content digest of the payload (the payload itself is
            not stored here).
        idempotency_key: Key that makes the effect exactly-once across retries.
        requested_by: Optional actor that requested the effect.
    """

    intent_id: str
    worldline_id: str
    target: str
    operation: str
    payload_digest: str
    idempotency_key: str
    requested_by: str | None = None

    def __post_init__(self) -> None:
        """Validate that required fields are non-empty.

        Raises:
            OutboxError: If any required field is empty or whitespace.
        """
        required = {
            "intent_id": self.intent_id,
            "worldline_id": self.worldline_id,
            "target": self.target,
            "operation": self.operation,
            "payload_digest": self.payload_digest,
            "idempotency_key": self.idempotency_key,
        }
        empty = sorted(name for name, value in required.items() if not value.strip())
        if empty:
            raise OutboxError(
                f"external effect intent fields must be non-empty: {', '.join(empty)}"
            )


@dataclass(frozen=True, slots=True)
class ExternalEffectResult:
    """What one handler attempt reported for one intent.

    Attributes:
        intent_id: Intent the result belongs to.
        idempotency_key: Key the result was produced under.
        status: STATUS_APPLIED, STATUS_DUPLICATE_SUPPRESSED, STATUS_AMBIGUOUS
            or STATUS_FAILED.
        external_ref: Optional reference returned by the external system.
        detail: Human-readable detail; never contains secret payloads.
    """

    intent_id: str
    idempotency_key: str
    status: str
    external_ref: str | None
    detail: str

    def __post_init__(self) -> None:
        """Validate the result status against the closed status set.

        Raises:
            OutboxError: If the status is not a known result status.
        """
        if self.status not in RESULT_STATUSES:
            raise OutboxError(
                f"external effect result status must be one of "
                f"{sorted(RESULT_STATUSES)}: got {self.status!r}"
            )


@dataclass(frozen=True, slots=True)
class ExternalEffectAttempt:
    """One append-only attempt record: a pre-call marker or a result.

    Attributes:
        intent_id: Intent the attempt belongs to.
        idempotency_key: Key the attempt was made under.
        attempt_no: 1-based attempt number, monotonic per intent.
        status: ATTEMPT_MARKER_STATUS or a result status.
        external_ref: External reference when the record is a result.
        detail: Human-readable detail for result records.
    """

    intent_id: str
    idempotency_key: str
    attempt_no: int
    status: str
    external_ref: str | None
    detail: str


class ExternalEffectHandler(Protocol):
    """Boundary adapter that applies one external effect.

    Implementations live at the system edge (email, payment, device, cloud).
    """

    handler_id: str

    def apply(self, intent: ExternalEffectIntent) -> ExternalEffectResult:
        """Apply the effect and report the external result.

        Args:
            intent: Intent to apply.

        Returns:
            Result of the attempt. STATUS_AMBIGUOUS means the effect may or may
            not have happened and must be reconciled manually.
        """
        ...
