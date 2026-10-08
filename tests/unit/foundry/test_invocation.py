"""Invocation of admitted capabilities: proposal-only outcomes, no commit path."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import pytest
from dataclasses import replace

from wanxiang_execution import ExecutionClass, ExecutionPolicy
from wanxiang_foundry.errors import InvocationError
from wanxiang_foundry.invocation import CapabilityRequest, invoke
from wanxiang_foundry.package import CapabilityPackage
from wanxiang_foundry.registry import VerifiedCapabilityRegistry
from wanxiang_foundry.verification import VerificationReport

_MakePackage = Callable[[str], CapabilityPackage]


def _request() -> CapabilityRequest:
    return CapabilityRequest(
        execution_id="inv-1",
        command=(sys.executable, "-c", "print('ok')"),
    )


@pytest.mark.unit
def test_invoking_unregistered_capability_raises(
    package_with_digest: _MakePackage,
    full_pass_report: VerificationReport,
    untrusted_policy: ExecutionPolicy,
    tmp_path: Path,
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)

    with pytest.raises(InvocationError):
        invoke(registry, package, _request(), untrusted_policy, tmp_path)


@pytest.mark.unit
def test_invoking_revoked_capability_raises(
    package_with_digest: _MakePackage,
    full_pass_report: VerificationReport,
    untrusted_policy: ExecutionPolicy,
    tmp_path: Path,
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)
    registry.revoke("cap.demo", "1.0.0", "withdrawn")

    with pytest.raises(InvocationError):
        invoke(registry, package, _request(), untrusted_policy, tmp_path)


@pytest.mark.unit
def test_invoking_admitted_capability_returns_proposal_only_outcome(
    package_with_digest: _MakePackage,
    full_pass_report: VerificationReport,
    untrusted_policy: ExecutionPolicy,
    tmp_path: Path,
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)

    outcome = invoke(registry, package, _request(), untrusted_policy, tmp_path)

    assert outcome.capability_id == "cap.demo"
    assert outcome.proposal["proposal_only"] is True
    assert outcome.observation["proposal_only"] is True
    assert len(outcome.execution_digest) == 64


@pytest.mark.unit
def test_capability_outcome_exposes_no_commit_path(
    package_with_digest: _MakePackage,
    full_pass_report: VerificationReport,
    untrusted_policy: ExecutionPolicy,
    tmp_path: Path,
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)

    outcome = invoke(registry, package, _request(), untrusted_policy, tmp_path)

    assert not hasattr(outcome, "commit")
    assert not hasattr(outcome, "commit_to_world")


@pytest.mark.unit
def test_invocation_refuses_runtime_class_drift(
    package_with_digest: _MakePackage,
    full_pass_report: VerificationReport,
    untrusted_policy: ExecutionPolicy,
    tmp_path: Path,
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)
    container_policy = replace(
        untrusted_policy,
        execution_class=ExecutionClass.CONTAINER,
    )

    with pytest.raises(InvocationError, match="execution class"):
        invoke(registry, package, _request(), container_policy, tmp_path)
