"""Shared safe HTTP primitives for visual/spatial provider gateways."""

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


def _validate_provider_endpoint(endpoint: str, *, label: str) -> str:
    normalized = endpoint.strip()
    parsed = urlsplit(normalized)
    if parsed.username or parsed.password or parsed.fragment:
        raise ValueError(f"{label} endpoint cannot contain credentials or fragments")
    host = parsed.hostname
    if not host:
        raise ValueError(f"{label} endpoint requires a host")
    try:
        _ = parsed.port
    except ValueError as exc:
        raise ValueError(f"{label} endpoint contains an invalid port") from exc
    if parsed.scheme == "http" and host in {"localhost", "127.0.0.1", "::1"}:
        return normalized
    if parsed.scheme == "https":
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            return normalized
        if address.is_global or address.is_loopback:
            return normalized
        raise ValueError(f"{label} endpoint cannot target a non-global IP address")
    raise ValueError(f"{label} endpoint must use HTTPS or loopback HTTP")
