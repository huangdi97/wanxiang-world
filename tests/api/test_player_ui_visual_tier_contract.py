"""Atlas place rows expose source support and visual tier without inventing presence."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_api.player_ui_script import SCRIPT
from wanxiang_substrate.playable.player_i18n import _copy_for


def test_player_script_renders_visual_tier_and_source_evidence_count() -> None:
    assert "visual_tier_" in SCRIPT
    assert "visual_evidence_count" in SCRIPT
    assert "atlas_more_places" in SCRIPT
    assert "visual_budget_status" in SCRIPT


def test_visual_tier_copy_is_available_in_both_locales() -> None:
    for locale in ("zh-CN", "en-US"):
        copy = _copy_for(locale)
        assert copy.text("visual_tier_t0")
        assert copy.text("visual_tier_t1")
        assert copy.text("visual_tier_t3")
        assert "{count}" in copy.text("visual_evidence_count")
        assert "{count}" in copy.text("atlas_more_places")
        assert "{used}" in copy.text("visual_budget_status")
        assert "{limit}" in copy.text("visual_budget_status")
