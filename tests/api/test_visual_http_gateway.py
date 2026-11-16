"""HTTP T1 gateway transports bounded briefs and validates responses."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import base64
import json
from email.message import Message
from typing import Any

import pytest
import wanxiang_substrate.assets.book_scene_http_gateway as gateway
from wanxiang_substrate.assets.book_scene_http_gateway import HttpJsonImageClient
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief


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
    def __init__(self, payload: bytes) -> None:
        self.payload = payload
        self.request: Any = None

    def open(self, request: Any, *, timeout: float) -> _FakeResponse:
        assert timeout > 0
        self.request = request
        return _FakeResponse(self.payload)


def _fake_build_opener(payload: bytes) -> tuple[_FakeOpener, object]:
    opener = _FakeOpener(payload)

    def factory(*handlers: object) -> _FakeOpener:
        _ = handlers
        return opener

    return opener, factory


def _brief() -> _SceneGenerationBrief:
    return _SceneGenerationBrief(
        brief_id="brief:test",
        scene_key="scene-1",
        place_name="机关桥",
        style_profile_id="style:test",
        style_key="style-key",
        semantic_prompt='{"place":"机关桥","task":"environment"}',
        source_refs=(),
        source_context_candidates=("object:石灯",),
        negative_constraints=("no-readable-source-paragraphs",),
    )


def test_http_gateway_sends_only_bounded_brief_and_decodes_inline_image(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = bytes.fromhex("89504e470d0a1a0a") + b"scene"
    raw = json.dumps(
        {
            "image_base64": base64.b64encode(image).decode("ascii"),
            "media_type": "image/png",
        }
    ).encode()
    opener, factory = _fake_build_opener(raw)
    monkeypatch.setattr(gateway, "build_opener", factory)
    client = HttpJsonImageClient(
        "https://gateway.example/generate",
        bearer_token="secret-token",
    )

    result = client.generate(_brief())

    assert result.content == image
    assert result.media_type == "image/png"
    assert opener.request is not None
    sent = json.loads(opener.request.data.decode("utf-8"))
    assert sent["place_name"] == "机关桥"
    assert sent["context_candidates"] == ["object:石灯"]
    assert "source_refs" not in sent
    assert "full_source" not in sent
    assert opener.request.headers["Authorization"] == "Bearer secret-token"


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://example.com/generate",
        "ftp://example.com/image",
        "https://user:pass@example.com/image",
        "https://example.com/image#fragment",
        "https://169.254.169.254/latest/meta-data",
        "https://10.0.0.5/generate",
        "https://[fe80::1]/generate",
        "https://example.com:notaport/generate",
    ],
)
def test_http_gateway_rejects_unsafe_endpoint_forms(endpoint: str) -> None:
    with pytest.raises(ValueError):
        HttpJsonImageClient(endpoint)


def test_http_gateway_allows_loopback_http_for_local_model_gateway() -> None:
    client = HttpJsonImageClient("http://127.0.0.1:8188/generate")
    assert client.endpoint.startswith("http://127.0.0.1:")


def test_http_gateway_rejects_malformed_base64(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = json.dumps({"image_base64": "not@@base64", "media_type": "image/png"}).encode()
    _, factory = _fake_build_opener(raw)
    monkeypatch.setattr(gateway, "build_opener", factory)
    with pytest.raises(ValueError, match="invalid base64"):
        HttpJsonImageClient("https://gateway.example/generate").generate(_brief())


def test_http_gateway_rejects_bearer_token_header_injection() -> None:
    with pytest.raises(ValueError, match="line breaks"):
        HttpJsonImageClient(
            "https://gateway.example/generate",
            bearer_token="token\r\nX-Injected: yes",
        )


def test_http_gateway_allows_public_ip_https_and_loopback_https() -> None:
    public = HttpJsonImageClient("https://8.8.8.8/generate")
    loopback = HttpJsonImageClient("https://127.0.0.1/generate")
    assert public.endpoint.startswith("https://")
    assert loopback.endpoint.startswith("https://")
