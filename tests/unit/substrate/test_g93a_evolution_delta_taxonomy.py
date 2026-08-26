"""G93A: explicit evolution Delta taxonomy and Commit Authority boundary."""

from __future__ import annotations

from dataclasses import fields
from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.evolution.delta import (
    BeliefDelta,
    CapabilityEvolutionDelta,
    EvolutionCommitPolicy,
    EvolutionDelta,
    EvolutionProvenance,
    OrganizationDelta,
    PersonaDelta,
    RelationshipDelta,
    StateDelta,
)
from wanxiang_substrate.evolution.delta_common import PrimitiveValue

ACTOR_A = EntityId("actor_a")
ACTOR_B = EntityId("actor_b")
PROVENANCE = EvolutionProvenance(
    origin_ref="run:g93a",
    source_refs=("source:g93a",),
    event_refs=("event:g93a:1",),
    producer="runtime_projection",
)


def _records() -> tuple[EvolutionDelta, ...]:
    return (
        StateDelta(
            "state_1",
            EntityId("state_subject"),
            "status",
            "idle",
            "active",
            "event",
            PROVENANCE,
        ),
        BeliefDelta(
            "belief_1",
            ACTOR_A,
            EntityId("belief_1"),
            "support",
            0.2,
            0.8,
            "unknown",
            "supported",
            "evidence",
            PROVENANCE,
        ),
        RelationshipDelta(
            "relation_1",
            "relation_a_b",
            ACTOR_A,
            ACTOR_B,
            "trust",
            0.1,
            0.6,
            "shared event",
            PROVENANCE,
        ),
        CapabilityEvolutionDelta(
            "capability_1",
            ACTOR_A,
            "calligraphy",
            0,
            1,
            0.0,
            0.2,
            0.0,
            0.7,
            "practice passed",
            PROVENANCE,
        ),
        PersonaDelta(
            actor_id=ACTOR_A,
            trait="temperament",
            from_value="open",
            to_value="guarded",
            rationale="repeated observed loss",
            evidence_refs=("event:g93a:1",),
            delta_id="persona_1",
            provenance=PROVENANCE,
        ),
        OrganizationDelta(
            "organization_1",
            EntityId("org_g93a"),
            "joined",
            ACTOR_A,
            None,
            "scribe",
            "accepted role",
            PROVENANCE,
        ),
    )


def test_six_delta_kinds_are_explicit_and_serializable() -> None:
    records = _records()
    assert {record.kind for record in records} == {
        "state",
        "belief",
        "relationship",
        "capability",
        "persona",
        "organization",
    }
    assert len({record.fingerprint() for record in records}) == len(records)
    assert all(record.to_dict()["schema_version"] == 1 for record in records)
    assert all("provenance" in record.to_dict() for record in records)


def test_taxonomy_has_no_generic_evolution_blob() -> None:
    forbidden = {"payload", "data", "metadata"}
    for record in _records():
        assert not forbidden.intersection(item.name for item in fields(record))
        assert isinstance(record.to_dict(), dict)


def test_provenance_policy_accepts_proposals_and_receipts_only_after_commit() -> None:
    proposal = _records()[0]
    EvolutionCommitPolicy.validate_proposal(proposal)
    receipt = EvolutionCommitPolicy.receipt(
        proposal,
        event_ref="event:canonical:1",
        branch_revision=1,
        authority_ref="commit-authority:world-1",
    )
    assert receipt.delta_id == proposal.delta_id
    assert receipt.delta_kind == "state"
    assert receipt.event_ref == "event:canonical:1"


def test_proposal_without_evidence_or_from_commit_authority_is_rejected() -> None:
    no_evidence = StateDelta(
        "state_no_evidence",
        EntityId("state_subject"),
        "status",
        "idle",
        "active",
        "unattributed",
        EvolutionProvenance("run:unattributed"),
    )
    with pytest.raises(ContractError, match="provenance"):
        EvolutionCommitPolicy.validate_proposal(no_evidence)

    authority_proposal = StateDelta(
        "state_authority",
        EntityId("state_subject"),
        "status",
        "idle",
        "active",
        "bad producer",
        EvolutionProvenance("run:authority", event_refs=("event:1",), producer="commit_authority"),
    )
    with pytest.raises(ContractError, match="consumer"):
        EvolutionCommitPolicy.validate_proposal(authority_proposal)


def test_schema_and_scalar_invariants_are_enforced() -> None:
    with pytest.raises(ContractError, match="schema"):
        StateDelta(
            "bad_schema",
            EntityId("state_subject"),
            "status",
            "idle",
            "active",
            "bad version",
            PROVENANCE,
            schema_version=2,
        )
    with pytest.raises(ContractError, match="scalar"):
        StateDelta(
            "bad_scalar",
            EntityId("state_subject"),
            "status",
            cast(PrimitiveValue, {"not": "a scalar"}),
            "active",
            "bad payload",
            PROVENANCE,
        )
