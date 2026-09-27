"""Verified capability registry: C3 admission, versioning and revocation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import pytest
from wanxiang_foundry.errors import RegistryError
from wanxiang_foundry.levels import PromotionLevel
from wanxiang_foundry.package import CapabilityPackage
from wanxiang_foundry.registry import VerifiedCapabilityRegistry
from wanxiang_foundry.verification import (
    CaseKind,
    CaseResult,
    FailureLayer,
    VerificationCase,
    VerificationReport,
    verify,
)

_MakeCase = Callable[[str, CaseKind], VerificationCase]
_PassResult = Callable[[VerificationCase], CaseResult]
_FailResult = Callable[[VerificationCase, FailureLayer], CaseResult]
_MakePackage = Callable[[str], CapabilityPackage]


def _report_with_golden_failure(
    make_case: _MakeCase, pass_result: _PassResult, fail_result: _FailResult
) -> VerificationReport:
    cases = tuple(make_case(f"case-{kind.value}", kind) for kind in CaseKind)
    results = tuple(
        fail_result(case, FailureLayer.GENERATED_WRAPPER)
        if case.kind is CaseKind.GOLDEN
        else pass_result(case)
        for case in cases
    )
    return verify(cases, results)


@pytest.mark.unit
def test_admission_requires_full_pass_c3_report(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)

    registry.admit(package, full_pass_report)

    assert registry.get("cap.demo", "1.0.0") == package
    assert registry.versions("cap.demo") == ("1.0.0",)


@pytest.mark.unit
def test_failed_case_blocks_admission_and_leaves_registry_unchanged(
    make_case: _MakeCase,
    pass_result: _PassResult,
    fail_result: _FailResult,
    package_with_digest: _MakePackage,
) -> None:
    report = _report_with_golden_failure(make_case, pass_result, fail_result)
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(report.evidence_digest)

    with pytest.raises(RegistryError):
        registry.admit(package, report)

    assert registry.get("cap.demo", "1.0.0") is None
    assert registry.versions("cap.demo") == ()


@pytest.mark.unit
def test_mismatched_verification_digest_blocks_admission(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest("f" * 64)

    with pytest.raises(RegistryError):
        registry.admit(package, full_pass_report)

    assert registry.get("cap.demo", "1.0.0") is None


@pytest.mark.unit
def test_two_versions_coexist_without_overwrite(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    first = package_with_digest(full_pass_report.evidence_digest)
    second = replace(first, version="2.0.0")

    registry.admit(first, full_pass_report)
    registry.admit(second, full_pass_report)

    assert registry.versions("cap.demo") == ("1.0.0", "2.0.0")
    assert registry.get("cap.demo", "1.0.0") == first
    assert registry.active("cap.demo") == second


@pytest.mark.unit
def test_admitting_the_same_version_twice_is_refused(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)

    with pytest.raises(RegistryError):
        registry.admit(package, full_pass_report)

    assert registry.versions("cap.demo") == ("1.0.0",)


@pytest.mark.unit
def test_revocation_is_recorded_and_blocks_invocation(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)

    registry.revoke("cap.demo", "1.0.0", "superseded by 2.0.0")

    assert registry.is_invocable("cap.demo", "1.0.0") is False
    assert registry.get("cap.demo", "1.0.0") == package
    grant = registry.promotions("cap.demo", "1.0.0")
    assert grant is not None
    assert grant.level is PromotionLevel.C3_VERIFIED
    assert grant.evidence_digest == full_pass_report.evidence_digest


@pytest.mark.unit
def test_revoking_unregistered_capability_is_refused() -> None:
    registry = VerifiedCapabilityRegistry()

    with pytest.raises(RegistryError):
        registry.revoke("cap.missing", "1.0.0", "unknown")
