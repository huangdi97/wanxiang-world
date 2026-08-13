"""G04B: source registry & source gate.

Covers review transitions with audit, rights decisions, canonical-eligibility
gates, malicious-injection isolation, conflicting claims and provenance.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.sources.errors import (
    DuplicateSource,
    InvalidTransition,
    MaliciousSource,
    RightsDenied,
    SourceNotApproved,
)
from wanxiang_substrate.sources.fixture import (
    approved_source,
    conflicting_claims,
    malicious_source,
    rejected_source,
)
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.model import SourceRecord, payload_hash
from wanxiang_substrate.sources.policy import SourcePolicy
from wanxiang_substrate.sources.registry import SourceRegistry


@pytest.mark.unit
def test_approved_source_is_canonical_eligible() -> None:
    record = approved_source()
    gate = SourceGate()
    decision = gate.decide(record)
    assert decision.ok is True
    gate.require_compile(record)


@pytest.mark.unit
def test_rights_denied_source_blocked() -> None:
    record = rejected_source()
    gate = SourceGate()
    decision = gate.decide(record)
    assert decision.ok is False
    with pytest.raises(RightsDenied):
        gate.require_compile(record)


@pytest.mark.unit
def test_unapproved_stage_blocked() -> None:
    payload = "A fact waiting for review."
    record = SourceRecord(
        source_id="src_pending",
        kind="text",
        content_hash=payload_hash(payload),
        content_ref="ref://pending",
        stage="E1",
        rights=approved_source().rights,
        payload=payload,
        provenance="fixture:pending",
    )
    gate = SourceGate()
    assert gate.decide(record).ok is False
    with pytest.raises(SourceNotApproved):
        gate.require_compile(record)


@pytest.mark.unit
def test_malicious_source_cannot_alter_behavior() -> None:
    record = malicious_source()
    gate = SourceGate()
    decision = gate.decide(record)
    assert decision.ok is False
    with pytest.raises(MaliciousSource):
        gate.require_compile(record)
    # The payload is never surfaced as data once flagged.
    with pytest.raises(MaliciousSource):
        gate.read_as_data(record)


@pytest.mark.unit
def test_conflicting_claims_coexist_with_evidence() -> None:
    claim_a, claim_b = conflicting_claims()
    assert claim_a.claim_id != claim_b.claim_id
    assert claim_a.status == "eligible" and claim_b.status == "eligible"
    assert claim_a.proposition != claim_b.proposition
    assert claim_a.evidence_links[0].source_id != claim_b.evidence_links[0].source_id
    # Neither claim overwrites the other; both are retained as candidates.


@pytest.mark.unit
def test_transitions_are_audited_and_immutable() -> None:
    registry = SourceRegistry()
    record = approved_source()
    registry.register(record)
    upgraded = registry.transition("src_charter", "E4", reviewer="reviewer-1", policy_version=2)
    assert upgraded.stage == "E4"
    history = registry.audit_history("src_charter")
    assert len(history) == 2
    assert history[1].reviewer == "reviewer-1"
    assert history[1].policy_version == 2
    assert history[1].to_stage == "E4"
    # A rejected source cannot be resurrected to E3.
    with pytest.raises(InvalidTransition):
        registry.transition("src_charter", "E3", reviewer="reviewer-2", policy_version=2)


@pytest.mark.unit
def test_duplicate_content_rejected() -> None:
    registry = SourceRegistry()
    first = approved_source()
    registry.register(first)
    duplicate = SourceRecord(
        source_id="src_charter_copy",
        kind="text",
        content_hash=first.content_hash,
        content_ref="ref://charter_copy",
        stage="E3",
        rights=first.rights,
        payload=first.payload,
        provenance="fixture:duplicate",
    )
    with pytest.raises(DuplicateSource):
        registry.register(duplicate)


@pytest.mark.unit
def test_decision_has_provenance_fields() -> None:
    gate = SourceGate(SourcePolicy(policy_version=3))
    decision = gate.decide(approved_source())
    assert decision.policy_version == 3
    assert decision.reviewer == "source_gate"
    assert decision.source_id == "src_charter"
    assert decision.reason
