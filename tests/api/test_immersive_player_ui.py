"""Guard opt-in visual player boundaries; not M95 human evidence."""

from wanxiang_api.immersive_player_ui import immersive_player_html
from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_routes import router


def test_experimental_visual_page_has_real_3d_canvas_and_authoritative_api_path() -> None:
    html = immersive_player_html()
    assert '<canvas id="scene"' in html
    assert "babylonjs/7.54.3/babylon.js" in html
    assert "new B.Engine(canvas" in html
    assert "new B.UniversalCamera(" in html
    assert "new B.ArcRotateCamera(" in html
    assert "window.localStorage" not in html
    assert "/experience/player/instances/" in html
    assert "此世界暂未制作专属空间场景" in html
    assert "示意场景" in html
    assert "WorldSceneManifest" in html
    assert "Commit Authority" not in html


def test_visual_route_is_opt_in_not_a_new_public_openapi_operation() -> None:
    matches = [route for route in router.routes if route.path == "/experience/visual"]
    assert len(matches) == 1
    assert matches[0].include_in_schema is False


def test_existing_player_only_exposes_3d_link_inside_live_session() -> None:
    document = player_html("zh-CN")
    assert 'id="visual-entry"' in document
    assert "visual.hidden=!model.instanceId" in document
    assert 'w.name!=="江南机关城"' in document
    assert 'id="send-action"' in document
