"""Small HTTP control helpers for the vendor-neutral T3 gateway."""

from __future__ import annotations

from typing import Protocol

_MAX_JSON_RESPONSE_BYTES = 48 * 1024 * 1024
_MAX_ARTIFACT_BYTES = 128 * 1024 * 1024
_MAX_ARTIFACTS = 8
_VALID_STATES = frozenset({"queued", "running", "succeeded", "failed", "cancelled", "expired"})


class _PostJson(Protocol):
    def __call__(
        self,
        endpoint: str,
        payload: dict[str, object],
        *,
        idempotency_key: str = "",
    ) -> dict[str, object]: ...


def _spatial_http_headers(bearer_token: str, idempotency_key: str = "") -> dict[str, str]:
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Wanxiang-T3-Gateway/1",
    }
    if bearer_token:
        headers["authorization"] = f"Bearer {bearer_token}"
    if idempotency_key:
        headers["idempotency-key"] = idempotency_key
    return headers


def _spatial_cancellation_payload(task_ref: str, request_id: str) -> dict[str, object]:
    values = (task_ref, request_id)
    if any(
        not value.strip() or len(value) > 1024 or "\r" in value or "\n" in value for value in values
    ):
        raise ValueError("spatial HTTP cancellation requires safe task and request ids")
    return {"task_ref": task_ref, "request_id": request_id}


def _cancel_spatial_http(
    endpoint: str,
    task_ref: str,
    request_id: str,
    post_json: _PostJson,
) -> None:
    if not endpoint:
        raise ValueError("spatial HTTP provider does not support cancellation")
    body = post_json(
        endpoint,
        _spatial_cancellation_payload(task_ref, request_id),
        idempotency_key=request_id,
    )
    if body.get("accepted") is not True:
        raise ValueError("spatial HTTP cancellation was not accepted")
