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


def test_english_player_html_has_no_cjk_punctuation() -> None:
    """English chrome must not borrow Chinese punctuation either."""

    english = player_html("en-US")

    leaked = sorted(set(re.findall(r"[\u3000-\u303f\uff00-\uffef]", english)))
    assert leaked == [], f"CJK punctuation leaked into en-US: {leaked}"


def test_player_scripts_keep_punctuation_in_the_catalog() -> None:
    """Labels, separators and fallbacks come from the copy catalog, not literals."""

    from wanxiang_api.player_ui_home_script import HOME_SCRIPT
    from wanxiang_api.player_ui_replay_script import REPLAY_SCRIPT
    from wanxiang_api.player_ui_script import SCRIPT
    from wanxiang_api.player_ui_worldline_script import WORLDLINE_SCRIPT

    for name, source in (
        ("SCRIPT", SCRIPT),
        ("HOME_SCRIPT", HOME_SCRIPT),
        ("REPLAY_SCRIPT", REPLAY_SCRIPT),
        ("WORLDLINE_SCRIPT", WORLDLINE_SCRIPT),
    ):
        leaked = sorted(set(re.findall(r"[\u3000-\u303f\uff00-\uffef]", source)))
        assert leaked == [], f"{name} still hardcodes CJK punctuation: {leaked}"


def test_locale_catalog_exposes_separators_and_panorama_aria() -> None:
    from wanxiang_substrate.playable.player_i18n import _copy_for

    zh = _copy_for("zh-CN")
    en = _copy_for("en-US")

    assert zh.text("list_separator") == "\u3001"
    assert zh.text("label_separator") == "\uff1a"
    assert en.text("list_separator") == ", "
    assert en.text("label_separator") == ": "
    assert zh.text("panorama_stage_aria") != en.text("panorama_stage_aria")
    assert re.search(r"[\u4e00-\u9fff]", en.text("panorama_stage_aria")) is None


def test_atlas_relation_chips_label_the_source_relation() -> None:
    """The atlas must not print a raw source relation type at the player."""

    from wanxiang_api.player_ui_script import SCRIPT

    assert "atlasRelationLabel(item.relation_type)" in SCRIPT
    assert "${safe(item.relation_type)}" not in SCRIPT
