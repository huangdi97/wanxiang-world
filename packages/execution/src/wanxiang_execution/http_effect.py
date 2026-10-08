"""Real HTTP adapter for the irreversible-external-effect outbox.

Implemented with the standard library only (``urllib.request``). Each ``apply``
call performs exactly one request: retry policy and duplicate suppression stay
in ``OutboxExecutor``, never in this adapter.

The request body carries only identifiers and the payload digest; the payload
itself is never sent, and this adapter never logs request material.

SECURITY: this adapter holds no credentials and targets a caller-supplied base
URL. It is not a third-party SaaS client.

SECURITY INVARIANT: the result of an HTTP attempt is a proposal only. It is
never world history and can never be appended to canonical history; only a
Commit Authority may decide whether anything becomes canonical.
"""

from __future__ import annotations

import http.client
import json
import socket
import urllib.error
import urllib.request
from collections.abc import Mapping
from typing import cast

from wanxiang_execution.outbox_records import (
    STATUS_AMBIGUOUS,
    STATUS_APPLIED,
    STATUS_DUPLICATE_SUPPRESSED,
    STATUS_FAILED,
    ExternalEffectIntent,
    ExternalEffectResult,
)

HANDLER_ID = "execution-http-effect"
_EFFECT_PATH = "/effect"
_JSON_CONTENT_TYPE = "application/json"
_OK_STATUSES = (200, 201)
_CLIENT_CONFLICT_STATUS = 409
_APPLIED_BODY_STATUS = "applied"
_DUPLICATE_BODY_STATUS = "duplicate"
_AMBIGUOUS_BODY_STATUS = "ambiguous"

# SAFETY: transport failures that may have delivered the request are ambiguous,
# never failed. `failed` would invite an automatic retry of an effect that may
# already have happened.
_MAY_HAVE_HAPPENED_ERRORS = (
    TimeoutError,
    socket.timeout,
    ConnectionResetError,
    ConnectionAbortedError,
    http.client.IncompleteRead,
)


class HttpEffectHandler:
    """Apply one external effect by POSTing its intent to an effect service."""

    handler_id = HANDLER_ID

    def __init__(self, base_url: str, timeout_seconds: float = 5.0) -> None:
        """Wire the handler to one effect service.

        Args:
            base_url: Service root, e.g. ``"http://127.0.0.1:8000"``.
            timeout_seconds: Per-request socket timeout; 0 disables it.
        """
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._apply_url = f"{self._base_url}{_EFFECT_PATH}"

    def apply(self, intent: ExternalEffectIntent) -> ExternalEffectResult:
        """POST the intent and map the response to one result status.

        Args:
            intent: Intent to apply. Its payload is never transmitted.

        Returns:
            STATUS_APPLIED, STATUS_DUPLICATE_SUPPRESSED, STATUS_AMBIGUOUS or
            STATUS_FAILED per :func:`_result_from_response`.
        """
        request = urllib.request.Request(
            self._apply_url,
            data=_request_body(intent),
            headers={
                "Content-Type": _JSON_CONTENT_TYPE,
                "Idempotency-Key": intent.idempotency_key,
            },
            method="POST",
        )
        timeout = self._timeout_seconds if self._timeout_seconds > 0 else None
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status_code = int(response.status)
                body = bytes(response.read())
                return _result_from_response(intent, status_code, body)
        except urllib.error.HTTPError as exc:
            return _result_from_response(intent, int(exc.code), _safe_read(exc))
        except urllib.error.URLError as exc:
            return _transport_result(intent, exc.reason)
        except _MAY_HAVE_HAPPENED_ERRORS as exc:
            return _ambiguous(
                intent,
                f"transport lost before a full answer ({type(exc).__name__}); may have happened",
            )
        except OSError as exc:
            return _failed(
                intent,
                f"transport error before the effect was sent ({type(exc).__name__})",
            )


