"""G57A-G57G: CandidateEnvelope + distiller DAG + reference passes (M54)."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.candidates.envelope import CandidateEnvelope, CandidateKind
from wanxiang_substrate.distill.passes import (
    EventTimeSpacePass,
    IdentityPass,
    RelationOrganizationPass,
)
from wanxiang_substrate.distill.passes_knowledge import (
    CharacterKnowledgePass,
    ObjectRuleSkillPass,
)
from wanxiang_substrate.distill.protocol import DistillerDAG, DistillerRegistry
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, Segment, build_segments
from wanxiang_substrate.sources.adapter import IngestResult

GEDCOM = """0 @I1@ INDI
1 NAME Alice /Zhang/
1 BIRT
2 DATE 1980-01-01
2 PLAC Beijing
0 @I2@ INDI
1 NAME Bob /Li/
1 BIRT
2 DATE 1982-03-04
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 CHIL @I3@
"""


def _segments(content: str, fmt: str = "gedcom") -> tuple[Segment, ...]:
    result = IngestResult(source_id="s1", kind=fmt, content=content, detected_format=fmt)
    parsed = StructureParser().parse(result, source_id="s1", version="1")
    return build_segments(parsed, fmt=cast(LocatorFormat, fmt))


def _default_dag() -> DistillerDAG:
    return DistillerDAG(
        (
            IdentityPass(),
            EventTimeSpacePass(),
            RelationOrganizationPass(),
            CharacterKnowledgePass(),
            ObjectRuleSkillPass(),
        )
    )


@pytest.mark.unit
def test_envelope_validation() -> None:
    with pytest.raises(ContractError):
        CandidateEnvelope(
            candidate_id="",
            kind="identity",
            origin_pass="p",
            payload=(),
            confidence=0.5,
            source_refs=(),
            distiller_version=1,
        )
    with pytest.raises(ContractError):
        CandidateEnvelope(
            candidate_id="c",
            kind=cast(CandidateKind, "bogus"),
            origin_pass="p",
            payload=(),
            confidence=0.5,
            source_refs=(),
            distiller_version=1,
        )  # type: ignore[arg-type]


@pytest.mark.unit
def test_envelope_hash_stable() -> None:
    a = CandidateEnvelope(
        candidate_id="c1",
        kind="identity",
        origin_pass="identity",
        payload=(("k", "v"),),
        confidence=0.5,
        source_refs=("s",),
        distiller_version=1,
    )
    b = CandidateEnvelope(
        candidate_id="c1",
        kind="identity",
        origin_pass="identity",
        payload=(("k", "v"),),
        confidence=0.5,
        source_refs=("s",),
        distiller_version=1,
    )
    assert a.compute_hash() == b.compute_hash()
    assert a.with_status("eligible").status == "eligible"


@pytest.mark.unit
def test_identity_pass_extracts_gedcom_identities() -> None:
    candidates = IdentityPass().distill(_segments(GEDCOM), source_id="s1")
    identities = [c for c in candidates if c.kind == "identity"]
    assert len(identities) == 2
    assert {dict(c.payload)["display_name"] for c in identities} == {"Alice Zhang", "Bob Li"}
    assert all(c.source_refs for c in identities)


@pytest.mark.unit
def test_event_time_space_pass() -> None:
    candidates = EventTimeSpacePass().distill(_segments(GEDCOM), source_id="s1")
    events = [c for c in candidates if c.kind == "event"]
    assert any(dict(c.payload)["event_type"] == "birth" for c in events)
    places = [c for c in candidates if c.kind == "place"]
    assert any("Beijing" in dict(c.payload)["name"] for c in places)


@pytest.mark.unit
def test_relation_organization_pass() -> None:
    candidates = RelationOrganizationPass().distill(_segments(GEDCOM), source_id="s1")
    relations = [c for c in candidates if c.kind == "relation"]
    assert any(dict(c.payload)["relation_type"] == "spouse" for c in relations)
    memberships = [c for c in candidates if c.kind == "membership"]
    assert memberships


@pytest.mark.unit
def test_character_knowledge_pass() -> None:
    candidates = CharacterKnowledgePass().distill(_segments(GEDCOM), source_id="s1")
    arcs = [c for c in candidates if c.kind == "life_arc"]
    assert arcs and dict(arcs[0].payload)["start"] == "1980-01-01"


@pytest.mark.unit
def test_object_rule_skill_pass() -> None:
    segments = _segments(
        "rule: no duels at dawn\nnorm: bow to elders\nskill: calligraphy\n", fmt="text"
    )
    candidates = ObjectRuleSkillPass().distill(segments, source_id="s1")
    kinds = {c.kind for c in candidates}
    assert {"rule", "norm", "skill"} <= kinds


@pytest.mark.unit
def test_dag_runs_all_passes_with_provenance() -> None:
    candidates = _default_dag().run(_segments(GEDCOM), source_id="s1")
    origins = {c.origin_pass for c in candidates}
    assert {
        "identity",
        "event_time_space",
        "relation_organization",
        "character_knowledge",
    } <= origins
    assert all(c.distiller_version == 1 for c in candidates)
    assert all(c.status == "pending" for c in candidates)


@pytest.mark.unit
def test_registry_and_pass_names() -> None:
    registry = DistillerRegistry()
    registry.register(IdentityPass())
    registry.register(EventTimeSpacePass())
    dag = registry.dag()
    assert dag.pass_names() == ("identity", "event_time_space")
    assert registry.run(_segments(GEDCOM), source_id="s1")
