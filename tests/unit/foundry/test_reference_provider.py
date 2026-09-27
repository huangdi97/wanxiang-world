"""Reference provider honesty and its refusal to fabricate."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_foundry.candidate import ArtifactRef
from wanxiang_foundry.errors import CandidateError
from wanxiang_foundry.reference_provider import RuleBasedFoundryProvider


def _declaration() -> dict[str, object]:
    return {
        "capability_id": "cap.demo",
        "proposed_version": "0.1.0",
        "inputs": ["int"],
        "outputs": ["str"],
        "requested_side_effects": ["none"],
    }


@pytest.mark.unit
def test_reference_provider_is_honest_about_identity() -> None:
    provider = RuleBasedFoundryProvider()

    assert provider.is_reference_provider is True
    assert provider.provider_id == "foundry-rule-based-reference"
    assert "paper2agent" not in provider.provider_id.lower()


@pytest.mark.unit
def test_reference_provider_builds_candidate_from_declaration(artifact: ArtifactRef) -> None:
    candidate = RuleBasedFoundryProvider().propose(artifact, _declaration())

    assert candidate.capability_id == "cap.demo"
    assert candidate.proposed_version == "0.1.0"
    assert candidate.proposed_interface["inputs"] == ("int",)
    assert candidate.proposed_interface["outputs"] == ("str",)
    assert candidate.artifact == artifact


@pytest.mark.unit
def test_reference_provider_refuses_missing_rights_basis(artifact: ArtifactRef) -> None:
    no_rights = replace(artifact, rights_basis="")

    with pytest.raises(CandidateError):
        RuleBasedFoundryProvider().propose(no_rights, _declaration())


@pytest.mark.unit
def test_reference_provider_refuses_missing_interface_contract(artifact: ArtifactRef) -> None:
    declaration = _declaration()
    del declaration["inputs"]

    with pytest.raises(CandidateError):
        RuleBasedFoundryProvider().propose(artifact, declaration)


@pytest.mark.unit
def test_reference_provider_refuses_ill_typed_field(artifact: ArtifactRef) -> None:
    declaration = _declaration()
    declaration["capability_id"] = 123

    with pytest.raises(CandidateError):
        RuleBasedFoundryProvider().propose(artifact, declaration)


@pytest.mark.unit
def test_reference_provider_refuses_unknown_side_effect(artifact: ArtifactRef) -> None:
    declaration = _declaration()
    declaration["requested_side_effects"] = ["canonical_write"]

    with pytest.raises(CandidateError):
        RuleBasedFoundryProvider().propose(artifact, declaration)
