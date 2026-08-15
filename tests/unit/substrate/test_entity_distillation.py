"""G35D: place/object/organization + topology distillation (mechanism; synthetic corpus).

Tests use an explicitly-labeled SYNTHETIC fixture ONLY - never real
《红楼梦》 canon. Real full-text acquisition remains EXTERNAL_BLOCKED (G35A).
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.sources.entity_distill import (
    EdgeKind,
    EntityCandidate,
    EntityDistiller,
    EntityKind,
    EntityMention,
    EntityReviewGate,
)
from wanxiang_substrate.sources.errors import SourceNotApproved
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.locator import SourceLocator, source_slice
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

# Synthetic corpus ONLY - never real《红楼梦》canon text.
SYNTHETIC = (
    "第一回\n"
    "潇湘馆在园内。林黛玉居潇湘馆。\n"
    "怡红院在园内。贾宝玉居怡红院。\n"
    "沁芳桥连接潇湘馆与怡红院。\n"
    "第二回\n"
    "紫鹃送药给黛玉。书信藏于妆匣。\n"
    "贾府设宴。\n"
)

# Synthetic-only rules (edition-agnostic mechanism; rules are caller-supplied).
ENTITY_RULES: dict[str, tuple[str, EntityKind, str]] = {
    "潇湘馆": ("xiaoxiang", "place", "潇湘馆"),
    "怡红院": ("yihong", "place", "怡红院"),
    "沁芳桥": ("qinfang_bridge", "path", "沁芳桥"),
    "书信": ("letter", "object", "书信"),
    "药": ("medicine", "object", "药"),
    "妆匣": ("makeup_case", "object", "妆匣"),
    "贾府": ("jia_household", "organization", "贾府"),
}


def extract_entities(text: str) -> tuple[tuple[str, EntityKind, str], ...]:
    return tuple(rule for token, rule in ENTITY_RULES.items() if token in text)


def extract_connections(text: str) -> tuple[tuple[str, str, str, EdgeKind], ...]:
    out: list[tuple[str, str, str, EdgeKind]] = []
    if "沁芳桥连接潇湘馆与怡红院" in text:
        out.append(("xiaoxiang", "yihong", "沁芳桥", "path"))
    if "书信藏于妆匣" in text:
        out.append(("letter", "makeup_case", "藏于妆匣", "containment"))
    if "通向北院" in text:
        out.append(("yihong", "north_courtyard", "北院", "path"))
    return tuple(out)


def distiller() -> EntityDistiller:
    return EntityDistiller(
        extract_entities=extract_entities,
        extract_connections=extract_connections,
    )


@pytest.mark.unit
def test_place_object_organization_distillation_with_evidence() -> None:
    distilled = distiller().distill("src_rc_synth", SYNTHETIC)
    by_key = {c.key: c for c in distilled.candidates}
    assert by_key["xiaoxiang"].kind == "place"
    assert by_key["yihong"].kind == "place"
    assert by_key["qinfang_bridge"].kind == "path"
    assert by_key["letter"].kind == "object"
    assert by_key["jia_household"].kind == "organization"
    # Every candidate carries a resolvable source locator.
    for candidate in distilled.candidates:
        assert candidate.evidence_locators
        locator = candidate.evidence_locators[0]
        assert source_slice(SYNTHETIC, locator).strip()


@pytest.mark.unit
def test_topology_connection_candidate_is_source_bound() -> None:
    distilled = distiller().distill("src_rc_synth", SYNTHETIC)
    path_edge = next(c for c in distilled.connections if c.kind == "path")
    assert (path_edge.source_key, path_edge.target_key) == ("xiaoxiang", "yihong")
    assert path_edge.label == "沁芳桥"
    assert path_edge.locators
    containment = next(c for c in distilled.connections if c.kind == "containment")
    assert (containment.source_key, containment.target_key) == ("letter", "makeup_case")
    # Deterministic ordering.
    assert distilled.connections == tuple(
        sorted(distilled.connections, key=lambda c: c.connection_id)
    )


@pytest.mark.unit
def test_unresolved_connection_target_goes_to_completion() -> None:
    corpus = "第一回\n怡红院通向北院。\n"
    distilled = distiller().distill("src_rc_synth", corpus)
    assert distilled.unresolved_targets == ("north_courtyard",)
    # The missing target is NOT invented as a candidate.
    assert "north_courtyard" not in {c.key for c in distilled.candidates}


@pytest.mark.unit
def test_completion_note_is_never_evidence() -> None:
    distilled = distiller().distill("src_rc_synth", SYNTHETIC)
    candidate = next(c for c in distilled.candidates if c.key == "xiaoxiang")
    note = "潇湘馆内部房间布局未在来源切片中证实 (Completion)"
    with_note = EntityCandidate(
        candidate_id=candidate.candidate_id,
        kind=candidate.kind,
        key=candidate.key,
        display_name=candidate.display_name,
        mentions=candidate.mentions,
        completion_notes=(note,),
        provenance=candidate.provenance,
    )
    # A completion note is a string, never a locator/evidence.
    assert all(isinstance(loc, SourceLocator) for loc in with_note.evidence_locators)
    gate = EntityReviewGate()
    decision = gate.review(with_note, source_text=SYNTHETIC, reviewer="human")
    assert decision.approved  # real locators carry eligibility
    # A candidate whose ONLY claims do not resolve is rejected despite notes.
    dangling = SourceLocator(
        source_id="src",
        chapter="第一回",
        segment_id="d",
        start_offset=100,
        end_offset=101,
        locator="src#第一回:100-101",
    )
    bad = EntityCandidate(
        candidate_id="ent_bad",
        kind="place",
        key="x",
        display_name="X",
        mentions=(EntityMention(key="x", kind="place", display_name="X", locators=(dangling,)),),
        completion_notes=("布局未证实 (Completion)",),
    )
    decision = gate.review(bad, source_text=SYNTHETIC, reviewer="human")
    assert not decision.approved
    assert "does not resolve" in decision.reason


@pytest.mark.unit
def test_entity_review_gate_requires_authorized_reviewer() -> None:
    distilled = distiller().distill("src_rc_synth", SYNTHETIC)
    gate = EntityReviewGate()
    decision = gate.review(
        distilled.candidates[0],
        source_text=SYNTHETIC,
        reviewer="system",
    )
    assert not decision.approved
    assert "not authorized" in decision.reason


@pytest.mark.unit
def test_approved_entity_becomes_eligible() -> None:
    distilled = distiller().distill("src_rc_synth", SYNTHETIC)
    gate = EntityReviewGate()
    candidate = next(c for c in distilled.candidates if c.key == "xiaoxiang")
    decision = gate.review(
        candidate,
        source_text=SYNTHETIC,
        reviewer="human",
        connections=distilled.connections,
    )
    assert decision.approved
    assert candidate.with_status("eligible").status == "eligible"


@pytest.mark.unit
def test_distillation_is_deterministic() -> None:
    first = distiller().distill("src_rc_synth", SYNTHETIC)
    second = distiller().distill("src_rc_synth", SYNTHETIC)
    assert first == second


@pytest.mark.unit
def test_e0_to_e5_stage_classification() -> None:
    rights = RightsEnvelope(owner="fixture", usage="corpus:test", approved=True, reviewer="system")
    stages: dict[str, SourceRecord] = {}
    for stage in ("E0", "E1", "E2", "E3", "E4", "E5"):
        stages[stage] = SourceRecord(
            source_id=f"src_{stage}",
            kind="text",
            content_hash=payload_hash(stage),
            content_ref=f"fixture://{stage}",
            stage=stage,  # type: ignore[arg-type]
            rights=rights if stage == "E3" else None,
        )
    # Only E3 (approved + rights) is canonical-eligible.
    assert stages["E0"].canonical_eligible() is False
    assert stages["E1"].canonical_eligible() is False
    assert stages["E2"].canonical_eligible() is False
    assert stages["E3"].canonical_eligible() is True
    assert stages["E4"].canonical_eligible() is False
    assert stages["E5"].canonical_eligible() is False
    # Forward transitions only; rejected/superseded are terminal.
    assert stages["E0"].can_transition_to("E1")
    assert stages["E2"].can_transition_to("E3")
    assert stages["E3"].can_transition_to("E4") is True  # E3 approved -> E4 rejected
    assert stages["E4"].can_transition_to("E5") is False
    assert stages["E5"].can_transition_to("E3") is False
    SourceGate().require_compile(stages["E3"])
    # E2 (content reviewed but not approved) with rights is still not canonical.
    e2_with_rights = SourceRecord(
        source_id="src_E2r",
        kind="text",
        content_hash=payload_hash("e2"),
        content_ref="fixture://e2r",
        stage="E2",  # type: ignore[arg-type]
        rights=rights,
    )
    with pytest.raises(SourceNotApproved):
        SourceGate().require_compile(e2_with_rights)
