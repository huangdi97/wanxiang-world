"""Review/conflict/completion API routes (G58G).

Thin transport over the review core; read-only + propose-only surfaces.
Candidates are never promoted to Canon through these routes.
"""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from wanxiang_substrate.completion.planner import (
    CompletionPlan,
    CompletionPlanner,
    MissingRequirement,
)
from wanxiang_substrate.evidence.binding import EvidenceBindings
from wanxiang_substrate.evidence.conflict import ConflictLedger, ConflictSet
from wanxiang_substrate.review.decisions import ReviewDecision, ReviewLedger

router = APIRouter(prefix="/forge")


class ReviewRequest(BaseModel):
    target_id: str
    action: str
    reviewer: str
    rationale: str
    evidence_refs: list[str] = []


class ReviewDecisionResponse(BaseModel):
    decision_id: str
    target_id: str
    action: str
    reviewer: str
    rationale: str


class ConflictRequest(BaseModel):
    conflict_id: str
    claim_ids: list[str] = Field(min_length=2)
    source_refs: list[str] = []
    description: str


class ConflictResponse(BaseModel):
    conflict_id: str
    claim_ids: list[str]
    source_refs: list[str]
    description: str
    status: str


class RequirementRequest(BaseModel):
    requirement_id: str
    kind: str
    detail: str
    blocking: bool = True


class CompletionPlanResponse(BaseModel):
    plan_id: str
    candidates: list[dict[str, object]]
    unknown: list[dict[str, object]]
    has_blocking_unknown: bool


class EvidenceResponse(BaseModel):
    candidate_id: str
    links: list[dict[str, object]]


@router.post("/reviews", response_model=ReviewDecisionResponse, status_code=201)
def record_review(payload: ReviewRequest, request: Request) -> ReviewDecisionResponse:
    ledger: ReviewLedger = request.app.state.review_ledger
    decision = ledger.record(
        ReviewDecision(
            decision_id=f"rev_{payload.target_id}_{len(ledger.history(payload.target_id)) + 1}",
            target_id=payload.target_id,
            action=payload.action,  # type: ignore[arg-type]
            reviewer=payload.reviewer,
            rationale=payload.rationale,
            evidence_refs=tuple(payload.evidence_refs),
        )
    )
    return ReviewDecisionResponse(
        decision_id=decision.decision_id,
        target_id=decision.target_id,
        action=decision.action,
        reviewer=decision.reviewer,
        rationale=decision.rationale,
    )


@router.get("/reviews/{target_id}", response_model=list[ReviewDecisionResponse])
def review_history(target_id: str, request: Request) -> list[ReviewDecisionResponse]:
    ledger: ReviewLedger = request.app.state.review_ledger
    return [
        ReviewDecisionResponse(
            decision_id=d.decision_id,
            target_id=d.target_id,
            action=d.action,
            reviewer=d.reviewer,
            rationale=d.rationale,
        )
        for d in ledger.history(target_id)
    ]


@router.post("/conflicts", response_model=ConflictResponse, status_code=201)
def register_conflict(payload: ConflictRequest, request: Request) -> ConflictResponse:
    ledger: ConflictLedger = request.app.state.conflict_ledger
    conflict = ledger.register(
        ConflictSet(
            conflict_id=payload.conflict_id,
            claim_ids=tuple(payload.claim_ids),
            source_refs=tuple(payload.source_refs),
            description=payload.description,
        )
    )
    return ConflictResponse(
        conflict_id=conflict.conflict_id,
        claim_ids=list(conflict.claim_ids),
        source_refs=list(conflict.source_refs),
        description=conflict.description,
        status=conflict.status,
    )


@router.get("/conflicts", response_model=list[ConflictResponse])
def list_conflicts(request: Request) -> list[ConflictResponse]:
    ledger: ConflictLedger = request.app.state.conflict_ledger
    return [
        ConflictResponse(
            conflict_id=c.conflict_id,
            claim_ids=list(c.claim_ids),
            source_refs=list(c.source_refs),
            description=c.description,
            status=c.status,
        )
        for c in ledger.all()
    ]


@router.post("/completions/plan", response_model=CompletionPlanResponse)
def build_completion_plan(
    payload: list[RequirementRequest], request: Request
) -> CompletionPlanResponse:
    planner: CompletionPlanner = request.app.state.completion_planner
    requirements = tuple(
        MissingRequirement(
            requirement_id=r.requirement_id,
            kind=r.kind,  # type: ignore[arg-type]
            detail=r.detail,
            blocking=r.blocking,
        )
        for r in payload
    )
    plan: CompletionPlan = planner.plan(requirements)
    return CompletionPlanResponse(
        plan_id=plan.plan_id,
        candidates=[
            {
                "completion_id": c.completion_id,
                "description": c.description,
                "completion_class": c.completion_class,
                "confidence": c.confidence,
                "can_enter_canon": c.can_enter_canon,
            }
            for c in plan.candidates
        ],
        unknown=[
            {"requirement_id": r.requirement_id, "kind": r.kind, "detail": r.detail}
            for r in plan.unknown
        ],
        has_blocking_unknown=plan.has_blocking_unknown,
    )


@router.get("/candidates/{candidate_id}/evidence", response_model=EvidenceResponse)
def candidate_evidence(candidate_id: str, request: Request) -> EvidenceResponse:
    bindings: EvidenceBindings = request.app.state.evidence_bindings
    links = bindings.links_for_candidate(candidate_id)
    return EvidenceResponse(
        candidate_id=candidate_id,
        links=[
            {
                "link_id": link.link_id,
                "locator": link.locator.to_string(),
                "role": link.role,
                "weight": link.weight,
            }
            for link in links
        ],
    )
