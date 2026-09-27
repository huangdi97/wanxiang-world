"""Shared fixtures for Capability Foundry tests."""

from __future__ import annotations

import hashlib
from collections.abc import Callable

import pytest
from wanxiang_execution import ExecutionClass, ExecutionPolicy
from wanxiang_foundry.candidate import ArtifactKind, ArtifactRef
from wanxiang_foundry.levels import KnowledgeLevel, PromotionLevel
from wanxiang_foundry.package import (
    CapabilityPackage,
    OutputClass,
    RuntimeRequirement,
    Validity,
    WorldEffect,
)
from wanxiang_foundry.provenance import ProvenanceLayer, ProvenanceRecord
from wanxiang_foundry.verification import (
    CaseKind,
    CaseResult,
    FailureLayer,
    VerificationCase,
    VerificationReport,
    verify,
)


def sha256_hex(text: str) -> str:
    """Return the sha256 hex digest of text encoded as UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@pytest.fixture
def digest() -> Callable[[str], str]:
    """Return a helper computing the sha256 hex digest of a text."""
    return sha256_hex


@pytest.fixture
def untrusted_policy() -> ExecutionPolicy:
    """Baseline untrusted policy: PROCESS, no network, no secrets."""
    return ExecutionPolicy.default_untrusted()


@pytest.fixture
def artifact() -> ArtifactRef:
    """A well-formed paper artifact with a declared rights basis."""
    return ArtifactRef(
        kind=ArtifactKind.PAPER,
        uri="paper:10.1000/example",
        digest=sha256_hex("artifact-content"),
        rights_basis="CC-BY-4.0",
    )


@pytest.fixture
def make_case() -> Callable[[str, CaseKind], VerificationCase]:
    """Return a factory building a verification case for a given kind."""

    def _make(case_id: str, kind: CaseKind) -> VerificationCase:
        return VerificationCase(
            case_id=case_id,
            kind=kind,
            command=("python", "-c", "print('ok')"),
            expected_stdout_digest=sha256_hex("ok\n"),
            expected_exit_status=0,
        )

    return _make


@pytest.fixture
def pass_result() -> Callable[[VerificationCase], CaseResult]:
    """Return a factory building a passing result for a case."""

    def _make(case: VerificationCase) -> CaseResult:
        return CaseResult(
            case_id=case.case_id,
            kind=case.kind,
            passed=True,
            observed_digest=case.expected_stdout_digest,
            exit_status=case.expected_exit_status,
            failure_layer=FailureLayer.NONE,
        )

    return _make


@pytest.fixture
def fail_result() -> Callable[[VerificationCase, FailureLayer], CaseResult]:
    """Return a factory building a failing result with a given layer."""

    def _make(case: VerificationCase, layer: FailureLayer) -> CaseResult:
        return CaseResult(
            case_id=case.case_id,
            kind=case.kind,
            passed=False,
            observed_digest=sha256_hex("wrong"),
            exit_status=1,
            failure_layer=layer,
        )

    return _make


@pytest.fixture
def full_pass_report(
    make_case: Callable[[str, CaseKind], VerificationCase],
    pass_result: Callable[[VerificationCase], CaseResult],
) -> VerificationReport:
    """A report granting C3: one passing case of every kind."""
    cases = tuple(make_case(f"case-{kind.value}", kind) for kind in CaseKind)
    results = tuple(pass_result(case) for case in cases)
    return verify(cases, results)


@pytest.fixture
def package_with_digest() -> Callable[[str], CapabilityPackage]:
    """Return a factory building a valid package with a given evidence digest."""

    def _make(verification_digest: str) -> CapabilityPackage:
        return CapabilityPackage(
            capability_id="cap.demo",
            version="1.0.0",
            artifact_digest=sha256_hex("artifact"),
            interface_digest=sha256_hex("interface"),
            provenance=(
                ProvenanceRecord(
                    layer=ProvenanceLayer.SOURCE_METHOD,
                    ref="paper:10.1000/example",
                    digest=sha256_hex("source"),
                    note="original method",
                ),
                ProvenanceRecord(
                    layer=ProvenanceLayer.GENERATED_WRAPPER,
                    ref="wrapper:v1",
                    digest=sha256_hex("wrapper"),
                    note="synthesized wrapper",
                ),
            ),
            validity=Validity(
                supported_inputs=("int",),
                known_limitations=("small inputs only",),
                environment_hash=sha256_hex("environment"),
            ),
            runtime=RuntimeRequirement(
                execution_class=ExecutionClass.PROCESS,
                policy_fingerprint=sha256_hex("policy"),
            ),
            world_effect=WorldEffect(allowed_output_class=OutputClass.OBSERVATION),
            knowledge_level=KnowledgeLevel.K3_VERIFIED_ENVIRONMENTAL,
            promotion_level=PromotionLevel.C3_VERIFIED,
            verification_digest=verification_digest,
        )

    return _make
