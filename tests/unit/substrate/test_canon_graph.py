"""M36: full corpus -> canon graph (mechanism; synthetic corpus)."""

from __future__ import annotations

import pytest
from wanxiang_substrate.canon_graph import FullCorpusPipeline
from wanxiang_substrate.sources.locator import segment_source

SYNTHETIC = "第一回\nc1 进府。c1 居于园。\n第二回\nc2 病于室。c3 探望 c2。\n"

LOCATORS = segment_source("src_corpus_full", SYNTHETIC)


def _run(retries: int = 0):
    return FullCorpusPipeline().run(
        SYNTHETIC,
        chapter_of=((LOCATORS[0], "1"), (LOCATORS[1], "2")),
        place_of=((LOCATORS[0], "garden"), (LOCATORS[1], "sickroom")),
        participant_of=((LOCATORS[0], "c1"), (LOCATORS[1], "c2"), (LOCATORS[1], "c3")),
        identities=(
            ("c1", "c1", ("c1a",), "resident", "adult"),
            ("c2", "c2", ("c2a",), "patient", "adult"),
        ),
        relations=(("c3", "c2", "visits", None, None),),
        connectivity=(("garden", "sickroom", "path"),),
        containment=(("box", "letter"),),
        custody=(("letter", "c1"),),
        membership=(("c3", "household"),),
        events=(
            ("e1", "c1 进府", "before", ("c1",), "garden"),
            ("e2", "c3 探望 c2", "after", ("c3", "c2"), "sickroom"),
        ),
        claims=(
            ("cl1", "c1 进府", "event", "shared", (LOCATORS[0].locator,)),
            ("cl2", "c2 病于室", "event", "shared", (LOCATORS[1].locator,)),
        ),
        retries=retries,
    )


@pytest.mark.unit
def test_scene_candidates_detected() -> None:
    result = _run()
    assert len(result.scenes) == 2
    assert all(s.place_keys for s in result.scenes)


@pytest.mark.unit
def test_character_graph() -> None:
    result = _run()
    node = result.characters.node("c1")
    assert node is not None
    assert node.role == "resident"
    assert "c1a" in node.aliases
    assert any(e.relation_type == "visits" for e in result.characters.edges)


@pytest.mark.unit
def test_source_graph() -> None:
    result = _run()
    assert ("garden", "sickroom", "path") in result.source_graph.place_connectivity
    assert ("box", "letter") in result.source_graph.place_containment
    assert ("letter", "c1") in result.source_graph.item_custody
    assert ("c3", "household") in result.source_graph.org_membership


@pytest.mark.unit
def test_timeline_graph() -> None:
    result = _run()
    assert len(result.timeline.events) == 2
    assert result.timeline.before("e1", "e2") is True


@pytest.mark.unit
def test_canon_graph_categories_and_edition_views() -> None:
    result = _run()
    assert {c.category for c in result.canon.claims} == {"event"}
    assert len(result.canon.edition_view("shared")) == 2


@pytest.mark.unit
def test_contradictions_preserved() -> None:
    graph = build_contradictory()
    assert graph.contradictions() == (("cl_a", "cl_b"),)
    assert len(graph.claims) == 2


def build_contradictory():
    from wanxiang_substrate.canon_graph import build_canon_graph

    return build_canon_graph(
        claims=(
            ("cl_a", "X 在园", "place", "edition_a", ()),
            ("cl_b", "X 在室", "place", "edition_b", ()),
        ),
        contradictions=(("cl_a", "cl_b"),),
    )


@pytest.mark.unit
def test_coverage_report_and_resume() -> None:
    pipeline = FullCorpusPipeline()
    first = pipeline.run(
        SYNTHETIC,
        chapter_of=((LOCATORS[0], "1"), (LOCATORS[1], "2")),
        place_of=((LOCATORS[0], "garden"), (LOCATORS[1], "sickroom")),
        participant_of=((LOCATORS[0], "c1"), (LOCATORS[1], "c2"), (LOCATORS[1], "c3")),
        identities=(("c1", "c1", ("c1a",), "resident", "adult"),),
        relations=(),
        connectivity=(),
        containment=(),
        custody=(),
        membership=(),
        events=(),
        claims=(("cl1", "c1 进府", "event", "shared", (LOCATORS[0].locator,)),),
    )
    assert first.coverage.source_segments == 2
    assert first.coverage.source_to_claim_traceable is True
    second = pipeline.run(
        SYNTHETIC,
        chapter_of=((LOCATORS[0], "1"), (LOCATORS[1], "2")),
        place_of=((LOCATORS[0], "garden"), (LOCATORS[1], "sickroom")),
        participant_of=((LOCATORS[0], "c1"), (LOCATORS[1], "c2"), (LOCATORS[1], "c3")),
        identities=(("c1", "c1", ("c1a",), "resident", "adult"),),
        relations=(),
        connectivity=(),
        containment=(),
        custody=(),
        membership=(),
        events=(),
        claims=(("cl1", "c1 进府", "event", "shared", (LOCATORS[0].locator,)),),
    )
    assert second.coverage.resumed_from_cache is True
    assert second.scenes == first.scenes


@pytest.mark.unit
def test_retry_count_recorded() -> None:
    result = _run(retries=3)
    assert result.coverage.retried == 3
