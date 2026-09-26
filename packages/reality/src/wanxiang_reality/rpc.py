"""JSON-RPC 2.0 over stdio: the Wanxiang history-authority server.

Entry point: ``python -m wanxiang_reality.rpc --stdio``.

One compact request object per stdin line, exactly one compact response object
per stdout line, flushed after every response. Diagnostics go to stderr, so
stdout stays machine-parseable for the Node client that speaks this protocol.
"""

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from collections.abc import Callable, Sequence
from typing import Final, TextIO, cast

from wanxiang_reality.contracts import SERVICE_CONTRACTS
from wanxiang_reality.rpc_support import (
    COMMIT_DENIED,
    INTERNAL_ERROR,
    INVALID_PARAMS,
    INVALID_REQUEST,
    JSONRPC_VERSION,
    PARSE_ERROR,
    REVISION_CONFLICT,
    UNKNOWN_METHOD,
    HistoryEvent,
    RpcError,
    error_envelope,
    events_field,
    force_utf8_stdio,
    int_field,
    params_object,
    parse_request_id,
    seam_digest,
    success_envelope,
    text_field,
)

SERVER_NAME: Final[str] = "wanxiang-reality-rpc"
SERVER_VERSION: Final[str] = "0.1.0"
SCHEMA_ID: Final[str] = "wanxiang.r7.history-rpc.v1"

__all__ = ["HistoryAuthority", "RpcError", "dispatch", "main", "serve_stdio"]


def _fold_state(state: str, event: HistoryEvent) -> str:
    """Fold one event into the running state hash (frozen wire rule)."""
    material = f"{state}|{event.event_id}:{event.payload_digest}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


class HistoryAuthority:
    """In-memory append-only history authority for one server process.

    Only this class mutates worldline history. Every append is guarded by an
    issued capability token and an optimistic expected-revision check, so a
    duplicate or stale command never changes world state.
    """

    def __init__(self) -> None:
        self._events: dict[str, list[HistoryEvent]] = {}
        self._state_hashes: dict[str, str] = {}
        self._holder_audit_refs: dict[str, str] = {}
        self._capability_tokens: set[str] = set()

    def register_holder(self, holder_id: str, audit_ref: str) -> None:
        """Register or re-register a holder; re-registration keeps the latest ref."""
        self._holder_audit_refs[holder_id] = audit_ref

    def grant(self, holder_id: str) -> str:
        """Issue a fresh capability token to a registered holder.

        Raises:
            RpcError: ``-32002`` when ``holder_id`` was never registered.
        """
        if holder_id not in self._holder_audit_refs:
            raise RpcError(COMMIT_DENIED, "unknown holder", {"reason": "unknown-holder"})
        token = uuid.uuid4().hex
        self._capability_tokens.add(token)
        return token

    def head(self, worldline_id: str) -> dict[str, object]:
        """Return ``{"revision", "stateHash"}``; a new worldline is 0 and ``""``."""
        return {
            "revision": len(self._events.get(worldline_id, [])),
            "stateHash": self._state_hashes.get(worldline_id, ""),
        }

    def read(self, worldline_id: str, from_revision: int) -> dict[str, object]:
        """Return events at or after ``from_revision`` in append order."""
        events = self._events.get(worldline_id, [])
        return {"events": [event.to_wire() for event in events[from_revision:]]}

    def append(
        self,
        worldline_id: str,
        expected_revision: int,
        events: Sequence[HistoryEvent],
        capability_token: str,
    ) -> dict[str, object]:
        """Append validated events after the capability and revision checks."""
        if capability_token not in self._capability_tokens:
            raise RpcError(
                COMMIT_DENIED,
                "capability token is not valid",
                {"reason": "unknown-capability-token"},
            )
        current_revision = len(self._events.get(worldline_id, []))
        if expected_revision != current_revision:
            raise RpcError(
                REVISION_CONFLICT,
                "stale expected revision",
                {"expectedRevision": expected_revision, "actualRevision": current_revision},
            )
        if not events:
            raise RpcError(INVALID_PARAMS, "'events' must not be empty")
        state = self._state_hashes.get(worldline_id, "")
        for event in events:
            state = _fold_state(state, event)
        stored = self._events.setdefault(worldline_id, [])
        stored.extend(events)
        self._state_hashes[worldline_id] = state
        return {
            "revision": len(stored),
            "stateHash": state,
            "eventIds": [event.event_id for event in events],
        }

    def checkpoint(self, worldline_id: str) -> dict[str, object]:
        """Return the current head as the checkpoint view (same shape)."""
        return self.head(worldline_id)

    def worldlines(self) -> list[str]:
        """Return known worldline ids in ascending order."""
        return sorted(self._events)


Handler = Callable[[HistoryAuthority, dict[str, object]], dict[str, object]]


def _handle_runtime_info(
    _authority: HistoryAuthority, _params: dict[str, object]
) -> dict[str, object]:
    return {"server": SERVER_NAME, "version": SERVER_VERSION, "schema": SCHEMA_ID}


def _handle_seam_digest(
    _authority: HistoryAuthority, _params: dict[str, object]
) -> dict[str, object]:
    return seam_digest(SERVICE_CONTRACTS)


