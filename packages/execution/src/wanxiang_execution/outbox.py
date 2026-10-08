"""Append-only JSONL store for irreversible external effects.

The file is the durability boundary: every record is written and flushed
immediately, and records are never updated or deleted. Constructing an Outbox
performs no I/O; a missing file reads as empty.

INVARIANT: an external effect result never writes canonical state. It becomes
an observation/proposal for the authority to decide on, and only the authority
may turn it into canonical history.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import TypeGuard

from wanxiang_execution.errors import OutboxError
from wanxiang_execution.outbox_records import (
    ATTEMPT_MARKER_STATUS,
    RECORD_TYPE_ATTEMPT,
    RECORD_TYPE_INTENT,
    ExternalEffectAttempt,
    ExternalEffectIntent,
    ExternalEffectResult,
)


class Outbox:
    """Append-only JSONL store of external-effect intents and attempts."""

    def __init__(self, path: Path) -> None:
        """Store the JSONL path; nothing is created until the first append.

        Args:
            path: JSONL file backing this outbox.
        """
        self._path = path

    @property
    def path(self) -> Path:
        """Filesystem location of the JSONL store."""
        return self._path

    def append(self, intent: ExternalEffectIntent) -> None:
        """Append one intent record.

        Args:
            intent: Intent to record.

        Raises:
            OutboxError: If the same intent_id is already recorded.
        """
        if any(existing.intent_id == intent.intent_id for existing in self.intents()):
            raise OutboxError(
                f"intent_id={intent.intent_id!r} is already recorded; the outbox is append-only"
            )
        self._append_record(_encode_intent(intent))

    def intents(self) -> tuple[ExternalEffectIntent, ...]:
        """Read every intent in append order."""
        return tuple(
            _intent_from_record(record, self._path) for record in self._records(RECORD_TYPE_INTENT)
        )

    def attempts(self) -> tuple[ExternalEffectAttempt, ...]:
        """Read every attempt record, markers and results, in append order."""
        return tuple(
            _attempt_from_record(record, self._path)
            for record in self._records(RECORD_TYPE_ATTEMPT)
        )

    def record_attempt_marker(self, intent: ExternalEffectIntent, attempt_no: int) -> None:
        """Append the pre-call durability marker for one attempt.

        SAFETY: written before the handler is called so a crash cannot lose the
        fact that an irreversible effect may have been applied.

        Args:
            intent: Intent being attempted.
            attempt_no: 1-based attempt number.
        """
        self._append_record(_encode_attempt_marker(intent, attempt_no))

    def record_attempt(
        self, intent: ExternalEffectIntent, result: ExternalEffectResult, attempt_no: int
    ) -> None:
        """Append the handler result for one attempt.

        Args:
            intent: Intent that was attempted.
            result: Handler result; its ids must match the intent.
            attempt_no: Attempt number the result belongs to.

        Raises:
            OutboxError: If the result ids do not match the intent.
        """
        self._append_record(_encode_attempt_result(intent, result, attempt_no))

    def _append_record(self, record: Mapping[str, object]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(dict(record), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()

    def _records(self, record_type: str) -> list[dict[str, object]]:
        if not self._path.is_file():
            return []
        records: list[dict[str, object]] = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = _decode_record(line, self._path)
            if record.get("record_type") == record_type:
                records.append(record)
        return records


def _encode_intent(intent: ExternalEffectIntent) -> dict[str, object]:
    return {
        "record_type": RECORD_TYPE_INTENT,
        "intent_id": intent.intent_id,
        "worldline_id": intent.worldline_id,
        "target": intent.target,
        "operation": intent.operation,
        "payload_digest": intent.payload_digest,
        "idempotency_key": intent.idempotency_key,
        "requested_by": intent.requested_by,
    }


def _encode_attempt_marker(intent: ExternalEffectIntent, attempt_no: int) -> dict[str, object]:
    return {
        "record_type": RECORD_TYPE_ATTEMPT,
        "intent_id": intent.intent_id,
        "idempotency_key": intent.idempotency_key,
        "attempt_no": attempt_no,
        "status": ATTEMPT_MARKER_STATUS,
        "external_ref": None,
        "detail": "",
    }


def _encode_attempt_result(
    intent: ExternalEffectIntent, result: ExternalEffectResult, attempt_no: int
) -> dict[str, object]:
    if result.intent_id != intent.intent_id or result.idempotency_key != intent.idempotency_key:
        raise OutboxError(
            "attempt result does not belong to the intent: "
            f"intent_id={result.intent_id!r}/{intent.intent_id!r}, "
            f"idempotency_key={result.idempotency_key!r}/{intent.idempotency_key!r}"
        )
    return {
        "record_type": RECORD_TYPE_ATTEMPT,
        "intent_id": intent.intent_id,
        "idempotency_key": intent.idempotency_key,
        "attempt_no": attempt_no,
        "status": result.status,
        "external_ref": result.external_ref,
        "detail": result.detail,
    }


def _decode_record(line: str, path: Path) -> dict[str, object]:
    try:
        parsed = json.loads(line)
    except json.JSONDecodeError as exc:
        raise OutboxError(f"corrupt outbox record in {path}: {exc}") from exc
    if not _is_record(parsed):
        raise OutboxError(f"outbox record in {path} must be a JSON object")
    return parsed


def _is_record(value: object) -> TypeGuard[dict[str, object]]:
    """Narrow a decoded JSON value to an outbox record object."""
    return isinstance(value, dict)


def _required_str(record: Mapping[str, object], key: str, path: Path) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise OutboxError(f"outbox record field {key!r} must be a non-empty string in {path}")
    return value


def _optional_str(record: Mapping[str, object], key: str, path: Path) -> str | None:
    value = record.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise OutboxError(f"outbox record field {key!r} must be a string or null in {path}")
    return value


def _required_int(record: Mapping[str, object], key: str, path: Path) -> int:
    value = record.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise OutboxError(f"outbox record field {key!r} must be an integer in {path}")
    return value


def _intent_from_record(record: Mapping[str, object], path: Path) -> ExternalEffectIntent:
    return ExternalEffectIntent(
        intent_id=_required_str(record, "intent_id", path),
        worldline_id=_required_str(record, "worldline_id", path),
        target=_required_str(record, "target", path),
        operation=_required_str(record, "operation", path),
        payload_digest=_required_str(record, "payload_digest", path),
        idempotency_key=_required_str(record, "idempotency_key", path),
        requested_by=_optional_str(record, "requested_by", path),
    )


def _attempt_from_record(record: Mapping[str, object], path: Path) -> ExternalEffectAttempt:
    return ExternalEffectAttempt(
        intent_id=_required_str(record, "intent_id", path),
        idempotency_key=_required_str(record, "idempotency_key", path),
        attempt_no=_required_int(record, "attempt_no", path),
        status=_required_str(record, "status", path),
        external_ref=_optional_str(record, "external_ref", path),
        detail=_optional_str(record, "detail", path) or "",
    )
