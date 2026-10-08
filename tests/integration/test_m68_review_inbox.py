"""M68 impact scoring, approval, inbox, batch, preview, audit, and UX contracts."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
from wanxiang_substrate.authoring.review_inbox import (
    AutoApprovalPolicy,
    ImpactContext,
    ReviewInbox,
)
from wanxiang_substrate.candidates.envelope import CandidateEnvelope


def _candidate(
    candidate_id: str,
    kind: str = "object",
    confidence: float = 0.9,
    payload: tuple[tuple[str, str], ...] = (("entity_id", "alice"),),
) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass="m68",
        payload=payload,
        confidence=confidence,
        source_refs=(f"source:{candidate_id}",),
        distiller_version=1,
    )


@pytest.mark.integration
def test_impact_scoring_includes_uncertainty_conflict_rights_and_downstream() -> None:
    inbox = ReviewInbox()
    low = inbox.score(_candidate("low"))
    high = inbox.score(
        _candidate("high", "relation", confidence=0.4),
        ImpactContext(
            downstream_count=5,
            conflict=True,
            rights_blocked=True,
            uncertainty=0.8,
        ),
    )
    assert low.score < high.score
    assert {"uncertainty", "source conflict", "rights blocker"} <= set(high.reasons)
    assert high.score == 1.0


@pytest.mark.integration
def test_auto_approval_and_review_queue_are_policy_driven_and_idempotent() -> None:
    inbox = ReviewInbox()
    candidates = (_candidate("safe"), _candidate("needs", "identity", confidence=0.6))
    items = inbox.build(
        candidates,
        contexts={"needs": ImpactContext(conflict=True)},
        policy=AutoApprovalPolicy(),
    )
    assert items[0].auto_approved is True
    assert items[1].needs_human_review is True
    assert inbox.review_queue(items)[0].candidate.candidate_id == "needs"
    first = inbox.approve_low_risk(items, reviewer="rule_engine")
    second = inbox.approve_low_risk(items, reviewer="rule_engine")
    assert first == second
    assert inbox.ledger.latest("safe") is not None
    assert inbox.audit()[0].actor_type == "rule"
    assert inbox.audit()[0].actor_id == "rule_engine"


@pytest.mark.integration
def test_batch_review_maps_keep_unknown_to_defer_and_preserves_audit() -> None:
    inbox = ReviewInbox()
    decisions = inbox.batch(
        ("c1", "c2", "c1"),
        action="keep_unknown",
        reviewer="human",
        rationale="insufficient evidence; preserve unknown",
    )
    assert [decision.target_id for decision in decisions] == ["c1", "c2"]
    assert all(decision.action == "defer" for decision in decisions)
    assert len(inbox.audit()) == 2
    assert all(a.actor_type == "human" for a in inbox.audit())


@pytest.mark.integration
def test_impact_preview_is_stable_and_studio_inbox_is_server_truth() -> None:
    inbox = ReviewInbox()
    candidate = _candidate(
        "preview",
        "event",
        payload=(
            ("event_id", "arrival"),
            ("entity_id", "alice"),
            ("scenario_id", "scenario_1"),
        ),
    )
    preview = inbox.preview(
        candidate,
        ImpactContext(
            affected_entities=("alice", "bob"),
            affected_events=("arrival",),
            affected_scenarios=("scenario_1",),
            package_sections=("draft.events", "package.preview"),
        ),
    )
    assert preview.entities == ("alice", "bob")
    assert preview.events == ("arrival",)
    assert preview.scenarios == ("scenario_1",)
    assert (
        preview.preview_hash
        == inbox.preview(
            candidate,
            ImpactContext(
                affected_entities=("alice", "bob"),
                affected_events=("arrival",),
                affected_scenarios=("scenario_1",),
                package_sections=("draft.events", "package.preview"),
            ),
        ).preview_hash
    )

    client: Any = TestClient(create_app())
    response = client.post(
        "/studio/jobs",
        json={
            "job_id": "job_m68_api",
            "sources": [
                {
                    "source_id": "m68_api_source",
                    "kind": "text",
                    "content": "# Chapter\nAlice arrived in Beijing in 1985.",
                    "stage": "E3",
                    "rights_approved": True,
                    "access": "public",
                }
            ],
        },
    )
    assert response.status_code == 201
    assert client.post("/studio/jobs/job_m68_api/start").status_code == 200
    inbox_response = client.get("/studio/jobs/job_m68_api/review-inbox")
    assert inbox_response.status_code == 200
    api_items = inbox_response.json()["items"]
    assert api_items and "preview" in api_items[0]
    batch = client.post(
        "/studio/jobs/job_m68_api/review-inbox/batch",
        json={
            "candidate_ids": [api_items[0]["candidate_id"]],
            "action": "keep_unknown",
            "reviewer": "human",
            "rationale": "keep unresolved for later evidence",
        },
    )
    assert batch.status_code == 201
    assert batch.json()["decisions"][0]["action"] == "defer"
    audit = client.get("/studio/jobs/job_m68_api/review-inbox/audit")
    assert audit.status_code == 200
    assert audit.json()["audits"][0]["actor_type"] == "human"
