"""G90D: hybrid source/prompt fusion preserves provenance and dissent."""

from __future__ import annotations

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.workshop import (
    CreatorIntent,
    HybridClaim,
    HybridGenesisPolicy,
    build_prompt_contract,
    claim_from_candidate,
    fuse_hybrid_genesis,
)


def test_hybrid_source_precedence_never_discards_conflicting_prompt_claim() -> None:
    source = CandidateEnvelope(
        "source_rule",
        "rule",
        "source-pass",
        (("key", "rule"), ("value", "visitors register")),
        0.9,
        ("book#rule-1",),
        1,
    )
    prompt = build_prompt_contract(
        CreatorIntent("intent_hybrid", "author", "rule: visitors enter freely")
    )
    result = fuse_hybrid_genesis((claim_from_candidate(source),), prompt)
    assert result.review_required is True
    assert len(result.conflicts) == 1
    assert result.selected_claim_ids == ("source_rule",)
    assert {claim.origin for claim in result.claims} == {"source", "prompt"}
    assert all(trace.source_refs or trace.intent_ref for trace in result.traces)


def test_hybrid_policy_is_configurable_and_conflict_is_explicit() -> None:
    source = HybridClaim("s1", "rule:rule", "register", "source", "E3", ("s1#1",))
    prompt = build_prompt_contract(
        CreatorIntent("intent_hybrid_conflict", "author", "rule: free entry")
    )
    result = fuse_hybrid_genesis(
        (source,),
        prompt,
        policy=HybridGenesisPolicy("preserve_dissent"),
    )
    assert result.policy.precedence == "preserve_dissent"
    assert result.selected_claim_ids == ()
    assert len(result.conflicts) == 1
    assert {claim.evidence_class for claim in result.claims} == {"E3", "E5"}
