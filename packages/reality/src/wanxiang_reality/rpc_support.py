"""Wire helpers for the JSON-RPC 2.0 history-authority server.

The server module (:mod:`wanxiang_reality.rpc`) owns transport and dispatch;
this module owns the frozen wire vocabulary: JSON-RPC error codes, the event
value object, request-parameter validation and the seam digest rule.
"""

from __future__ import annotations

import hashlib
import io
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final, cast

from wanxiang_reality.contracts import ServiceContract

JSONRPC_VERSION: Final[str] = "2.0"

PARSE_ERROR: Final[int] = -32700
INVALID_REQUEST: Final[int] = -32600
UNKNOWN_METHOD: Final[int] = -32601
INVALID_PARAMS: Final[int] = -32602
INTERNAL_ERROR: Final[int] = -32603
REVISION_CONFLICT: Final[int] = -32001
COMMIT_DENIED: Final[int] = -32002


class RpcError(Exception):
    """A JSON-RPC failure carrying the frozen wire code and structured data."""

    def __init__(self, code: int, message: str, data: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.data: dict[str, object] = {} if data is None else data


@dataclass(frozen=True, slots=True)
class HistoryEvent:
    """One append-only history event in its frozen wire form."""

    event_id: str
    kind: str
    payload_digest: str

    def to_wire(self) -> dict[str, object]:
        """Return the compact JSON object this event travels as."""
        return {"eventId": self.event_id, "kind": self.kind, "payloadDigest": self.payload_digest}


def as_object(value: object, message: str) -> dict[str, object]:
    """Return ``value`` as a JSON object or raise RpcError(-32602)."""
    if not isinstance(value, dict):
        raise RpcError(INVALID_PARAMS, message)
    # JSON objects only ever carry string keys; this narrows the parsed
    # boundary to the typed shape that every accessor below re-validates.
    return cast(dict[str, object], value)


def text_field(fields: dict[str, object], key: str) -> str:
    """Return a required string field or raise RpcError(-32602)."""
    value = fields.get(key)
    if not isinstance(value, str):
        raise RpcError(INVALID_PARAMS, f"{key!r} must be a string")
    return value


def int_field(fields: dict[str, object], key: str) -> int:
    """Return a required integer field or raise RpcError(-32602).

    JSON ``true``/``false`` decode to Python bools, which are rejected here:
    revisions and offsets must be real integers on the wire.
    """
    value = fields.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise RpcError(INVALID_PARAMS, f"{key!r} must be an integer")
    return value


def parse_event(raw: object) -> HistoryEvent:
    """Validate one wire event object or raise RpcError(-32602)."""
    fields = as_object(raw, "each event must be a JSON object")
    return HistoryEvent(
        event_id=text_field(fields, "eventId"),
        kind=text_field(fields, "kind"),
        payload_digest=text_field(fields, "payloadDigest"),
    )


def events_field(fields: dict[str, object]) -> tuple[HistoryEvent, ...]:
    """Return the validated ``events`` array or raise RpcError(-32602)."""
    raw = fields.get("events")
    if not isinstance(raw, list):
        raise RpcError(INVALID_PARAMS, "'events' must be an array")
    items = cast(list[object], raw)
    return tuple(parse_event(item) for item in items)


def params_object(request: dict[str, object]) -> dict[str, object]:
    """Return the request ``params`` object, defaulting to an empty object."""
    raw = request.get("params")
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise RpcError(INVALID_PARAMS, "'params' must be a JSON object")
    return cast(dict[str, object], raw)


def parse_request_id(request: dict[str, object]) -> int | str | None:
    """Return the request id when it is an integer or string, else ``None``."""
    value = request.get("id")
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, str)):
        return value
    return None


def success_envelope(request_id: int | str, result: dict[str, object]) -> dict[str, object]:
    """Build the frozen JSON-RPC success envelope."""
    return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}


def error_envelope(request_id: int | str | None, error: RpcError) -> dict[str, object]:
    """Build the frozen JSON-RPC error envelope (``data`` is always present)."""
    return {
        "jsonrpc": JSONRPC_VERSION,
        "id": request_id,
        "error": {"code": error.code, "message": error.message, "data": error.data},
    }


def seam_digest(contracts: Sequence[ServiceContract]) -> dict[str, object]:
    """Return the frozen seam digest and its sorted contract identity list.

    The digest is sha256 over the compact UTF-8 JSON encoding of
    ``[{"id": ..., "apiVersion": ...}]`` sorted by ``id`` with no spaces, so
    it matches JavaScript ``JSON.stringify`` byte for byte.
    """
    entries: list[dict[str, str]] = [
        {"id": contract.contract_id, "apiVersion": contract.api_version} for contract in contracts
    ]
    entries.sort(key=lambda entry: entry["id"])
    encoded = json.dumps(entries, separators=(",", ":"), ensure_ascii=False)
    return {
        "digest": hashlib.sha256(encoded.encode("utf-8")).hexdigest(),
        "contracts": entries,
    }


def force_utf8_stdio() -> None:
    """Reconfigure the standard streams to the frozen UTF-8 wire encoding."""
    # COMPATIBILITY: the wire format is UTF-8 while Windows console streams
    # default to the ANSI code page, so both ends must agree.
    for stream in (sys.stdin, sys.stdout):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8")
