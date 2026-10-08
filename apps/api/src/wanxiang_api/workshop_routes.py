"""World Workshop transport routes over the shared substrate service."""

from __future__ import annotations

from typing import Literal, cast

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.models import PlayableWorldProfile, Visibility
from wanxiang_substrate.workshop import CreatorIntent, WorkshopBuild, WorkshopService

from wanxiang_api.authoring_sources import SourceInput, source_records

router = APIRouter(prefix="/workshop")


class WorkshopIntentInput(BaseModel):
    intent_id: str
    author_id: str
    text: str
    source_channel: Literal["creator_intent"] = "creator_intent"

    def intent(self) -> CreatorIntent:
        return CreatorIntent(
            self.intent_id,
            self.author_id,
            self.text,
            source_channel=self.source_channel,
        )


class SourceWorkshopRequest(BaseModel):
    workshop_id: str
    owner_id: str
    sources: list[SourceInput] = Field(default_factory=lambda: list[SourceInput]())
    profile: str = "book"
    visibility: Visibility = "private"
    display_name: str | None = None
    semantic_provider: str | None = None


class PromptWorkshopRequest(BaseModel):
    workshop_id: str
    owner_id: str
    intent: WorkshopIntentInput
    visibility: Visibility = "private"
    display_name: str | None = None


class HybridWorkshopRequest(PromptWorkshopRequest):
    sources: list[SourceInput] = Field(default_factory=lambda: list[SourceInput]())
    profile: str = "book"
    semantic_provider: str | None = None


class WorkshopReviewRequest(BaseModel):
    action: str


def _service(request: Request) -> WorkshopService:
    return cast(WorkshopService, request.app.state.workshop)


def _playable(request: Request) -> PlayableService | None:
    service = request.app.state.playable
    return cast(PlayableService | None, service)


def _register_if_publishable(request: Request, build: WorkshopBuild) -> PlayableWorldProfile | None:
    if not build.publishing.publishable:
        return None
    playable = _playable(request)
    experience = build.workshop.experience
    if playable is None or experience is None:
        return None
    return playable.register_package(
        build.package,
        owner_id=experience.owner_id,
        visibility=experience.visibility,
        display_name=experience.display_name,
    )


def _build_response(request: Request, build: WorkshopBuild) -> dict[str, object]:
    response = build.to_dict()
    response["evidence_audit"] = _service(request).evidence_audit(build.workshop.workshop_id)
    profile = _register_if_publishable(request, build)
    if profile is not None:
        response["playable_profile"] = profile.to_dict()
    return response


@router.get("")
def workshop_home(request: Request) -> dict[str, object]:
    return _service(request).home().to_dict()


@router.post("/from-source", status_code=201)
def create_from_source(payload: SourceWorkshopRequest, request: Request) -> dict[str, object]:
    service = _service(request)
    build = service.create_from_source(
        payload.workshop_id,
        owner_id=payload.owner_id,
        sources=source_records(service.authoring, payload.sources),
        profile=payload.profile,
        visibility=payload.visibility,
        display_name=payload.display_name,
        semantic_provider=payload.semantic_provider,
    )
    return _build_response(request, build)


@router.post("/from-prompt", status_code=201)
def create_from_prompt(payload: PromptWorkshopRequest, request: Request) -> dict[str, object]:
    build = _service(request).create_from_prompt(
        payload.workshop_id,
        owner_id=payload.owner_id,
        intent=payload.intent.intent(),
        visibility=payload.visibility,
        display_name=payload.display_name,
    )
    return _build_response(request, build)


@router.post("/from-hybrid", status_code=201)
def create_hybrid(payload: HybridWorkshopRequest, request: Request) -> dict[str, object]:
    service = _service(request)
    build = service.create_hybrid(
        payload.workshop_id,
        owner_id=payload.owner_id,
        sources=source_records(service.authoring, payload.sources),
        intent=payload.intent.intent(),
        profile=payload.profile,
        visibility=payload.visibility,
        display_name=payload.display_name,
        semantic_provider=payload.semantic_provider,
    )
    return _build_response(request, build)


@router.get("/{workshop_id}")
def get_workshop(workshop_id: str, request: Request) -> dict[str, object]:
    return _build_response(request, _service(request).get(workshop_id))


@router.get("/{workshop_id}/evidence")
def workshop_evidence(workshop_id: str, request: Request) -> dict[str, object]:
    return _service(request).evidence_audit(workshop_id)


@router.post("/{workshop_id}/review")
def review_workshop(
    workshop_id: str, payload: WorkshopReviewRequest, request: Request
) -> dict[str, object]:
    build = _service(request).accept_prompt_review(workshop_id, payload.action)
    return _build_response(request, build)


__all__ = ["router"]
