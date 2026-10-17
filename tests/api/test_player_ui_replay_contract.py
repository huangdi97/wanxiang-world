"""Player history replay stays explicit, read-only, and accessible."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_replay_script import REPLAY_SCRIPT
from wanxiang_api.player_ui_script import SCRIPT
from wanxiang_substrate.playable.player_i18n import _copy_for


def test_player_html_exposes_replay_banner_and_exit_control() -> None:
    html = player_html("zh-CN")

    assert 'id="stage-replay-banner"' in html
    assert 'id="stage-replay-exit"' in html
    assert "返回现在" in html
    assert "function replayAt(" in html


def test_player_script_replays_through_the_player_route_and_resets_on_entry() -> None:
    assert "/replay?at_ticks=" in REPLAY_SCRIPT
    assert "function replayAt(" in REPLAY_SCRIPT
    assert "function exitReplay(" in REPLAY_SCRIPT
    assert "model.replay=null" in SCRIPT
    assert '$("stage-replay-exit").addEventListener("click",exitReplay)' in REPLAY_SCRIPT


def test_replay_copy_is_available_in_both_locales() -> None:
    for locale in ("zh-CN", "en-US"):
        copy = _copy_for(locale)
        banner = copy.text("replay_banner")
        assert copy.text("replay_mode")
        assert copy.text("replay_hint")
        assert copy.text("replay_exit")
        assert "{time}" in banner
        assert "{count}" in banner
