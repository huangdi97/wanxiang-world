"""Mobile Stage keeps 44px touch targets and respects the bottom safe area."""

from __future__ import annotations

from wanxiang_api.player_ui_style import STYLE


def test_mobile_stage_uses_44px_touch_targets_and_safe_area() -> None:
    assert "min-height:44px" in STYLE
    assert "env(safe-area-inset-bottom)" in STYLE
    assert ".visual-place" in STYLE
    assert "#observer-scene-list button" in STYLE


def test_player_html_links_the_mobile_style() -> None:
    from wanxiang_api.player_ui_asset import player_html

    html = player_html("zh-CN")
    assert "safe-area-inset-bottom" in html
