"""T3-specific bounded reads over shared safe HTTP endpoint primitives."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import Any

from wanxiang_substrate.assets.book_http_transport import _validate_provider_endpoint


def _validate_endpoint(endpoint: str) -> str:
    return _validate_provider_endpoint(endpoint, label="spatial HTTP")


def _bounded_read(response: Any, limit: int, *, label: str) -> bytes:
    content_length = response.headers.get("content-length")
    if content_length is not None:
        try:
            declared_size = int(content_length)
        except ValueError as exc:
            raise ValueError(f"{label} returned invalid content-length") from exc
        if declared_size > limit:
            raise ValueError(f"{label} response exceeds size limit")
    raw = response.read(limit + 1)
    if len(raw) > limit:
        raise ValueError(f"{label} response exceeds size limit")
    return raw
