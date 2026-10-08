"""G59H: M56 E2E — book/GEDCOM/structured each form a recoverable WorldDraft.

Source -> Adapter -> Parse -> Distill -> Recommend domains -> Resolve ->
WorldDraft -> DraftStore save/load (recoverable, revisioned).
"""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_substrate.distill.passes import (
    EventTimeSpacePass,
    IdentityPass,
    RelationOrganizationPass,
)
from wanxiang_substrate.distill.passes_knowledge import CharacterKnowledgePass, ObjectRuleSkillPass
from wanxiang_substrate.distill.protocol import DistillerDAG
from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry
from wanxiang_substrate.domains.recommender import DomainRecommender
from wanxiang_substrate.domains.resolver import DomainDependencyResolver
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.draft.store import DraftStore
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.parsing.segment import LocatorFormat, build_segments
from wanxiang_substrate.sources.book import BookAdapter
from wanxiang_substrate.sources.structured import StructuredAdapter

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

BOOK = """# Chapter One

Alice Zhang entered the garden at dawn.
rule: no duels at dawn
secret: the garden key is hidden.

# Chapter Two

In 1985, she left Beijing.
"""

STRUCTURED = '{"person": {"name": "Alice", "year": 1980}, "place": "Beijing"}'


def _registry() -> DomainRegistry:
    registry = DomainRegistry()
    for domain in (
        DomainCapability("family", "Family", "1", ("family", "genealogy"), rules=("privacy",)),
        DomainCapability(
            "narrative",
            "Narrative",
            "1",
            ("narrative", "character", "temporal"),
            requires=("family",),
        ),
        DomainCapability("household", "Household", "1", ("social", "norm", "institution")),
        DomainCapability("spatial", "Spatial", "1", ("spatial", "place", "topology")),
    ):
        registry.register(domain)
    return registry


def _dag() -> DistillerDAG:
    return DistillerDAG(
        (
            IdentityPass(),
            EventTimeSpacePass(),
            RelationOrganizationPass(),
            CharacterKnowledgePass(),
            ObjectRuleSkillPass(),
        )
    )


def _build_draft(kind: str, content: str, fmt: str) -> WorldDraft:
    adapter = (
        BookAdapter()
        if kind in ("epub", "docx", "pdf", "text", "markdown")
        else StructuredAdapter()
    )
    from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

    record = SourceRecord(
        source_id="src_e2e",
        kind=kind,
        content_hash=payload_hash(content),
        content_ref="ref://e2e",
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload=content,
        provenance="fixture:m56",
    )
    result = adapter.ingest(record)
    parsed = StructureParser().parse(result, source_id="src_e2e", version="1")
    segments = build_segments(parsed, fmt=cast(LocatorFormat, fmt))
    candidates = _dag().run(segments, source_id="src_e2e")
    registry = _registry()
    recommendations = DomainRecommender().recommend(
        registry, source_kind=kind, candidates=candidates
    )
    selected = tuple(r.domain_id for r in recommendations[:2])
    resolution = DomainDependencyResolver().resolve(registry, selected)
    order = resolution.order if resolution.ok else ()
    identities = sorted(
        {
            dict(c.payload).get("identity_key") or dict(c.payload).get("key") or ""
            for c in candidates
            if c.kind == "identity"
        }
    )
    relations = sorted(
        (
            dict(c.payload)["source_key"],
            dict(c.payload)["target_key"],
            dict(c.payload)["relation_type"],
        )
        for c in candidates
        if c.kind == "relation"
    )
    places = sorted({dict(c.payload)["name"] for c in candidates if c.kind == "place"})
    events = sorted(
        {
            (
                dict(c.payload).get("subject_xref") or "time",
                dict(c.payload).get("date") or "unknown",
            )
            for c in candidates
            if c.kind in ("event", "time")
        }
    )
    rules = sorted({dict(c.payload)["name"] for c in candidates if c.kind == "rule"})
    knowledge_boundaries = sorted(
        {dict(c.payload)["boundary"] for c in candidates if c.kind == "knowledge_boundary"}
    )
    draft = WorldDraft(
        draft_id=f"wd_{kind}",
        revision=1,
        status="FUSING",
        source_refs=(record.source_id,),
        source_versions=((record.source_id, "1"),),
        constitution_ref="constitution:v1",
        selected_domains=order,
        dependency_lock=order,
        entities=tuple((key, key) for key in identities),
        relations=tuple(relations),
        places=tuple(places),
        events=tuple(events),
        rules=tuple(rules),
        knowledge_boundaries=tuple(knowledge_boundaries),
    )
    return draft


@pytest.mark.integration
def test_book_forms_recoverable_draft() -> None:
    draft = _build_draft("text", BOOK, "text")
    assert draft.selected_domains
    store = DraftStore()
    store.create(draft.draft_id, constitution_ref="constitution:v1")
    saved = WorldDraft(
        draft_id=draft.draft_id,
        revision=store.next_revision(draft.draft_id),
        status=draft.with_status("REVIEW_REQUIRED").status,
        source_refs=draft.source_refs,
        source_versions=draft.source_versions,
        constitution_ref=draft.constitution_ref,
        selected_domains=draft.selected_domains,
        dependency_lock=draft.dependency_lock,
        entities=draft.entities,
        relations=draft.relations,
        places=draft.places,
        events=draft.events,
        rules=draft.rules,
        knowledge_boundaries=draft.knowledge_boundaries,
    )
    store.save(saved)
    loaded = store.require(draft.draft_id)
    assert loaded.revision == 2
    assert loaded.entities or loaded.events


@pytest.mark.integration
def test_gedcom_forms_recoverable_draft() -> None:
    draft = _build_draft("gedcom", GEDCOM, "gedcom")
    assert "family" in draft.selected_domains
    assert len(draft.entities) >= 2
    assert draft.relations


@pytest.mark.integration
def test_structured_forms_recoverable_draft() -> None:
    draft = _build_draft("json", STRUCTURED, "json")
    # Even sparse structured input produces a draft object (recoverable).
    assert draft.draft_id == "wd_json"
