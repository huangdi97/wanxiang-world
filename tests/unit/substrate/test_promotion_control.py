"""G33C: promotion replayable & revocable control."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import RULES, SCHEMA, build_fixture_events
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.evolution.promotion.control import (
    PromotionControlLedger,
    PromotionRecord,
)


@pytest.mark.unit
def test_promotion_ledger_is_append_only_and_replayable() -> None:
    ledger = PromotionControlLedger()
    ledger.record(
        PromotionRecord(
            record_id="promo_1",
            derived_definition_id="wd_rc_derived",
            source_worldline_ref="wl_rc_001",
            parent_definition_ref="wd_rc_parent",
        )
    )
    ledger.record(
        PromotionRecord(
            record_id="promo_2",
            derived_definition_id="wd_rc_derived_b",
            source_worldline_ref="wl_rc_002",
            parent_definition_ref="wd_rc_parent",
        )
    )
    assert ledger.count() == 2
    assert [r.record_id for r in ledger.records()] == ["promo_1", "promo_2"]
    assert ledger.status("promo_1") == "active"


@pytest.mark.unit
def test_withdraw_only_changes_installability_status() -> None:
    ledger = PromotionControlLedger()
    ledger.record(
        PromotionRecord(
            record_id="promo_1",
            derived_definition_id="wd_rc_derived",
            source_worldline_ref="wl_rc_001",
            parent_definition_ref="wd_rc_parent",
        )
    )
    withdrawn = ledger.withdraw("promo_1", rationale="rights review pending")
    assert withdrawn.status == "withdrawn"
    assert ledger.status("promo_1") == "withdrawn"
    # The record is NOT deleted: history remains for audit/replay.
    assert ledger.count() == 1
    with pytest.raises(ValueError):
        ledger.withdraw("promo_1")  # already withdrawn


@pytest.mark.integration
def test_withdraw_derived_definition_does_not_affect_parent_replay() -> None:
    ledger = PromotionControlLedger()
    ledger.record(
        PromotionRecord(
            record_id="promo_1",
            derived_definition_id="wd_rc_derived",
            source_worldline_ref="wl_rc_001",
            parent_definition_ref="wd_rc_parent",
        )
    )
    parent_before = ReplayEngine(RULES, SCHEMA).replay(build_fixture_events()).semantic_hash()
    ledger.withdraw("promo_1")
    parent_after = ReplayEngine(RULES, SCHEMA).replay(build_fixture_events()).semantic_hash()
    # Withdrawal only affects the derived definition's registry status; the
    # parent worldline history replays identically.
    assert parent_after == parent_before
    assert parent_after == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
