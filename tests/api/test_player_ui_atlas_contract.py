"""Conflicting source relations are visible in the Player Atlas, not silent."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_script import SCRIPT


def test_atlas_relation_chips_mark_source_conflicts() -> None:
    assert "is-conflicting" in SCRIPT
    assert "visual-relation-type" in SCRIPT
    assert "visual_relation_conflict" in SCRIPT
    assert "visual_scene_alt" in SCRIPT
    assert "illustrative scene preview, not canonical truth" in player_html("en-US")
    assert "场景示意预览" in player_html("zh-CN")
    html = player_html("zh-CN")
    assert "来源存在不同说法" in html
    assert "is-conflicting" in html


def test_scene_clues_are_a_labelled_list() -> None:
    html = player_html("en-US")

    assert 'id="scene-visual-clues-heading"' in html
    assert 'role="list" aria-labelledby="scene-visual-clues-heading"' in html
    assert 'class="scene-clue" role="listitem"' in SCRIPT


def test_visual_images_describe_their_captions() -> None:
    html = player_html("en-US")

    assert 'aria-describedby="detail-visual-caption"' in html
    assert 'aria-describedby="scene-visual-caption"' in html


def test_world_toolbar_group_has_a_label() -> None:
    english = player_html("en-US")

    assert 'role="group"' in english
    assert 'aria-label="World search and filters"' in english


def test_gallery_thumbnails_are_decorative() -> None:
    assert '<img alt="" src="${safe(item.data_uri)}">' in SCRIPT


def test_world_list_announces_count_without_reading_every_card() -> None:
    html = player_html("en-US")

    assert 'id="world-list-status"' in html
    assert 'id="world-list" aria-live' not in html
    assert 'aria-controls="world-list"' in html
    assert 'data-filter="all" aria-pressed="true"' in html
    assert 'data-filter="recent" aria-pressed="false"' in html
    assert "world_count" in SCRIPT
