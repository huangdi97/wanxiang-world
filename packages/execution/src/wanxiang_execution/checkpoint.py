"""Execution boundary checkpoint/resume for preemption-safe R7 runs.

This is deliberately *not* a VM/process-memory snapshot. The local provider can
persist a completed, side-effect-free execution boundary (trace + capped output
blobs) and fast-forward an identical request after a crash/restart without
re-executing it. Non-idempotent external effects stay in the Outbox path.

Checkpoint data is execution evidence, never World History.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from wanxiang_execution.errors import ExecutionError
from wanxiang_execution.fabric import ExecutionRequest, ExecutionResult, LocalProcessProvider
from wanxiang_execution.policy import SecretAccess, SideEffectClass
from wanxiang_execution.trace import (
    EXIT_STATUS_COMPLETED,
    ExecutionTrace,
    environment_hash,
    trace_digest,
)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    return _sha256_bytes(encoded)


def request_fingerprint(request: ExecutionRequest) -> str:
    """Digest every execution-relevant request field without persisting secrets."""
    policy = request.policy
    return _canonical_digest(
        {
            "capability_id": request.capability_id,
            "capability_version": request.capability_version,
            "command": list(request.command),
            "input_refs": list(request.input_refs),
            "environment_hash": environment_hash(request.environment),
            "stdin_digest": _sha256_bytes((request.stdin_text or "").encode("utf-8")),
            "policy": {
                "trust": policy.trust.value,
                "execution_class": policy.execution_class.value,
                "filesystem": policy.filesystem.value,
                "network": policy.network.value,
                "secrets": policy.secrets.value,
                "cpu_seconds_limit": policy.cpu_seconds_limit,
                "memory_mb_limit": policy.memory_mb_limit,
                "wall_seconds_limit": policy.wall_seconds_limit,
                "reproducibility": policy.reproducibility,
                "cost_class": policy.cost_class,
                "side_effects": policy.side_effects.value,
            },
        }
    )


@dataclass(frozen=True, slots=True)
class ExecutionCheckpoint:
    """Content-addressed record for one completed execution boundary."""

    checkpoint_ref: str
    request_fingerprint: str
    trace_digest: str
    stdout_blob: str
    stderr_blob: str
    trace: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "checkpoint_ref": self.checkpoint_ref,
            "request_fingerprint": self.request_fingerprint,
            "trace_digest": self.trace_digest,
            "stdout_blob": self.stdout_blob,
            "stderr_blob": self.stderr_blob,
            "trace": self.trace,
            "canonical": False,
            "snapshot_kind": "boundary-result",
        }


class FileExecutionCheckpointStore:
    """Small content-addressed checkpoint store for local/reference execution."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def save(self, request: ExecutionRequest, result: ExecutionResult) -> str:
        """Persist a reusable completed boundary and return its checkpoint ref."""
        if request.policy.secrets is not SecretAccess.NONE:
            raise ExecutionError("checkpointing secret-bearing execution is forbidden")
        if request.policy.side_effects is not SideEffectClass.NONE:
            raise ExecutionError("external side effects must resume through the outbox")
        if result.trace.exit_status != EXIT_STATUS_COMPLETED or result.trace.exit_code != 0:
            raise ExecutionError("only successfully completed execution can be checkpointed")

        stdout_bytes = result.stdout_text.encode("utf-8")
        stderr_bytes = result.stderr_text.encode("utf-8")
        stdout_blob = _sha256_bytes(stdout_bytes)
        stderr_blob = _sha256_bytes(stderr_bytes)
        self._write_blob(stdout_blob, stdout_bytes)
        self._write_blob(stderr_blob, stderr_bytes)

        request_digest = request_fingerprint(request)
        raw_trace = asdict(result.trace)
        raw_trace["execution_class"] = result.trace.execution_class.value
        raw_trace["trust"] = result.trace.trust.value
        base = {
            "request_fingerprint": request_digest,
            "trace_digest": trace_digest(result.trace),
            "stdout_blob": stdout_blob,
            "stderr_blob": stderr_blob,
            "trace": raw_trace,
        }
        digest = _canonical_digest(base)
        checkpoint_ref = f"execution-checkpoint:{digest}"
        checkpoint = ExecutionCheckpoint(checkpoint_ref=checkpoint_ref, **base)
        self._write_json(self._checkpoint_path(digest), checkpoint.to_dict())
        self._write_json(
            self._request_path(request_digest),
            {"checkpoint_ref": checkpoint_ref, "request_fingerprint": request_digest},
        )
        return checkpoint_ref

    def resume(self, request: ExecutionRequest) -> ExecutionResult | None:
        """Load an identical completed request or return None when no checkpoint exists."""
        request_digest = request_fingerprint(request)
        request_path = self._request_path(request_digest)
        if not request_path.exists():
            return None
        pointer = self._read_json(request_path)
        checkpoint_ref = pointer.get("checkpoint_ref")
        if not isinstance(checkpoint_ref, str) or not checkpoint_ref.startswith(
            "execution-checkpoint:"
        ):
            raise ExecutionError("checkpoint request index is corrupt")
        digest = checkpoint_ref.split(":", 1)[1]
        payload = self._read_json(self._checkpoint_path(digest))
        if payload.get("request_fingerprint") != request_digest:
            raise ExecutionError("checkpoint request fingerprint mismatch")
        self._verify_checkpoint_digest(payload, digest)
        trace = self._trace_from_payload(payload.get("trace"))
        stored_trace_digest = payload.get("trace_digest")
        if stored_trace_digest != trace_digest(trace):
            raise ExecutionError("checkpoint trace digest mismatch")
        stdout = self._read_blob(payload.get("stdout_blob"))
        stderr = self._read_blob(payload.get("stderr_blob"))
        resumed_trace = replace(
            trace,
            snapshot_ref=checkpoint_ref,
            resume_ref=checkpoint_ref,
        )
        observation = {
            "kind": "execution-observation",
            "execution_id": request.execution_id,
            "trace_digest": trace_digest(resumed_trace),
            "stdout_digest": resumed_trace.stdout_digest,
            "proposal_only": True,
            "resumed": True,
            "checkpoint_ref": checkpoint_ref,
        }
        return ExecutionResult(
            trace=resumed_trace,
            stdout_text=stdout.decode("utf-8"),
            stderr_text=stderr.decode("utf-8"),
            observation=observation,
        )

    def _write_blob(self, digest: str, value: bytes) -> None:
        path = self._root / "blobs" / digest
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(value)

    def _read_blob(self, value: object) -> bytes:
        if not isinstance(value, str) or len(value) != 64:
            raise ExecutionError("checkpoint blob reference is invalid")
        path = self._root / "blobs" / value
        if not path.exists():
            raise ExecutionError("checkpoint blob is missing")
        data = path.read_bytes()
        if _sha256_bytes(data) != value:
            raise ExecutionError("checkpoint blob digest mismatch")
        return data

    def _checkpoint_path(self, digest: str) -> Path:
        return self._root / "checkpoints" / f"{digest}.json"

    def _request_path(self, digest: str) -> Path:
        return self._root / "requests" / f"{digest}.json"

    @staticmethod
    def _write_json(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _read_json(path: Path) -> dict[str, object]:
        if not path.exists():
            raise ExecutionError("checkpoint metadata is missing")
        try:
            value: object = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ExecutionError("checkpoint metadata is corrupt") from exc
        if not isinstance(value, dict):
            raise ExecutionError("checkpoint metadata must be an object")
        return {str(key): item for key, item in value.items()}

    @staticmethod
    def _verify_checkpoint_digest(payload: dict[str, object], digest: str) -> None:
        base = {
            "request_fingerprint": payload.get("request_fingerprint"),
            "trace_digest": payload.get("trace_digest"),
            "stdout_blob": payload.get("stdout_blob"),
            "stderr_blob": payload.get("stderr_blob"),
            "trace": payload.get("trace"),
        }
        if _canonical_digest(base) != digest:
            raise ExecutionError("checkpoint metadata digest mismatch")

    @staticmethod
    def _trace_from_payload(value: object) -> ExecutionTrace:
        if not isinstance(value, dict):
            raise ExecutionError("checkpoint trace must be an object")
        from wanxiang_execution.policy import ExecutionClass, TrustLevel

        fields = dict(value)
        try:
            fields["execution_class"] = ExecutionClass(str(fields["execution_class"]))
            fields["trust"] = TrustLevel(str(fields["trust"]))
            return ExecutionTrace(**fields)  # type: ignore[arg-type]
        except (KeyError, TypeError, ValueError) as exc:
            raise ExecutionError("checkpoint trace is invalid") from exc


class CheckpointedProcessRunner:
    """Fast-forward identical completed work; otherwise execute and checkpoint it."""

    def __init__(
        self,
        provider: LocalProcessProvider,
        store: FileExecutionCheckpointStore,
    ) -> None:
        self._provider = provider
        self._store = store

    def run(self, request: ExecutionRequest, workspace_dir: Path) -> ExecutionResult:
        resumed = self._store.resume(request)
        if resumed is not None:
            return resumed
        result = self._provider.run(request, workspace_dir)
        if result.trace.exit_status != EXIT_STATUS_COMPLETED or result.trace.exit_code != 0:
            return result
        checkpoint_ref = self._store.save(request, result)
        trace = replace(result.trace, snapshot_ref=checkpoint_ref)
        observation = dict(result.observation)
        observation["checkpoint_ref"] = checkpoint_ref
        return replace(result, trace=trace, observation=observation)


__all__ = [
    "CheckpointedProcessRunner",
    "ExecutionCheckpoint",
    "FileExecutionCheckpointStore",
    "request_fingerprint",
]
