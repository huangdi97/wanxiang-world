"""Reference agent harness: a real JSON-RPC process for the R7 harness bridge.

This is a **reference** harness, not the official DeepSeek Harness binary. It
speaks the `wanxiang.r7.agent-harness-rpc.v1` protocol over newline-delimited
JSON-RPC 2.0 on stdio and answers announcements of the world's decision so the
committed/rejected consequence path can be exercised end to end.

Run it directly: `uv run python scripts/r7_reference_harness.py --stdio`.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections.abc import Callable, Mapping
from typing import TextIO, cast

HARNESS_ID = "wanxiang-reference-rule-harness"
HARNESS_VERSION = "1.0.0"
HARNESS_KIND = "reference-rule-harness"
PROTOCOL = "wanxiang.r7.agent-harness-rpc.v1"
DEFAULT_TARGET_REVISION = 3

ERROR_PARSE = -32700
ERROR_INVALID_REQUEST = -32600
ERROR_UNKNOWN_METHOD = -32601
ERROR_INVALID_PARAMS = -32602

JsonObject = dict[str, object]
Handler = Callable[[JsonObject], JsonObject]


class RpcFault(Exception):
    """A JSON-RPC error carrying its wire code."""

    def __init__(self, code: int, message: str, data: JsonObject | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.data: JsonObject = data or {}


def _as_object(value: object, name: str) -> JsonObject:
    """Narrow a decoded JSON value to a string-keyed object.

    INVARIANT:
    The cast is confined to this one JSON boundary and happens only after the
    mapping check; every value stays typed as `object` and is narrowed again at
    its own use site, so no untyped data leaks into the handlers.
    """
    if not isinstance(value, Mapping):
        raise RpcFault(ERROR_INVALID_PARAMS, f"{name} must be an object")
    return cast("JsonObject", value)


def _params(request: JsonObject) -> JsonObject:
    params = request.get("params")
    if params is None:
        return {}
    return _as_object(params, "params")


def _observation(params: JsonObject) -> JsonObject:
    observation = params.get("observation")
    if observation is None:
        raise RpcFault(ERROR_INVALID_PARAMS, "observation is required")
    return _as_object(observation, "observation")


def _text(observation: JsonObject, key: str, default: str) -> str:
    value = observation.get(key)
    return value if isinstance(value, str) else default


def _revision(observation: JsonObject) -> int:
    value = observation.get("revision")
    if not isinstance(value, int) or isinstance(value, bool):
        raise RpcFault(ERROR_INVALID_PARAMS, "observation.revision must be an integer")
    return value


def _context(observation: JsonObject) -> dict[str, str]:
    context = observation.get("allowedContext")
    if context is None:
        return {}
    fields = _as_object(context, "allowedContext")
    return {str(key): str(value) for key, value in fields.items()}


def _proposal_digest(proposal_id: str, action: str) -> str:
    return hashlib.sha256(f"{proposal_id}|{action}".encode()).hexdigest()


def handle_info(params: JsonObject) -> JsonObject:
    """Harness identity. `officialDsh` is false and stays false."""
    del params
    return {
        "harnessId": HARNESS_ID,
        "harnessVersion": HARNESS_VERSION,
        "kind": HARNESS_KIND,
        "protocol": PROTOCOL,
        "officialDsh": False,
    }


def handle_decide(params: JsonObject) -> JsonObject:
    """Deterministic rule: propose until the target revision, then abstain."""
    observation = _observation(params)
    worldline_id = _text(observation, "worldlineId", "")
    if not worldline_id:
        raise RpcFault(ERROR_INVALID_PARAMS, "observation.worldlineId is required")
    revision = _revision(observation)
    context = _context(observation)
    try:
        target = int(context.get("targetRevision", str(DEFAULT_TARGET_REVISION)))
    except ValueError as exc:
        raise RpcFault(ERROR_INVALID_PARAMS, "targetRevision must be an integer") from exc

    if revision >= target:
        return {
            "status": "abstained",
            "proposal": None,
            "reason": f"revision {revision} reached the target {target}",
        }
    action = context.get("pendingAction", "set_status")
    proposal_id = f"prop_{worldline_id}_{revision + 1}"
    return {
        "status": "proposed",
        "proposal": {
            "proposalId": proposal_id,
            "action": action,
            "rationaleRef": f"{HARNESS_KIND}#advance-to-{target}",
            "payloadDigest": _proposal_digest(proposal_id, action),
        },
        "reason": "rule: advance one step towards the target revision",
    }


def handle_consequence(params: JsonObject) -> JsonObject:
    """Acknowledge the committed or rejected consequence."""
    status = params.get("status")
    if status not in ("committed", "rejected"):
        raise RpcFault(ERROR_INVALID_PARAMS, "status must be committed or rejected")
    if not isinstance(params.get("proposalId"), str):
        raise RpcFault(ERROR_INVALID_PARAMS, "proposalId is required")
    return {"acknowledged": True, "status": str(status)}


HANDLERS: dict[str, Handler] = {
    "harness.info": handle_info,
    "harness.decide": handle_decide,
    "harness.consequence": handle_consequence,
}


def dispatch(raw: object, request_id: object) -> JsonObject:
    """Turn one request object into a JSON-RPC response object."""
    if not isinstance(raw, Mapping):
        return _error(request_id, RpcFault(ERROR_INVALID_REQUEST, "request must be an object"))
    request = cast("JsonObject", raw)
    method = request.get("method")
    if not isinstance(method, str):
        return _error(request_id, RpcFault(ERROR_INVALID_REQUEST, "method is required"))
    handler = HANDLERS.get(method)
    if handler is None:
        return _error(request_id, RpcFault(ERROR_UNKNOWN_METHOD, f"unknown method {method}"))
    try:
        return {"jsonrpc": "2.0", "id": request_id, "result": handler(_params(request))}
    except RpcFault as fault:
        return _error(request_id, fault)


def _error(request_id: object, fault: RpcFault) -> JsonObject:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": fault.code, "message": str(fault), "data": fault.data},
    }


def _request_id(decoded: object) -> object:
    """Extract the JSON-RPC id when the decoded line is an object."""
    if not isinstance(decoded, Mapping):
        return None
    return cast("JsonObject", decoded).get("id")


def serve(reader: TextIO, writer: TextIO) -> None:
    """Serve newline-delimited JSON-RPC until the input closes."""
    for line in reader:
        line = line.strip()
        if not line:
            continue
        try:
            decoded: object = json.loads(line)
        except json.JSONDecodeError:
            response = _error(None, RpcFault(ERROR_PARSE, "request is not JSON"))
        else:
            response = dispatch(decoded, _request_id(decoded))
        writer.write(json.dumps(response, ensure_ascii=False) + "\n")
        writer.flush()


def main(argv: list[str] | None = None) -> int:
    """Entry point; only `--stdio` (the default) is supported."""
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] not in ("--stdio",):
        print(f"unsupported arguments: {args}", file=sys.stderr)
        return 2
    serve(sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":  # pragma: no cover - process entry point
    raise SystemExit(main())
