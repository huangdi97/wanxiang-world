"""M71-M78 regression contracts for real-book semantic distillation."""

from __future__ import annotations

from collections import Counter
from typing import Any

import pytest
from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_domain.errors import WanxiangError
from wanxiang_substrate.authoring import LocalSemanticProvider
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.sources.adapter import IngestResult
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

BOOK = """第一章 起因
张三来到北京市，李四随后到达。张三说，李四回答。
规则：重要文件不得外传。
第二章 关系
张三和李四在北京市见面，张三决定调查。
"""


def _record(source_id: str = "book_m71") -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(BOOK),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(
            owner="explicit-test-declaration",
            usage="private-package",
            approved=True,
            package_inclusion_allowed=True,
        ),
        payload=BOOK,
        provenance="synthetic:m71-m78",
        access="private",
    )


@pytest.mark.integration
def test_chinese_structure_and_configured_provider_reach_world_draft() -> None:
    parsed = StructureParser().parse(
        IngestResult(source_id="book_m71", kind="text", content=BOOK, detected_format="text"),
        source_id="book_m71",
        version="1",
    )
    assert sum(node.kind == "chapter" for node in parsed.nodes) == 2
    service = AuthoringService(providers=ProviderRouter((LocalSemanticProvider(),)))
    result = OneClickAuthoring(service).run(
        "job_m71_provider",
        (_record(),),
        profile="book",
        semantic_provider="local",
    )
    kinds = Counter(candidate.kind for candidate in service.build(result.job_id).candidates)  # type: ignore[union-attr]
    assert all(kinds[kind] > 0 for kind in ("character", "place", "event", "relation"))
    assert result.package.evidence_coverage > 0.0
    assert all(candidate.source_refs for candidate in service.build(result.job_id).candidates)  # type: ignore[union-attr]


@pytest.mark.integration
def test_no_provider_is_terminal_and_not_an_empty_success() -> None:
    service = AuthoringService()
    service.create_job("job_m71_no_provider", sources=(_record("book_m71_no_provider"),))
    with pytest.raises(WanxiangError) as error:
        service.start("job_m71_no_provider")
    assert error.value.code == "semantic_provider_required"
    snapshot = service.status("job_m71_no_provider")
    assert snapshot.status == "failed"
    assert snapshot.product_state == "SEMANTIC_PROVIDER_REQUIRED"
    assert snapshot.parsed_nodes > 0
    assert snapshot.segment_count > 0
    assert snapshot.batch_count > 0


@pytest.mark.integration
def test_api_exposes_product_state_and_does_not_generate_empty_scenarios() -> None:
    client: Any = TestClient(create_app())
    response = client.post(
        "/studio/one-click",
        json={
            "job_id": "job_m71_api_no_provider",
            "profile": "book",
            "sources": [
                {
                    "source_id": "book_m71_api_no_provider",
                    "kind": "text",
                    "content": BOOK,
                    "stage": "E3",
                    "rights_approved": True,
                    "package_inclusion_allowed": True,
                    "access": "private",
                }
            ],
        },
    )
    assert response.status_code == 422
    assert response.json()["code"] == "semantic_provider_required"
    status = client.get("/studio/jobs/job_m71_api_no_provider")
    assert status.json()["status"] == "failed"
    assert status.json()["product_state"] == "SEMANTIC_PROVIDER_REQUIRED"
    assert client.get("/studio/jobs/job_m71_api_no_provider/scenarios").json()["scenarios"] == []


@pytest.mark.integration
def test_runtime_worldness_and_living_evidence_use_commit_replay_and_branch() -> None:
    runtime = build_reference_runtime()
    client: Any = TestClient(create_app(runtime))
    response = client.post(
        "/studio/one-click",
        json={
            "job_id": "job_m71_runtime",
            "profile": "book",
            "semantic_provider": "local",
            "sources": [
                {
                    "source_id": "book_m71_runtime",
                    "kind": "text",
                    "content": BOOK,
                    "stage": "E3",
                    "rights_approved": True,
                    "package_inclusion_allowed": True,
                    "access": "private",
                }
            ],
        },
    )
    assert response.status_code == 201
    worldness = client.post("/studio/jobs/job_m71_runtime/worldness")
    assert worldness.status_code == 200
    payload = worldness.json()["worldness"]
    assert payload["passed"] is True
    assert {item["name"] for item in payload["evidence"]} == {
        "persistence",
        "identity",
        "temporal",
        "spatial",
        "causal_action",
        "epistemic_isolation",
        "object_persistence",
        "evidence_traceability",
        "uncertainty",
        "branch_replay_readiness",
    }
    assert payload["living"]["action"]["committed"] is True
    assert payload["living"]["action"]["replay_equal"] is True
    assert payload["branch_proof"]["isolated"] is True
    entered = client.post("/studio/jobs/job_m71_runtime/enter")
    assert entered.status_code == 200
    assert entered.json()["perception"]["entities"]
