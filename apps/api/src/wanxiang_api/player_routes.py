"""Player-only JSON projections over the shared playable service."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import cast

import wanxiang_substrate.playable.player_i18n as _player_i18n
from fastapi import APIRouter, Header, HTTPException, Request
from wanxiang_substrate.playable import (
    CharacterRecord,
    PlayableService,
    SessionCard,
    WorldCard,
)
from wanxiang_substrate.playable.player_service import player_observe, player_world

from wanxiang_api.playable_routes import (
    ActionRequest,
    CharacterCreateRequest,
    EnterExperienceRequest,
)
from wanxiang_api.player_spatial_recovery import rehydrate_spatial_attachments

router = APIRouter(prefix="/experience/player")


def _viewer(user: str | None) -> str:
    return user or "anonymous"


def _locale(value: str | None) -> str:
    return _player_i18n._normalize_locale(value)


def _service(request: Request) -> PlayableService:
    service = request.app.state.playable
    if service is None:
        raise HTTPException(status_code=503, detail="playable runtime is not configured")
    return cast(PlayableService, service)


def _character(character: CharacterRecord) -> dict[str, object]:
    return {
        "character_id": character.character_id,
        "name": character.display_name,
        "identity": character.identity,
        "intro": character.intro,
        "stance": character.stance,
        "starting_location": character.starting_location,
        "knowledge_boundary": character.knowledge_boundary,
        "compatible_profile_ids": list(character.compatible_profile_ids),
    }


@router.get("/plaza")
def player_plaza(
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    service = _service(request)
    cards = service.plaza.explore_worlds(viewer)
    mine = service.plaza.my_worlds(viewer)
    recent = service.plaza.recent_sessions(viewer)
    current = service.plaza.continue_last(viewer)
    recent_ids = {item.profile_id for item in recent}

    def world_cards(items: tuple[WorldCard, ...]) -> list[dict[str, object]]:
        mine_ids = {owned.profile_id for owned in mine}

        def project(item: WorldCard) -> dict[str, object]:
            result = player_world(service, item.profile_id, viewer_id=viewer, locale=locale)
            can_continue = item.profile_id in recent_ids
            result.update(
                {
                    "is_public": item.visibility == "public",
                    "is_owned": item.profile_id in mine_ids,
                    "can_continue": can_continue,
                }
            )
            if can_continue:
                result["status"] = _player_i18n._copy_for(locale).text("card_continue")
            return result

        return [project(item) for item in items]

    def session_card(session: SessionCard) -> dict[str, object]:
        view = player_observe(service, session.instance_id, viewer, locale=locale)
        summary = cast(dict[str, object], view["session"])
        return {
            "instance_id": session.instance_id,
            "profile_id": session.profile_id,
            **summary,
        }

    return {
        "locale": locale,
        "worlds": world_cards(cards),
        "my_worlds": world_cards(mine),
        "recent_sessions": [session_card(item) for item in recent],
        "continue": session_card(current) if current else None,
    }


@router.get("/worlds/{profile_id}")
def player_world_detail(
    profile_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    service = _service(request)
    rehydrate_spatial_attachments(request, service, profile_id, viewer_id=viewer)
    world = player_world(
        service,
        profile_id,
        viewer_id=viewer,
        locale=locale,
        include_visual=True,
    )
    characters = [
        _character(item)
        for item in service.entry.my_characters(viewer)
        if item.compatible_with(profile_id)
    ]
    return {"locale": locale, "world": world, "characters": characters}


@router.get("/characters")
def player_characters(
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    return {
        "locale": _locale(x_wanxiang_locale),
        "characters": [_character(item) for item in _service(request).entry.my_characters(viewer)],
    }


@router.post("/characters", status_code=201)
def create_player_character(
    payload: CharacterCreateRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    character = _service(request).entry.create_character(
        viewer,
        payload.display_name,
        compatible_profile_ids=tuple(payload.compatible_profile_ids),
        character_id=payload.character_id,
        identity=payload.identity,
        intro=payload.intro,
        stance=payload.stance,
        starting_location=payload.starting_location,
        knowledge_boundary=payload.knowledge_boundary,
    )
    return {"locale": _locale(x_wanxiang_locale), "character": _character(character)}


@router.post("/worlds/{profile_id}/enter")
def player_enter_world(
    profile_id: str,
    payload: EnterExperienceRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    service = _service(request)
    rehydrate_spatial_attachments(request, service, profile_id, viewer_id=viewer)
    entered = service.enter(
        profile_id,
        viewer_id=viewer,
        mode=payload.mode,
        session_id=payload.session_id,
        character_id=payload.character_id,
    )
    instance = cast(dict[str, object], entered["instance"])
    instance_id = str(instance["instance_id"])
    return {
        "locale": locale,
        "instance_id": instance_id,
        "view": player_observe(service, instance_id, viewer, locale=locale),
    }


@router.get("/instances/{instance_id}")
def player_observe_instance(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    return {
        "locale": locale,
        "instance_id": instance_id,
        "view": player_observe(_service(request), instance_id, viewer, locale=locale),
    }


@router.get("/instances/{instance_id}/replay")
def player_replay_instance(
    instance_id: str,
    at_ticks: int,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    """Return a read-only projection of the instance at a past world tick."""
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    try:
        view = _service(request).replay_at(
            instance_id,
            viewer_id=viewer,
            at_ticks=at_ticks,
            locale=locale,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "locale": locale,
        "instance_id": instance_id,
        "replay": view.get("replay"),
        "view": view,
    }


@router.post("/instances/{instance_id}/action")
def player_action_instance(
    instance_id: str,
    payload: ActionRequest,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    service = _service(request)
    result = service.action(
        instance_id,
        viewer_id=viewer,
        text=payload.text,
        action_type=payload.action_type,
        payload=payload.payload,
    )
    return {
        "locale": locale,
        "instance_id": instance_id,
        "status": "committed",
        "changed": not result.diff.no_change,
        "view": player_observe(service, instance_id, viewer, diff=result.diff, locale=locale),
    }


@router.post("/instances/{instance_id}/leave")
def player_leave_instance(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    service = _service(request)
    result = service.leave(instance_id, viewer_id=_viewer(x_wanxiang_user))
    return {
        "locale": _locale(x_wanxiang_locale),
        "instance_id": instance_id,
        "status": result["status"],
    }


@router.post("/instances/{instance_id}/continue")
def player_continue_instance(
    instance_id: str,
    request: Request,
    x_wanxiang_user: str | None = Header(default=None),
    x_wanxiang_locale: str | None = Header(default=None),
) -> dict[str, object]:
    viewer = _viewer(x_wanxiang_user)
    locale = _locale(x_wanxiang_locale)
    service = _service(request)
    service.continue_instance(instance_id, viewer_id=viewer)
    return {
        "locale": locale,
        "instance_id": instance_id,
        "view": player_observe(service, instance_id, viewer, locale=locale),
    }
