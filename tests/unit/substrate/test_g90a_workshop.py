"""G90A: one World Workshop home and one optimistic draft backend."""

from __future__ import annotations

import pytest
from wanxiang_substrate.workshop import DraftRevisionConflict, WorldWorkshop


def test_workshop_exposes_three_creation_modes_and_shared_panels() -> None:
    workshop = WorldWorkshop()
    home = workshop.home()
    assert home.creation_modes == ("source", "prompt", "hybrid")
    assert {panel.panel_id for panel in home.panels} >= {
        "source",
        "prompt",
        "hybrid",
        "scenario",
        "experience",
        "publishing",
    }
    assert "WorkshopDraftStore" in home.shared_draft_backend


def test_shared_draft_backend_preserves_history_and_rejects_stale_editor() -> None:
    store = WorldWorkshop().drafts
    created = store.create("w1", mode="prompt", owner_id="author")
    saved = store.transition(
        "w1",
        status="review_required",
        expected_revision=created.revision,
        intent_id="intent_1",
        generated_claim_refs=("claim_1",),
    )
    assert store.get_revision("w1", 1).status == "draft"
    assert saved.revision == 2
    with pytest.raises(DraftRevisionConflict):
        store.transition("w1", status="previewable", expected_revision=1)
