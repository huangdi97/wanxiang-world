"""G32H: M29 gate ? synthetic society habit->norm->institution controlled chain."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.authority import CommitAuthority
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.evolution.distillation import BehaviorRecord, SocialPatternDistiller
from wanxiang_substrate.evolution.institution_promotion import (
    MIN_STABILITY,
    InstitutionCandidate,
    InstitutionPromotionChain,
)


def _base_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


@pytest.mark.integration
def test_habit_never_automatically_crosses_higher_gates() -> None:
    """A single habit (one window) never becomes a norm or institution."""
    distiller = SocialPatternDistiller(threshold=2)
    distiller.observe(BehaviorRecord("norm:quiet_after_curfew", "guard", 1))
    assert distiller.distill() == ()  # not even a candidate
    store = InMemoryEventStore()
    chain = InstitutionPromotionChain(CommitAuthority(store, RULES, SCHEMA), RULES, SCHEMA)
    state = _base_state()
    candidate = InstitutionCandidate(
        candidate_id="cand_curfew",
        rule="quiet_after_curfew",
        evidence=("win:1",),
        origin="distill://guard",
    )
    # Not approved -> institution gate not crossed; Gamma unchanged.
    with pytest.raises(PermissionDenied):
        chain.promote(
            candidate, state, instance_id=INSTANCE, branch_id=BRANCH, world_time=WorldTime(1)
        )
    assert store.load(INSTANCE, BRANCH) == ()


@pytest.mark.integration
def test_synthetic_society_long_run_habit_to_norm_to_institution() -> None:
    distiller = SocialPatternDistiller(threshold=2)
    for window in range(1, 6):
        distiller.observe_batch(
            [
                BehaviorRecord("norm:quiet_after_curfew", "guard", window),
                BehaviorRecord("group:night_watch", "guard", window),
            ]
        )
    candidates = distiller.distill()
    by_key = {c.key: c for c in candidates}
    norm = by_key["norm:quiet_after_curfew"]
    group = by_key["group:night_watch"]
    assert norm.pattern_type == "norm" and norm.meets_threshold
    assert group.pattern_type == "group" and group.meets_threshold

    # The norm candidate crosses the institution gate ONLY through the
    # controlled chain (validate + approve + LawCommit).
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    chain = InstitutionPromotionChain(authority, RULES, SCHEMA)
    state = _base_state()
    institution_candidate = InstitutionCandidate(
        candidate_id="cand_curfew",
        rule=norm.key,
        evidence=norm.provenance,
        origin=norm.origin_ref,
        stability_score=MIN_STABILITY,
    )
    assert chain.validate(institution_candidate) is True
    approved = chain.approve(institution_candidate, "reviewer")
    event = chain.promote(
        approved, state, instance_id=INSTANCE, branch_id=BRANCH, world_time=WorldTime(1)
    )
    assert event.revision.value == 1

    # Replay stays deterministic and Branch isolation is preserved (parent root).
    replayed = ReplayEngine(RULES, SCHEMA).replay(store.load(INSTANCE, BRANCH))
    assert replayed.revision.value == 1
    assert (
        replayed.semantic_hash()
        == ReplayEngine(RULES, SCHEMA).replay(store.load(INSTANCE, BRANCH)).semantic_hash()
    )
