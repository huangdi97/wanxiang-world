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
    assert "visual?.generation" in SCRIPT
    assert "visual_sources_merged" in SCRIPT
    assert "visual_place_more_count" in SCRIPT


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
        assert "{count}" in copy.text("visual_sources_merged")
        assert "{count}" in copy.text("visual_place_more_count")
        panorama = copy.text("panorama_upgrade_available")
        assert "{cost}" in panorama
        assert "{remaining}" in panorama
        assert "{budget}" in panorama

def test_visual_generation_budget_errors_are_localized_and_not_generic() -> None:
    assert "error_visual_attempt_reserved" in SCRIPT
    assert "error_visual_budget_exhausted" in SCRIPT
    chinese = _copy_for("zh-CN")
    english = _copy_for("en-US")

    assert "重复计费" in chinese.text("error_visual_attempt_reserved")
    assert "额度已用完" in chinese.text("error_visual_budget_exhausted")
    assert "duplicate billing" in english.text("error_visual_attempt_reserved")
    assert "budget is exhausted" in english.text("error_visual_budget_exhausted")
