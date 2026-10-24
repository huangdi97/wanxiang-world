"""Marble native operation semantics stay idempotent and non-authoritative."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from email.message import Message
from typing import Any

import pytest
import wanxiang_substrate.assets.book_spatial_marble_operations as marble
from wanxiang_substrate.assets.book_spatial_marble_operations import _MarbleOperationClient


class _Response:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload
        self.headers = Message()
        self.headers["content-length"] = str(len(payload))

    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *args: object) -> None:
        _ = args

    def read(self, limit: int) -> bytes:
        return self.payload[:limit]


class _Opener:
    def __init__(self, payloads: list[bytes]) -> None:
        self.payloads = payloads
        self.requests: list[Any] = []

    def open(self, request: Any, *, timeout: float) -> _Response:
        assert timeout > 0
        self.requests.append(request)
        return _Response(self.payloads.pop(0))


def _install(monkeypatch: pytest.MonkeyPatch, payloads: list[dict[str, object]]) -> _Opener:
    opener = _Opener([json.dumps(payload, separators=(",", ":")).encode() for payload in payloads])

    def factory(*handlers: object) -> _Opener:
        _ = handlers
        return opener

    monkeypatch.setattr(marble, "build_opener", factory)
    return opener


def _client() -> _MarbleOperationClient:
    return _MarbleOperationClient(
        "https://api.atlas-beta.worldlabs.ai/api/v2",
        api_key="wl-test-secret",
    )


def test_marble_submit_uses_project_key_and_stable_idempotency_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opener = _install(
        monkeypatch,
        [
            {
                "id": "op-1",
                "done": False,
                "response": None,
                "error": None,
                "metadata": {"task": "atlasTextToImage"},
            }
        ],
    )

    operation = _client().submit_task(
        "atlasTextToImage",
        {"prompt": "quiet source-grounded courtyard"},
        idempotency_key="scene-logical-1",
    )

    assert operation.operation_id == "op-1"
    assert operation.state == "running"
    request = opener.requests[0]
    assert request.full_url.endswith("/api/v2/tasks:atlasTextToImage")
    assert request.get_header("Wlt-api-key") == "wl-test-secret"
    assert request.get_header("Idempotency-key") == "scene-logical-1"
    assert json.loads(request.data.decode()) == {"prompt": "quiet source-grounded courtyard"}


def test_marble_poll_uses_done_as_only_terminal_signal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opener = _install(
        monkeypatch,
        [
            {
                "id": "op-1",
                "done": True,
                "response": {"frames": [{"imageAsset": {"assetId": "asset-1"}}]},
                "error": None,
                "metadata": {"task": "atlasTextToImage"},
            }
        ],
    )

    operation = _client().poll("op-1")

    assert operation.state == "succeeded"
    assert operation.response == {"frames": [{"imageAsset": {"assetId": "asset-1"}}]}
    assert operation.task == "atlasTextToImage"
    assert opener.requests[0].get_method() == "GET"


def test_marble_terminal_error_stays_provider_state_not_world_fact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install(
        monkeypatch,
        [
            {
                "id": "op-failed",
                "done": True,
                "response": None,
                "error": {"code": 13, "message": "execution failed"},
            }
        ],
    )

    operation = _client().poll("op-failed")

    assert operation.state == "failed"
    assert operation.error_code == 13
    assert operation.error_message == "execution failed"
    assert operation.response is None


def test_marble_cancel_uses_stable_request_id_and_remains_nonterminal_when_running(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opener = _install(
        monkeypatch,
        [
            {
                "id": "op/cancel-me",
                "done": False,
                "response": None,
                "error": None,
            }
        ],
    )

    operation = _client().cancel(
        "op/cancel-me",
        request_id="cancel-scene-1",
        reason="source scene replaced",
    )

    assert operation.state == "running"
    request = opener.requests[0]
    assert request.full_url.endswith("/operations/op%2Fcancel-me:cancel")
    assert request.get_method() == "POST"
    assert json.loads(request.data.decode()) == {
        "requestId": "cancel-scene-1",
        "reason": "source scene replaced",
    }
    assert request.get_header("Wlt-api-key") == "wl-test-secret"
    assert request.get_header("Idempotency-key") is None


@pytest.mark.parametrize(
    "body",
    [
        {"id": "op", "done": False, "response": {}, "error": None},
        {"id": "op", "done": True, "response": None, "error": None},
        {"id": "op", "done": True, "response": {}, "error": {"code": 1}},
        {"id": "op", "done": True, "response": None, "error": {"code": True}},
        {"id": "op", "done": "yes", "response": None, "error": None},
    ],
)
def test_marble_operation_envelope_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
    body: dict[str, object],
) -> None:
    _install(monkeypatch, [body])
    with pytest.raises(ValueError, match="Marble"):
        _client().poll("op")


def test_marble_rejects_unknown_task_and_unsafe_control_ids() -> None:
    client = _client()
    with pytest.raises(ValueError, match="not allowlisted"):
        client.submit_task("futureUnknownTask", {}, idempotency_key="one")
    with pytest.raises(ValueError, match="idempotency key"):
        client.submit_task("atlasGenerate", {}, idempotency_key="bad\nkey")
    with pytest.raises(ValueError, match="cancellation request id"):
        client.cancel("op", request_id="x" * 37)


def test_marble_requires_safe_project_key_and_positive_limits() -> None:
    with pytest.raises(ValueError, match="project API key"):
        _MarbleOperationClient(
            "https://api.atlas-beta.worldlabs.ai/api/v2",
            api_key="",
        )
    with pytest.raises(ValueError, match="line breaks"):
        _MarbleOperationClient(
            "https://api.atlas-beta.worldlabs.ai/api/v2",
            api_key="bad\nkey",
        )
    with pytest.raises(ValueError, match="positive integer"):
        _MarbleOperationClient(
            "https://api.atlas-beta.worldlabs.ai/api/v2",
            api_key="key",
            max_json_bytes=True,
        )
