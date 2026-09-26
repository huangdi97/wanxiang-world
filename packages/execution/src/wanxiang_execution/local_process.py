"""Local process mechanics for the execution fabric.

This module owns the "how a process is actually run" concern: execution-id
validation, the minimal child environment, subprocess invocation, timeout
normalization and output capture. It holds no policy vocabulary and no
observation construction; `fabric.py` owns those.

SAFETY: nothing here can write canonical world state; the module only spawns
processes and reads their captured output.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from wanxiang_execution.errors import ExecutionError
from wanxiang_execution.trace import (
    EXIT_STATUS_COMPLETED,
    EXIT_STATUS_FAILED,
    EXIT_STATUS_TIMEOUT,
    TIMEOUT_EXIT_CODE,
)

MAX_CAPTURE_BYTES = 64 * 1024
"""Captured stdout/stderr bytes returned to the caller. Digests and byte counts
always cover the full, uncapped output."""

_ENV_ALLOWLIST = ("PATH", "SYSTEMROOT", "PATHEXT")
_SCRATCH_ENV_VARS = ("TEMP", "TMP")
_PYTHON_ENV_VARS: tuple[tuple[str, str], ...] = (
    ("PYTHONIOENCODING", "utf-8"),
    ("PYTHONHASHSEED", "0"),
)
_EXECUTION_ID_RE = re.compile(r"[A-Za-z0-9._-]+")


@dataclass(frozen=True, slots=True)
class ProcessOutcome:
    """Normalized subprocess outcome before digests, capping and tracing.

    Attributes:
        exit_status: EXIT_STATUS_COMPLETED, EXIT_STATUS_TIMEOUT or
            EXIT_STATUS_FAILED.
        exit_code: Process exit code; TIMEOUT_EXIT_CODE (-9) on a timeout.
        stdout_text: Full captured stdout text.
        stderr_text: Full captured stderr text.
    """

    exit_status: str
    exit_code: int
    stdout_text: str
    stderr_text: str


def validate_execution_id(execution_id: str) -> None:
    """Reject ids that could escape the workspace when used as a directory name.

    Args:
        execution_id: Id supplied by the caller.

    Raises:
        ExecutionError: If the id is empty, contains anything outside
            ``[A-Za-z0-9._-]``, or is ``.``/``..``.
    """
    # SAFETY: the id becomes a path component. "." and ".." pass the character
    # class but would traverse outside workspace_dir, so they are rejected too.
    if execution_id in {".", ".."} or _EXECUTION_ID_RE.fullmatch(execution_id) is None:
        raise ExecutionError(
            "execution_id must match [A-Za-z0-9._-]+ and must not be '.' or '..': "
            f"got {execution_id!r}"
        )


def build_child_environment(extra: Mapping[str, str], scratch_dir: Path) -> dict[str, str]:
    """Build the minimal child environment for one execution.

    The documented allowlist is PATH, SYSTEMROOT and PATHEXT (so the interpreter
    can start), TEMP/TMP pointing at the scratch directory, PYTHONIOENCODING
    and PYTHONHASHSEED for reproducible text capture. ``extra`` is applied first
    so fabric-owned variables always win; anything else in the parent
    environment is not visible to the child.

    Args:
        extra: Extra variables declared on the request.
        scratch_dir: Per-execution scratch directory used for TEMP/TMP.

    Returns:
        The complete environment mapping for the child process.
    """
    child_env: dict[str, str] = dict(extra)
    for name in _ENV_ALLOWLIST:
        value = os.environ.get(name)
        if value is not None:
            child_env[name] = value
    for name in _SCRATCH_ENV_VARS:
        child_env[name] = str(scratch_dir)
    for name, value in _PYTHON_ENV_VARS:
        child_env[name] = value
    return child_env


def run_command(
    *,
    command: tuple[str, ...],
    stdin_text: str | None,
    child_env: Mapping[str, str],
    scratch_dir: Path,
    timeout_seconds: int,
) -> ProcessOutcome:
    """Run one command and normalize the outcome.

    ``encoding``/``errors`` are always explicit so a locale codec cannot break
    capture, and a timeout is returned as data instead of being raised.

    Args:
        command: Non-empty argv tuple.
        stdin_text: Text for the child's stdin; ``None`` closes stdin instead of
            inheriting the parent's.
        child_env: Complete child environment.
        scratch_dir: Working directory for the child.
        timeout_seconds: Positive wall-clock budget.

    Returns:
        Normalized process outcome.
    """
    stdin_target = subprocess.DEVNULL if stdin_text is None else None
    try:
        completed = subprocess.run(
            command,
            cwd=scratch_dir,
            env=child_env,
            stdin=stdin_target,
            input=stdin_text,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired as exc:
        # PROVIDER: partial output is best effort. Windows returns what was
        # captured before the kill; POSIX may return nothing.
        return ProcessOutcome(
            exit_status=EXIT_STATUS_TIMEOUT,
            exit_code=TIMEOUT_EXIT_CODE,
            stdout_text=decode_partial(exc.stdout),
            stderr_text=decode_partial(exc.stderr),
        )
    return ProcessOutcome(
        exit_status=EXIT_STATUS_COMPLETED if completed.returncode == 0 else EXIT_STATUS_FAILED,
        exit_code=completed.returncode,
        stdout_text=completed.stdout,
        stderr_text=completed.stderr,
    )


def decode_partial(value: object) -> str:
    """Decode partial output captured before a timeout.

    Args:
        value: ``TimeoutExpired.stdout``/``.stderr``: bytes, str or None.

    Returns:
        Decoded text, or an empty string when nothing was captured.

    Raises:
        ExecutionError: If the provider reports an unexpected output type.
    """
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        return value
    raise ExecutionError(f"unexpected partial output type from provider: {type(value).__name__}")


def sha256_text(text: str) -> str:
    """Return the sha256 hex digest of ``text`` encoded as UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def truncate_to_bytes(text: str, limit_bytes: int) -> str:
    """Cap text to at most ``limit_bytes`` UTF-8 bytes without splitting a character."""
    encoded = text.encode("utf-8")
    if len(encoded) <= limit_bytes:
        return text
    return encoded[:limit_bytes].decode("utf-8", errors="replace")


def output_refs(stdout_digest: str, stderr_digest: str, outcome: ProcessOutcome) -> tuple[str, ...]:
    """Content-address the captured output streams, skipping empty ones."""
    refs: list[str] = []
    if outcome.stdout_text:
        refs.append(stdout_digest)
    if outcome.stderr_text:
        refs.append(stderr_digest)
    return tuple(refs)


def process_isolation() -> dict[str, str]:
    """Return the honest enforcement report for the local process provider."""
    return {
        "process": "enforced",
        "filesystem_scratch": "enforced",
        "environment": "scrubbed",
        "network": "not_enforced",
        "memory": "not_enforced",
    }
