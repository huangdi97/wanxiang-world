"""The default browser entry for ordinary players."""

# pyright: reportPrivateUsage=false

import wanxiang_substrate.playable.player_i18n as _player_i18n
from fastapi import APIRouter, Header
from fastapi.responses import HTMLResponse

from wanxiang_api.immersive_player_ui import immersive_player_html
from wanxiang_api.player_ui_asset import player_html

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
@router.get("/experience/ui", response_class=HTMLResponse)
@router.get("/player", response_class=HTMLResponse)
def player_ui(
    locale: str | None = None,
    x_wanxiang_locale: str | None = Header(default=None),
) -> HTMLResponse:
    requested = locale if locale is not None else x_wanxiang_locale
    return HTMLResponse(
        player_html(_player_i18n._normalize_locale(requested)),
        headers={"Cache-Control": "no-store"},
    )


@router.get("/experience/visual", response_class=HTMLResponse, include_in_schema=False)
def immersive_player_ui() -> HTMLResponse:
    """Optional WebGL experiment; never substitutes for M95/Stable acceptance."""
    return HTMLResponse(immersive_player_html(), headers={"Cache-Control": "no-store"})
