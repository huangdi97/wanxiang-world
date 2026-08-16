"""G58G: Forge review/conflict/completion API surface."""

from __future__ import annotations

from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
from wanxiang_substrate.evidence.binding import EvidenceLink
from wanxiang_substrate.parsing.segment import StableLocator


@pytest.mark.e2e
def test_review_record_and_history() -> None:
    app = create_app()
    client: Any = TestClient(app)
    with client:
        resp = client.post(
            "/forge/reviews",
            json={
                "target_id": "cand_1",
                "action": "approve",
                "reviewer": "human",
                "rationale": "evidence ok",
                "evidence_refs": ["ref://a"],
            },
        )
        assert resp.status_code == 201
        decision = cast(dict[str, Any], resp.json())
        assert decision["target_id"] == "cand_1"
        assert decision["action"] == "approve"
        history = cast(list[dict[str, Any]], client.get("/forge/reviews/cand_1").json())
        assert len(history) == 1


@pytest.mark.e2e
def test_conflict_register_and_list() -> None:
    app = create_app()
    client: Any = TestClient(app)
    with client:
        resp = client.post(
            "/forge/conflicts",
            json={
                "conflict_id": "cf_1",
                "claim_ids": ["claim_a", "claim_b"],
                "source_refs": ["ref://a", "ref://b"],
                "description": "edition disagreement",
            },
        )
        assert resp.status_code == 201
        conflicts = cast(list[dict[str, Any]], client.get("/forge/conflicts").json())
        assert len(conflicts) == 1
        assert conflicts[0]["conflict_id"] == "cf_1"


@pytest.mark.e2e
def test_completion_plan_keeps_unknown() -> None:
    app = create_app()
    client: Any = TestClient(app)
    with client:
        resp = client.post(
            "/forge/completions/plan",
            json=[
                {
                    "requirement_id": "r1",
                    "kind": "actor_initial_location",
                    "detail": "alice",
                    "blocking": True,
                },
                {
                    "requirement_id": "r2",
                    "kind": "location_connectivity",
                    "detail": "garden->hall",
                    "blocking": True,
                },
            ],
        )
        assert resp.status_code == 200
        plan = cast(dict[str, Any], resp.json())
        assert plan["has_blocking_unknown"] is True
        assert all(not c["can_enter_canon"] for c in plan["candidates"])


@pytest.mark.e2e
def test_candidate_evidence_endpoint() -> None:
    app = create_app()
    locator = StableLocator(source_id="s1", fmt="text", kind="paragraph", ref="2")
    app.state.evidence_bindings.add(
        EvidenceLink(link_id="l1", candidate_id="cand_1", locator=locator, role="supports")
    )
    client: Any = TestClient(app)
    with client:
        resp = client.get("/forge/candidates/cand_1/evidence")
        assert resp.status_code == 200
        body = cast(dict[str, Any], resp.json())
        assert body["candidate_id"] == "cand_1"
        assert len(body["links"]) == 1
        assert body["links"][0]["locator"] == locator.to_string()
