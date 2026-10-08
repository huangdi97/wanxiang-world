"""G93F: evidence-backed reputation, observer scope, and social labels."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.evolution.delta import EvolutionProvenance
from wanxiang_substrate.evolution.reputation import (
    ReputationEvent,
    ReputationProjection,
    ReputationScope,
    ReputationState,
    SocialRole,
    SocialRoleProjection,
    advance_reputation_projection,
    advance_social_role_projection,
    apply_reputation_proposal,
    assign_social_role,
    initial_reputation_state,
    propose_reputation_update,
    propose_social_role,
    review_reputation_proposal,
    review_social_role_proposal,
)
from wanxiang_substrate.evolution.reputation_model import ReputationEvidenceKind

ALICE = EntityId("actor_alice_g93f")
BOB = EntityId("actor_bob_g93f")
CAROL = EntityId("actor_carol_g93f")
PROVENANCE = EvolutionProvenance(
    origin_ref="run:g93f",
    source_refs=("memory://g93f_source",),
    event_refs=("event:g93f:root",),
    producer="runtime_projection",
)


def _event(
    event_ref: str,
    *,
    observer: EntityId = BOB,
    valence: float = 1.0,
    at_ticks: int = 1,
    scope: str = "local",
    scope_ref: str = "archive:g93f",
) -> ReputationEvent:
    return ReputationEvent(
        event_ref=event_ref,
        observer_id=observer,
        subject_actor_id=ALICE,
        dimension="trustworthiness",
        signal="kept_commitment",
        valence=valence,
        strength=0.8,
        scope=cast("ReputationScope", scope),
        scope_ref=scope_ref,
        at_ticks=at_ticks,
        evidence_ref="event-evidence:" + event_ref,
    )


def _local_state(observer: EntityId | None = BOB) -> ReputationState:
    return initial_reputation_state(
        ALICE,
        dimension="trustworthiness",
        scope="local",
        scope_ref="archive:g93f",
        observer_actor_id=observer,
    )


def test_local_global_and_observer_specific_reputation_are_immutable_views() -> None:
    local = _local_state()
    local_proposal = propose_reputation_update(
        proposal_id="local_positive",
        current=local,
        events=(_event("event:g93f:local:bob"),),
        provenance=PROVENANCE,
    )
    with pytest.raises(PermissionDenied, match="explicit review"):
        apply_reputation_proposal(local, local_proposal)
    approved_local = review_reputation_proposal(local_proposal, reviewer="policy")
    local_after = apply_reputation_proposal(local, approved_local)
    assert local_after.score == pytest.approx(0.2)
    assert local_after.observer_actor_id == BOB

    global_state = initial_reputation_state(
        ALICE,
        dimension="trustworthiness",
        scope="global",
        scope_ref="world:g93f",
    )
    global_proposal = propose_reputation_update(
        proposal_id="global_mixed_observers",
        current=global_state,
        events=(
            _event("event:g93f:global:bob", scope="global", scope_ref="world:g93f"),
            _event(
                "event:g93f:global:carol",
                observer=CAROL,
                scope="global",
                scope_ref="world:g93f",
            ),
        ),
        provenance=PROVENANCE,
    )
    global_after = apply_reputation_proposal(
        global_state,
        review_reputation_proposal(global_proposal, reviewer="reviewer"),
    )
    assert global_after.score == pytest.approx(0.2)
    projection = ReputationProjection(states=(local_after, global_after))
    assert projection.visible_to(BOB) == (local_after, global_after)
    assert projection.visible_to(CAROL) == (global_after,)
    assert projection.state(ALICE, "trustworthiness", "local", "archive:g93f", BOB) == local_after
    assert projection.state(ALICE, "trustworthiness", "local", "archive:g93f", CAROL) is None


def test_social_role_is_review_gated_and_separate_from_institution_roles() -> None:
    current = _local_state()
    reputation = apply_reputation_proposal(
        current,
        review_reputation_proposal(
            propose_reputation_update(
                proposal_id="role_reputation",
                current=current,
                events=(_event("event:g93f:role"),),
                provenance=PROVENANCE,
            ),
            reviewer="policy",
        ),
    )
    role = SocialRole(
        role_id=EntityId("social_role_trusted_keeper_g93f"),
        name="trusted keeper",
        dimension="trustworthiness",
        minimum_score=0.1,
        scope="local",
        scope_ref="archive:g93f",
        observer_actor_id=BOB,
    )
    proposal = propose_social_role(
        proposal_id="role_assignment",
        subject_actor_id=ALICE,
        role=role,
        reputation=reputation,
        provenance=PROVENANCE,
    )
    assert proposal.eligible is True
    with pytest.raises(PermissionDenied, match="explicit review"):
        assign_social_role(proposal)
    reviewed = review_social_role_proposal(proposal, reviewer="policy")
    assignment = assign_social_role(reviewed)
    role_projection = advance_social_role_projection(SocialRoleProjection(), reviewed)
    assert assignment.subject_actor_id == ALICE
    assert role_projection.assignments_for(ALICE) == (assignment,)
    assert role_projection.assignments[0].role.role_id == role.role_id


def test_belief_and_rumor_are_rejected_as_reputation_evidence() -> None:
    for kind in ("belief", "rumor"):
        with pytest.raises(ContractError, match="belief or rumor"):
            ReputationEvent(
                event_ref="event:g93f:invalid:" + kind,
                observer_id=BOB,
                subject_actor_id=ALICE,
                dimension="trustworthiness",
                signal="kept_commitment",
                valence=1.0,
                strength=1.0,
                scope="local",
                scope_ref="archive:g93f",
                at_ticks=1,
                evidence_ref="memory://g93f:" + kind,
                evidence_kind=cast(ReputationEvidenceKind, kind),
            )


def test_authority_and_scope_checks_prevent_silent_bypass() -> None:
    current = _local_state()
    event = _event("event:g93f:authority")
    with pytest.raises(ContractError, match="Commit Authority"):
        propose_reputation_update(
            proposal_id="authority_provider",
            current=current,
            events=(event,),
            provenance=PROVENANCE,
            provider_ref="commit_authority",
        )
    with pytest.raises(ContractError, match="does not match projection scope"):
        propose_reputation_update(
            proposal_id="wrong_scope",
            current=current,
            events=(_event("event:g93f:wrong", observer=CAROL),),
            provenance=PROVENANCE,
        )
    assert advance_reputation_projection(
        ReputationProjection(states=(current,)),
        review_reputation_proposal(
            propose_reputation_update(
                proposal_id="projection_advance",
                current=current,
                events=(event,),
                provenance=PROVENANCE,
            ),
            reviewer="policy",
        ),
    ).states[0].score == pytest.approx(0.2)
