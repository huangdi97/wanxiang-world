"""English action suggestions send English intent, not Chinese commands."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import re

from wanxiang_api.player_ui_asset import player_html


def test_english_ui_suggestions_send_english_action_text() -> None:
    english = player_html("en-US")

    assert 'data-action="set status to awake"' in english
    assert 'data-action="set status to alert"' in english
    assert 'data-action="set status to resting"' in english
    assert "让自己保持清醒" not in english
    assert "让自己休息" not in english


def test_english_player_html_has_no_chinese_copy() -> None:
    english = player_html("en-US")

    assert re.search(r"[\u4e00-\u9fff]", english) is None


def test_chinese_ui_keeps_chinese_action_text() -> None:
    chinese = player_html("zh-CN")

    assert "让自己保持清醒" in chinese
    assert "让自己休息" in chinese
