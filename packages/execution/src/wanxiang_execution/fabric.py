"""Isolated execution fabric: the public request/result/provider API.

SAFETY:
The fabric is a proposal source only: this module imports no state writer, so
there is no path from execution to canonical world state. A provider returns
an observation, never a world mutation.

Honest isolation boundary of `LocalProcessProvider`: the process boundary, the
per-execution scratch directory and the scrubbed environment are enforced;
network and memory limits are NOT enforced and every trace says so.
"""

from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from wanxiang_execution.errors import ExecutionError
from wanxiang_execution.local_process import (
    MAX_CAPTURE_BYTES,
    ProcessOutcome,
    build_child_environment,
    output_refs,
    process_isolation,
    run_command,
    sha256_text,
    truncate_to_bytes,
    validate_execution_id,
)
from wanxiang_execution.policy import ExecutionPolicy, authorize
from wanxiang_execution.trace import ExecutionTrace, environment_hash, trace_digest


@dataclass(frozen=True, slots=True)
class ExecutionRequest:
    """One capability execution request for the fabric.

    Attributes:
        execution_id: Unique id; also the scratch directory name, so it must
            match ``[A-Za-z0-9._-]+`` and must not be ``.`` or ``..``.
        capability_id: Capability to execute.
        capability_version: Capability version string.
        command: Non-empty argv tuple to run.
        input_refs: Content digests of the inputs.
        policy: Declared execution policy; authorized before any process starts.
        environment: Extra environment variables for the child. Fabric-owned
            variables (PATH, TEMP/TMP, PYTHONIOENCODING, PYTHONHASHSEED) win.
        stdin_text: Optional text written to the child's stdin; ``None`` closes
            stdin instead of inheriting the parent's.
    """

    execution_id: str
    capability_id: str
    capability_version: str
    command: tuple[str, ...]
    input_refs: tuple[str, ...]
    policy: ExecutionPolicy
    environment: Mapping[str, str] = field(default_factory=dict[str, str])
    stdin_text: str | None = None

    def __post_init__(self) -> None:
        """Validate the id and command shape.

        Raises:
            ExecutionError: If the execution id could escape the workspace, or
                the command is empty or contains an empty argument.
        """
        validate_execution_id(self.execution_id)
        if not self.command:
            raise ExecutionError("command must be a non-empty argv tuple")
        if any(not argument for argument in self.command):
            raise ExecutionError("command arguments must be non-empty strings")


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Outcome of one execution: trace, capped output text, observation.

    Attributes:
        trace: Provider trace for the execution.
        stdout_text: Captured stdout, capped at `MAX_CAPTURE_BYTES`.
        stderr_text: Captured stderr, capped at `MAX_CAPTURE_BYTES`.
        observation: Proposal-only observation for a downstream authority to
            judge; it never mutates world state by itself.
    """

    trace: ExecutionTrace
    stdout_text: str
    stderr_text: str
    observation: dict[str, object]


class LocalProcessProvider:
    """Run one command as a local subprocess with a scrubbed environment.

    Only PROCESS execution is implemented; `authorize` refuses every other
    execution class before a process is created.
    """

    provider_id: str = "execution-local-process"
    provider_version: str = "1.0.0"

    def run(self, request: ExecutionRequest, workspace_dir: Path) -> ExecutionResult:
        """Execute one request in a fresh scratch directory.

        Args:
            request: Validated execution request.
            workspace_dir: Parent directory for the per-execution scratch dir.

        Returns:
            ExecutionResult with the trace, capped output text and a
            proposal-only observation.

        Raises:
            PolicyViolation: If `authorize` refuses the declared policy; in that
                case nothing is executed and no scratch directory is created.
        """
        authorize(request.policy)
        scratch_dir = workspace_dir / request.execution_id
        scratch_dir.mkdir(parents=True, exist_ok=True)
        child_env = build_child_environment(request.environment, scratch_dir)
        started = time.monotonic()
        outcome = run_command(
            command=request.command,
            stdin_text=request.stdin_text,
            child_env=child_env,
            scratch_dir=scratch_dir,
            timeout_seconds=request.policy.wall_seconds_limit,
        )
        wall_ms = int((time.monotonic() - started) * 1000)
        return self._build_result(request, child_env, outcome, wall_ms)

    def _build_result(
        self,
        request: ExecutionRequest,
        child_env: Mapping[str, str],
        outcome: ProcessOutcome,
        wall_ms: int,
    ) -> ExecutionResult:
        """Build the trace, capped outputs and proposal-only observation."""
        stdout_digest = sha256_text(outcome.stdout_text)
        stderr_digest = sha256_text(outcome.stderr_text)
        trace = ExecutionTrace(
            execution_id=request.execution_id,
            capability_id=request.capability_id,
            capability_version=request.capability_version,
            provider_id=self.provider_id,
            provider_version=self.provider_version,
            execution_class=request.policy.execution_class,
            trust=request.policy.trust,
            environment_hash=environment_hash(child_env),
            input_refs=request.input_refs,
            commands=(request.command,),
            output_refs=output_refs(stdout_digest, stderr_digest, outcome),
            exit_status=outcome.exit_status,
            exit_code=outcome.exit_code,
            wall_ms=wall_ms,
            stdout_bytes=len(outcome.stdout_text.encode("utf-8")),
            stderr_bytes=len(outcome.stderr_text.encode("utf-8")),
            stdout_digest=stdout_digest,
            stderr_digest=stderr_digest,
            snapshot_ref=None,
            resume_ref=None,
            isolation=process_isolation(),
        )
        observation: dict[str, object] = {
            "kind": "execution-observation",
            "execution_id": request.execution_id,
            "trace_digest": trace_digest(trace),
            "stdout_digest": trace.stdout_digest,
            "proposal_only": True,
        }
        return ExecutionResult(
            trace=trace,
            stdout_text=truncate_to_bytes(outcome.stdout_text, MAX_CAPTURE_BYTES),
            stderr_text=truncate_to_bytes(outcome.stderr_text, MAX_CAPTURE_BYTES),
            observation=observation,
        )
