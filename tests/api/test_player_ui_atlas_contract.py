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


def test_visual_images_describe_their_captions() -> None:
    html = player_html("en-US")

    assert 'aria-describedby="detail-visual-caption"' in html
    assert 'aria-describedby="scene-visual-caption"' in html


def test_gallery_thumbnails_are_decorative() -> None:
    assert '<img alt="" src="${safe(item.data_uri)}">' in SCRIPT
