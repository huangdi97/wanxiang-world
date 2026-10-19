"""Tencent TokenHub Hy-World panorama transport behind Wanxiang T2 governance.

This adapter understands TokenHub's synchronous panorama response shape, but it
still receives only a bounded SceneGenerationBrief. Returned temporary URLs are
downloaded only from explicitly allowlisted artifact hosts.
"""

# pyright: reportPrivateUsage=false, reportUnusedClass=false, reportUnusedFunction=false

from __future__ import annotations

import json
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

from wanxiang_substrate.assets.book_http_transport import (
    _NoRedirects,
    _validate_provider_endpoint,
)
from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageClient,
    _ExternalImageResult,
)
from wanxiang_substrate.assets.book_scene_panorama import _PromptedPanoramaSceneProvider
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider
from wanxiang_substrate.assets.book_tokenhub_prompt import _tokenhub_scene_prompt

_MAX_JSON_BYTES = 1024 * 1024
_MAX_IMAGE_BYTES = 20 * 1024 * 1024


def _image_media_type(content: bytes) -> str:
    if content.startswith(bytes.fromhex("89504e470d0a1a0a")):
        return "image/png"
    if content.startswith(bytes.fromhex("ffd8ff")):
        return "image/jpeg"
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("TokenHub panorama artifact is not PNG, JPEG or WebP")


def _bounded_read(response: object, limit: int, *, label: str) -> bytes:
    headers = getattr(response, "headers", None)
    content_length = headers.get("content-length") if headers is not None else None
    if content_length is not None:
        try:
            declared = int(content_length)
        except ValueError as exc:
            raise ValueError(f"{label} returned invalid content-length") from exc
        if declared > limit:
            raise ValueError(f"{label} exceeds size limit")
    reader = getattr(response, "read", None)
    if not callable(reader):
        raise ValueError(f"{label} response is unreadable")
    content = cast(bytes, reader(limit + 1))
    if len(content) > limit:
        raise ValueError(f"{label} exceeds size limit")
    return content


class _TokenHubPanoramaClient(_ExternalImageClient):
    """Call Hy-World-2.1-panorama and persist the signed output locally."""

    def __init__(
        self,
        endpoint: str,
        *,
        bearer_token: str,
        artifact_hosts: frozenset[str],
        timeout_seconds: float = 120.0,
        max_json_bytes: int = _MAX_JSON_BYTES,
        max_image_bytes: int = _MAX_IMAGE_BYTES,
    ) -> None:
        self.endpoint = _validate_provider_endpoint(endpoint, label="TokenHub panorama")
        if "\r" in bearer_token or "\n" in bearer_token:
            raise ValueError("TokenHub panorama bearer token cannot contain line breaks")
        if not bearer_token.strip():
            raise ValueError("TokenHub panorama requires an API key")
        hosts = frozenset(item.strip().casefold() for item in artifact_hosts if item.strip())
        if not hosts or any("/" in host or "://" in host or "@" in host for host in hosts):
            raise ValueError("TokenHub panorama requires bare artifact host allowlist entries")
        if timeout_seconds <= 0 or max_json_bytes <= 0 or max_image_bytes <= 0:
            raise ValueError("TokenHub panorama transport limits must be positive")
        self.bearer_token = bearer_token
        self.artifact_hosts = hosts
        self.timeout_seconds = timeout_seconds
        self.max_json_bytes = max_json_bytes
        self.max_image_bytes = max_image_bytes

    def _open(self, request: Request, *, label: str, limit: int) -> bytes:
        try:
            with build_opener(_NoRedirects()).open(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                return _bounded_read(response, limit, label=label)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"{label} request failed") from exc

    def _download(self, url: str) -> bytes:
        endpoint = _validate_provider_endpoint(url, label="TokenHub panorama artifact")
        host = (urlsplit(endpoint).hostname or "").casefold()
        if host not in self.artifact_hosts:
            raise ValueError("TokenHub panorama artifact host is not allowed")
        return self._open(
            Request(
                endpoint,
                headers={"accept": "image/*", "user-agent": "Wanxiang-T2-TokenHub/1"},
                method="GET",
            ),
            label="TokenHub panorama artifact",
            limit=self.max_image_bytes,
        )

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        prompt = _tokenhub_scene_prompt(brief)
        payload = json.dumps(
            {"model": "hy-world2-panorama", "prompt": prompt},
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        raw = self._open(
            Request(
                self.endpoint,
                data=payload,
                headers={
                    "accept": "application/json",
                    "authorization": f"Bearer {self.bearer_token}",
                    "content-type": "application/json",
                    "user-agent": "Wanxiang-T2-TokenHub/1",
                },
                method="POST",
            ),
            label="TokenHub panorama",
            limit=self.max_json_bytes,
        )
        try:
            decoded: object = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError("TokenHub panorama returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise ValueError("TokenHub panorama response must be an object")
        body = cast(dict[str, object], decoded)
        if body.get("status") != "succeeded":
            raise RuntimeError("TokenHub panorama generation did not succeed")
        data = body.get("data")
        if not isinstance(data, list) or not data or not isinstance(data[0], dict):
            raise ValueError("TokenHub panorama response has no generated image")
        first = cast(dict[str, object], data[0])
        url = first.get("super_resolution_image_url")
        if not isinstance(url, str) or not url.strip():
            raise ValueError("TokenHub panorama response is missing the main panorama URL")
        content = self._download(url)
        return _ExternalImageResult(content, _image_media_type(content))


def build_tokenhub_panorama_provider(
    *,
    endpoint: str,
    bearer_token: str,
    artifact_hosts: frozenset[str],
    timeout_seconds: float = 120.0,
    cost_units_per_asset: int = 500_000,
    private_safe: bool = False,
) -> SceneImageProvider:
    """Build the direct TokenHub T2 adapter; caller still controls network/budget rights."""
    return _PromptedPanoramaSceneProvider(
        provider_id="tencent-tokenhub-panorama",
        provider_version="hy-world2-panorama",
        client=_TokenHubPanoramaClient(
            endpoint,
            bearer_token=bearer_token,
            artifact_hosts=artifact_hosts,
            timeout_seconds=timeout_seconds,
        ),
        cost_units_per_asset=cost_units_per_asset,
        private_safe=private_safe,
    )
