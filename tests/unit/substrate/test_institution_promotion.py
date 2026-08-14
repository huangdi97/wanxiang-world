"""G32E: institution/organization rule promotion chain."""

from __future__ import annotations

from typing import cast

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.delta import EntityCreate
from wanxiang_domain.errors import PermissionDenied
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.authority import CommitAuthority
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState
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


def _candidate(score: float = MIN_STABILITY) -> InstitutionCandidate:
    return InstitutionCandidate(
        candidate_id="cand_curfew",
        rule="quiet_after_curfew",
        evidence=("win:1", "win:2", "win:3"),
        origin="distill://guard",
        stability_score=score,
    )


@pytest.mark.unit
def test_unapproved_candidate_does_not_change_gamma() -> None:
    store = InMemoryEventStore()
    chain = InstitutionPromotionChain(CommitAuthority(store, RULES, SCHEMA), RULES, SCHEMA)
    state = _base_state()
    candidate = _candidate()
    assert chain.validate(candidate) is True
    with pytest.raises(PermissionDenied):
        chain.promote(
            candidate, state, instance_id=INSTANCE, branch_id=BRANCH, world_time=WorldTime(1)
        )
    # Gamma (law set / event stream) unchanged: no LawCommit was produced.
    assert store.load(INSTANCE, BRANCH) == ()
    assert state.revision == BranchRevision(0)


@pytest.mark.unit
def test_law_commit_is_replayable_after_approval() -> None:
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    chain = InstitutionPromotionChain(authority, RULES, SCHEMA)
    state = _base_state()
    candidate = chain.approve(_candidate(), "reviewer")
    event = chain.promote(
        candidate, state, instance_id=INSTANCE, branch_id=BRANCH, world_time=WorldTime(1)
    )
    assert event.revision.value == 1
    events = store.load(INSTANCE, BRANCH)
    assert len(events) == 1
    # LawCommit is replayable like any event.
    replayed = ReplayEngine(RULES, SCHEMA).replay(events)
    assert replayed.revision.value == 1
    law_op = cast(EntityCreate, event.delta.operations[0])
    assert replayed.entity(law_op.entity_id) is not None


@pytest.mark.unit
def test_unstable_candidate_fails_validation_even_if_approved() -> None:
    store = InMemoryEventStore()
    chain = InstitutionPromotionChain(CommitAuthority(store, RULES, SCHEMA), RULES, SCHEMA)
    state = _base_state()
    weak = chain.approve(_candidate(score=0.1), "policy")
    with pytest.raises(PermissionDenied):
        chain.promote(weak, state, instance_id=INSTANCE, branch_id=BRANCH, world_time=WorldTime(1))
    assert store.load(INSTANCE, BRANCH) == ()


@pytest.mark.unit
def test_approval_hook_requires_authorized_approver() -> None:
    chain = InstitutionPromotionChain(
        CommitAuthority(InMemoryEventStore(), RULES, SCHEMA), RULES, SCHEMA
    )
    with pytest.raises(PermissionDenied):
        chain.approve(_candidate(), "nobody")
