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
    # The rest suggestion must use the same parseable shape as the others. The old
    # "让自己休息" phrasing was refused by the action contract with
    # missing_fields:entity_id,status, so it must never come back.
    assert "让自己保持休息" in chinese
    assert 'data-action="让自己休息"' not in chinese


def test_chinese_action_suggestions_share_the_parseable_shape() -> None:
    """Guard the shape that made every suggestion commit, not just looks Chinese."""

    from wanxiang_substrate.playable.player_i18n import _copy_for

    zh = _copy_for("zh-CN")
    values = [
        zh.text(key) for key in ("action_awake_value", "action_alert_value", "action_rest_value")
    ]
    assert all(value.startswith("让自己保持") for value in values), values
    en = _copy_for("en-US")
    assert en.text("action_rest_value") == "set status to resting"


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


def test_builtin_stage_renderers_take_copy_from_the_catalog_only() -> None:
    """A missing stage key must stay visible, never silently replaced by English.

    Measured 2026-11-13: the spatial built-in carried English literals for three keys
    (`spatial_stage_point_count`, `spatial_stage_controls_hint`, `spatial_stage_reset`,
    the last one twice) and the panorama built-in for `panorama_stage_aria` (twice), so
    a renamed catalog key would have shown English inside the zh-CN player. All four
    keys do exist in both catalogs, so this pins that they keep existing and that no
    literal fallback argument comes back.
    """

    from wanxiang_api.player_ui_panorama_builtin import BUILTIN_PANORAMA_RENDERER_SCRIPT
    from wanxiang_api.player_ui_spatial_builtin import BUILTIN_SPATIAL_RENDERER_SCRIPT
    from wanxiang_substrate.playable.player_i18n import _copy_for

    catalogs = {locale: _copy_for(locale) for locale in ("zh-CN", "en-US")}
    used = 0
    for name, source in (
        ("spatial", BUILTIN_SPATIAL_RENDERER_SCRIPT),
        ("panorama", BUILTIN_PANORAMA_RENDERER_SCRIPT),
    ):
        assert "copy=(key,values={})" in source, f"{name} builtin changed its copy helper"
        assert source.index("copy=(key,values={})") < source.index('copy("'), (
            f"{name} builtin uses copy() before defining it"
        )
        literal = re.search(r'copy\("[a-z0-9_]+",\s*["\']', source)
        assert literal is None, f"{name} builtin hardcodes a fallback: {literal.group(0)}"
        keys = set(re.findall(r'copy\("([a-z0-9_]+)"', source))
        assert keys, f"{name} builtin no longer reads the copy catalog"
        used += len(keys)
        for key in keys:
            for locale, copy in catalogs.items():
                assert copy.text(key) != key, f"{name} builtin uses {key!r}, missing in {locale}"
            placeholders = {
                locale: re.findall(r"\{(\w+)\}", copy.text(key))
                for locale, copy in catalogs.items()
            }
            assert placeholders["zh-CN"] == placeholders["en-US"], (
                f"{key} placeholders differ between locales: {placeholders}"
            )
    assert used >= 4, "the stage renderers must still label their controls from the catalog"
