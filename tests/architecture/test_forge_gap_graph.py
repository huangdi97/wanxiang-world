"""G54C: Forge gap graph validation (M51)."""

from __future__ import annotations

import json
import pathlib

import pytest
import scripts.forge_gap_graph as gap

ROOT = pathlib.Path(__file__).resolve().parents[2]
GRAPH = ROOT / "reports" / "forge_gap_graph.json"


@pytest.mark.architecture
def test_every_non_exists_stage_has_closure_goals() -> None:
    graph = gap.build_graph()
    errors = gap.validate(graph, gap.collect_goal_ids())
    assert errors == []


@pytest.mark.architecture
def test_graph_reports_honest_statuses() -> None:
    """Stages 10/11/12/14/19 are genuinely missing today; do not over-claim."""
    graph = gap.build_graph()
    status = {s.stage: s.status for s in graph}
    for stage in (10, 14, 19):
        assert status[stage] == "MISSING"
    # Completion planner (G58F) exists; missingness graph still missing.
    assert status[12] == "PARTIAL"
    # WorldDraft v1 (G59D) exists.
    assert status[11] == "EXISTS"
    # Foundation registry/locator/package/living stages exist.
    for stage in (1, 2, 5, 20, 21):
        assert status[stage] == "EXISTS"


@pytest.mark.architecture
def test_pipeline_has_21_stages() -> None:
    graph = gap.build_graph()
    assert [s.stage for s in graph] == list(range(1, 22))


@pytest.mark.architecture
def test_committed_graph_matches_current() -> None:
    data = json.loads(GRAPH.read_text(encoding="utf-8"))
    assert data["stages"] == [gap.stage_payload(s) for s in gap.build_graph()]

