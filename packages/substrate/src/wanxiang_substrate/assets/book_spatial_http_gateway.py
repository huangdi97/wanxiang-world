"""Vendor-neutral HTTP transport for non-authoritative T3 spatial generation.

The remote endpoint receives one bounded scene brief, never a full source. It
must honor Wanxiang's idempotency key and expose a submit/poll JSON protocol.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import base64
import binascii
import hashlib
import json
from dataclasses import replace
from typing import cast
from urllib.request import Request, build_opener

from wanxiang_substrate.assets.book_http_transport import _NoRedirects
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_prompt import (
    _compile_scene_generation_brief,
    _story_visual_profile_from_style_key,
)
from wanxiang_substrate.assets.book_spatial_http_transport import (
    _bounded_read,
    _validate_endpoint,
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialPollResult,
)

_MAX_JSON_RESPONSE_BYTES = 48 * 1024 * 1024
_MAX_ARTIFACT_BYTES = 128 * 1024 * 1024
_MAX_ARTIFACTS = 8
_VALID_STATES = frozenset({"queued", "running", "succeeded", "failed", "cancelled", "expired"})


class _HttpJsonSpatialProvider(_SpatialGenerationProvider):
    def __init__(
        self,
        submit_endpoint: str,
        poll_endpoint: str,
        *,
        bearer_token: str,
        provider_id: str,
        provider_version: str,
        cost_units_per_job: int,
        private_safe: bool,
        allowed_media_types: frozenset[str],
        timeout_seconds: float,
        max_json_response_bytes: int,
        max_artifact_bytes: int,
    ) -> None:
        self.submit_endpoint = _validate_endpoint(submit_endpoint)
        self.poll_endpoint = _validate_endpoint(poll_endpoint)
        if "\r" in bearer_token or "\n" in bearer_token:
            raise ValueError("spatial HTTP bearer token cannot contain line breaks")
        if not provider_id.strip() or not provider_version.strip():
            raise ValueError("spatial HTTP provider requires id and version")
        if cost_units_per_job < 0:
            raise ValueError("spatial HTTP provider cost must be non-negative")
        if timeout_seconds <= 0 or max_json_response_bytes <= 0 or max_artifact_bytes <= 0:
            raise ValueError("spatial HTTP limits must be positive")
        if not allowed_media_types:
            raise ValueError("spatial HTTP provider requires allowed media types")
        self.bearer_token = bearer_token
        self.provider_id = provider_id.strip()
        self.provider_version = provider_version.strip()
        self.cost_units_per_job = cost_units_per_job
        self.private_safe = private_safe
        self.allowed_media_types = allowed_media_types
        self.timeout_seconds = timeout_seconds
        self.max_json_response_bytes = max_json_response_bytes
        self.max_artifact_bytes = max_artifact_bytes
        self.requires_network = True

    def _headers(self, *, idempotency_key: str = "") -> dict[str, str]:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": "Wanxiang-T3-Gateway/1",
        }
        if self.bearer_token:
            headers["authorization"] = f"Bearer {self.bearer_token}"
        if idempotency_key:
            headers["idempotency-key"] = idempotency_key
        return headers

    def _post_json(
        self,
        endpoint: str,
        payload: dict[str, object],
        *,
        idempotency_key: str = "",
    ) -> dict[str, object]:
        request = Request(
            endpoint,
            data=json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
            headers=self._headers(idempotency_key=idempotency_key),
            method="POST",
        )
        try:
            with build_opener(_NoRedirects()).open(
                request, timeout=self.timeout_seconds
            ) as response:
                raw = _bounded_read(
                    response,
                    self.max_json_response_bytes,
                    label="spatial HTTP gateway",
                )
        except (TimeoutError, OSError) as exc:
            raise RuntimeError("spatial HTTP gateway request failed") from exc
        try:
            decoded: object = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError("spatial HTTP gateway returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise ValueError("spatial HTTP gateway response must be an object")
        return cast(dict[str, object], decoded)

    def submit(self, request: _SourceSceneRequest, *, idempotency_key: str) -> str:
        if not idempotency_key.strip() or "\r" in idempotency_key or "\n" in idempotency_key:
            raise ValueError("spatial HTTP submission requires a safe idempotency key")
        style_key = (
            request.style_key
            or hashlib.sha256(f"{request.cache_key}:story-style".encode()).hexdigest()[:24]
        )
        profile = _story_visual_profile_from_style_key(style_key)
        brief = replace(_compile_scene_generation_brief(request, profile), source_refs=())
        body = self._post_json(
            self.submit_endpoint,
            {
                "brief_id": brief.brief_id,
                "scene_key": brief.scene_key,
                "place_name": brief.place_name,
                "style_profile_id": brief.style_profile_id,
                "style_key": brief.style_key,
                "prompt": brief.semantic_prompt,
                "context_candidates": list(brief.source_context_candidates),
                "negative_constraints": list(brief.negative_constraints),
                "brief_version": brief.version,
            },
            idempotency_key=idempotency_key,
        )
        task_ref = body.get("task_ref")
        if (
            not isinstance(task_ref, str)
            or not task_ref.strip()
            or len(task_ref) > 1024
            or "\r" in task_ref
            or "\n" in task_ref
        ):
            raise ValueError("spatial HTTP gateway returned invalid task_ref")
        return task_ref.strip()

    def _download_artifact(self, url: str) -> bytes:
        endpoint = _validate_endpoint(url)
        request = Request(
            endpoint,
            headers={"accept": "*/*", "user-agent": "Wanxiang-T3-Gateway/1"},
            method="GET",
        )
        try:
            with build_opener(_NoRedirects()).open(
                request, timeout=self.timeout_seconds
            ) as response:
                return _bounded_read(
                    response,
                    self.max_artifact_bytes,
                    label="spatial artifact download",
                )
        except (TimeoutError, OSError) as exc:
            raise RuntimeError("spatial artifact download failed") from exc

    def _artifact(self, raw: object) -> _SpatialArtifactCandidate:
        if not isinstance(raw, dict):
            raise ValueError("spatial HTTP artifact must be an object")
        item = cast(dict[str, object], raw)
        media_type = item.get("media_type")
        encoded = item.get("content_base64")
        artifact_url = item.get("artifact_url")
        if not isinstance(media_type, str) or media_type not in self.allowed_media_types:
            raise ValueError("spatial HTTP artifact media type is not allowed")
        if (isinstance(encoded, str)) == (isinstance(artifact_url, str)):
            raise ValueError("spatial HTTP artifact requires exactly one content source")
        if isinstance(encoded, str):
            try:
                content = base64.b64decode(encoded, validate=True)
            except (ValueError, binascii.Error) as exc:
                raise ValueError("spatial HTTP gateway returned invalid base64 artifact") from exc
            if len(content) > self.max_artifact_bytes:
                raise ValueError("spatial HTTP artifact exceeds size limit")
        else:
            assert isinstance(artifact_url, str)
            content = self._download_artifact(artifact_url)
        return _SpatialArtifactCandidate(
            content=content,
            media_type=media_type,
            content_sha256=hashlib.sha256(content).hexdigest(),
        )

    def poll(self, task_ref: str) -> _SpatialPollResult:
        if not task_ref.strip() or len(task_ref) > 1024 or "\r" in task_ref or "\n" in task_ref:
            raise ValueError("spatial HTTP poll requires a safe task_ref")
        body = self._post_json(self.poll_endpoint, {"task_ref": task_ref})
        state = body.get("state")
        if not isinstance(state, str) or state not in _VALID_STATES:
            raise ValueError("spatial HTTP gateway returned invalid state")
        reason = body.get("reason", "")
        if not isinstance(reason, str):
            raise ValueError("spatial HTTP gateway returned invalid reason")
        if state != "succeeded":
            return _SpatialPollResult(state, reason=reason[:2000])  # type: ignore[arg-type]
        raw_artifacts = body.get("artifacts", [])
        if not isinstance(raw_artifacts, list):
            raise ValueError("spatial HTTP gateway returned invalid artifact list")
        artifact_rows = cast(list[object], raw_artifacts)
        if len(artifact_rows) > _MAX_ARTIFACTS:
            raise ValueError("spatial HTTP gateway returned invalid artifact list")
        artifacts = tuple(self._artifact(item) for item in artifact_rows)
        return _SpatialPollResult("succeeded", artifacts, reason[:2000])


def _build_http_spatial_provider(
    *,
    submit_endpoint: str,
    poll_endpoint: str,
    bearer_token: str = "",
    provider_id: str = "http-json-spatial",
    provider_version: str = "1",
    cost_units_per_job: int = 1,
    private_safe: bool = False,
    allowed_media_types: frozenset[str] = frozenset(
        {
            "application/x-ply",
            "image/jpeg",
            "image/png",
            "image/webp",
            "model/gltf-binary",
            "model/ply",
        }
    ),
    timeout_seconds: float = 60.0,
    max_json_response_bytes: int = _MAX_JSON_RESPONSE_BYTES,
    max_artifact_bytes: int = _MAX_ARTIFACT_BYTES,
) -> _SpatialGenerationProvider:
    return _HttpJsonSpatialProvider(
        submit_endpoint,
        poll_endpoint,
        bearer_token=bearer_token,
        provider_id=provider_id,
        provider_version=provider_version,
        cost_units_per_job=cost_units_per_job,
        private_safe=private_safe,
        allowed_media_types=allowed_media_types,
        timeout_seconds=timeout_seconds,
        max_json_response_bytes=max_json_response_bytes,
        max_artifact_bytes=max_artifact_bytes,
    )
