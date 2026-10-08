"""Run verification cases through the real execution fabric.

Each case command is executed as a real local subprocess by the execution fabric
under an authorized policy. The observed digest is the sha256 of captured stdout
and the exit status is compared with the case's declared expectation.

INVARIANT: no canonical world state is touched here. The execution trace stays
in memory as verification evidence and is never appended to world history; the
fabric only produces proposal-only observations.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from wanxiang_execution import (
    ExecutionError,
    ExecutionPolicy,
    ExecutionRequest,
    ExecutionRouter,
    LocalProcessProvider,
    PolicyViolation,
)

from wanxiang_foundry.verification import CaseResult, FailureLayer, VerificationCase

_UNSAFE_ID_CHARS = re.compile(r"[^A-Za-z0-9._-]")


def run_cases(
    cases: Sequence[VerificationCase],
    policy: ExecutionPolicy,
    workspace_dir: Path,
    *,
    router: ExecutionRouter | None = None,
) -> tuple[CaseResult, ...]:
    """Run every case as a real subprocess and return observed results.

    A policy violation, a non-started execution or a malformed command yields a
    failed CaseResult with a typed failure layer; no exception leaks to the
    caller.

    Args:
        cases: Cases to run.
        policy: Execution policy; authorized by the fabric before any process.
        workspace_dir: Parent directory for per-case scratch directories.

    Returns:
        One CaseResult per case, in input order.
    """
    resolved_router = router or ExecutionRouter((LocalProcessProvider(),))
    return tuple(_run_case(case, policy, workspace_dir, resolved_router) for case in cases)


def _run_case(
    case: VerificationCase,
    policy: ExecutionPolicy,
    workspace_dir: Path,
    router: ExecutionRouter,
) -> CaseResult:
    """Run one case, converting any fabric refusal into a typed failure layer."""
    try:
        request = ExecutionRequest(
            execution_id=_execution_id(case.case_id),
            capability_id="verification",
            capability_version="0.0.0",
            command=case.command,
            input_refs=(),
            policy=policy,
        )
    except ExecutionError:
        return _failed(case, FailureLayer.AGENT_MISUSE)
    try:
        result = router.run(request, workspace_dir)
    except PolicyViolation:
        return _failed(case, FailureLayer.ENVIRONMENT)
    except ExecutionError:
        return _failed(case, FailureLayer.ENVIRONMENT)
    digest = result.trace.stdout_digest
    exit_status = result.trace.exit_code
    passed = digest == case.expected_stdout_digest and exit_status == case.expected_exit_status
    if passed:
        return CaseResult(
            case_id=case.case_id,
            kind=case.kind,
            passed=True,
            observed_digest=digest,
            exit_status=exit_status,
            failure_layer=FailureLayer.NONE,
        )
    # The wrapper produced output or an exit status the source expectation did
    # not predict; the wrapper is the first place to look, not the world.
    return CaseResult(
        case_id=case.case_id,
        kind=case.kind,
        passed=False,
        observed_digest=digest,
        exit_status=exit_status,
        failure_layer=FailureLayer.GENERATED_WRAPPER,
    )


def _failed(case: VerificationCase, layer: FailureLayer) -> CaseResult:
    """Build a failed result that records the diagnosis without raising."""
    return CaseResult(
        case_id=case.case_id,
        kind=case.kind,
        passed=False,
        observed_digest=None,
        exit_status=None,
        failure_layer=layer,
    )


def _execution_id(case_id: str) -> str:
    """Sanitize a case id into a valid, unique per-case execution id."""
    sanitized = _UNSAFE_ID_CHARS.sub("_", case_id).strip("._")
    if not sanitized:
        sanitized = "case"
    return f"verify_{sanitized}"[:64]
