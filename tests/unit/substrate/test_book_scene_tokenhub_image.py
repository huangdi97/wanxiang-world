"""Direct TokenHub T1 adapter keeps scene briefs bounded and downloads safe rasters."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from email.message import Message
from typing import Any

import pytest
import wanxiang_substrate.assets.book_scene_tokenhub_image as tokenhub
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_scene_tokenhub_image import _TokenHubImageClient


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


def _install_opener(monkeypatch: pytest.MonkeyPatch, payloads: list[bytes]) -> _Opener:
    opener = _Opener(payloads)

    def factory(*handlers: object) -> _Opener:
        _ = handlers
        return opener

    monkeypatch.setattr(tokenhub, "build_opener", factory)
    return opener


def _brief(
    prompt: str = '{"place":"机关桥","task":"immersive environment"}',
) -> _SceneGenerationBrief:
    return _SceneGenerationBrief(
        brief_id="brief:t1-tokenhub",
        scene_key="scene-bridge",
        place_name="机关桥",
        style_profile_id="style:test",
        style_key="style-key",
        semantic_prompt=prompt,
        source_refs=(),
        source_context_candidates=("object:石灯",),
        negative_constraints=("no-readable-source-paragraphs",),
    )


def _success(url: str = "https://assets.example/output.webp") -> bytes:
    return json.dumps(
        {
            "id": "wand-image-1",
            "data": [{"url": url}],
            "tokenhub_usage": {"total_tokens": 20000},
        }
    ).encode()


def test_tokenhub_t1_posts_bounded_deterministic_request_and_downloads_allowlisted_raster(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = b"RIFF" + b"\x10\x00\x00\x00" + b"WEBP" + b"image"
    opener = _install_opener(monkeypatch, [_success(), image])
    client = _TokenHubImageClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/v3-generation",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    result = client.generate(_brief())

    assert result.content == image
    assert result.media_type == "image/webp"
    assert len(opener.requests) == 2
    submitted = json.loads(opener.requests[0].data.decode("utf-8"))
    assert submitted["model"] == "hy-image-v3"
    assert submitted["size"] == "1280x720"
    assert submitted["revise"] is False
    assert 1 <= submitted["seed"] <= 4294967295
    assert submitted["prompt"] == _brief().semantic_prompt
    assert opener.requests[0].headers["Authorization"] == "Bearer secret"
    assert opener.requests[1].full_url == "https://assets.example/output.webp"


def test_tokenhub_t1_rejects_unallowlisted_artifact_host(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_opener(monkeypatch, [_success("https://evil.example/output.png")])
    client = _TokenHubImageClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/v3-generation",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    with pytest.raises(ValueError, match="host is not allowed"):
        client.generate(_brief())


@pytest.mark.parametrize(
    "payload",
    [
        json.dumps({"data": []}).encode(),
        json.dumps({"data": [{}]}).encode(),
        json.dumps({"data": [{"url": ""}]}).encode(),
        json.dumps(
            {
                "data": [{"url": "https://assets.example/output.png"}],
                "tokenhub_usage": {"total_tokens": -1},
            }
        ).encode(),
    ],
)
def test_tokenhub_t1_fails_closed_on_invalid_generation_response(
    monkeypatch: pytest.MonkeyPatch,
    payload: bytes,
) -> None:
    _install_opener(monkeypatch, [payload])
    client = _TokenHubImageClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/v3-generation",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    with pytest.raises(ValueError):
        client.generate(_brief())


def test_tokenhub_t1_enforces_prompt_limit_before_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opener = _install_opener(monkeypatch, [])
    client = _TokenHubImageClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/v3-generation",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    with pytest.raises(ValueError, match="prompt exceeds"):
        client.generate(_brief("x" * 8193))
    assert opener.requests == []


def test_tokenhub_t1_requires_key_and_explicit_artifact_hosts() -> None:
    endpoint = "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/v3-generation"
    with pytest.raises(ValueError, match="API key"):
        _TokenHubImageClient(
            endpoint,
            bearer_token="",
            artifact_hosts=frozenset({"assets.example"}),
        )
    with pytest.raises(ValueError, match="artifact host"):
        _TokenHubImageClient(
            endpoint,
            bearer_token="secret",
            artifact_hosts=frozenset(),
        )