def _request_body(intent: ExternalEffectIntent) -> bytes:
    """Serialize the identifier-only request body, excluding the payload."""
    body = {
        "intentId": intent.intent_id,
        "worldlineId": intent.worldline_id,
        "target": intent.target,
        "operation": intent.operation,
        "payloadDigest": intent.payload_digest,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _safe_read(exc: urllib.error.HTTPError) -> bytes:
    """Read an error body, tolerating a stream that closes early."""
    try:
        return bytes(exc.read())
    except OSError:
        return b""


def _result_from_response(
    intent: ExternalEffectIntent, status_code: int, body: bytes
) -> ExternalEffectResult:
    """Map an HTTP status and body to a result status.

    Mapping:
        200/201 with ``{"status": "applied", "externalRef": ...}`` -> APPLIED
        200 with ``{"status": "duplicate"}`` or HTTP 409 -> DUPLICATE_SUPPRESSED
        200 with ``{"status": "ambiguous"}`` -> AMBIGUOUS
        HTTP 5xx or an unparseable / unknown body -> FAILED
    """
    if status_code == _CLIENT_CONFLICT_STATUS:
        return _duplicate(intent, status_code)
    if 500 <= status_code < 600:
        return _failed(intent, f"http {status_code}: server error; the effect was not applied")
    if status_code not in _OK_STATUSES:
        return _failed(intent, f"http {status_code}: unexpected status; the effect was not applied")
    payload = _parse_object(body)
    if payload is None:
        return _failed(intent, f"http {status_code}: response body did not parse as JSON")
    reported = payload.get("status")
    if reported == _APPLIED_BODY_STATUS:
        return _applied(intent, status_code, _optional_str(payload.get("externalRef")))
    if reported == _DUPLICATE_BODY_STATUS:
        return _duplicate(intent, status_code)
    if reported == _AMBIGUOUS_BODY_STATUS:
        return _ambiguous(
            intent,
            f"http {status_code}: service reported an ambiguous outcome; may have happened",
        )
    return _failed(
        intent, f"http {status_code}: unknown body status {reported!r}; effect was not confirmed"
    )


def _transport_result(intent: ExternalEffectIntent, reason: object) -> ExternalEffectResult:
    """Classify a wrapped transport error: ambiguous if it may have happened."""
    if isinstance(reason, _MAY_HAVE_HAPPENED_ERRORS):
        return _ambiguous(
            intent,
            f"transport lost before a full answer ({type(reason).__name__}); may have happened",
        )
    return _failed(intent, f"transport error before the effect was sent ({type(reason).__name__})")


def _parse_object(body: bytes) -> Mapping[str, object] | None:
    """Decode a JSON object body, or return None when it does not parse."""
    try:
        parsed = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    if isinstance(parsed, Mapping):
        # INVARIANT: the cast is confined to this JSON boundary and only runs
        # after the mapping check, so no untyped value leaves this function.
        return cast("Mapping[str, object]", parsed)
    return None


def _optional_str(value: object) -> str | None:
    """Return value when it is a non-empty string, else None."""
    return value if isinstance(value, str) and value else None


def _applied(
    intent: ExternalEffectIntent, status_code: int, external_ref: str | None
) -> ExternalEffectResult:
    return ExternalEffectResult(
        intent_id=intent.intent_id,
        idempotency_key=intent.idempotency_key,
        status=STATUS_APPLIED,
        external_ref=external_ref,
        detail=f"http {status_code}: effect applied",
    )


def _duplicate(intent: ExternalEffectIntent, status_code: int) -> ExternalEffectResult:
    return ExternalEffectResult(
        intent_id=intent.intent_id,
        idempotency_key=intent.idempotency_key,
        status=STATUS_DUPLICATE_SUPPRESSED,
        external_ref=None,
        detail=f"http {status_code}: duplicate suppressed by idempotency key",
    )


def _ambiguous(intent: ExternalEffectIntent, detail: str) -> ExternalEffectResult:
    return ExternalEffectResult(
        intent_id=intent.intent_id,
        idempotency_key=intent.idempotency_key,
        status=STATUS_AMBIGUOUS,
        external_ref=None,
        detail=detail,
    )


def _failed(intent: ExternalEffectIntent, detail: str) -> ExternalEffectResult:
    return ExternalEffectResult(
        intent_id=intent.intent_id,
        idempotency_key=intent.idempotency_key,
        status=STATUS_FAILED,
        external_ref=None,
        detail=detail,
    )
