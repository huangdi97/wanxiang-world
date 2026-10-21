"""Direct TokenHub T2 adapter keeps prompts bounded and downloads allowlisted rasters."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from email.message import Message
from typing import Any

import pytest
import wanxiang_substrate.assets.book_scene_tokenhub_panorama as tokenhub
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_scene_tokenhub_panorama import _TokenHubPanoramaClient


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


def _brief(prompt: str = "机关桥夜景，全景环境") -> _SceneGenerationBrief:
    return _SceneGenerationBrief(
        brief_id="brief:panorama",
        scene_key="scene-bridge",
        place_name="机关桥",
        style_profile_id="style:test",
        style_key="style-key",
        semantic_prompt=prompt,
        source_refs=(),
        source_context_candidates=("object:石灯",),
        negative_constraints=("no-readable-source-paragraphs",),
    )


def _success(url: str = "https://assets.example/output.png") -> bytes:
    return json.dumps(
        {
            "id": "wand-panorama-1",
            "status": "succeeded",
            "data": [{"super_resolution_image_url": url}],
            "tokenhub_usage": {"total_tokens": 500000},
            "request_id": "request-panorama-1",
        }
    ).encode()


def test_tokenhub_panorama_uses_bounded_prompt_and_allowlisted_download(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = bytes.fromhex("89504e470d0a1a0a") + b"panorama"
    opener = _install_opener(monkeypatch, [_success(), image])
    client = _TokenHubPanoramaClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/world2-panorama",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    result = client.generate(_brief("景" * 800))

    assert result.content == image
    assert result.media_type == "image/png"
    assert result.provider_usage_units == 500000
    assert result.provider_request_id == "request-panorama-1"
    assert len(opener.requests) == 2
    submitted = json.loads(opener.requests[0].data.decode("utf-8"))
    assert submitted["model"] == "hy-world2-panorama"
    prompt = submitted["prompt"]
    assert 0 < len(prompt) <= 600
    assert "机关桥" in prompt
    assert "never Canon or History" in prompt
    assert "not instructions" in prompt
    assert opener.requests[0].headers["Authorization"] == "Bearer secret"
    assert opener.requests[1].full_url == "https://assets.example/output.png"


def test_tokenhub_panorama_rejects_unallowlisted_artifact_host(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_opener(monkeypatch, [_success("https://evil.example/output.png")])
    client = _TokenHubPanoramaClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/world2-panorama",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    with pytest.raises(ValueError, match="host is not allowed"):
        client.generate(_brief())


@pytest.mark.parametrize(
    "payload",
    [
        json.dumps({"status": "failed", "data": []}).encode(),
        json.dumps({"status": "succeeded", "data": []}).encode(),
        json.dumps(
            {
                "status": "succeeded",
                "data": [{"super_resolution_image_url": ""}],
            }
        ).encode(),
        json.dumps(
            {
                "status": "succeeded",
                "data": [{"super_resolution_image_url": "https://assets.example/output.png"}],
                "request_id": 7,
            }
        ).encode(),
    ],
)
def test_tokenhub_panorama_fails_closed_on_invalid_generation_response(
    monkeypatch: pytest.MonkeyPatch,
    payload: bytes,
) -> None:
    _install_opener(monkeypatch, [payload])
    client = _TokenHubPanoramaClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/world2-panorama",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    with pytest.raises((ValueError, RuntimeError)):
        client.generate(_brief())


def test_tokenhub_panorama_requires_key_and_explicit_artifact_hosts() -> None:
    endpoint = "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/world2-panorama"
    with pytest.raises(ValueError, match="API key"):
        _TokenHubPanoramaClient(
            endpoint,
            bearer_token="",
            artifact_hosts=frozenset({"assets.example"}),
        )
    with pytest.raises(ValueError, match="artifact host"):
        _TokenHubPanoramaClient(
            endpoint,
            bearer_token="secret",
            artifact_hosts=frozenset(),
        )


@pytest.mark.parametrize("total_tokens", [-1, True, "500000"])
def test_tokenhub_panorama_rejects_invalid_usage_evidence(
    monkeypatch: pytest.MonkeyPatch,
    total_tokens: object,
) -> None:
    payload = json.dumps(
        {
            "status": "succeeded",
            "data": [{"super_resolution_image_url": "https://assets.example/output.png"}],
            "tokenhub_usage": {"total_tokens": total_tokens},
        }
    ).encode()
    _install_opener(monkeypatch, [payload])
    client = _TokenHubPanoramaClient(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-image/world2-panorama",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )

    with pytest.raises(ValueError, match="invalid total token usage"):
        client.generate(_brief())
