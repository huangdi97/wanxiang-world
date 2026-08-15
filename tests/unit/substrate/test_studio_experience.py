"""M39: studio & experience surface (mechanism; synthetic)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.studio_experience import (
    CandidateReview,
    ExperienceEntry,
    SourceBrowserEntry,
    build_experience_catalog,
    build_living_world_view,
    build_studio_workspace,
    run_fresh_user_flow,
    summarize_return,
)


@pytest.mark.unit
def test_studio_workspace_source_and_candidates() -> None:
    ws = build_studio_workspace(
        source_browser=(
            SourceBrowserEntry(
                locator="src#第一回:1-2",
                chapter="第一回",
                slice_preview="...",
                candidates=("cand_1",),
            ),
        ),
        candidates=(
            CandidateReview(
                candidate_id="cand_1",
                proposition="X",
                evidence=("loc://1",),
                conflicts=(),
                status="pending",
            ),
        ),
        character_graph_nodes=("c1",),
        timeline_events=("e1",),
        future_canon_permission=False,
        map_topology=("garden",),
        schedules=(("c1", ((6, "meal"),)),),
        norms=("morning_greeting",),
        duties=(("c1", "greeting", 5),),
    )
    assert ws.source_browser[0].locator.startswith("src#")
    assert ws.candidates[0].status == "pending"
    assert ws.future_canon_permission is False


@pytest.mark.unit
def test_experience_catalog_and_modes() -> None:
    entries = (
        ExperienceEntry(
            entry_id="e1", world_ref="rc001", scenario_ref="arrival", role_ref="c1", mode="scenario"
        ),
        ExperienceEntry(
            entry_id="e2", world_ref="rc001", scenario_ref="illness", role_ref="c2", mode="canon"
        ),
    )
    catalog = build_experience_catalog(entries)
    assert len(catalog) == 2
    assert {e.mode for e in catalog} == {"scenario", "canon"}


@pytest.mark.unit
def test_living_world_view_fields() -> None:
    view = build_living_world_view(
        map_cells=("garden", "hall"),
        actors=("c1",),
        items=("letter",),
        actions=("move", "read"),
        dialogue=("greeting",),
        perceptions=("sight",),
        time=6,
    )
    assert "letter" in view.items
    assert view.time == 6


@pytest.mark.unit
def test_embodiment_return_summary() -> None:
    summary = summarize_return(
        left_branch="br_a",
        returned_branch="br_a",
        timeline_distance=3,
        lineage_distance=1,
        canon_distance=0.0,
        background_policy="deterministic",
    )
    assert summary.left_branch == "br_a"
    assert summary.canon_distance == 0.0
    assert summary.background_policy == "deterministic"


@pytest.mark.unit
def test_fresh_user_flow_and_accessibility() -> None:
    flow = run_fresh_user_flow()
    assert flow.ok is True
    assert flow.steps_completed == ("catalog", "scenario", "embody", "view")
    assert "role_label" in flow.accessibility_labels
