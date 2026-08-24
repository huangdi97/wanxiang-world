"""M58 no-API authoring service plus API/CLI-equivalent backend contract."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.sources.errors import OcrRequired
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

BOOK = """# Chapter One

Alice arrived in Beijing in 1985.
rule: keep promises
object: family letter
"""


def _record(
    source_id: str = "book_m58", *, kind: str = "text", content: str = BOOK
) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind=kind,
        content_hash=payload_hash(content),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="fixture", usage="test", approved=True),
        payload=content,
        provenance="synthetic:m58",
        access="public",
    )


@pytest.mark.integration
def test_authoring_service_reference_e2e_and_idempotent_preview() -> None:
    service = AuthoringService()
    created = service.create_job("job_m58", sources=(_record(),))
    assert created.status == "created"
    started = service.start("job_m58")
    assert started.stage == "drafted"
    assert started.candidate_count > 0
    package = service.build_package("job_m58")
    assert package.manifest.kind == "world"
    first = service.preview("job_m58")
    second = service.preview("job_m58")
    assert first == second
    assert first.scoped_ref.startswith("preview://")


@pytest.mark.integration
def test_studio_api_uses_same_authoring_backend() -> None:
    client: Any = TestClient(create_app())
    response = client.post(
        "/studio/jobs",
        json={
            "job_id": "job_api_m58",
            "sources": [
                {
                    "source_id": "book_api",
                    "kind": "text",
                    "content": BOOK,
                    "stage": "E3",
                    "rights_approved": True,
                    "access": "public",
                }
            ],
        },
    )
    assert response.status_code == 201
    started = client.post("/studio/jobs/job_api_m58/start")
    assert started.status_code == 200
    assert started.json()["stage"] == "drafted"
    draft = client.get("/studio/jobs/job_api_m58/draft")
    assert draft.status_code == 200
    assert draft.json()["draft"]["draft_id"] == "wd_job_api_m58"
    scenarios = client.get("/studio/jobs/job_api_m58/scenarios")
    assert scenarios.status_code == 200
    assert len(scenarios.json()["scenarios"]) == 3
    built = client.post("/studio/jobs/job_api_m58/build")
    assert built.status_code == 200
    preview = client.post("/studio/jobs/job_api_m58/preview")
    assert preview.status_code == 200
    assert preview.json()["scoped_ref"].startswith("preview://")


@pytest.mark.unit
def test_cancel_then_resume_keeps_checkpoint_contract() -> None:
    service = AuthoringService()
    service.create_job("job_resume", sources=(_record("book_resume"),))
    service.start("job_resume")
    # A completed draft is idempotent; cancellation does not erase it.
    cancelled = service.cancel("job_resume")
    assert cancelled.status == "cancelled"
    resumed = service.resume("job_resume")
    assert resumed.stage == "drafted"
    assert resumed.candidate_count > 0


@pytest.mark.unit
def test_scan_pdf_without_provider_is_explicit_ocr_required() -> None:
    service = AuthoringService()
    service.create_job(
        "job_ocr",
        sources=(_record("scan", kind="pdf", content="%PDF-1.7\n/image-only"),),
    )
    with pytest.raises(OcrRequired):
        service.start("job_ocr")
    assert service.status("job_ocr").error.startswith("OcrRequired:")
