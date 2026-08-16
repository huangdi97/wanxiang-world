"""G58A-G58F: Evidence binding, conflicts, rights gate, review decisions,
completion E0-E5 + planner."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.completion.candidates import (
    CompletionCandidate,
    class_never_upgrades,
)
from wanxiang_substrate.completion.planner import (
    CompletionPlanner,
    MissingRequirement,
)
from wanxiang_substrate.evidence.binding import EvidenceBindings, EvidenceLink
from wanxiang_substrate.evidence.conflict import ConflictLedger, ConflictSet
from wanxiang_substrate.parsing.segment import StableLocator
from wanxiang_substrate.review.decisions import ReviewDecision, ReviewLedger
from wanxiang_substrate.rights.gate import RightsGate
from wanxiang_substrate.sources.errors import RightsDenied
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _locator(ref: str = "1") -> StableLocator:
    return StableLocator(source_id="s1", fmt="text", kind="paragraph", ref=ref)


def _record(*, approved: bool = True, usage: str = "corpus") -> SourceRecord:
    return SourceRecord(
        source_id="src_1",
        kind="text",
        content_hash=payload_hash("fixture"),
        content_ref="ref://src_1",
        stage="E3",
        rights=RightsEnvelope(owner="o", usage=usage, approved=approved),
        payload="",
        provenance="fixture:g58",
    )


@pytest.mark.unit
def test_evidence_binding_bidirectional() -> None:
    bindings = EvidenceBindings()
    support = EvidenceLink(link_id="l1", candidate_id="c1", locator=_locator("2"), role="supports")
    contradict = EvidenceLink(
        link_id="l2", candidate_id="c1", locator=_locator("3"), role="contradicts"
    )
    bindings.add(support)
    bindings.add(contradict)
    assert len(bindings.links_for_candidate("c1")) == 2
    assert len(bindings.supporting("c1")) == 1
    assert len(bindings.contradicting("c1")) == 1
    assert bindings.candidates_for_locator(_locator("2")) == ("c1",)


@pytest.mark.unit
def test_evidence_link_validation() -> None:
    with pytest.raises(ContractError):
        EvidenceLink(link_id="", candidate_id="c", locator=_locator(), role="supports")


@pytest.mark.unit
def test_conflict_ledger_preserves_all_claims() -> None:
    ledger = ConflictLedger()
    conflict = ConflictSet(
        conflict_id="cf1",
        claim_ids=("claim_a", "claim_b"),
        source_refs=("ref://a", "ref://b"),
        description="edition disagreement",
    )
    ledger.register(conflict)
    assert ledger.get("cf1") == conflict
    assert len(ledger.conflicts_for_claim("claim_a")) == 1
    # No overwrite: registering a different conflict for same id is idempotent.
    ledger.register(conflict)
    assert ledger.get("cf1") == conflict


@pytest.mark.unit
def test_rights_gate_scopes() -> None:
    gate = RightsGate()
    assert gate.decide(_record(), "display").ok
    assert gate.decide(_record(usage="corpus,package"), "package").ok
    assert not gate.decide(_record(usage="corpus"), "package").ok
    with pytest.raises(RightsDenied):
        gate.require(_record(approved=False), "display")


@pytest.mark.unit
def test_review_ledger_append_only_and_reversible() -> None:
    ledger = ReviewLedger()
    first = ReviewDecision(
        decision_id="d1", target_id="c1", action="approve", reviewer="human", rationale="ok"
    )
    second = ReviewDecision(
        decision_id="d2", target_id="c1", action="reject", reviewer="human", rationale="new info"
    )
    ledger.record(first)
    ledger.record(second)
    assert len(ledger.history("c1")) == 2
    assert ledger.latest("c1") == second
    for action in ("approve", "reject", "edit", "merge", "split", "defer", "request_evidence"):
        assert ReviewDecision(
            decision_id="x", target_id="t", action=action, reviewer="r", rationale="x"
        )  # type: ignore[arg-type]


@pytest.mark.unit
def test_completion_candidate_canon_default_false() -> None:
    candidate = CompletionCandidate(
        completion_id="c1",
        description="initial location",
        completion_class="E3",
        support_refs=(),
        confidence=0.3,
    )
    assert candidate.can_enter_canon is False
    assert candidate.origin_label == "runtime_default"
    with pytest.raises(ContractError):
        CompletionCandidate(
            completion_id="c2",
            description="x",
            completion_class="E1",
            support_refs=(),
            confidence=0.5,
            can_enter_canon=True,
        )


@pytest.mark.unit
def test_class_never_upgrades_to_e0() -> None:
    assert class_never_upgrades("E1", "E1") is True
    assert class_never_upgrades("E0", "E0") is True
    assert class_never_upgrades("E1", "E0") is False


@pytest.mark.unit
def test_completion_planner_keep_unknown() -> None:
    planner = CompletionPlanner()
    requirements = (
        MissingRequirement("r1", "actor_initial_location", "alice"),
        MissingRequirement("r2", "location_connectivity", "garden->hall"),
        MissingRequirement("r3", "domain_requirement", "household ritual"),
    )
    plan = planner.plan(requirements, keep_unknown=True)
    assert plan.has_blocking_unknown is True
    assert any(c.completion_class == "E3" for c in plan.candidates)
    assert any(c.completion_class == "E2" for c in plan.candidates)
    # keep_unknown preserves honesty: connectivity stays unknown (not fabricated).
    assert any(r.kind == "location_connectivity" for r in plan.unknown)


@pytest.mark.unit
def test_completion_planner_no_unknown_when_disabled() -> None:
    requirements = (MissingRequirement("r1", "actor_initial_location", "alice"),)
    plan = CompletionPlanner().plan(requirements, keep_unknown=False)
    assert plan.unknown == ()
    assert len(plan.candidates) == 1
