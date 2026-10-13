"""The Player exposes one renderer-neutral Stage for verified spatial assets."""

from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_spatial_renderer import SPATIAL_RENDERER_SCRIPT


def test_player_html_exposes_optional_spatial_stage_without_vendor_dependency() -> None:
    html = player_html("zh-CN")

    assert 'id="world-stage-spatial"' in html
    assert 'id="spatial-stage-toggle"' in html
    assert "__WANXIANG_SPATIAL_RENDERER__" in html
    assert "__WANXIANG_SPATIAL_STAGE__" in html
    assert "/spatial-assets/" in html
    assert "loadAsset" in SPATIAL_RENDERER_SCRIPT
    assert "three.js" not in SPATIAL_RENDERER_SCRIPT.casefold()
    assert "worldlabs" not in SPATIAL_RENDERER_SCRIPT.casefold()
    assert "hunyuan" not in SPATIAL_RENDERER_SCRIPT.casefold()
