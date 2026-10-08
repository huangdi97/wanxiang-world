"""M63 domain inference, gap-pack, reuse, and validation contracts."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.composition import (
    DomainValidationSandbox,
    check_cross_world_reuse,
    compose_domains,
    fingerprint_domain_signals,
    make_capability_candidates,
    make_gap_pack,
)
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry


def _candidate(candidate_id: str, kind: str, payload: dict[str, str]) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass="m63_fixture",
        payload=tuple(sorted(payload.items())),
        confidence=0.7,
        source_refs=("source_m63#1",),
        distiller_version=1,
    )


def _registry() -> DomainRegistry:
    registry = DomainRegistry()
    registry.register(
        DomainCapability(
            "family",
            "Family",
            "1.0.0",
            ("family", "genealogy"),
            actions=("visit",),
            rules=("consent",),
        )
    )
    registry.register(
        DomainCapability(
            "narrative",
            "Narrative",
            "1.0.0",
            ("narrative", "temporal"),
            requires=("family",),
        )
    )
    return registry


@pytest.mark.integration
def test_domain_fingerprint_and_composition_are_deterministic() -> None:
    candidates = (
        _candidate("id", "identity", {"key": "alice"}),
        _candidate("place", "place", {"name": "Beijing"}),
        _candidate("rule", "rule", {"name": "consent"}),
    )
    first = fingerprint_domain_signals(candidates)
    second = fingerprint_domain_signals(tuple(reversed(candidates)))
    assert first == second
    composition = compose_domains(_registry(), ("narrative", "family"), composition_id="m63")
    assert composition.dependency_order == ("family", "narrative")
    assert composition.dependency_lock == composition.dependency_order
    assert composition.candidate_only is True


@pytest.mark.integration
def test_gap_pack_capability_candidates_and_sandbox_validation() -> None:
    registry = _registry()
    composition = compose_domains(registry, ("narrative",), composition_id="gap")
    gaps = make_gap_pack(composition, registry)
    assert gaps
    scaffolds = make_capability_candidates(gaps, source_refs=("source_m63#1",))
    assert scaffolds[0].sandbox_only is True
    proposal = scaffolds[0].capability_candidates[0]
    result = DomainValidationSandbox().validate(proposal, registry)
    assert result.passed is False
    assert "not declared" in result.violations[0]
    valid = proposal.__class__(
        "valid_cap",
        "family",
        "family",
        "declared capability",
        proposal.source_refs,
        0.0,
    )
    assert DomainValidationSandbox().validate(valid, registry).passed is True


@pytest.mark.unit
def test_cross_world_reuse_requires_explicit_source_consent() -> None:
    candidate = make_capability_candidates(
        (make_gap_pack(compose_domains(_registry(), ("narrative",)), _registry())[0],),
        source_refs=("private_source#1",),
    )[0].capability_candidates[0]
    denied = check_cross_world_reuse(candidate, target_world_id="world_b", consented_source_ids=())
    allowed = check_cross_world_reuse(
        candidate,
        target_world_id="world_b",
        consented_source_ids=("private_source",),
    )
    assert denied.reusable is False
    assert allowed.reusable is True
