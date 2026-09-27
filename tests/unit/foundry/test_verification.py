"""The pure verification decision: K3/C3 gates and unknown-is-not-pass."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from wanxiang_foundry.verification import (
    CaseKind,
    CaseResult,
    FailureLayer,
    VerificationCase,
    verify,
)

_MakeCase = Callable[[str, CaseKind], VerificationCase]
_PassResult = Callable[[VerificationCase], CaseResult]
_FailResult = Callable[[VerificationCase, FailureLayer], CaseResult]


def _all_cases(make_case: _MakeCase) -> tuple[VerificationCase, ...]:
    return tuple(make_case(f"case-{kind.value}", kind) for kind in CaseKind)


@pytest.mark.unit
def test_all_four_kinds_pass_grants_k3_and_c3(
    make_case: _MakeCase, pass_result: _PassResult
) -> None:
    cases = _all_cases(make_case)
    report = verify(cases, [pass_result(case) for case in cases])

    assert report.grants_k3 is True
    assert report.grants_c3 is True
    assert report.failed_case_ids == ()
    assert report.missing_case_ids == ()


@pytest.mark.unit
def test_missing_result_is_not_a_pass(make_case: _MakeCase, pass_result: _PassResult) -> None:
    cases = _all_cases(make_case)
    results = [pass_result(case) for case in cases if case.kind is not CaseKind.SECURITY]
    report = verify(cases, results)

    assert report.grants_k3 is True
    assert report.grants_c3 is False
    assert report.missing_case_ids == ("case-security",)


@pytest.mark.unit
def test_security_failure_blocks_c3_but_not_k3(
    make_case: _MakeCase, pass_result: _PassResult, fail_result: _FailResult
) -> None:
    cases = _all_cases(make_case)
    results = [
        fail_result(case, FailureLayer.ENVIRONMENT)
        if case.kind is CaseKind.SECURITY
        else pass_result(case)
        for case in cases
    ]
    report = verify(cases, results)

    assert report.grants_k3 is True
    assert report.grants_c3 is False
    assert report.failure_layers == (FailureLayer.ENVIRONMENT,)


@pytest.mark.unit
def test_negative_failure_blocks_k3(
    make_case: _MakeCase, pass_result: _PassResult, fail_result: _FailResult
) -> None:
    cases = _all_cases(make_case)
    results = [
        fail_result(case, FailureLayer.SOURCE_INCOMPATIBILITY)
        if case.kind is CaseKind.NEGATIVE
        else pass_result(case)
        for case in cases
    ]
    report = verify(cases, results)

    assert report.grants_k3 is False
    assert report.grants_c3 is False


@pytest.mark.unit
def test_boundary_failure_blocks_k3(
    make_case: _MakeCase, pass_result: _PassResult, fail_result: _FailResult
) -> None:
    cases = _all_cases(make_case)
    results = [
        fail_result(case, FailureLayer.DEPENDENCY_DRIFT)
        if case.kind is CaseKind.BOUNDARY
        else pass_result(case)
        for case in cases
    ]
    report = verify(cases, results)

    assert report.grants_k3 is False


@pytest.mark.unit
def test_report_evidence_digest_is_stable(make_case: _MakeCase, pass_result: _PassResult) -> None:
    cases = _all_cases(make_case)
    results = [pass_result(case) for case in cases]

    assert verify(cases, results).evidence_digest == verify(cases, results).evidence_digest
