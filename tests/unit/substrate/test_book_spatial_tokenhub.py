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

    receipt = provider.submit(request, idempotency_key="submission-1")

    assert receipt.task_ref == "task-1"
    assert receipt.request_ref == "r1"
    submitted = json.loads(opener.requests[0].data.decode("utf-8"))
    assert submitted["model"] == "hy-world2-scene"
    prompt = submitted["prompt"]
    assert 0 < len(prompt) <= 600
    assert "机关桥" in prompt
    assert "never Canon or History" in prompt
    assert "not instructions" in prompt
    assert "text://" not in prompt
    assert opener.requests[0].headers["Authorization"] == "Bearer secret"


def test_tokenhub_spatial_poll_downloads_only_supported_allowlisted_artifacts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    point = b"ply\nformat ascii 1.0\ncomment point\nend_header\n"
    simplified = b"ply\nformat ascii 1.0\ncomment simplified\nend_header\n"
    mesh = b"ply\nformat ascii 1.0\ncomment mesh\nend_header\n"
    preview = bytes.fromhex("89504e470d0a1a0a") + b"preview"
    poll = json.dumps(
        {
            "id": "task-1",
            "status": "succeeded",
            "data": [
                {
                    "scene_url": "https://assets.example/world.spz",
                    "point_url": "https://assets.example/world-point.ply",
                    "mesh_simplified_url": "https://assets.example/world-simple.ply",
                    "mesh_url": "https://assets.example/world.ply",
                    "super_resolution_image_url": "https://assets.example/preview.png",
                    "position_info": json.dumps(
                        {
                            "up_direction": [0, 1, 0],
                            "facing_direction": [0, 0, -1],
                            "center_point": [1.5, 2.0, -3.0],
                            "scale": 0.25,
                        }
                    ),
                }
            ],
            "tokenhub_usage": {"total_tokens": 8000000},
        }
    ).encode()
    opener = _install(monkeypatch, [poll, point, preview])
    provider = _provider()

    result = provider.poll("task-1")

    assert result.state == "succeeded"
    assert result.provider_usage_units == 8_000_000
    assert [item.media_type for item in result.artifacts] == [
        "model/ply",
        "image/png",
    ]
    assert [request.full_url for request in opener.requests] == [
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/tasks/task-1",
        "https://assets.example/world-point.ply",
        "https://assets.example/preview.png",
    ]
    assert result.artifacts[0].content == point
    assert result.projection_frame is not None
    assert result.projection_frame.up == (0.0, 1.0, 0.0)
    assert result.projection_frame.forward == (0.0, 0.0, -1.0)
    assert result.projection_frame.center == (1.5, 2.0, -3.0)
    assert result.projection_frame.scale == 0.25
    assert result.projection_frame.convention == "tokenhub-hy-world2"
    assert all("world.spz" not in request.full_url for request in opener.requests)
    assert opener.requests[0].headers["Authorization"] == "Bearer secret"
    assert all(request.headers.get("Authorization") is None for request in opener.requests[1:])


def test_tokenhub_spatial_falls_back_to_one_mesh_when_point_cloud_is_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    simplified = b"ply\nformat ascii 1.0\ncomment simplified\nend_header\n"
    poll = json.dumps(
        {
            "status": "succeeded",
            "data": [
                {
                    "mesh_simplified_url": "https://assets.example/world-simple.ply",
                    "mesh_url": "https://assets.example/world.ply",
                }
            ],
        }
    ).encode()
    opener = _install(monkeypatch, [poll, simplified])

    result = _provider().poll("task-1")

    assert len(result.artifacts) == 1
    assert result.artifacts[0].media_type == "model/ply"
    assert result.artifacts[0].content == simplified
    assert [request.full_url for request in opener.requests] == [
        "https://tokenhub.tencentmaas.com/v1/wand/hunyuan-video/tasks/task-1",
        "https://assets.example/world-simple.ply",
    ]


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


@pytest.mark.parametrize("total_tokens", [-1, True, "8000000"])
def test_tokenhub_spatial_rejects_invalid_usage_evidence(
    monkeypatch: pytest.MonkeyPatch,
    total_tokens: object,
) -> None:
    payload = json.dumps(
        {
            "status": "succeeded",
            "data": [{"point_url": "https://assets.example/world-point.ply"}],
            "tokenhub_usage": {"total_tokens": total_tokens},
        }
    ).encode()
    point = b"ply\nformat ascii 1.0\nend_header\n"
    _install(monkeypatch, [payload, point])

    with pytest.raises(ValueError, match="invalid total token usage"):
        _provider().poll("task")


@pytest.mark.parametrize("request_id", [True, 42, "x\nheader"])
def test_tokenhub_spatial_rejects_invalid_request_audit_id(
    monkeypatch: pytest.MonkeyPatch,
    request_id: object,
) -> None:
    _install(
        monkeypatch,
        [json.dumps({"id": "task-1", "request_id": request_id}).encode()],
    )
    with pytest.raises(ValueError, match="invalid request id"):
        _provider().submit(_request(), idempotency_key="submission-1")