def _handle_register_holder(
    authority: HistoryAuthority, params: dict[str, object]
) -> dict[str, object]:
    holder_id = text_field(params, "holderId")
    authority.register_holder(holder_id, text_field(params, "auditRef"))
    return {"holderId": holder_id, "registered": True}


def _handle_grant(authority: HistoryAuthority, params: dict[str, object]) -> dict[str, object]:
    holder_id = text_field(params, "holderId")
    return {"holderId": holder_id, "capabilityToken": authority.grant(holder_id)}


def _handle_head(authority: HistoryAuthority, params: dict[str, object]) -> dict[str, object]:
    return authority.head(text_field(params, "worldlineId"))


def _handle_read(authority: HistoryAuthority, params: dict[str, object]) -> dict[str, object]:
    from_revision = int_field(params, "fromRevision")
    if from_revision < 0:
        raise RpcError(INVALID_PARAMS, "'fromRevision' must not be negative")
    return authority.read(text_field(params, "worldlineId"), from_revision)


def _handle_checkpoint(authority: HistoryAuthority, params: dict[str, object]) -> dict[str, object]:
    return authority.checkpoint(text_field(params, "worldlineId"))


def _handle_worldlines(
    authority: HistoryAuthority, _params: dict[str, object]
) -> dict[str, object]:
    return {"worldlines": authority.worldlines()}


def _capability_token(params: dict[str, object]) -> str:
    """Return the append capability token or raise RpcError(-32002)."""
    if "capabilityToken" not in params:
        raise RpcError(
            COMMIT_DENIED, "capability token required", {"reason": "missing-capability-token"}
        )
    token = params["capabilityToken"]
    if not isinstance(token, str):
        raise RpcError(
            COMMIT_DENIED,
            "capability token must be a string",
            {"reason": "invalid-capability-token"},
        )
    return token


def _handle_append(authority: HistoryAuthority, params: dict[str, object]) -> dict[str, object]:
    token = _capability_token(params)
    return authority.append(
        worldline_id=text_field(params, "worldlineId"),
        expected_revision=int_field(params, "expectedRevision"),
        events=events_field(params),
        capability_token=token,
    )


_HANDLERS: Final[dict[str, Handler]] = {
    "runtime.info": _handle_runtime_info,
    "seam.digest": _handle_seam_digest,
    "authority.register_holder": _handle_register_holder,
    "authority.grant": _handle_grant,
    "history.head": _handle_head,
    "history.read": _handle_read,
    "history.checkpoint": _handle_checkpoint,
    "history.worldlines": _handle_worldlines,
    "history.append": _handle_append,
}


def dispatch(
    authority: HistoryAuthority, method: str, params: dict[str, object]
) -> dict[str, object]:
    """Run one JSON-RPC method call, raising ``RpcError`` on protocol failure."""
    handler = _HANDLERS.get(method)
    if handler is None:
        raise RpcError(UNKNOWN_METHOD, f"unknown method: {method}")
    return handler(authority, params)


def _handle_line(authority: HistoryAuthority, line: str) -> dict[str, object]:
    """Parse and execute one request line; always returns a response object."""
    try:
        parsed: object = json.loads(line)
    except ValueError:
        return error_envelope(None, RpcError(PARSE_ERROR, "request is not valid JSON"))
    if not isinstance(parsed, dict):
        return error_envelope(None, RpcError(INVALID_REQUEST, "request must be a JSON object"))
    # JSON objects only ever carry string keys; this narrows the parsed boundary.
    request = cast(dict[str, object], parsed)
    request_id = parse_request_id(request)
    if request_id is None:
        return error_envelope(
            None, RpcError(INVALID_REQUEST, "request 'id' must be an integer or string")
        )
    try:
        if request.get("jsonrpc") != JSONRPC_VERSION:
            raise RpcError(INVALID_REQUEST, "request must declare jsonrpc '2.0'")
        method = request.get("method")
        if not isinstance(method, str) or not method:
            raise RpcError(INVALID_REQUEST, "request 'method' must be a non-empty string")
        result = dispatch(authority, method, params_object(request))
    except RpcError as error:
        return error_envelope(request_id, error)
    except Exception as error:
        # SAFETY: one bad request must never kill the line server; the failure
        # is reported as a typed internal error rather than a traceback.
        print(f"{SERVER_NAME}: internal error: {type(error).__name__}", file=sys.stderr)
        return error_envelope(request_id, RpcError(INTERNAL_ERROR, "internal error"))
    return success_envelope(request_id, result)


def serve_stdio(reader: TextIO, writer: TextIO) -> None:
    """Serve requests line by line until EOF; blank lines are tolerated."""
    authority = HistoryAuthority()
    for raw_line in reader:
        line = raw_line.strip()
        if not line:
            continue
        response = _handle_line(authority, line)
        writer.write(json.dumps(response, separators=(",", ":"), ensure_ascii=False))
        writer.write("\n")
        writer.flush()


def main(argv: Sequence[str] | None = None) -> int:
    """Run the stdio server; ``--stdio`` is accepted and is the default."""
    args = list(sys.argv[1:] if argv is None else argv)
    if args not in ([], ["--stdio"]):
        print("usage: python -m wanxiang_reality.rpc [--stdio]", file=sys.stderr)
        return 2
    force_utf8_stdio()
    serve_stdio(sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
