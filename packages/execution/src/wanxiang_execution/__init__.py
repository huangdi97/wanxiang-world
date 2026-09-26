"""Wanxiang isolated execution fabric and irreversible external-effect outbox.

The fabric runs local processes under an explicit policy and returns traces and
proposal-only observations; it can never write canonical world state. The
outbox records irreversible external effects append-only, suppresses duplicate
execution by idempotency key and never retries an ambiguous effect.
"""

from wanxiang_execution.errors import (
    AmbiguousEffectResult,
    DuplicateEffectSuppressed,
    ExecutionError,
    ExecutionFailed,
    ExecutionTimeout,
    OutboxError,
    PolicyViolation,
)
from wanxiang_execution.fabric import (
    ExecutionRequest,
    ExecutionResult,
    LocalProcessProvider,
)
from wanxiang_execution.local_process import MAX_CAPTURE_BYTES
from wanxiang_execution.outbox import Outbox
from wanxiang_execution.outbox_executor import OutboxExecutor
from wanxiang_execution.outbox_records import (
    ATTEMPT_MARKER_STATUS,
    STATUS_AMBIGUOUS,
    STATUS_APPLIED,
    STATUS_DUPLICATE_SUPPRESSED,
    STATUS_FAILED,
    ExternalEffectAttempt,
    ExternalEffectHandler,
    ExternalEffectIntent,
    ExternalEffectResult,
)
from wanxiang_execution.policy import (
    ExecutionClass,
    ExecutionPolicy,
    FilesystemAccess,
    NetworkAccess,
    SecretAccess,
    SideEffectClass,
    TrustLevel,
    authorize,
)
from wanxiang_execution.trace import (
    EXIT_STATUS_COMPLETED,
    EXIT_STATUS_FAILED,
    EXIT_STATUS_POLICY_DENIED,
    EXIT_STATUS_TIMEOUT,
    TIMEOUT_EXIT_CODE,
    ExecutionTrace,
    environment_hash,
    trace_digest,
)

__version__ = "0.1.0"

__all__ = [
    "ATTEMPT_MARKER_STATUS",
    "EXIT_STATUS_COMPLETED",
    "EXIT_STATUS_FAILED",
    "EXIT_STATUS_POLICY_DENIED",
    "EXIT_STATUS_TIMEOUT",
    "MAX_CAPTURE_BYTES",
    "STATUS_AMBIGUOUS",
    "STATUS_APPLIED",
    "STATUS_DUPLICATE_SUPPRESSED",
    "STATUS_FAILED",
    "TIMEOUT_EXIT_CODE",
    "AmbiguousEffectResult",
    "DuplicateEffectSuppressed",
    "ExecutionClass",
    "ExecutionError",
    "ExecutionFailed",
    "ExecutionPolicy",
    "ExecutionRequest",
    "ExecutionResult",
    "ExecutionTimeout",
    "ExecutionTrace",
    "ExternalEffectAttempt",
    "ExternalEffectHandler",
    "ExternalEffectIntent",
    "ExternalEffectResult",
    "FilesystemAccess",
    "LocalProcessProvider",
    "NetworkAccess",
    "Outbox",
    "OutboxError",
    "OutboxExecutor",
    "PolicyViolation",
    "SecretAccess",
    "SideEffectClass",
    "TrustLevel",
    "authorize",
    "environment_hash",
    "trace_digest",
]
