"""M60-M69 deterministic authoring contracts."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.completion_engine import CompletionEngine, MissingnessNode
from wanxiang_substrate.authoring.fusion import (
    DissentPolicy,
    build_provenance_graph,
    fuse_candidates,
    open_conflict_workbench,
)
from wanxiang_substrate.authoring.multimodal import BundleEntry, SourceBundleManifest
from wanxiang_substrate.authoring.orchestrator import AuthoringBudget, AuthoringOrchestrator
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.review_inbox import ReviewInbox
from wanxiang_substrate.authoring.scenario_engine import ScenarioEngine
from wanxiang_substrate.authoring.semantic import SemanticAnalyzer
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.authoring.worldness import RepairLoop, WorldnessEvaluator, WorldnessInput
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.sources.errors import OcrRequired
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _candidate(
    candidate_id: str, kind: str, payload: dict[str, str], source: str
) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass="test",
        payload=tuple(sorted(payload.items())),
        confidence=0.8,
        source_refs=(source,),
        distiller_version=1,
    )


@pytest.mark.unit
def test_semantic_fusion_and_dissent_are_reversible() -> None:
    candidates = (
        _candidate("c1", "identity", {"key": "alice", "display_name": "Alice"}, "s1#1"),
        _candidate("c2", "alias", {"identity_key": "alice", "alias": "A"}, "s1#2"),
        _candidate("c3", "event", {"event_type": "arrival", "date": "1985"}, "s1#3"),
        _candidate("c4", "place", {"name": "Beijing"}, "s1#4"),
        _candidate(
            "c5",
            "relation",
            {"source_key": "alice", "target_key": "bob", "relation_type": "knows"},
            "s1#5",
        ),
    )
    result = fuse_candidates(candidates)
    assert not result.conflict_ids
    analysis = SemanticAnalyzer().analyze(candidates)
    assert analysis.identities.canonical_keys == ("alice",)
    assert analysis.temporal.events
    assert analysis.graph.edges
    assert build_provenance_graph(candidates).edges
    assert open_conflict_workbench(result, policy=DissentPolicy()).policy.choose_winner is False


@pytest.mark.unit
def test_provider_and_completion_boundaries_are_honest() -> None:
    with pytest.raises(OcrRequired, match="OCR_REQUIRED"):
        ProviderRouter().propose("ocr", ("source#1",), "image")
    solved = CompletionEngine().solve(
        (MissingnessNode("n1", "initial location", True, ("s1", "s2")),)
    )
    assert solved.candidates[0].completion_class == "E1"
    assert solved.candidates[0].can_enter_canon is False
    with pytest.raises(ValueError, match="cannot be silently upgraded"):
        CompletionEngine().reject_e0_upgrade("E1", "E0")


@pytest.mark.unit
def test_scenarios_worldness_review_and_bundle() -> None:
    draft = WorldDraft(
        draft_id="draft_advanced",
        revision=1,
        status="READY_TO_COMPILE",
        source_refs=("s1",),
        source_versions=(("s1", "1"),),
        entities=(("alice", "Alice"), ("bob", "Bob")),
        relations=(("alice", "bob", "knows"),),
        places=("Beijing",),
        events=(("arrival", "1985"),),
        scenario_candidates=("scenario_1",),
        coverage=0.8,
    )
    plans = ScenarioEngine().build_three(draft)
    assert len(plans) == 3
    assert len({plan.snapshot_hash for plan in plans}) == 3
    score = WorldnessEvaluator().evaluate(
        WorldnessInput(2, 1, 2, 1, 0.1, replay_equal=True, branch_isolated=True)
    )
    assert {name for name, _value in score.dimensions} == {
        "persistence",
        "causality",
        "epistemic",
        "spatial",
        "consequence",
        "autonomy",
        "branch_isolation",
        "replayability",
        "provenance",
        "uncertainty",
    }
    repair = RepairLoop().run(WorldnessInput(0, 0, 0, 0, 0.8, False, False))
    assert repair.candidates
    inbox = ReviewInbox().build((_candidate("c", "object", {"name": "letter"}, "s1#1"),))
    assert inbox[0].auto_approved is True
    manifest = SourceBundleManifest.build("bundle_1", (BundleEntry("s1", "text", "a" * 64, True),))
    assert manifest.rights_ok is True


@pytest.mark.integration
def test_orchestrator_runs_reference_pipeline_with_budget() -> None:
    content = "# Chapter\nAlice arrived in 1985 at Beijing.\nrule: keep promises\n"
    record = SourceRecord(
        source_id="s_orch",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://s_orch",
        stage="E3",
        rights=RightsEnvelope(owner="fixture", usage="test", approved=True),
        payload=content,
        provenance="synthetic:orchestrator",
        access="public",
    )
    service = AuthoringService()
    service.create_job("job_orch", sources=(record,))
    run = AuthoringOrchestrator().run(
        service, "job_orch", budget=AuthoringBudget(max_candidates=100)
    )
    assert run.snapshot.preview_id is not None
    assert run.stages[-1] == "evaluate"
