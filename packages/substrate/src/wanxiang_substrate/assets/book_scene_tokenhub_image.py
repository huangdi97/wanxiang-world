"""Direct Tencent TokenHub Hy-Image T1 adapter behind Wanxiang visual governance.

The synchronous provider receives only a bounded SceneGenerationBrief. Wanxiang
downloads the temporary result immediately from an explicit artifact host and
returns verified raster bytes to the shared T1 materializer.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import hashlib
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
    _PromptedExternalSceneProvider,
)
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider

_MAX_JSON_BYTES = 2 * 1024 * 1024
_MAX_IMAGE_BYTES = 20 * 1024 * 1024
_MAX_PROMPT_CHARS = 8192
_DEFAULT_SIZE = "1280x720"


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


def _image_media_type(content: bytes) -> str:
    if content.startswith(bytes.fromhex("89504e470d0a1a0a")):
        return "image/png"
    if content.startswith(bytes.fromhex("ffd8ff")):
        return "image/jpeg"
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError("TokenHub image artifact is not PNG, JPEG or WebP")


def _validate_usage(body: dict[str, object]) -> int | None:
    raw = body.get("tokenhub_usage")
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError("TokenHub image returned invalid tokenhub_usage")
    total = cast(dict[str, object], raw).get("total_tokens")
    if isinstance(total, bool) or not isinstance(total, int) or total < 0:
        raise ValueError("TokenHub image returned invalid total token usage")
    return total


def _provider_operation_id(body: dict[str, object]) -> str:
    raw = body.get("id", "")
    if not isinstance(raw, str):
        raise ValueError("TokenHub image returned invalid id")
    value = raw.strip()
    if len(value) > 1024 or "\r" in value or "\n" in value:
        raise ValueError("TokenHub image returned invalid id")
    return value


def _provider_request_id(body: dict[str, object]) -> str:
    raw = body.get("request_id", "")
    if not isinstance(raw, str):
        raise ValueError("TokenHub image returned invalid request_id")
    value = raw.strip()
    if len(value) > 1024 or "\r" in value or "\n" in value:
        raise ValueError("TokenHub image returned invalid request_id")
    return value


class _TokenHubImageClient(_ExternalImageClient):
    """Call Hy-Image-3.0 and copy its temporary raster into Wanxiang storage."""

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
        self.endpoint = _validate_provider_endpoint(endpoint, label="TokenHub image")
        if not bearer_token.strip():
            raise ValueError("TokenHub image requires an API key")
        if "\r" in bearer_token or "\n" in bearer_token:
            raise ValueError("TokenHub image API key cannot contain line breaks")
        hosts = frozenset(item.strip().casefold() for item in artifact_hosts if item.strip())
        if not hosts or any("/" in host or "://" in host or "@" in host for host in hosts):
            raise ValueError("TokenHub image requires bare artifact host allowlist entries")
        if timeout_seconds <= 0 or max_json_bytes <= 0 or max_image_bytes <= 0:
            raise ValueError("TokenHub image transport limits must be positive")
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
        endpoint = _validate_provider_endpoint(url, label="TokenHub image artifact")
        host = (urlsplit(endpoint).hostname or "").casefold()
        if host not in self.artifact_hosts:
            raise ValueError("TokenHub image artifact host is not allowed")
        return self._open(
            Request(
                endpoint,
                headers={"accept": "image/*", "user-agent": "Wanxiang-T1-TokenHub/1"},
                method="GET",
            ),
            label="TokenHub image artifact",
            limit=self.max_image_bytes,
        )

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        prompt = brief.semantic_prompt.strip()
        if not prompt or len(prompt) > _MAX_PROMPT_CHARS:
            raise ValueError("TokenHub image prompt exceeds provider limit")
        seed = int(hashlib.sha256(brief.brief_id.encode()).hexdigest()[:8], 16) or 1
        payload = json.dumps(
            {
                "model": "hy-image-v3",
                "prompt": prompt,
                "size": _DEFAULT_SIZE,
                "seed": seed,
                "revise": False,
            },
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
                    "user-agent": "Wanxiang-T1-TokenHub/1",
                },
                method="POST",
            ),
            label="TokenHub image",
            limit=self.max_json_bytes,
        )
        try:
            decoded: object = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError("TokenHub image returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise ValueError("TokenHub image response must be an object")
        body = cast(dict[str, object], decoded)
        provider_usage_units = _validate_usage(body)
        provider_operation_id = _provider_operation_id(body)
        provider_request_id = _provider_request_id(body)
        data = body.get("data")
        if not isinstance(data, list) or not data or not isinstance(data[0], dict):
            raise ValueError("TokenHub image response has no generated image")
        url = cast(dict[str, object], data[0]).get("url")
        if not isinstance(url, str) or not url.strip():
            raise ValueError("TokenHub image response is missing the generated image URL")
        content = self._download(url)
        return _ExternalImageResult(
            content,
            _image_media_type(content),
            provider_usage_units=provider_usage_units,
            provider_request_id=provider_request_id,
            provider_operation_id=provider_operation_id,
        )


def build_tokenhub_image_provider(
    *,
    endpoint: str,
    bearer_token: str,
    artifact_hosts: frozenset[str],
    timeout_seconds: float = 120.0,
    cost_units_per_asset: int = 20_000,
    private_safe: bool = False,
) -> SceneImageProvider:
    """Build direct Hy-Image T1 transport; shared materializer owns rights/budget/cache."""
    return _PromptedExternalSceneProvider(
        provider_id="tencent-tokenhub-image",
        provider_version="hy-image-v3",
        client=_TokenHubImageClient(
            endpoint,
            bearer_token=bearer_token,
            artifact_hosts=artifact_hosts,
            timeout_seconds=timeout_seconds,
        ),
        cost_units_per_asset=cost_units_per_asset,
        private_safe=private_safe,
    )
