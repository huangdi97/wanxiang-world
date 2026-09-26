"""Typed error taxonomy for the execution fabric and the external-effect outbox.

Errors are split by layer so callers can tell a policy refusal from a provider
failure and from outbox bookkeeping failure. The fabric reports ordinary
process failures and timeouts as trace data; `ExecutionFailed` and
`ExecutionTimeout` exist for callers that explicitly want raising semantics.
"""

from __future__ import annotations


class ExecutionError(Exception):
    """Base class for every execution fabric / outbox error."""


class PolicyViolation(ExecutionError):
    """The declared execution policy is not authorized by this fabric."""


class ExecutionFailed(ExecutionError):
    """A provider reported a hard execution failure.

    `LocalProcessProvider` never raises this: it records ``exit_status="failed"``
    in the trace. Callers that want raising semantics must raise it themselves.
    """


class ExecutionTimeout(ExecutionError):
    """A provider exceeded the wall-clock limit.

    `LocalProcessProvider` never raises this: it records
    ``exit_status="timeout"`` in the trace. Callers that want raising semantics
    must raise it themselves.
    """


class OutboxError(ExecutionError):
    """The external-effect outbox is inconsistent or the operation is invalid."""


class DuplicateEffectSuppressed(ExecutionError):
    """A retry hit an already-applied idempotency key.

    The executor returns a ``duplicate_suppressed`` result instead of raising;
    this error exists for callers that treat duplicate suppression as failure.
    """


class AmbiguousEffectResult(ExecutionError):
    """An irreversible effect may or may not have been applied.

    The executor returns an ``ambiguous`` result instead of raising and never
    retries it automatically; this error exists for callers that treat
    ambiguity as failure and demand explicit reconciliation.
    """
