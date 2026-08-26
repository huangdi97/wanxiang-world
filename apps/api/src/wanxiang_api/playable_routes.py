"""Playable product routes over the shared PlayableService facade."""

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field
from wanxiang_substrate.playable import PlayableService

router = APIRouter(prefix="/experience")


class CharacterCreateRequest(BaseModel):
    display_name: str
    compatible_profile_ids: list[str] = Field(default_factory=list)
    character_id: str | None = None


class EnterExperienceRequest(BaseModel):
    mode: str = "observer"
    session_id: str
    character_id: str = ""


class ActionRequest(BaseModel):
    text: str = ""
    action_type: str = ""
    payload: dict[str, object] = Field(default_factory=dict)


def _viewer(user: str | None) -> str:
    return user or "anonymous"


def _service(request: Request) -> PlayableService:
    service = request.app.state.playable
    if service is None:
        raise HTTPException(status_code=503, detail="playable runtime is not configured")
    return cast(PlayableService, service)


@router.get("/plaza")
def plaza(
    request: Request, x_wanxiang_user: str | None = Header(default=None)
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    service = _service(request)
    current = service.plaza.continue_last(viewer)
    return {
        "worlds": [card.to_dict() for card in service.plaza.explore_worlds(viewer)],
        "my_worlds": [card.to_dict() for card in service.plaza.my_worlds(viewer)],
        "recent_sessions": [card.to_dict() for card in service.plaza.recent_sessions(viewer)],
        "continue": current.to_dict() if current else None,
    }


@router.get("/worlds")
def worlds(
    request: Request, x_wanxiang_user: str | None = Header(default=None)
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    return {"worlds": [card.to_dict() for card in _service(request).plaza.explore_worlds(viewer)]}


@router.get("/characters")
def characters(
    request: Request, x_wanxiang_user: str | None = Header(default=None)
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    return {
        "characters": [
            {
                "character_id": item.character_id,
                "display_name": item.display_name,
                "compatible_profile_ids": list(item.compatible_profile_ids),
            }
            for item in _service(request).entry.my_characters(viewer)
        ]
    }


@router.post("/characters", status_code=201)
def create_character(
    payload: CharacterCreateRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    character = _service(request).entry.create_character(
        _viewer(x_wanxiang_user),
        payload.display_name,
        compatible_profile_ids=tuple(payload.compatible_profile_ids),
        character_id=payload.character_id,
    )
    return {
        "character_id": character.character_id,
        "display_name": character.display_name,
        "compatible_profile_ids": list(character.compatible_profile_ids),
    }


@router.post("/worlds/{profile_id}/enter")
def enter_world(
    profile_id: str,
    payload: EnterExperienceRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    return _service(request).enter(
        profile_id,
        viewer_id=_viewer(x_wanxiang_user),
        mode=payload.mode,
        session_id=payload.session_id,
        character_id=payload.character_id,
    )


@router.get("/instances/{instance_id}")
def observe_instance(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    return _service(request).observe(instance_id, _viewer(x_wanxiang_user))


@router.post("/instances/{instance_id}/action")
def action_instance(
    instance_id: str,
    payload: ActionRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    return (
        _service(request)
        .action(
            instance_id,
            viewer_id=_viewer(x_wanxiang_user),
            text=payload.text,
            action_type=payload.action_type,
            payload=payload.payload,
        )
        .to_dict()
    )


@router.post("/instances/{instance_id}/leave")
def leave_instance(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    return _service(request).leave(instance_id, viewer_id=_viewer(x_wanxiang_user))


@router.post("/instances/{instance_id}/continue")
def continue_instance(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
) -> dict[str, object]:
    return _service(request).continue_instance(instance_id, viewer_id=_viewer(x_wanxiang_user))
