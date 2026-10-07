"""R7 Paper2Agent-style paper+repo -> verified capability reference integration.

This does not claim to execute Paper2Agent itself. It implements the same R7
contract with a real paper/repository pair: frozen citation metadata plus the
paper's pinned MIT-licensed upstream Python method are packaged, executed and
verified through Wanxiang's Capability Foundry / Execution Fabric.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest
from wanxiang_execution import ExecutionClass, ExecutionPolicy
from wanxiang_foundry import (
    ArtifactKind,
    ArtifactRef,
    CapabilityPackage,
    CapabilityRequest,
    CaseKind,
    KnowledgeLevel,
    OutputClass,
    PromotionLevel,
    ProvenanceLayer,
    ProvenanceRecord,
    RuleBasedFoundryProvider,
    RuntimeRequirement,
    Validity,
    VerificationCase,
    VerifiedCapabilityRegistry,
    WorldEffect,
    canonical_sha256,
    invoke,
    run_cases,
    verify,
)

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "reference_worlds" / "r7" / "paper_capability"
PAPER_METADATA = REFERENCE / "paper_metadata.json"
UPSTREAM = REFERENCE / "upstream" / "optimality_search.py"
WRAPPER = REFERENCE / "paper_capability.py"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@pytest.mark.integration
def test_real_paper_repo_artifacts_become_verified_proposal_only_capability(
    tmp_path: Path,
) -> None:
    paper = ArtifactRef(
        kind=ArtifactKind.PAPER,
        uri="arxiv:2606.28989v2#citation-metadata",
        digest=_sha(PAPER_METADATA),
        rights_basis="citation metadata only; paper text is not redistributed",
    )
    repository = ArtifactRef(
        kind=ArtifactKind.REPO,
        uri=(
            "https://github.com/TimoKellerMath/PointCountsAbelianVarieties"
            "@f9fcaf80b059378c6130532ca9a4ce7b1b18f47b:optimality_search.py"
        ),
        digest=_sha(UPSTREAM),
        rights_basis="MIT License; upstream license is vendored beside the source",
    )

    candidate = RuleBasedFoundryProvider().propose(
        repository,
        {
            "capability_id": "cap.paper.pointcounts-g3-collision-study",
            "proposed_version": "1.0.0",
            "inputs": ["q in {2,3}; fixed N=2"],
            "outputs": ["bounded collision-study summary"],
            "environment": {"python": "3.12+", "network": "none"},
            "requested_side_effects": ["none"],
        },
    )
    cases = (
        VerificationCase(
            "paper-repo-golden-q2",
            CaseKind.GOLDEN,
            (sys.executable, str(WRAPPER), "2"),
            _text_digest(
                '{"collisions": 29, "images": 183, "injective": false, "q": 2, "weil": 215}\n'
            ),
            0,
        ),
        VerificationCase(
            "paper-repo-negative-out-of-envelope",
            CaseKind.NEGATIVE,
            (sys.executable, str(WRAPPER), "4"),
            _text_digest(""),
            2,
        ),
        VerificationCase(
            "paper-repo-boundary-q3",
            CaseKind.BOUNDARY,
            (sys.executable, str(WRAPPER), "3"),
            _text_digest(
                '{"collisions": 69, "images": 607, "injective": false, "q": 3, "weil": 677}\n'
            ),
            0,
        ),
        VerificationCase(
            "paper-repo-security-no-secret",
            CaseKind.SECURITY,
            (sys.executable, str(WRAPPER), "--security"),
            _text_digest("safe\n"),
            0,
        ),
    )
    policy = ExecutionPolicy.default_untrusted()
    observed = run_cases(cases, policy, tmp_path / "verification")
    report = verify(cases, observed)
    assert report.grants_c3 is True

    wrapper_digest = _sha(WRAPPER)
    package = CapabilityPackage(
        capability_id=candidate.capability_id,
        version=candidate.proposed_version,
        artifact_digest=repository.digest,
        source_artifacts=(paper, repository),
        interface_digest=canonical_sha256(dict(candidate.proposed_interface)),
        interface_inputs=("q in {2,3}; fixed N=2",),
        interface_outputs=("bounded collision-study summary",),
        verification_case_ids=tuple(case.case_id for case in cases),
        provenance=(
            ProvenanceRecord(
                ProvenanceLayer.SOURCE_METHOD,
                paper.uri,
                paper.digest,
                "paper identity/citation metadata bound to the repository fixture",
            ),
            ProvenanceRecord(
                ProvenanceLayer.SOURCE_METHOD,
                repository.uri,
                repository.digest,
                "exact pinned upstream method implementation",
            ),
            ProvenanceRecord(
                ProvenanceLayer.GENERATED_WRAPPER,
                "reference_worlds/r7/paper_capability/paper_capability.py",
                wrapper_digest,
                "thin wrapper imports and calls upstream study(); no method reimplementation",
            ),
            ProvenanceRecord(
                ProvenanceLayer.VALIDATION_FIXTURE,
                "verification:r7-paper-repo-reference",
                report.evidence_digest,
                "golden/negative/boundary/security evidence",
            ),
            ProvenanceRecord(
                ProvenanceLayer.RUNTIME_ADAPTER,
                "execution:local-process@1.0.0",
                canonical_sha256({"provider": "execution-local-process", "version": "1.0.0"}),
                "process-boundary Execution Fabric provider",
            ),
        ),
        validity=Validity(
            supported_inputs=("q in {2,3}; fixed N=2",),
            known_limitations=(
                "bounded qualification fixture, not the full paper algorithm",
                "does not establish realizability of every q-Weil polynomial",
                "PROCESS is not a hostile-code sandbox",
            ),
            environment_hash=canonical_sha256(
                {
                    "python": f"{sys.version_info.major}.{sys.version_info.minor}",
                    "upstream_commit": "f9fcaf80b059378c6130532ca9a4ce7b1b18f47b",
                    "execution_class": policy.execution_class.value,
                }
            ),
        ),
        runtime=RuntimeRequirement(
            execution_class=ExecutionClass.PROCESS,
            policy_fingerprint=canonical_sha256(
                {
                    "trust": policy.trust.value,
                    "execution_class": policy.execution_class.value,
                    "filesystem": policy.filesystem.value,
                    "network": policy.network.value,
                    "secrets": policy.secrets.value,
                    "side_effects": policy.side_effects.value,
                    "wall_seconds_limit": policy.wall_seconds_limit,
                }
            ),
        ),
        world_effect=WorldEffect(allowed_output_class=OutputClass.OBSERVATION),
        knowledge_level=KnowledgeLevel.K3_VERIFIED_ENVIRONMENTAL,
        promotion_level=PromotionLevel.C3_VERIFIED,
        verification_digest=report.evidence_digest,
    )
    registry = VerifiedCapabilityRegistry()
    registry.admit(package, report)
    outcome = invoke(
        registry,
        package,
        CapabilityRequest(
            execution_id="r7-paper-capability",
            command=(sys.executable, str(WRAPPER), "2"),
        ),
        policy,
        tmp_path / "invoke",
    )

    assert outcome.capability_version == "1.0.0"
    assert outcome.observation["proposal_only"] is True
    assert outcome.proposal["proposal_only"] is True
    assert package.source_artifacts == (paper, repository)
