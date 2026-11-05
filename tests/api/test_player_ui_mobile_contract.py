"""Mobile Stage keeps 44px touch targets and respects the bottom safe area."""

from __future__ import annotations

import re

from wanxiang_api.player_ui_style import STYLE

# Every control a player must be able to hit with a thumb at <=720px.
_TOUCH_TARGET_SELECTORS = (
    ".nav-button",
    ".text-button",
    ".filter-button",
    ".suggestion",
    ".secondary-button",
    ".primary-button",
    ".stage-focus-toggle",
    ".stage-exit",
    ".stage-replay-exit",
    ".chronicle-replay",
    ".chronicle-expand",
    ".visual-place",
    ".atlas-entrance",
    "#observer-scene-list button",
    "summary",
)
_TEXT_FIELD_SELECTORS = (
    ".search",
    ".visual-place-search",
    "textarea",
    "select",
)


def _mobile_rule_text() -> str:
    """Body of every <=720px media block, without the media wrapper."""

    bodies: list[str] = []
    for line in STYLE.splitlines():
        if "@media(max-width:720px)" not in line:
            continue
        bodies.append(line.split("{", 1)[1].rsplit("}", 1)[0])
    return "\n".join(bodies)


def _selectors_with_min_height(min_height: str) -> set[str]:
    """Selectors declared with a given min-height inside <=720px rules."""

    found: set[str] = set()
    for match in re.finditer(r"([^{}]+)\{([^}]*" + min_height + r"[^}]*)\}", _mobile_rule_text()):
        found.update(part.strip() for part in match.group(1).split(",") if part.strip())
    return found


def test_mobile_stage_uses_44px_touch_targets_and_safe_area() -> None:
    targets = _selectors_with_min_height("min-height:44px")
    missing = [selector for selector in _TOUCH_TARGET_SELECTORS if selector not in targets]
    assert missing == [], f"touch targets without 44px at <=720px: {missing}"
    fields = [selector for selector in _TEXT_FIELD_SELECTORS if selector not in targets]
    assert fields == [], f"text fields without 44px at <=720px: {fields}"
    assert "env(safe-area-inset-bottom)" in STYLE
    assert re.search(r"\.world-action-dock\{[^}]*env\(safe-area-inset-bottom\)", STYLE)


def test_mobile_layout_bounds_its_own_width() -> None:
    """The narrow shell bounds its own width instead of scrolling sideways."""

    assert re.search(r"\.world-experience-view\{[^}]*overflow-wrap:anywhere", STYLE)
    assert re.search(r"\.site-shell\{[^}]*padding:0 1rem", STYLE)


def test_player_html_links_the_mobile_style() -> None:
    from wanxiang_api.player_ui_asset import player_html

    html = player_html("zh-CN")
    assert "safe-area-inset-bottom" in html
