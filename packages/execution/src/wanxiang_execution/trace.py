"""Execution traces: evidence about one run, never canonical world history.

INVARIANT:
An ExecutionTrace is NOT world history and can never be appended to canonical
history. It is a provider-produced observation about one isolated run; the
fabric only proposes, and this module holds no path to a state writer.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass

from wanxiang_execution.policy import ExecutionClass, TrustLevel

EXIT_STATUS_COMPLETED = "completed"
EXIT_STATUS_TIMEOUT = "timeout"
EXIT_STATUS_FAILED = "failed"
EXIT_STATUS_POLICY_DENIED = "policy_denied"

TIMEOUT_EXIT_CODE = -9


@dataclass(frozen=True, slots=True)
class ExecutionTrace:
    """What one provider observed while executing one request.

    INVARIANT: an ExecutionTrace is NOT world history and can never be appended
    to canonical history. Only a commit authority can turn an observation into
    canonical state.

    Attributes:
        execution_id: Sanitized execution id from the request.
        capability_id: Capability that was executed.
        capability_version: Capability version string.
        provider_id: Provider that ran the execution.
        provider_version: Provider version string.
        execution_class: Declared isolation class.
        trust: Declared trust level.
        environment_hash: sha256 of the canonical JSON of the child environment.
        input_refs: Content digests of the declared inputs.
        commands: Argv of every command that was executed.
        output_refs: Content digests of captured output streams, stdout first
            then stderr, empty streams skipped.
        exit_status: One of EXIT_STATUS_COMPLETED, EXIT_STATUS_TIMEOUT,
            EXIT_STATUS_FAILED or EXIT_STATUS_POLICY_DENIED.
        exit_code: Process exit code; TIMEOUT_EXIT_CODE (-9) on a timeout.
        wall_ms: Measured wall-clock duration in milliseconds.
        stdout_bytes: Full captured stdout size in bytes, before capping.
        stderr_bytes: Full captured stderr size in bytes, before capping.
        stdout_digest: sha256 of the full (uncapped) stdout text.
        stderr_digest: sha256 of the full (uncapped) stderr text.
        snapshot_ref: Always None; snapshot capture is not implemented here.
        resume_ref: Always None; resume is not implemented here.
        isolation: Honest enforcement level per dimension, e.g.
            ``{"process": "enforced", "filesystem_scratch": "enforced",
            "environment": "scrubbed", "network": "not_enforced",
            "memory": "not_enforced"}``. Treat the mapping as read-only.
    """

    execution_id: str
    capability_id: str
    capability_version: str
    provider_id: str
    provider_version: str
    execution_class: ExecutionClass
    trust: TrustLevel
    environment_hash: str
    input_refs: tuple[str, ...]
    commands: tuple[tuple[str, ...], ...]
    output_refs: tuple[str, ...]
    exit_status: str
    exit_code: int
    wall_ms: int
    stdout_bytes: int
    stderr_bytes: int
    stdout_digest: str
    stderr_digest: str
    snapshot_ref: str | None
    resume_ref: str | None
    isolation: dict[str, str]


def trace_digest(trace: ExecutionTrace) -> str:
    """Return the sha256 over the canonical JSON form of every trace field.

    Args:
        trace: Trace to digest.

    Returns:
        Lowercase hex sha256 digest, stable for equal field values.
    """
    payload = json.dumps(asdict(trace), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def environment_hash(environment: Mapping[str, str]) -> str:
    """Return the sha256 over the canonical JSON form of an environment mapping.

    Args:
        environment: Environment variables visible to a child process.

    Returns:
        Lowercase hex sha256 digest; insensitive to key order, sensitive to
        values.
    """
    payload = json.dumps(
        dict(environment), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
