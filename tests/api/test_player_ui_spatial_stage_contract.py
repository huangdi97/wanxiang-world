"""The Player exposes one renderer-neutral Stage for verified spatial assets."""

from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_panorama_builtin import BUILTIN_PANORAMA_RENDERER_SCRIPT
from wanxiang_api.player_ui_panorama_renderer import PANORAMA_RENDERER_SCRIPT
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


def test_player_html_exposes_optional_panorama_stage_without_vendor_dependency() -> None:
    html = player_html("zh-CN")

    assert 'id="world-stage-panorama"' in html
    assert 'id="panorama-stage-toggle"' in html
    assert "__WANXIANG_PANORAMA_RENDERER__" in html
    assert "__WANXIANG_PANORAMA_STAGE__" in html
    assert "dataUri" in html
    assert "pannellum" not in html.casefold()
    assert "marzipano" not in html.casefold()


def test_player_bundles_dependency_free_interactive_panorama_renderer() -> None:
    html = player_html("zh-CN")

    assert 'getContext("webgl"' in BUILTIN_PANORAMA_RENDERER_SCRIPT
    assert "pointermove" in BUILTIN_PANORAMA_RENDERER_SCRIPT
    assert "ArrowLeft" in BUILTIN_PANORAMA_RENDERER_SCRIPT
    assert "ResizeObserver" in BUILTIN_PANORAMA_RENDERER_SCRIPT
    assert "TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE" in BUILTIN_PANORAMA_RENDERER_SCRIPT
    assert "window.__WANXIANG_PANORAMA_RENDERER__={supports:" in BUILTIN_PANORAMA_RENDERER_SCRIPT
    assert html.index(BUILTIN_PANORAMA_RENDERER_SCRIPT) < html.index(PANORAMA_RENDERER_SCRIPT)
