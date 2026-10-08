"""The fabric runner executes real subprocesses and returns typed failures."""

from __future__ import annotations

import hashlib
import sys
from dataclasses import replace
from pathlib import Path

import pytest
from wanxiang_execution import ExecutionClass, ExecutionPolicy
from wanxiang_foundry.fabric_runner import run_cases
from wanxiang_foundry.verification import CaseKind, FailureLayer, VerificationCase


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _case(case_id: str, command: tuple[str, ...], expected: str) -> VerificationCase:
    return VerificationCase(
        case_id=case_id,
        kind=CaseKind.GOLDEN,
        command=command,
        expected_stdout_digest=expected,
        expected_exit_status=0,
    )


@pytest.mark.unit
def test_runner_matches_expected_stdout_digest(
    untrusted_policy: ExecutionPolicy, tmp_path: Path
) -> None:
    case = _case("golden", (sys.executable, "-c", "print('ok')"), _digest("ok\n"))

    (result,) = run_cases([case], untrusted_policy, tmp_path)

    assert result.passed is True
    assert result.exit_status == 0
    assert result.observed_digest == _digest("ok\n")
    assert result.failure_layer is FailureLayer.NONE


@pytest.mark.unit
def test_runner_reports_failing_case_with_typed_layer(
    untrusted_policy: ExecutionPolicy, tmp_path: Path
) -> None:
    case = _case("golden", (sys.executable, "-c", "print('ok')"), _digest("different"))

    (result,) = run_cases([case], untrusted_policy, tmp_path)

    assert result.passed is False
    assert result.failure_layer is FailureLayer.GENERATED_WRAPPER


@pytest.mark.unit
def test_runner_reports_policy_violation_as_environment_failure(
    untrusted_policy: ExecutionPolicy, tmp_path: Path
) -> None:
    case = _case("golden", (sys.executable, "-c", "print('ok')"), _digest("ok\n"))
    policy = replace(untrusted_policy, execution_class=ExecutionClass.CONTAINER)

    (result,) = run_cases([case], policy, tmp_path)

    assert result.passed is False
    assert result.failure_layer is FailureLayer.ENVIRONMENT
    assert result.observed_digest is None


@pytest.mark.unit
def test_runner_reports_malformed_command_as_agent_misuse(
    untrusted_policy: ExecutionPolicy, tmp_path: Path
) -> None:
    case = _case("golden", (sys.executable, ""), _digest("ok\n"))

    (result,) = run_cases([case], untrusted_policy, tmp_path)

    assert result.passed is False
    assert result.failure_layer is FailureLayer.AGENT_MISUSE
