"""Deployable vendor-neutral HTTP bridge for governed T1 image generation.

The endpoint is deployment configuration, never player input. Wanxiang sends
only the already-bounded SceneGenerationBrief and accepts inline base64 raster
bytes; redirects are disabled to keep the outbound trust boundary explicit.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import base64
import binascii
import json
import os
from dataclasses import dataclass
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
_DEFAULT_TIMEOUT_SECONDS = 60.0


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


def _bool_env(name: str, *, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    value = raw.strip().casefold()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean flag")


def _int_env(name: str, *, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


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


@dataclass(frozen=True, slots=True)
class _HttpJsonImageClient(_ExternalImageClient):
    endpoint: str
    bearer_token: str = ""
    timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS
    max_response_bytes: int = _MAX_GATEWAY_RESPONSE_BYTES

    def __post_init__(self) -> None:
        _validate_endpoint(self.endpoint)
        if self.timeout_seconds <= 0:
            raise ValueError("visual HTTP timeout must be positive")
        if self.max_response_bytes <= 0:
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
            raise ValueError(
                "visual HTTP gateway response requires image_base64 and media_type"
            )
        try:
            image = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error) as exc:
            raise ValueError("visual HTTP gateway returned invalid base64 image") from exc
        return _ExternalImageResult(image, media_type)


@dataclass(frozen=True, slots=True)
class _VisualHttpRuntime:
    provider: SceneImageProvider | None
    allow_network: bool
    max_cost_units: int


def _visual_http_runtime_from_env() -> _VisualHttpRuntime:
    endpoint = os.environ.get("WANXIANG_VISUAL_HTTP_ENDPOINT", "").strip()
    allow_network = _bool_env("WANXIANG_VISUAL_ALLOW_NETWORK")
    max_cost_units = _int_env("WANXIANG_VISUAL_MAX_COST_UNITS", default=0)
    if not endpoint:
        if allow_network:
            raise ValueError(
                "WANXIANG_VISUAL_ALLOW_NETWORK requires WANXIANG_VISUAL_HTTP_ENDPOINT"
            )
        return _VisualHttpRuntime(None, False, max_cost_units)
    provider = _PromptedExternalSceneProvider(
        provider_id=(
            os.environ.get("WANXIANG_VISUAL_PROVIDER_ID", "http-json-image").strip()
            or "http-json-image"
        ),
        provider_version=(
            os.environ.get("WANXIANG_VISUAL_PROVIDER_VERSION", "1").strip() or "1"
        ),
        client=_HttpJsonImageClient(
            endpoint=_validate_endpoint(endpoint),
            bearer_token=os.environ.get("WANXIANG_VISUAL_HTTP_BEARER_TOKEN", ""),
            timeout_seconds=float(
                _int_env("WANXIANG_VISUAL_HTTP_TIMEOUT_SECONDS", default=60)
            ),
        ),
        cost_units_per_asset=_int_env("WANXIANG_VISUAL_COST_UNITS", default=1),
        private_safe=_bool_env("WANXIANG_VISUAL_PRIVATE_SAFE"),
    )
    return _VisualHttpRuntime(provider, allow_network, max_cost_units)
