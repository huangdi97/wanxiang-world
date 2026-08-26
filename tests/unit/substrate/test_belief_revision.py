"""G89D: belief revision lineage, unknown state, and future isolation."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.epistemic import (
    BeliefAssertion,
    BeliefEvidence,
    BeliefRevisionChain,
    BeliefRevisionEngine,
)


def belief() -> BeliefAssertion:
    return BeliefAssertion(EntityId("belief_old"), EntityId("actor_a"), "the gate is open", 0.7, 1)


@pytest.mark.unit
def test_support_contradict_refine_and_unknown_preserve_lineage() -> None:
    engine = BeliefRevisionEngine()
    base = belief()
    evidence = BeliefEvidence("obs:gate", EntityId("actor_a"), 2, 0.2, "present")
    supported = engine.revise(
        base,
        revision_id="rev_support",
        kind="support",
        evidence=evidence,
        reason="direct observation supports the claim",
        new_belief_id=EntityId("belief_supported"),
    )
    contradicted = engine.revise(
        base,
        revision_id="rev_contradict",
        kind="contradict",
        evidence=BeliefEvidence("obs:closed", EntityId("actor_a"), 3, 0.6, "past"),
        reason="later observation conflicts",
        new_belief_id=EntityId("belief_contested"),
    )
    refined = engine.revise(
        base,
        revision_id="rev_refine",
        kind="refine",
        evidence=evidence,
        reason="observation narrows the proposition",
        new_belief_id=EntityId("belief_refined"),
        refined_proposition="the east gate is open",
    )
    unknown = engine.revise(
        base,
        revision_id="rev_unknown",
        kind="unknown",
        evidence=evidence,
        reason="evidence is insufficient",
        new_belief_id=EntityId("belief_unknown"),
    )
    assert supported.after.confidence == 0.9
    assert contradicted.after.stance == "contested"
    assert refined.after.proposition == "the east gate is open"
    assert unknown.after.stance == "unknown" and unknown.after.confidence == 0.5
    chain = BeliefRevisionChain.start(base).append(contradicted)
    assert chain.assertions == (base, contradicted.after)
    assert chain.current.is_world_truth is False


@pytest.mark.unit
def test_future_evidence_cannot_leak_into_belief_revision() -> None:
    with pytest.raises(ContractError):
        BeliefRevisionEngine().revise(
            belief(),
            revision_id="rev_future",
            kind="support",
            evidence=BeliefEvidence("future:event", EntityId("actor_a"), 9, 1.0, "future"),
            reason="future knowledge",
            new_belief_id=EntityId("belief_leak"),
        )
