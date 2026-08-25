"""Studio authoring routes over the shared substrate service (G61A-G)."""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from wanxiang_substrate.authoring.scenario_engine import ScenarioEngine
from wanxiang_substrate.authoring.service import AuthoringService

from wanxiang_api.authoring_sources import SourceInput, source_records
from wanxiang_api.candidate_serializers import candidate_to_dict

router = APIRouter(prefix="/studio")


class CreateJobRequest(BaseModel):
    job_id: str
    version: str = "1"
    sources: list[SourceInput] = Field(default_factory=lambda: list[SourceInput]())
    created_by: str = "studio"
    semantic_provider: str | None = None


class ReviewCandidateRequest(BaseModel):
    action: str
    reviewer: str
    rationale: str


class BatchReviewRequest(BaseModel):
    candidate_ids: list[str] = Field(default_factory=list)
    action: str
    reviewer: str
    rationale: str


def _service(request: Request) -> AuthoringService:
    return request.app.state.authoring


@router.post("/jobs", status_code=201)
def create_job(payload: CreateJobRequest, request: Request) -> dict[str, object]:
    snapshot = _service(request).create_job(
        payload.job_id,
        version=payload.version,
        sources=source_records(_service(request), payload.sources),
        created_by=payload.created_by,
        semantic_provider=payload.semantic_provider,
    )
    return snapshot.to_dict()


@router.post("/jobs/{job_id}/sources")
def add_source(job_id: str, payload: SourceInput, request: Request) -> dict[str, object]:
    service = _service(request)
    return service.add_source(job_id, source_records(service, [payload])[0]).to_dict()


@router.post("/jobs/{job_id}/start")
def start_job(job_id: str, request: Request) -> dict[str, object]:
    return _service(request).start(job_id).to_dict()


@router.post("/jobs/{job_id}/resume")
def resume_job(job_id: str, request: Request) -> dict[str, object]:
    return _service(request).resume(job_id).to_dict()


@router.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: str, request: Request) -> dict[str, object]:
    return _service(request).cancel(job_id).to_dict()


@router.get("/jobs/{job_id}")
def get_job(job_id: str, request: Request) -> dict[str, object]:
    return _service(request).status(job_id).to_dict()


@router.get("/jobs/{job_id}/draft")
def get_draft(job_id: str, request: Request) -> dict[str, object]:
    build = _service(request).build(job_id)
    if build is None:
        return {"job_id": job_id, "draft": None, "candidates": []}
    draft = build.draft
    return {
        "job_id": job_id,
        "draft": {
            "draft_id": draft.draft_id,
            "revision": draft.revision,
            "status": draft.status,
            "source_refs": list(draft.source_refs),
            "source_versions": [list(item) for item in draft.source_versions],
            "selected_domains": list(draft.selected_domains),
            "entities": [list(item) for item in draft.entities],
            "relations": [list(item) for item in draft.relations],
            "places": list(draft.places),
            "events": [list(item) for item in draft.events],
            "completion_items": list(draft.completion_items),
            "unresolved_conflicts": list(draft.unresolved_conflicts),
            "unresolved_rights": list(draft.unresolved_rights),
            "coverage": draft.coverage,
            "uncertainty": draft.uncertainty,
        },
        "candidates": [candidate_to_dict(candidate) for candidate in build.candidates],
    }


@router.get("/jobs/{job_id}/scenarios")
def get_scenarios(job_id: str, request: Request) -> dict[str, object]:
    build = _service(request).build(job_id)
    if build is None:
        return {"job_id": job_id, "scenarios": []}
    plans = ScenarioEngine().build_three(build.draft)
    return {
        "job_id": job_id,
        "scenarios": [
            {
                "genesis_id": plan.genesis_id,
                "scenario_id": plan.scenario.scenario_id,
                "canon_mode": plan.scenario.canon_mode,
                "snapshot_hash": plan.snapshot_hash,
                "seed": plan.scenario.seed,
            }
            for plan in plans
        ],
    }


@router.post("/jobs/{job_id}/build")
def build_package(job_id: str, request: Request) -> dict[str, object]:
    package = _service(request).build_package(job_id)
    return {
        "package_id": package.package_id,
        "manifest_hash": package.manifest.content_hash,
        "draft_id": package.draft_id,
        "draft_revision": package.draft_revision,
        "preview_allowed": package.for_preview,
        "publishable": not package.unresolved_gaps and package.rights_ok,
    }


@router.post("/jobs/{job_id}/preview")
def preview_package(job_id: str, request: Request) -> dict[str, object]:
    install = _service(request).preview(job_id)
    return {
        "preview_id": install.preview_id,
        "scoped_ref": install.scoped_ref,
        "package_id": install.package_id,
        "draft_id": install.draft_id,
        "package_hash": install.package_hash,
    }


@router.post("/jobs/{job_id}/candidates/{candidate_id}/review", status_code=201)
def review_candidate(
    job_id: str,
    candidate_id: str,
    payload: ReviewCandidateRequest,
    request: Request,
) -> dict[str, object]:
    decision = _service(request).review_candidate(
        job_id,
        candidate_id,
        action=payload.action,
        reviewer=payload.reviewer,
        rationale=payload.rationale,
    )
    return {
        "decision_id": decision.decision_id,
        "target_id": decision.target_id,
        "action": decision.action,
        "reviewer": decision.reviewer,
        "rationale": decision.rationale,
    }


@router.get("/jobs/{job_id}/review-inbox")
def review_inbox(job_id: str, request: Request) -> dict[str, object]:
    items = _service(request).review_inbox(job_id)
    return {
        "job_id": job_id,
        "items": [
            {
                "candidate_id": item.candidate.candidate_id,
                "kind": item.candidate.kind,
                "confidence": item.candidate.confidence,
                "impact": item.impact.score,
                "reasons": list(item.impact.reasons),
                "auto_approved": item.auto_approved,
                "needs_human_review": item.needs_human_review,
                "preview": {
                    "entities": list(item.preview.entities) if item.preview else [],
                    "events": list(item.preview.events) if item.preview else [],
                    "scenarios": list(item.preview.scenarios) if item.preview else [],
                    "package_sections": list(item.preview.package_sections) if item.preview else [],
                    "preview_hash": item.preview.preview_hash if item.preview else "",
                },
            }
            for item in items
        ],
    }


@router.post("/jobs/{job_id}/review-inbox/batch", status_code=201)
def batch_review(job_id: str, payload: BatchReviewRequest, request: Request) -> dict[str, object]:
    decisions = _service(request).review_inbox_batch(
        job_id,
        tuple(payload.candidate_ids),
        action=payload.action,
        reviewer=payload.reviewer,
        rationale=payload.rationale,
    )
    return {
        "job_id": job_id,
        "decisions": [
            {
                "decision_id": decision.decision_id,
                "target_id": decision.target_id,
                "action": decision.action,
                "reviewer": decision.reviewer,
            }
            for decision in decisions
        ],
    }


@router.get("/jobs/{job_id}/review-inbox/audit")
def review_audit(job_id: str, request: Request) -> dict[str, object]:
    audits = _service(request).review_audit(job_id)
    return {
        "job_id": job_id,
        "audits": [
            {
                "audit_id": audit.audit_id,
                "decision_id": audit.decision_id,
                "target_id": audit.target_id,
                "actor_type": audit.actor_type,
                "actor_id": audit.actor_id,
                "rationale": audit.rationale,
                "impact_score": audit.impact_score,
                "source_refs": list(audit.source_refs),
            }
            for audit in audits
        ],
    }
