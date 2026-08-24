"""M60 multi-chapter semantic candidate and metric qualification."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.pipeline import SourceToDraftPipeline
from wanxiang_substrate.authoring.semantic import SemanticAnalyzer
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _candidate(
    candidate_id: str, kind: str, payload: dict[str, str], *refs: str
) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass="m60_fixture",
        payload=tuple(sorted(payload.items())),
        confidence=0.8,
        source_refs=refs,
        distiller_version=1,
    )


def _semantic_fixture() -> tuple[CandidateEnvelope, ...]:
    return (
        _candidate("id_alice", "identity", {"key": "alice", "display_name": "Alice"}, "s1#1"),
        _candidate("alias_alice", "alias", {"identity_key": "alice", "alias": "A"}, "s1#2"),
        _candidate(
            "arc_alice",
            "life_arc",
            {"subject": "alice", "phase": "exile", "goal": "return", "belief": "trust"},
            "s1#3",
        ),
        _candidate("coref_unknown", "coreference", {"identity_key": "alice"}, "s2#1"),
        _candidate("event_late", "event", {"event_type": "return", "date": "1990"}, "s1#4"),
        _candidate("event_early", "event", {"event_type": "departure", "date": "1985"}, "s1#5"),
        _candidate("event_unknown", "event", {"event_type": "meeting"}, "s1#6"),
        _candidate("relation", "relation", {"source_key": "alice", "target_key": "bob"}, "s1#7"),
        _candidate("place_a", "place", {"name": "Beijing"}, "s1#8"),
        _candidate("place_b", "place", {"name": "Garden"}, "s1#9"),
        _candidate(
            "topology",
            "connectivity",
            {"source_place": "Beijing", "target_place": "Garden"},
            "s1#10",
        ),
        _candidate("access_gap", "access", {"source_place": "Garden"}, "s1#11"),
        _candidate("object", "object", {"name": "jade seal"}, "s1#12"),
        _candidate(
            "transfer",
            "transfer",
            {"object_key": "jade seal", "owner": "alice", "place": "Garden", "date": "1985"},
            "s1#13",
        ),
        _candidate("institution", "organization", {"name": "Guild", "role": "keeper"}, "s1#14"),
        _candidate(
            "norm",
            "rule",
            {"institution": "Guild", "norm": "register visitors", "penalty": "fine"},
            "s1#15",
        ),
    )


@pytest.mark.integration
def test_m60_semantic_views_preserve_uncertainty_and_provenance() -> None:
    analysis = SemanticAnalyzer().analyze(_semantic_fixture())
    assert analysis.identities.canonical_keys == ("alice",)
    assert analysis.identities.aliases == (("alice", "A"),)
    assert analysis.identities.unresolved_mentions == ("coref_unknown",)
    assert analysis.temporal.unknown_time == ("meeting",)
    assert analysis.temporal.ordering_conflicts
    assert analysis.life_arcs[0].subject == "alice"
    assert analysis.spatial.edges == (("Beijing", "Garden", "connectivity"),)
    assert analysis.spatial.unresolved_access == ("access_gap",)
    assert analysis.object_biographies[0].object_key == "jade seal"
    assert analysis.institution_norms[0].institution == "Guild"
    assert 0.0 <= analysis.metrics.precision_proxy <= 1.0
    assert 0.0 <= analysis.metrics.recall_proxy <= 1.0
    assert analysis.metrics.conflict_count == 1
    assert analysis.metrics.unknown_count == 3


@pytest.mark.integration
def test_multichapter_reference_pipeline_is_deterministic_and_located() -> None:
    content = """# Chapter One

Alice arrived in Beijing in 1985.
object: jade seal
rule: visitors register
secret: the seal is hidden.

# Chapter Two

Alice returned to Beijing in 1990.
"""
    record = SourceRecord(
        source_id="novel_m60",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://novel_m60",
        stage="E3",
        rights=RightsEnvelope(owner="fixture", usage="test", approved=True),
        payload=content,
        provenance="synthetic:m60",
        access="public",
    )
    first = SourceToDraftPipeline().run((record,), draft_id="wd_novel_m60")
    second = SourceToDraftPipeline().run((record,), draft_id="wd_novel_m60")
    assert first.semantic_analysis == second.semantic_analysis
    assert first.draft.compiler_metadata == second.draft.compiler_metadata
    assert first.segments
    assert all(segment.locator.source_id == "novel_m60" for segment in first.segments)
    assert first.draft.completion_items
