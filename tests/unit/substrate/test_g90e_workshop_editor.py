"""G90E: versioned scenario/experience editing and preview isolation."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.playable import ExperiencePackage, ScenarioProfile
from wanxiang_substrate.workshop import WorkshopDraftStore, WorkshopEditor


def test_editor_versions_scenario_and_experience_in_one_draft() -> None:
    store = WorkshopDraftStore()
    initial = store.create("workshop_editor", mode="prompt", owner_id="author")
    editor = WorkshopEditor(store)
    scenario = ScenarioProfile("scenario_1", "world:prompt", starting_location_ref="town")
    after_scenario = editor.edit_scenario(
        initial.workshop_id, scenario, expected_revision=initial.revision
    )
    experience = ExperiencePackage(
        "experience_1",
        "world:prompt",
        scenario.scenario_id,
        "projection:player",
        visibility="private",
        owner_id="author",
    )
    after_experience = editor.edit_experience(
        initial.workshop_id, experience, expected_revision=after_scenario.revision
    )
    assert after_experience.revision == 3
    assert editor.validate("workshop_editor").ok is True


def test_editor_rejects_stale_revision_and_preview_does_not_publish() -> None:
    store = WorkshopDraftStore()
    initial = store.create("workshop_preview", mode="source", owner_id="author")
    editor = WorkshopEditor(store)
    scenario = ScenarioProfile("scenario_2", "world:source")
    editor.edit_scenario("workshop_preview", scenario, expected_revision=initial.revision)
    with pytest.raises(ContractError):
        editor.edit_scenario("workshop_preview", scenario, expected_revision=initial.revision)
    experience = ExperiencePackage(
        "experience_2",
        "world:source",
        scenario.scenario_id,
        "projection:player",
        visibility="private",
        owner_id="author",
    )
    editor.edit_experience("workshop_preview", experience, expected_revision=2)
    preview = editor.preview("workshop_preview")
    assert preview.published is False
    assert preview.preview_hash
    assert store.get("workshop_preview").status == "previewable"
