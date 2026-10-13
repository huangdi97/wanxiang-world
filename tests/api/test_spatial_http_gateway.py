"""T3 HTTP gateway preserves bounded prompts, idempotency and artifact safety."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import base64
import json
from email.message import Message
from typing import Any

import pytest
import wanxiang_substrate.assets.book_spatial_http_gateway as gateway
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.spatial import build_http_spatial_provider


class _FakeResponse:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self.headers = Message()
        self.headers["content-length"] = str(len(payload))

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        _ = args

    def read(self, limit: int) -> bytes:
        return self._payload[:limit]


class _FakeOpener:
    def __init__(self, payloads: list[bytes]) -> None:
        self.payloads = payloads
        self.requests: list[Any] = []

    def open(self, request: Any, *, timeout: float) -> _FakeResponse:
        assert timeout > 0
        self.requests.append(request)
        return _FakeResponse(self.payloads.pop(0))


def _install_opener(
    monkeypatch: pytest.MonkeyPatch, payloads: list[bytes]
) -> _FakeOpener:
    opener = _FakeOpener(payloads)

    def factory(*handlers: object) -> _FakeOpener:
        _ = handlers
        return opener

    monkeypatch.setattr(gateway, "build_opener", factory)
    return opener


def _request() -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name="机关桥",
        stable_key="scene-bridge",
        spec=SemanticSceneSpec(
            spec_id="scene-bridge",
            semantic_id="place:bridge",
            kind="illustrated-environment",
            requirements=("source_place_name:机关桥",),
        ),
        cache_key="cache-bridge",
        source_refs=("text://book#paragraph/3",),
        confidence=0.8,
        style_key="story-style-t3",
        context_candidates=("object:石灯",),
    )


def _glb(payload: bytes = b"world") -> bytes:
    size = 12 + len(payload)
    return b"glTF" + (2).to_bytes(4, "little") + size.to_bytes(4, "little") + payload


def _provider():
    return build_http_spatial_provider(
        submit_endpoint="https://gateway.example/spatial/submit",
        poll_endpoint="https://gateway.example/spatial/poll",
        bearer_token="secret-token",
        provider_id="provider:test-spatial",
        provider_version="2026-10",
        cost_units_per_job=7,
        allowed_media_types=frozenset({"model/gltf-binary"}),
    )


def test_t3_http_submit_sends_bounded_brief_and_stable_idempotency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opener = _install_opener(
        monkeypatch,
        [json.dumps({"task_ref": "operation-123"}).encode()],
    )
    task_ref = _provider().submit(_request(), idempotency_key="stable-key-123")

    assert task_ref == "operation-123"
    sent_request = opener.requests[0]
    sent = json.loads(sent_request.data.decode("utf-8"))
    assert sent["place_name"] == "机关桥"
    assert sent["context_candidates"] == ["object:石灯"]
    assert "source_refs" not in sent
    assert "full_source" not in sent
    assert sent_request.headers["Idempotency-key"] == "stable-key-123"
    assert sent_request.headers["Authorization"] == "Bearer secret-token"


def test_t3_http_poll_decodes_inline_asset_and_hashes_locally(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world = _glb()
    _install_opener(
        monkeypatch,
        [
            json.dumps(
                {
                    "state": "succeeded",
                    "artifacts": [
                        {
                            "media_type": "model/gltf-binary",
                            "content_base64": base64.b64encode(world).decode("ascii"),
                        }
                    ],
                }
            ).encode()
        ],
    )

    result = _provider().poll("operation-123")

    assert result.state == "succeeded"
    assert result.artifacts[0].content == world
    assert result.artifacts[0].content_sha256
    assert result.artifacts[0].media_type == "model/gltf-binary"


def test_t3_http_poll_can_fetch_safe_artifact_url_without_forwarding_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world = _glb(b"download")
    opener = _install_opener(
        monkeypatch,
        [
            json.dumps(
                {
                    "state": "succeeded",
                    "artifacts": [
                        {
                            "media_type": "model/gltf-binary",
                            "artifact_url": "https://assets.example/world.glb",
                        }
                    ],
                }
            ).encode(),
            world,
        ],
    )

    result = _provider().poll("operation-123")

    assert result.artifacts[0].content == world
    download = opener.requests[1]
    assert download.method == "GET"
    assert download.headers.get("Authorization") is None


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://example.com/spatial",
        "ftp://example.com/spatial",
        "https://user:pass@example.com/spatial",
        "https://example.com/spatial#fragment",
        "https://169.254.169.254/latest/meta-data",
        "https://10.0.0.5/spatial",
        "https://[fe80::1]/spatial",
        "https://example.com:notaport/spatial",
    ],
)
def test_t3_http_gateway_rejects_unsafe_endpoint_forms(endpoint: str) -> None:
    with pytest.raises(ValueError):
        build_http_spatial_provider(
            submit_endpoint=endpoint,
            poll_endpoint="https://gateway.example/poll",
        )


def test_t3_http_gateway_allows_loopback_for_local_world_model() -> None:
    provider = build_http_spatial_provider(
        submit_endpoint="http://127.0.0.1:8189/submit",
        poll_endpoint="http://127.0.0.1:8189/poll",
    )
    assert provider.provider_id == "http-json-spatial"


def test_t3_http_gateway_rejects_malformed_payloads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_opener(
        monkeypatch,
        [
            json.dumps(
                {
                    "state": "succeeded",
                    "artifacts": [
                        {
                            "media_type": "model/gltf-binary",
                            "content_base64": "not@@base64",
                        }
                    ],
                }
            ).encode()
        ],
    )
    with pytest.raises(ValueError, match="invalid base64"):
        _provider().poll("operation-123")


def test_t3_http_gateway_rejects_header_injection() -> None:
    with pytest.raises(ValueError, match="line breaks"):
        build_http_spatial_provider(
            submit_endpoint="https://gateway.example/submit",
            poll_endpoint="https://gateway.example/poll",
            bearer_token="token\r\nX-Injected: yes",
        )


def test_t3_http_gateway_rejects_unknown_state_or_ambiguous_artifact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_opener(monkeypatch, [json.dumps({"state": "done"}).encode()])
    with pytest.raises(ValueError, match="invalid state"):
        _provider().poll("operation-123")

    _install_opener(
        monkeypatch,
        [
            json.dumps(
                {
                    "state": "succeeded",
                    "artifacts": [
                        {
                            "media_type": "model/gltf-binary",
                            "content_base64": base64.b64encode(_glb()).decode("ascii"),
                            "artifact_url": "https://assets.example/world.glb",
                        }
                    ],
                }
            ).encode()
        ],
    )
    with pytest.raises(ValueError, match="exactly one content source"):
        _provider().poll("operation-123")
