"""Native Marble 2 operation control for future Wanxiang spatial pipelines.

This module implements provider operation semantics only: authenticated task
submission, idempotent retry identity, polling, and best-effort cancellation.
It deliberately does not claim that one Marble task produces a Wanxiang T3
world, and it has no Canon/History write authority.
"""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal, cast
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, build_opener

from wanxiang_substrate.assets.book_http_transport import (
    _NoRedirects,
    _validate_provider_endpoint,
)
from wanxiang_substrate.assets.book_spatial_http_transport import _bounded_read

_MARBLE_TASKS = frozenset(
    {
        "atlasChisel",
        "atlasGenerate",
        "atlasMasked",
        "atlasTextToImage",
        "images2PosedRGBD",
        "splats2Mesh",
    }
)
_MAX_JSON_BYTES = 2 * 1024 * 1024
_MarbleOperationState = Literal["running", "succeeded", "failed"]


@dataclass(frozen=True, slots=True)
class _MarbleOperation:
    operation_id: str
    state: _MarbleOperationState
    response: dict[str, object] | None = None
    error_code: int | None = None
    error_message: str = ""
    task: str = ""


class _MarbleOperationClient:
    """Strict transport for Marble operations, independent from world truth."""

    def __init__(
        self,
        api_base: str,
        *,
        api_key: str,
        timeout_seconds: float = 120.0,
        max_json_bytes: int = _MAX_JSON_BYTES,
    ) -> None:
        self.api_base = _validate_provider_endpoint(api_base, label="Marble API").rstrip("/")
        if not api_key.strip():
            raise ValueError("Marble API requires a project API key")
        if "\r" in api_key or "\n" in api_key:
            raise ValueError("Marble API key cannot contain line breaks")
        if timeout_seconds <= 0:
            raise ValueError("Marble API timeout must be positive")
        if (
            isinstance(max_json_bytes, bool)
            or not isinstance(max_json_bytes, int)
            or max_json_bytes <= 0
        ):
            raise ValueError("Marble JSON response limit must be a positive integer")
        self.api_key = api_key.strip()
        self.timeout_seconds = timeout_seconds
        self.max_json_bytes = max_json_bytes

    def _headers(self, *, idempotency_key: str = "") -> dict[str, str]:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "wlt-api-key": self.api_key,
            "user-agent": "Wanxiang-Marble-Operations/1",
        }
        if idempotency_key:
            headers["idempotency-key"] = idempotency_key
        return headers

    def _json(self, request: Request, *, label: str) -> dict[str, object]:
        try:
            with build_opener(_NoRedirects()).open(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                raw = _bounded_read(response, self.max_json_bytes, label=label)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"{label} request failed") from exc
        try:
            decoded: object = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError(f"{label} returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise ValueError(f"{label} response must be an object")
        return cast(dict[str, object], decoded)

    @staticmethod
    def _safe_id(value: object, *, label: str, max_chars: int) -> str:
        if (
            not isinstance(value, str)
            or not value.strip()
            or len(value) > max_chars
            or "\r" in value
            or "\n" in value
        ):
            raise ValueError(f"Marble {label} is invalid")
        return value.strip()

    @classmethod
    def _operation(cls, body: dict[str, object]) -> _MarbleOperation:
        operation_id = cls._safe_id(
            body.get("id"),
            label="operation id",
            max_chars=1024,
        )
        done = body.get("done")
        if not isinstance(done, bool):
            raise ValueError("Marble operation returned invalid done flag")

        metadata = body.get("metadata")
        task = ""
        if metadata is not None:
            if not isinstance(metadata, dict):
                raise ValueError("Marble operation returned invalid metadata")
            raw_task = cast(dict[str, object], metadata).get("task", "")
            if raw_task:
                task = cls._safe_id(raw_task, label="operation task", max_chars=128)

        response = body.get("response")
        error = body.get("error")
        if not done:
            if response is not None or error is not None:
                raise ValueError("Marble running operation cannot be terminal")
            return _MarbleOperation(operation_id, "running", task=task)

        if (response is None) == (error is None):
            raise ValueError("Marble terminal operation requires exactly one result")
        if response is not None:
            if not isinstance(response, dict):
                raise ValueError("Marble operation returned invalid response")
            return _MarbleOperation(
                operation_id,
                "succeeded",
                response=cast(dict[str, object], response),
                task=task,
            )

        if not isinstance(error, dict):
            raise ValueError("Marble operation returned invalid error")
        error_map = cast(dict[str, object], error)
        code = error_map.get("code")
        message = error_map.get("message", "")
        if isinstance(code, bool) or not isinstance(code, int):
            raise ValueError("Marble operation returned invalid error code")
        if not isinstance(message, str) or len(message) > 2000:
            raise ValueError("Marble operation returned invalid error message")
        return _MarbleOperation(
            operation_id,
            "failed",
            error_code=code,
            error_message=message,
            task=task,
        )

    def submit_task(
        self,
        task: str,
        payload: dict[str, object],
        *,
        idempotency_key: str,
    ) -> _MarbleOperation:
        if task not in _MARBLE_TASKS:
            raise ValueError("Marble task is not allowlisted")
        key = self._safe_id(
            idempotency_key,
            label="idempotency key",
            max_chars=128,
        )
        body = self._json(
            Request(
                f"{self.api_base}/tasks:{task}",
                data=json.dumps(
                    payload,
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8"),
                headers=self._headers(idempotency_key=key),
                method="POST",
            ),
            label=f"Marble {task} submit",
        )
        return self._operation(body)

    def poll(self, operation_id: str) -> _MarbleOperation:
        clean = self._safe_id(
            operation_id,
            label="operation id",
            max_chars=1024,
        )
        body = self._json(
            Request(
                f"{self.api_base}/operations/{quote(clean, safe='')}",
                headers=self._headers(),
                method="GET",
            ),
            label="Marble operation poll",
        )
        return self._operation(body)

    def cancel(
        self,
        operation_id: str,
        *,
        request_id: str,
        reason: str = "",
    ) -> _MarbleOperation:
        clean = self._safe_id(
            operation_id,
            label="operation id",
            max_chars=1024,
        )
        cancel_id = self._safe_id(
            request_id,
            label="cancellation request id",
            max_chars=36,
        )
        if not isinstance(reason, str) or len(reason) > 256:
            raise ValueError("Marble cancellation reason is invalid")
        payload: dict[str, object] = {"requestId": cancel_id}
        if reason:
            payload["reason"] = reason
        body = self._json(
            Request(
                f"{self.api_base}/operations/{quote(clean, safe='')}:cancel",
                data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
                headers=self._headers(),
                method="POST",
            ),
            label="Marble operation cancel",
        )
        return self._operation(body)
