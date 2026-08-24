"""M61 source-family, provenance, dissent, incremental, and rights contracts."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.fusion import (
    DissentPolicy,
    apply_rights_policy,
    build_provenance_graph,
    build_source_family,
    build_source_family_from_records,
    fuse_candidates,
    incremental_fuse,
    open_conflict_workbench,
)
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _candidate(
    candidate_id: str,
    kind: str,
    payload: dict[str, str],
    *source_refs: str,
) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass="m61_fixture",
        payload=tuple(sorted(payload.items())),
        confidence=0.8,
        source_refs=source_refs,
        distiller_version=1,
    )


def _record(source_id: str, content: str, *, version: str = "1", stage: str = "E3") -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(content),
        content_ref=f"memory://{source_id}",
        stage=stage,  # type: ignore[arg-type]
        rights=RightsEnvelope(owner="fixture", usage="test", approved=True),
        payload=content,
        provenance="synthetic:m61",
        version=version,
        access="public",
    )


@pytest.mark.integration
def test_source_family_alignment_and_provenance_preserve_dissent() -> None:
    family = build_source_family(
        (("novel", "edition_a", "1"), ("novel", "edition_b", "2")),
        roles=(("edition_a", "translation"), ("edition_b", "commentary")),
    )
    assert family.source_ids == ("edition_a", "edition_b")
    assert family.roles[1] == ("edition_b", "commentary")

    candidates = (
        _candidate("alice_a", "identity", {"key": "alice", "display_name": "Alice"}, "edition_a#1"),
        _candidate(
            "alice_b", "identity", {"key": "alice", "display_name": "Alicia"}, "edition_b#2"
        ),
        _candidate(
            "refine",
            "event",
            {"event_type": "arrival", "date": "1985", "refines": "alice_a"},
            "edition_b#3",
        ),
    )
    result = fuse_candidates(candidates)
    assert result.conflict_ids
    assert result.alignments[0][2] == ("edition_a", "edition_b")
    graph = build_provenance_graph(candidates)
    assert ("refine", "alice_a", "refines") in graph.edges
    workbench = open_conflict_workbench(
        result,
        policy=DissentPolicy(preferred_source_ids=("edition_b",)),
    )
    assert workbench.impact[0][1] == 2
    assert workbench.policy.choose_winner is False


@pytest.mark.unit
def test_incremental_supplemental_fusion_reports_affected_keys() -> None:
    stable = _candidate("stable", "place", {"name": "Beijing"}, "edition_a#1")
    previous = fuse_candidates((stable,))
    incoming = _candidate("alice_new", "identity", {"key": "alice"}, "supplement#1")
    update = incremental_fuse(previous, (incoming,))
    assert update.affected_keys == ("identity:alice",)
    assert update.reused_candidate_ids == ("stable",)


@pytest.mark.integration
def test_rights_policy_excludes_unreviewed_candidates_without_deleting_dissent() -> None:
    good = _record("good", "Alice")
    bad = _record("bad", "Bob", stage="E0")
    candidates = (
        _candidate("good_candidate", "identity", {"key": "alice"}, "good#1"),
        _candidate("bad_candidate", "identity", {"key": "bob"}, "bad#1"),
    )
    decision = apply_rights_policy(candidates, (good, bad))
    assert tuple(candidate.candidate_id for candidate in decision.included) == ("good_candidate",)
    assert decision.excluded_candidate_ids == ("bad_candidate",)
    assert decision.blocked_source_ids == ("bad",)


@pytest.mark.unit
def test_source_family_from_records_pins_versions_without_payloads() -> None:
    family = build_source_family_from_records(
        "family_1",
        (_record("v1", "one"), _record("v2", "two", version="2")),
    )
    assert family.family_id == "family_1"
    assert family.versions == (("v1", "1"), ("v2", "2"))
