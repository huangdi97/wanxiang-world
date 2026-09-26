"""R7 agent-harness bridge: JSON-RPC transport for the harness port.

The contract (world view, proposals, consequences, the port itself) lives in
:mod:`wanxiang_runtime.r7_agent_harness_contract`; this module is only the
transport. It holds no authority and no commit path: the harness receives the
world's decision, it never makes the world change.

Transport: newline-delimited JSON-RPC 2.0 — one request object per line on the
harness stdin, exactly one response object per line on its stdout. The stderr of
the harness is never treated as protocol.
"""

from __future__ import annotations

import json
import subprocess
import threading
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

from wanxiang_runtime.r7_agent_harness_contract import (
    ERROR_HARNESS_FAILED,
    ERROR_INVALID_PARAMS,
    ERROR_UNKNOWN_METHOD,
    HARNESS_PROTOCOL,
    AgentDecision,
    AgentHarnessProvider,
    AgentProposal,
    HarnessConsequence,
    HarnessError,
    HarnessInfo,
    HarnessProtocolError,
    HarnessUnavailable,
    WorldObservation,
    parse_decision,
)

__all__ = [
    "ERROR_HARNESS_FAILED",
    "ERROR_INVALID_PARAMS",
    "ERROR_UNKNOWN_METHOD",
    "HARNESS_PROTOCOL",
    "AgentDecision",
    "AgentHarnessProvider",
    "AgentProposal",
    "HarnessConsequence",
    "HarnessError",
    "HarnessInfo",
    "HarnessProtocolError",
    "HarnessUnavailable",
    "JsonRpcAgentHarnessProvider",
    "WorldObservation",
    "parse_decision",
]


def _as_field_map(value: Mapping[object, object]) -> dict[str, object]:
    """Normalize a decoded JSON object into a concretely typed mapping."""
    fields: dict[str, object] = {}
    for key, item in value.items():
        if isinstance(key, str):
            fields[key] = item
    return fields


def _as_object(line: str, method: str) -> dict[str, object]:
    """Decode one protocol line into a typed field map, or raise a typed error."""
    try:
        parsed = json.loads(line)
    except json.JSONDecodeError as exc:
        raise HarnessProtocolError(f"harness answer to {method} is not JSON: {exc}") from exc
    # SAFETY: json.loads is the untyped boundary of this module; the decoded
    # object is converted into a typed field map immediately below.
    if not isinstance(parsed, dict):
        raise HarnessProtocolError(f"harness answer to {method} is not an object")
    return _as_field_map(cast("Mapping[object, object]", parsed))


class JsonRpcAgentHarnessProvider:
    """Agent-harness provider that talks to a harness process over stdio."""

    provider_id = "agent-harness-rpc"

    def __init__(
        self,
        command: Sequence[str],
        *,
        cwd: Path,
        request_timeout_seconds: float = 30.0,
    ) -> None:
        if not command:
            raise HarnessUnavailable("a harness command is required")
        self._command = list(command)
        self._cwd = cwd
        self._timeout = request_timeout_seconds
        self._process: subprocess.Popen[str] | None = None
        self._sequence = 0

    def _ensure_process(self) -> subprocess.Popen[str]:
        if self._process is not None and self._process.poll() is None:
            return self._process
        try:
            self._process = subprocess.Popen(
                self._command,
                cwd=self._cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
        except OSError as exc:
            raise HarnessUnavailable(f"cannot start harness {self._command[0]}: {exc}") from exc
        return self._process

    def _read_answer(self, process: subprocess.Popen[str], method: str) -> str:
        """Read one answer line, honouring the request timeout for real.

        CONCURRENCY: a plain `readline()` on a silent harness blocks forever, so
        the read runs in a daemon thread and the caller waits only until the
        deadline; on expiry the child is killed and the caller gets a typed error.
        """
        if process.stdout is None:
            raise HarnessUnavailable("harness process has no usable stdout")
        box: dict[str, str] = {}

        def reader() -> None:
            assert process.stdout is not None
            box["line"] = process.stdout.readline()

        worker = threading.Thread(target=reader, daemon=True)
        worker.start()
        worker.join(self._timeout)
        if worker.is_alive():
            process.kill()
            raise HarnessUnavailable(f"harness did not answer {method} within {self._timeout}s")
        line = box.get("line", "")
        if not line:
            raise HarnessUnavailable(f"harness produced no answer to {method}")
        return line

    def _call(self, method: str, params: Mapping[str, object]) -> dict[str, object]:
        process = self._ensure_process()
        if process.stdin is None or process.stdout is None:
            raise HarnessUnavailable("harness process has no usable stdio")
        self._sequence += 1
        request = {"jsonrpc": "2.0", "id": self._sequence, "method": method, "params": dict(params)}
        try:
            process.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
            process.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise HarnessUnavailable(f"harness closed its input: {exc}") from exc
        line = self._read_answer(process, method)
        envelope = _as_object(line, method)
        error = envelope.get("error")
        if isinstance(error, dict):
            fault = _as_field_map(cast("Mapping[object, object]", error))
            code = fault.get("code")
            message = fault.get("message")
            if code == ERROR_UNKNOWN_METHOD:
                raise HarnessProtocolError(f"harness does not implement {method}")
            raise HarnessError(f"harness error {code}: {message}")
        result = envelope.get("result")
        if not isinstance(result, dict):
            raise HarnessProtocolError(f"harness answer to {method} has no result object")
        return _as_field_map(cast("Mapping[object, object]", result))

    def info(self) -> HarnessInfo:
        result = self._call("harness.info", {})
        harness_id = result.get("harnessId")
        harness_version = result.get("harnessVersion")
        kind = result.get("kind")
        if not isinstance(harness_id, str) or not isinstance(harness_version, str):
            raise HarnessProtocolError("harness.info must return harnessId and harnessVersion")
        return HarnessInfo(
            harness_id=harness_id,
            harness_version=harness_version,
            kind=kind if isinstance(kind, str) else "unknown",
            official_dsh=result.get("officialDsh") is True,
        )

    def decide(self, observation: WorldObservation) -> AgentDecision:
        result = self._call("harness.decide", {"observation": observation.payload()})
        return parse_decision(result)

    def deliver_consequence(self, consequence: HarnessConsequence) -> bool:
        result = self._call("harness.consequence", consequence.payload())
        return result.get("acknowledged") is True

    def close(self) -> None:
        process = self._process
        self._process = None
        if process is None:
            return
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive
            process.kill()
