"""Character creation offers an explicit source-role choice, defaulting to auto."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_script import SCRIPT
from wanxiang_substrate.playable.player_i18n import _copy_for


def test_character_form_exposes_the_source_cast_selector() -> None:
    html = player_html("zh-CN")

    assert 'id="character-actor"' in html
    assert "自动匹配来源角色" in html
    assert "function renderCast(" in SCRIPT
    assert 'character_id:values("character-actor")' in SCRIPT
    assert "function renderCast(" in html


def test_english_copy_names_the_source_role_choice() -> None:
    html = player_html("en-US")

    assert "Source role (optional)" in html
    assert "Auto-bind a source role" in html
    assert _copy_for("en-US").text("cast_label") == "Source role (optional)"
