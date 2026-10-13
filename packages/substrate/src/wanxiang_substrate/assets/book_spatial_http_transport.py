"""Shared safe HTTP primitives for the T3 spatial gateway."""

# pyright: reportUnusedClass=false, reportUnusedFunction=false

from __future__ import annotations

import ipaddress
from typing import Any
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request


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
        raise ValueError("spatial HTTP endpoint cannot contain credentials or fragments")
    host = parsed.hostname
    if not host:
        raise ValueError("spatial HTTP endpoint requires a host")
    try:
        _ = parsed.port
    except ValueError as exc:
        raise ValueError("spatial HTTP endpoint contains an invalid port") from exc
    if parsed.scheme == "http" and host in {"localhost", "127.0.0.1", "::1"}:
        return normalized
    if parsed.scheme == "https":
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            return normalized
        if address.is_global or address.is_loopback:
            return normalized
        raise ValueError("spatial HTTPS endpoint cannot target a non-global IP address")
    raise ValueError("spatial HTTP endpoint must use HTTPS or loopback HTTP")


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
