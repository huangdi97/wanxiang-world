"""Capability candidate digest stability and proposal-only invariants."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_execution import SideEffectClass
from wanxiang_foundry.candidate import ArtifactRef, CapabilityCandidate
from wanxiang_foundry.errors import CandidateError


def _candidate(artifact: ArtifactRef) -> CapabilityCandidate:
    return CapabilityCandidate(
        candidate_id="cand-1",
        capability_id="cap.demo",
        proposed_version="0.1.0",
        artifact=artifact,
        proposed_interface={"inputs": ("int",), "outputs": ("str",)},
        environment_declaration={"python": "3.12"},
        requested_side_effects=(SideEffectClass.NONE,),
    )


@pytest.mark.unit
def test_candidate_digest_is_stable(artifact: ArtifactRef) -> None:
    candidate = _candidate(artifact)

    assert candidate.candidate_digest() == candidate.candidate_digest()


@pytest.mark.unit
def test_candidate_digest_changes_when_a_field_changes(artifact: ArtifactRef) -> None:
    candidate = _candidate(artifact)
    other = replace(candidate, proposed_version="0.2.0")

    assert candidate.candidate_digest() != other.candidate_digest()


@pytest.mark.unit
def test_candidate_rejects_missing_interface(artifact: ArtifactRef) -> None:
    with pytest.raises(CandidateError):
        replace(_candidate(artifact), proposed_interface={})


@pytest.mark.unit
def test_candidate_rejects_empty_capability_id(artifact: ArtifactRef) -> None:
    with pytest.raises(CandidateError):
        replace(_candidate(artifact), capability_id="")


@pytest.mark.unit
def test_artifact_ref_rejects_non_hex_digest() -> None:
    with pytest.raises(CandidateError):
        replace(_candidate_artifact(), digest="not-a-digest")


@pytest.mark.unit
def test_candidate_exposes_no_registration_or_commit_path(artifact: ArtifactRef) -> None:
    candidate = _candidate(artifact)

    assert not hasattr(candidate, "admit")
    assert not hasattr(candidate, "commit")
    assert not hasattr(candidate, "invoke")


def _candidate_artifact() -> ArtifactRef:
    import hashlib

    from wanxiang_foundry.candidate import ArtifactKind

    return ArtifactRef(
        kind=ArtifactKind.REPO,
        uri="repo:example",
        digest=hashlib.sha256(b"repo").hexdigest(),
        rights_basis="Apache-2.0",
    )


def test_artifact_kinds_cover_the_full_artifact2capability_design() -> None:
    assert {kind.value for kind in ArtifactKind} == {
        "paper",
        "repo",
        "api",
        "manual",
        "standard",
        "notebook",
        "workflow",
        "dataset",
        "simulation",
    }
