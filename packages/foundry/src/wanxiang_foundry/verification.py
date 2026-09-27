"""Verification contracts and the pure verification decision.

A verification report is the evidence a registry uses to admit a package. The
decision is a pure function, ``verify(cases, results)``. "Unknown is not pass": a
declared case with no result FAILS verification and is reported as missing, never
ignored.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from wanxiang_foundry.digest import canonical_sha256, is_hex_digest
from wanxiang_foundry.errors import VerificationError


class CaseKind(StrEnum):
    """The four verification case kinds; all four are required for C3."""

    GOLDEN = "golden"
    NEGATIVE = "negative"
    BOUNDARY = "boundary"
    SECURITY = "security"


class FailureLayer(StrEnum):
    """The verifier's first-order diagnosis of why a case failed.

    SOURCE_INCOMPATIBILITY: the source method does not transfer.
    GENERATED_WRAPPER: the synthesized wrapper is wrong.
    DEPENDENCY_DRIFT: a dependency moved under the capability.
    ENVIRONMENT: the sandbox or policy prevented a clean observation.
    AGENT_MISUSE: the case declaration itself was malformed.
    """

    NONE = "none"
    SOURCE_INCOMPATIBILITY = "source_incompatibility"
    GENERATED_WRAPPER = "generated_wrapper"
    DEPENDENCY_DRIFT = "dependency_drift"
    ENVIRONMENT = "environment"
    AGENT_MISUSE = "agent_misuse"


@dataclass(frozen=True, slots=True)
class VerificationCase:
    """One declared verification case.

    Attributes:
        case_id: Non-empty stable id.
        kind: Which of the four kinds this case belongs to.
        command: Non-empty argv tuple to run.
        expected_stdout_digest: Expected sha256 hex digest of captured stdout.
        expected_exit_status: Expected process exit status.
    """

    case_id: str
    kind: CaseKind
    command: tuple[str, ...]
    expected_stdout_digest: str
    expected_exit_status: int

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise VerificationError("case_id must be a non-empty string")
        if not self.command:
            raise VerificationError(f"case {self.case_id!r} command must be a non-empty argv tuple")
        if not is_hex_digest(self.expected_stdout_digest):
            raise VerificationError(
                f"case {self.case_id!r} expected_stdout_digest must be a sha256 hex digest"
            )


@dataclass(frozen=True, slots=True)
class CaseResult:
    """The observed outcome of one case.

    Attributes:
        case_id: The case this result belongs to.
        kind: The case kind (cached for the report digest).
        passed: Whether the case met its declared expectation.
        observed_digest: Observed sha256 of captured stdout, or None if not run.
        exit_status: Observed exit status, or None if not run.
        failure_layer: First-order diagnosis; NONE on a pass.
    """

    case_id: str
    kind: CaseKind
    passed: bool
    observed_digest: str | None
    exit_status: int | None
    failure_layer: FailureLayer


@dataclass(frozen=True, slots=True)
class VerificationReport:
    """The pure verification decision and its tamper-evident evidence digest.

    Attributes:
        grants_k3: True only when all GOLDEN, BOUNDARY and NEGATIVE cases pass.
        grants_c3: True only when all four kinds pass and none failed.
        passed_case_ids: Ids of passing cases.
        failed_case_ids: Ids of failing cases.
        missing_case_ids: Ids of declared cases with no result.
        failure_layers: First-order failure diagnoses, de-duplicated in order.
        evidence_digest: sha256 over the cases and results.
    """

    grants_k3: bool
    grants_c3: bool
    passed_case_ids: tuple[str, ...]
    failed_case_ids: tuple[str, ...]
    missing_case_ids: tuple[str, ...]
    failure_layers: tuple[FailureLayer, ...]
    evidence_digest: str


def verify(cases: Sequence[VerificationCase], results: Sequence[CaseResult]) -> VerificationReport:
    """Decide K3/C3 from declared cases and observed results.

    Missing results are not passes: a declared case without a result fails
    verification and is reported in ``missing_case_ids``.

    Args:
        cases: Declared verification cases.
        results: Observed case results.

    Returns:
        The verification report.
    """
    by_id = {result.case_id: result for result in results}
    passed: list[str] = []
    failed: list[str] = []
    missing: list[str] = []
    layers: list[FailureLayer] = []
    kind_ok = dict.fromkeys(CaseKind, True)
    kind_seen = dict.fromkeys(CaseKind, False)
    for case in cases:
        kind_seen[case.kind] = True
        result = by_id.get(case.case_id)
        if result is None:
            missing.append(case.case_id)
            kind_ok[case.kind] = False
            layers.append(FailureLayer.ENVIRONMENT)
            continue
        if result.passed:
            passed.append(case.case_id)
            continue
        failed.append(case.case_id)
        kind_ok[case.kind] = False
        if result.failure_layer is not FailureLayer.NONE:
            layers.append(result.failure_layer)

    def kind_all_passed(kind: CaseKind) -> bool:
        return kind_seen[kind] and kind_ok[kind]

    grants_k3 = (
        kind_all_passed(CaseKind.GOLDEN)
        and kind_all_passed(CaseKind.BOUNDARY)
        and kind_all_passed(CaseKind.NEGATIVE)
    )
    grants_c3 = grants_k3 and kind_all_passed(CaseKind.SECURITY)
    return VerificationReport(
        grants_k3=grants_k3,
        grants_c3=grants_c3,
        passed_case_ids=tuple(passed),
        failed_case_ids=tuple(failed),
        missing_case_ids=tuple(missing),
        failure_layers=tuple(dict.fromkeys(layers)),
        evidence_digest=_evidence_digest(cases, results),
    )


def _evidence_digest(cases: Sequence[VerificationCase], results: Sequence[CaseResult]) -> str:
    """Return the sha256 over the canonical form of cases and results."""
    case_payload = [
        {
            "case_id": case.case_id,
            "kind": case.kind.value,
            "command": list(case.command),
            "expected_stdout_digest": case.expected_stdout_digest,
            "expected_exit_status": case.expected_exit_status,
        }
        for case in sorted(cases, key=lambda case: case.case_id)
    ]
    result_payload = [
        {
            "case_id": result.case_id,
            "kind": result.kind.value,
            "passed": result.passed,
            "observed_digest": result.observed_digest,
            "exit_status": result.exit_status,
            "failure_layer": result.failure_layer.value,
        }
        for result in sorted(results, key=lambda result: result.case_id)
    ]
    return canonical_sha256({"cases": case_payload, "results": result_payload})
