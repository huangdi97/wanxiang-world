"""Direct TokenHub T3 adapter translates official async jobs into Wanxiang artifacts."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from email.message import Message
from typing import Any

import pytest
import wanxiang_substrate.assets.book_spatial_tokenhub as tokenhub
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_spatial_tokenhub import _TokenHubSpatialProvider
from wanxiang_substrate.assets.foundry import SemanticSceneSpec


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


def _install(monkeypatch: pytest.MonkeyPatch, payloads: list[bytes]) -> _Opener:
    opener = _Opener(payloads)

    def factory(*handlers: object) -> _Opener:
        _ = handlers
        return opener

    monkeypatch.setattr(tokenhub, "build_opener", factory)
    return opener


def _request() -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name="机关桥",
        stable_key="scene-bridge",
        spec=SemanticSceneSpec(
            spec_id="scene-bridge",
            semantic_id="place:bridge",
            kind="illustrated-environment",
            requirements=(
                "source_place_name:机关桥",
                "source_context_candidate:object:石灯",
            ),
        ),
        cache_key="cache-bridge",
        style_key="style-key",
    )


def _provider() -> _TokenHubSpatialProvider:
    return _TokenHubSpatialProvider(
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/world2-scene",
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/tasks",
        bearer_token="secret",
        artifact_hosts=frozenset({"assets.example"}),
    )


def test_tokenhub_spatial_submit_uses_bounded_text_scene_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opener = _install(
        monkeypatch,
        [json.dumps({"id": "task-1", "request_id": "r1"}).encode()],
    )
    provider = _provider()
    request = _request()
    request = _SourceSceneRequest(
        request.place_name,
        request.stable_key,
        request.spec,
        request.cache_key,
        style_key=request.style_key,
        context_candidates=("object:" + "景" * 900,),
    )

    task_ref = provider.submit(request, idempotency_key="submission-1")

    assert task_ref == "task-1"
    submitted = json.loads(opener.requests[0].data.decode("utf-8"))
    assert submitted["model"] == "hy-world2-scene"
    assert 0 < len(submitted["prompt"]) <= 600
    assert opener.requests[0].headers["Authorization"] == "Bearer secret"


def test_tokenhub_spatial_poll_downloads_only_supported_allowlisted_artifacts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mesh = b"ply\nformat ascii 1.0\nend_header\n"
    preview = bytes.fromhex("89504e470d0a1a0a") + b"preview"
    poll = json.dumps(
        {
            "id": "task-1",
            "status": "succeeded",
            "data": [
                {
                    "scene_url": "https://assets.example/world.spz",
                    "mesh_url": "https://assets.example/world.ply",
                    "super_resolution_image_url": "https://assets.example/preview.png",
                }
            ],
            "tokenhub_usage": {"total_tokens": 8000000},
        }
    ).encode()
    opener = _install(monkeypatch, [poll, mesh, preview])
    provider = _provider()

    result = provider.poll("task-1")

    assert result.state == "succeeded"
    assert [item.media_type for item in result.artifacts] == ["model/ply", "image/png"]
    assert [request.full_url for request in opener.requests] == [
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/tasks/task-1",
        "https://assets.example/world.ply",
        "https://assets.example/preview.png",
    ]
    assert all("world.spz" not in request.full_url for request in opener.requests)
    assert opener.requests[0].headers["Authorization"] == "Bearer secret"
    assert all(request.headers.get("Authorization") is None for request in opener.requests[1:])


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("queued", "queued"),
        ("running", "running"),
        ("failed", "failed"),
        ("cancelled", "cancelled"),
        ("unknown", "running"),
    ],
)
def test_tokenhub_spatial_maps_provider_states(
    monkeypatch: pytest.MonkeyPatch,
    status: str,
    expected: str,
) -> None:
    _install(monkeypatch, [json.dumps({"status": status}).encode()])
    result = _provider().poll("task")
    assert result.state == expected


def test_tokenhub_spatial_rejects_unallowlisted_artifact_host(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    poll = json.dumps(
        {
            "status": "succeeded",
            "data": [{"mesh_url": "https://evil.example/world.ply"}],
        }
    ).encode()
    _install(monkeypatch, [poll])
    with pytest.raises(ValueError, match="host is not allowed"):
        _provider().poll("task")


def test_tokenhub_spatial_requires_key_and_artifact_allowlist() -> None:
    submit = "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/world2-scene"
    tasks = "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/tasks"
    with pytest.raises(ValueError, match="API key"):
        _TokenHubSpatialProvider(
            submit,
            tasks,
            bearer_token="",
            artifact_hosts=frozenset({"assets.example"}),
        )
    with pytest.raises(ValueError, match="artifact host"):
        _TokenHubSpatialProvider(
            submit,
            tasks,
            bearer_token="secret",
            artifact_hosts=frozenset(),
        )


def test_raw_tokenhub_spatial_submit_is_not_claimed_idempotent() -> None:
    assert _provider().submit_is_idempotent is False
