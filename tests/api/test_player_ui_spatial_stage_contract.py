"""The Player exposes one renderer-neutral Stage for verified spatial assets."""

from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_panorama_builtin import BUILTIN_PANORAMA_RENDERER_SCRIPT
from wanxiang_api.player_ui_panorama_renderer import PANORAMA_RENDERER_SCRIPT
from wanxiang_api.player_ui_script import SCRIPT
from wanxiang_api.player_ui_spatial_builtin import BUILTIN_SPATIAL_RENDERER_SCRIPT
from wanxiang_api.player_ui_spatial_renderer import SPATIAL_RENDERER_SCRIPT


def test_player_html_exposes_optional_spatial_stage_without_vendor_dependency() -> None:
    html = player_html("zh-CN")

    assert 'id="world-stage-spatial"' in html
    assert 'id="spatial-stage-toggle"' in html
    assert "__WANXIANG_SPATIAL_RENDERER__" in html
    assert "__WANXIANG_SPATIAL_STAGE__" in html
    assert "/spatial-assets/" in html
    assert "loadAsset" in SPATIAL_RENDERER_SCRIPT
    assert "projectionFrame" in SPATIAL_RENDERER_SCRIPT
    assert "asset_revision" in SPATIAL_RENDERER_SCRIPT
    assert "supportsScene" in SPATIAL_RENDERER_SCRIPT
    assert "assetDescriptors" in SPATIAL_RENDERER_SCRIPT
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


def test_player_spatial_generation_auto_polls_across_detail_and_live_world() -> None:
    assert "SPATIAL_POLL_MIN_MS=5000" in SCRIPT
    assert "SPATIAL_POLL_MAX_MS=30000" in SCRIPT
    assert "scheduleSpatialAutoPoll" in SCRIPT
    assert "refreshSpatialJobs(true)" in SCRIPT
    assert 'document.querySelector("#detail-view.is-active,#play-view.is-active")' in SCRIPT
    assert 'if(name!=="detail-view"&&name!=="play-view")stopSpatialAutoPoll()' in SCRIPT
    assert "syncLiveSpatialProjection" in SCRIPT
    assert "applySpatialWorldProjection" in SCRIPT
    assert 'else if(document.querySelector("#play-view.is-active"))renderPlay()' in SCRIPT
    assert 'model.view.visual_scene={...live,spatial:refreshed.spatial||null}' in SCRIPT
    assert "Math.round(delay*1.6)" in SCRIPT
    assert '"submission_ambiguous"' in SCRIPT
    assert 'tr("spatial_upgrade_ambiguous",{place})' in SCRIPT
    assert 'tr("spatial_budget_summary"' in SCRIPT
    assert "provider_usage_units" in SCRIPT
    zh = player_html("zh-CN")
    en = player_html("en-US")
    assert "重复付费" in zh
    assert "世界空间预算" in zh
    assert "Provider 实报" in zh
    assert "duplicate billing" in en
    assert "World spatial budget" in en
    assert "provider reported" in en
    assert "格式或图形能力不兼容" in zh
    assert "graphics capability mismatch" in en


def test_player_bundles_dependency_free_ply_spatial_renderer() -> None:
    html = player_html("zh-CN")

    assert '"model/ply"' in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "const available=()" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert '"WEBGL_lose_context"' in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "r.available()" in SPATIAL_RENDERER_SCRIPT
    assert "supportsAssets" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "size_bytes" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "for(const i of indices)" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert '"application/x-ply"' in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert 'getContext("webgl"' in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "binary_little_endian" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "DataView" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "MAX_POINTS=120000" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "pointermove" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "ResizeObserver" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "spatial_stage_reset" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "spatial_stage_controls_hint" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "projectionFrame" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "frameTransform" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "lastError" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "catch(error){lastError=error}" in BUILTIN_SPATIAL_RENDERER_SCRIPT
    assert "three.js" not in BUILTIN_SPATIAL_RENDERER_SCRIPT.casefold()
    assert "tokenhub" not in BUILTIN_SPATIAL_RENDERER_SCRIPT.casefold()
    assert html.index(BUILTIN_SPATIAL_RENDERER_SCRIPT) < html.index(SPATIAL_RENDERER_SCRIPT)
