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
def test_mismatched_verification_case_binding_blocks_admission(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = replace(
        package_with_digest(full_pass_report.evidence_digest),
        verification_case_ids=("case-golden",),
    )

    with pytest.raises(RegistryError, match="verification_case_ids"):
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


@pytest.mark.unit
def test_suspend_restore_deprecate_and_revoke_preserve_evidence(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)

    registry.suspend("cap.demo", "1.0.0", "upstream incident")
    assert registry.status("cap.demo", "1.0.0") == "SUSPENDED"
    assert registry.is_invocable("cap.demo", "1.0.0") is False
    assert registry.get("cap.demo", "1.0.0") == package

    registry.restore("cap.demo", "1.0.0", "incident cleared")
    assert registry.status("cap.demo", "1.0.0") == "ACTIVE"
    assert registry.is_invocable("cap.demo", "1.0.0") is True

    registry.deprecate("cap.demo", "1.0.0", "prefer newer version")
    assert registry.status("cap.demo", "1.0.0") == "DEPRECATED"
    assert registry.is_invocable("cap.demo", "1.0.0") is True

    registry.revoke("cap.demo", "1.0.0", "security regression")
    assert registry.status("cap.demo", "1.0.0") == "REVOKED"
    assert registry.is_invocable("cap.demo", "1.0.0") is False
    assert registry.get("cap.demo", "1.0.0") == package
    with pytest.raises(RegistryError, match="cannot be reactivated"):
        registry.restore("cap.demo", "1.0.0", "should not be allowed")

    actions = tuple(item[2] for item in registry.lifecycle("cap.demo"))
    assert actions == ("ADMIT", "SUSPENDED", "ACTIVE", "DEPRECATED", "REVOKED")


@pytest.mark.unit
def test_rollback_selects_old_version_for_future_calls_without_deleting_new_version(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    first = package_with_digest(full_pass_report.evidence_digest)
    second = replace(first, version="2.0.0")
    registry.admit(first, full_pass_report)
    registry.admit(second, full_pass_report)
    assert registry.active("cap.demo") == second

    registry.rollback("cap.demo", "1.0.0", "v2 behavioral regression")

    assert registry.active("cap.demo") == first
    assert registry.get("cap.demo", "2.0.0") == second
    assert registry.is_invocable("cap.demo", "2.0.0") is True
    assert registry.lifecycle("cap.demo")[-1] == (
        "cap.demo",
        "1.0.0",
        "ROLLBACK",
        "v2 behavioral regression",
    )


@pytest.mark.unit
def test_rollback_refuses_suspended_or_revoked_target(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    package = package_with_digest(full_pass_report.evidence_digest)
    registry.admit(package, full_pass_report)
    registry.suspend("cap.demo", "1.0.0", "investigating")

    with pytest.raises(RegistryError, match="non-invocable"):
        registry.rollback("cap.demo", "1.0.0", "cannot select suspended version")


@pytest.mark.unit
def test_deprecating_selected_latest_version_falls_back_to_prior_active_version(
    package_with_digest: _MakePackage, full_pass_report: VerificationReport
) -> None:
    registry = VerifiedCapabilityRegistry()
    first = package_with_digest(full_pass_report.evidence_digest)
    second = replace(first, version="2.0.0")
    registry.admit(first, full_pass_report)
    registry.admit(second, full_pass_report)
    assert registry.active("cap.demo") == second

    registry.deprecate("cap.demo", "2.0.0", "superseded but still pin-invocable")

    assert registry.is_invocable("cap.demo", "2.0.0") is True
    assert registry.active("cap.demo") == first
