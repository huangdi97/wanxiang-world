"""Direct Tencent TokenHub Hy-World T3 adapter behind Wanxiang spatial governance.

Hy-World-2.1-scene is asynchronous: submit returns a task id and polling later
returns signed artifact URLs. Wanxiang downloads only explicitly allowlisted,
locally-verifiable derived assets. SPZ is intentionally not attached until the
repository has a local SPZ validator and renderer contract.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import hashlib
import json
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, build_opener

from wanxiang_substrate.assets.book_http_transport import (
    _NoRedirects,
    _validate_provider_endpoint,
)
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_prompt import (
    _compile_scene_generation_brief,
    _story_visual_profile_from_style_key,
)
from wanxiang_substrate.assets.book_spatial_http_transport import _bounded_read
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialPollResult,
)

_MAX_JSON_BYTES = 2 * 1024 * 1024
_MAX_ARTIFACT_BYTES = 128 * 1024 * 1024
_SUPPORTED_MEDIA_TYPES = frozenset({"model/ply", "image/png", "image/jpeg", "image/webp"})


def _image_media_type(content: bytes) -> str:
    if content.startswith(bytes.fromhex("89504e470d0a1a0a")):
        return "image/png"
    if content.startswith(bytes.fromhex("ffd8ff")):
        return "image/jpeg"
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("TokenHub spatial preview is not PNG, JPEG or WebP")


class _TokenHubSpatialProvider(_SpatialGenerationProvider):
    """Translate TokenHub's async task protocol into Wanxiang's T3 provider ABI."""

    # The raw TokenHub request schema does not provide Wanxiang's idempotency key.
    submit_is_idempotent = False

    def __init__(
        self,
        submit_endpoint: str,
        tasks_endpoint: str,
        *,
        bearer_token: str,
        artifact_hosts: frozenset[str],
        timeout_seconds: float = 120.0,
        cost_units_per_job: int = 8_000_000,
        private_safe: bool = False,
        max_json_bytes: int = _MAX_JSON_BYTES,
        max_artifact_bytes: int = _MAX_ARTIFACT_BYTES,
    ) -> None:
        self.submit_endpoint = _validate_provider_endpoint(
            submit_endpoint, label="TokenHub spatial submit"
        )
        self.tasks_endpoint = _validate_provider_endpoint(
            tasks_endpoint, label="TokenHub spatial tasks"
        ).rstrip("/")
        if not bearer_token.strip():
            raise ValueError("TokenHub spatial requires an API key")
        if "\r" in bearer_token or "\n" in bearer_token:
            raise ValueError("TokenHub spatial API key cannot contain line breaks")
        hosts = frozenset(item.strip().casefold() for item in artifact_hosts if item.strip())
        if not hosts or any("/" in host or "://" in host or "@" in host for host in hosts):
            raise ValueError("TokenHub spatial requires bare artifact host allowlist entries")
        if timeout_seconds <= 0 or max_json_bytes <= 0 or max_artifact_bytes <= 0:
            raise ValueError("TokenHub spatial transport limits must be positive")
        if cost_units_per_job < 0:
            raise ValueError("TokenHub spatial cost must be non-negative")
        self.bearer_token = bearer_token
        self.artifact_hosts = hosts
        self.timeout_seconds = timeout_seconds
        self.max_json_bytes = max_json_bytes
        self.max_artifact_bytes = max_artifact_bytes
        self.provider_id = "tencent-tokenhub-spatial"
        self.provider_version = "hy-world2-scene"
        self.requires_network = True
        self.private_safe = private_safe
        self.cost_units_per_job = cost_units_per_job
        self.allowed_media_types = _SUPPORTED_MEDIA_TYPES

    def _headers(self, *, accept: str = "application/json") -> dict[str, str]:
        return {
            "accept": accept,
            "authorization": f"Bearer {self.bearer_token}",
            "user-agent": "Wanxiang-T3-TokenHub/1",
        }

    def _open(self, request: Request, *, label: str, limit: int) -> bytes:
        try:
            with build_opener(_NoRedirects()).open(
                request, timeout=self.timeout_seconds
            ) as response:
                return _bounded_read(response, limit, label=label)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"{label} request failed") from exc

    def _json(self, request: Request, *, label: str) -> dict[str, object]:
        raw = self._open(request, label=label, limit=self.max_json_bytes)
        try:
            decoded: object = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError(f"{label} returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise ValueError(f"{label} response must be an object")
        return cast(dict[str, object], decoded)

    def submit(self, request: _SourceSceneRequest, *, idempotency_key: str) -> str:
        if not idempotency_key.strip():
            raise ValueError("TokenHub spatial submission requires an idempotency key")
        style_key = request.style_key or request.cache_key[:24]
        profile = _story_visual_profile_from_style_key(style_key)
        brief = _compile_scene_generation_brief(request, profile)
        prompt = brief.semantic_prompt.strip()[:600]
        if not prompt:
            raise ValueError("TokenHub spatial requires a non-empty bounded prompt")
        payload = json.dumps(
            {"model": "hy-world2-scene", "prompt": prompt},
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        headers = self._headers()
        headers["content-type"] = "application/json"
        body = self._json(
            Request(
                self.submit_endpoint,
                data=payload,
                headers=headers,
                method="POST",
            ),
            label="TokenHub spatial submit",
        )
        task_ref = body.get("id")
        if (
            not isinstance(task_ref, str)
            or not task_ref.strip()
            or len(task_ref) > 1024
            or "\r" in task_ref
            or "\n" in task_ref
        ):
            raise ValueError("TokenHub spatial submit returned invalid task id")
        return task_ref.strip()

    def _download(self, url: str, *, media_type: str | None) -> _SpatialArtifactCandidate:
        endpoint = _validate_provider_endpoint(url, label="TokenHub spatial artifact")
        host = (urlsplit(endpoint).hostname or "").casefold()
        if host not in self.artifact_hosts:
            raise ValueError("TokenHub spatial artifact host is not allowed")
        # Provider credentials are scoped to TokenHub control-plane calls.
        # Returned artifact URLs may point at signed COS/CDN hosts; never
        # forward the TokenHub bearer token outside the provider endpoint.
        content = self._open(
            Request(
                endpoint,
                headers={
                    "accept": "*/*",
                    "user-agent": "Wanxiang-T3-TokenHub/1",
                },
                method="GET",
            ),
            label="TokenHub spatial artifact",
            limit=self.max_artifact_bytes,
        )
        resolved_media_type = media_type or _image_media_type(content)
        return _SpatialArtifactCandidate(
            content=content,
            media_type=resolved_media_type,
            content_sha256=hashlib.sha256(content).hexdigest(),
        )

    def poll(self, task_ref: str) -> _SpatialPollResult:
        clean_ref = task_ref.strip()
        if not clean_ref or len(clean_ref) > 1024 or "\r" in clean_ref or "\n" in clean_ref:
            raise ValueError("TokenHub spatial poll requires a safe task id")
        endpoint = _validate_provider_endpoint(
            f"{self.tasks_endpoint}/{quote(clean_ref, safe='')}",
            label="TokenHub spatial poll",
        )
        body = self._json(
            Request(endpoint, headers=self._headers(), method="GET"),
            label="TokenHub spatial poll",
        )
        state = body.get("status")
        if state in {"queued", "running"}:
            return _SpatialPollResult(state)  # type: ignore[arg-type]
        if state in {"failed", "cancelled"}:
            return _SpatialPollResult(
                state,
                reason="provider_task_terminal",  # type: ignore[arg-type]
            )
        if state == "unknown":
            return _SpatialPollResult("failed", reason="provider_task_unknown")
        if state != "succeeded":
            raise ValueError("TokenHub spatial poll returned invalid task state")

        data = body.get("data")
        if not isinstance(data, list) or not data or not isinstance(data[0], dict):
            raise ValueError("TokenHub spatial succeeded without artifact data")
        first = cast(dict[str, object], data[0])
        specs = (
            ("mesh_url", "model/ply"),
            ("mesh_simplified_url", "model/ply"),
            ("point_url", "model/ply"),
            ("super_resolution_image_url", None),
        )
        artifacts: list[_SpatialArtifactCandidate] = []
        for field, media_type in specs:
            url = first.get(field)
            if isinstance(url, str) and url.strip():
                artifacts.append(self._download(url, media_type=media_type))
        if not artifacts:
            raise ValueError("TokenHub spatial returned no locally supported artifacts")
        return _SpatialPollResult("succeeded", tuple(artifacts))


def build_tokenhub_spatial_provider(
    *,
    submit_endpoint: str,
    tasks_endpoint: str,
    bearer_token: str,
    artifact_hosts: frozenset[str],
    timeout_seconds: float = 120.0,
    cost_units_per_job: int = 8_000_000,
    private_safe: bool = False,
) -> _SpatialGenerationProvider:
    """Build direct Hy-World T3 transport; coordinator still owns policy and budget."""
    return _TokenHubSpatialProvider(
        submit_endpoint,
        tasks_endpoint,
        bearer_token=bearer_token,
        artifact_hosts=artifact_hosts,
        timeout_seconds=timeout_seconds,
        cost_units_per_job=cost_units_per_job,
        private_safe=private_safe,
    )
