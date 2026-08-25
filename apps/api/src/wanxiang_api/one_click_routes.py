"""Studio one-click source-to-living-world route."""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.service import AuthoringService

from wanxiang_api.authoring_sources import SourceInput, source_records

router = APIRouter(prefix="/studio")


class OneClickRequest(BaseModel):
    job_id: str
    profile: str = "mixed"
    sources: list[SourceInput] = Field(default_factory=lambda: list[SourceInput]())
    semantic_provider: str | None = None


def _service(request: Request) -> AuthoringService:
    return request.app.state.authoring


@router.post("/one-click", status_code=201)
def one_click(payload: OneClickRequest, request: Request) -> dict[str, object]:
    service = _service(request)
    result = OneClickAuthoring(service).run(
        payload.job_id,
        source_records(service, payload.sources),
        profile=payload.profile,
        semantic_provider=payload.semantic_provider,
    )
    validation = service.package_validation(result.job_id)
    return {
        "job_id": result.job_id,
        "profile": result.source_profile,
        "package_id": result.package.package_id,
        "manifest_hash": result.package.manifest.content_hash,
        "preview_id": result.preview.preview_id,
        "preview_ref": result.preview.scoped_ref,
        "publishable": validation.publish_ok,
        "publish_reasons": list(validation.reasons),
        "status": service.status(result.job_id).to_dict(),
    }


@router.post("/jobs/{job_id}/publish")
def publish_job(job_id: str, request: Request) -> dict[str, object]:
    service = _service(request)
    validation = service.publish(job_id)
    return {
        "job_id": job_id,
        "publishable": validation.publish_ok,
        "reasons": list(validation.reasons),
        "status": service.status(job_id).to_dict(),
    }
