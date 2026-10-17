"""Player worldline fork stays explicit, owned, and Kernel-backed."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_api.player_ui_asset import player_html
from wanxiang_api.player_ui_worldline_script import WORLDLINE_SCRIPT
from wanxiang_substrate.playable.player_i18n import _copy_for


def test_player_html_exposes_worldline_fork_control() -> None:
    html = player_html("zh-CN")

    assert 'id="fork-worldline"' in html
    assert 'id="worldline-toggle"' in html
    assert 'id="worldline-panel"' in html
    assert 'id="worldline-compare"' in html
    assert "从此刻分支" in html
    assert "function forkWorldline(" in html
    assert "function toggleWorldlines(" in html
    assert "function compareWorldline(" in html


def test_worldline_script_forks_then_leaves_the_parent_session() -> None:
    assert "/instances/${encodeURIComponent(parent)}/fork" in WORLDLINE_SCRIPT
    assert "/leave" in WORLDLINE_SCRIPT
    assert "window.__WANXIANG_LAST_FORKED_WORLDLINE__=result.worldline" in WORLDLINE_SCRIPT
    assert '$("fork-worldline").addEventListener("click",forkWorldline)' in WORLDLINE_SCRIPT


def test_worldline_script_lists_switches_and_compares_worldlines() -> None:
    assert "/worldlines`" in WORLDLINE_SCRIPT
    assert "/compare?with=" in WORLDLINE_SCRIPT
    assert "function switchWorldline(" in WORLDLINE_SCRIPT
    assert "function compareWorldline(" in WORLDLINE_SCRIPT
    assert '$("worldline-toggle").addEventListener("click",toggleWorldlines)' in WORLDLINE_SCRIPT
    assert "[data-switch-worldline]" in WORLDLINE_SCRIPT
    assert "[data-compare-worldline]" in WORLDLINE_SCRIPT


def test_fork_copy_is_available_in_both_locales() -> None:
    for locale in ("zh-CN", "en-US"):
        copy = _copy_for(locale)
        assert copy.text("fork_worldline")
        assert copy.text("status_forking")
        assert copy.text("status_forked")
        assert copy.text("worldlines_heading")
        assert copy.text("worldline_switch")
        assert copy.text("worldline_current")
        assert copy.text("status_worldline_switched")
        assert copy.text("worldline_compare")
        assert copy.text("worldline_compare_heading")
        assert "{revision}" in copy.text("worldline_compare_common")
