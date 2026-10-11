"""Vendor-neutral HTTP transport adapter for governed T1 scene images.

This module stays inside the asset/provider package so transport code may use
internal bounded-scene records without leaking them across package boundaries.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import base64
import binascii
import json
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageClient,
    _ExternalImageResult,
    _PromptedExternalSceneProvider,
)
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider

_MAX_GATEWAY_RESPONSE_BYTES = 28 * 1024 * 1024


class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request | None:
        _ = (req, fp, code, msg, headers, newurl)
        return None


def _validate_endpoint(endpoint: str) -> str:
    normalized = endpoint.strip()
    parsed = urlsplit(normalized)
    if parsed.username or parsed.password or parsed.fragment:
        raise ValueError("visual HTTP endpoint cannot contain credentials or fragments")
    if parsed.scheme == "https" and parsed.hostname:
        return normalized
    if parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        return normalized
    raise ValueError("visual HTTP endpoint must use HTTPS or loopback HTTP")


class HttpJsonImageClient(_ExternalImageClient):
    """POST one bounded scene brief and decode one inline base64 raster result."""

    def __init__(
        self,
        endpoint: str,
        *,
        bearer_token: str = "",
        timeout_seconds: float = 60.0,
        max_response_bytes: int = _MAX_GATEWAY_RESPONSE_BYTES,
    ) -> None:
        self.endpoint = _validate_endpoint(endpoint)
        self.bearer_token = bearer_token
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes
        if timeout_seconds <= 0:
            raise ValueError("visual HTTP timeout must be positive")
        if max_response_bytes <= 0:
            raise ValueError("visual HTTP response limit must be positive")

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        payload = json.dumps(
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
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": "Wanxiang-T1-Gateway/1",
        }
        if self.bearer_token:
            headers["authorization"] = f"Bearer {self.bearer_token}"
        request = Request(self.endpoint, data=payload, headers=headers, method="POST")
        opener = build_opener(_NoRedirects())
        try:
            with opener.open(request, timeout=self.timeout_seconds) as response:
                content_length = response.headers.get("content-length")
                if content_length is not None:
                    try:
                        declared_size = int(content_length)
                    except ValueError as exc:
                        raise ValueError(
                            "visual HTTP gateway returned invalid content-length"
                        ) from exc
                    if declared_size > self.max_response_bytes:
                        raise ValueError("visual HTTP gateway response exceeds size limit")
                raw = response.read(self.max_response_bytes + 1)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise RuntimeError("visual HTTP gateway request failed") from exc
        if len(raw) > self.max_response_bytes:
            raise ValueError("visual HTTP gateway response exceeds size limit")
        try:
            decoded: object = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError("visual HTTP gateway returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise ValueError("visual HTTP gateway response must be an object")
        body = cast(dict[str, object], decoded)
        encoded, media_type = body.get("image_base64"), body.get("media_type")
        if not isinstance(encoded, str) or not isinstance(media_type, str):
            raise ValueError("visual HTTP gateway response requires image_base64 and media_type")
        try:
            image = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error) as exc:
            raise ValueError("visual HTTP gateway returned invalid base64 image") from exc
        return _ExternalImageResult(image, media_type)


def build_http_scene_provider(
    *,
    endpoint: str,
    bearer_token: str = "",
    provider_id: str = "http-json-image",
    provider_version: str = "1",
    timeout_seconds: float = 60.0,
    cost_units_per_asset: int = 1,
    private_safe: bool = False,
) -> SceneImageProvider:
    """Build the governed T1 provider; network/cost rights remain materializer policy."""
    return _PromptedExternalSceneProvider(
        provider_id=provider_id,
        provider_version=provider_version,
        client=HttpJsonImageClient(
            endpoint,
            bearer_token=bearer_token,
            timeout_seconds=timeout_seconds,
        ),
        cost_units_per_asset=cost_units_per_asset,
        private_safe=private_safe,
    )


__all__ = ["HttpJsonImageClient", "build_http_scene_provider"]
