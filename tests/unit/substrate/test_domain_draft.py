"""G59A-G59G: Domain matching + WorldDraft tests."""

from __future__ import annotations

from typing import cast

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.candidates.envelope import CandidateEnvelope, CandidateKind
from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry
from wanxiang_substrate.domains.recommender import DomainRecommender
from wanxiang_substrate.domains.resolver import DomainDependencyResolver
from wanxiang_substrate.draft.coverage import CoverageAssessor
from wanxiang_substrate.draft.genesis import GenesisPlanBuilder
from wanxiang_substrate.draft.model import WorldDraft
from wanxiang_substrate.draft.scenarios import ScenarioMiner
from wanxiang_substrate.draft.store import DraftNotFound, DraftStore


def _registry() -> DomainRegistry:
    registry = DomainRegistry()
    registry.register(
        DomainCapability(
            domain_id="family",
            name="Family",
            version="1",
            provides=("family", "genealogy"),
            requires=(),
            rules=("privacy",),
        )
    )
    registry.register(
        DomainCapability(
            domain_id="narrative",
            name="Narrative",
            version="1",
            provides=("narrative", "character", "temporal"),
            requires=("family",),
        )
    )
    registry.register(
        DomainCapability(
            domain_id="household",
            name="Household",
            version="1",
            provides=("social", "norm", "institution"),
            requires=(),
        )
    )
    return registry


def _candidates() -> tuple[CandidateEnvelope, ...]:
    def c(kind: str, payload: dict[str, str]) -> CandidateEnvelope:
        return CandidateEnvelope(
            candidate_id=f"c_{kind}",
            kind=cast(CandidateKind, kind),
            origin_pass="p",
            payload=tuple(payload.items()),
            confidence=0.8,
            source_refs=("ref://1",),
            distiller_version=1,
        )

    return (
        c("identity", {"identity_key": "alice"}),
        c("relation", {"relation_type": "spouse"}),
        c("event", {"event_type": "birth"}),
        c("place", {"name": "Beijing"}),
    )


@pytest.mark.unit
def test_domain_capability_validation() -> None:
    with pytest.raises(ContractError):
        DomainCapability(domain_id="x", name="", version="1", provides=("a",))
    with pytest.raises(ContractError):
        DomainCapability(domain_id="x", name="X", version="1", provides=("x",), requires=("x",))


@pytest.mark.unit
def test_recommender_explainable() -> None:
    recommendations = DomainRecommender().recommend(
        _registry(), source_kind="gedcom", candidates=_candidates()
    )
    assert recommendations
    family = next(r for r in recommendations if r.domain_id == "family")
    assert family.score > 0
    assert family.reasons


@pytest.mark.unit
def test_dependency_resolver_order_and_conflicts() -> None:
    registry = _registry()
    resolution = DomainDependencyResolver().resolve(registry, ("narrative", "family"))
    assert resolution.ok
    assert resolution.order.index("family") < resolution.order.index("narrative")
    bad = DomainDependencyResolver().resolve(registry, ("unknown_domain",))
    assert not bad.ok


@pytest.mark.unit
def test_draft_lifecycle_and_store() -> None:
    store = DraftStore()
    draft = store.create("wd_1", constitution_ref="constitution:v1")
    assert draft.status == "CREATED"
    ingesting = draft.with_status("INGESTING")
    next_rev = WorldDraft(
        draft_id=ingesting.draft_id,
        revision=store.next_revision("wd_1"),
        status=ingesting.with_status("DISTILLING").status,
        constitution_ref=ingesting.constitution_ref,
    )
    assert store.save(next_rev) is not None
    loaded = store.require("wd_1")
    assert loaded.status == "DISTILLING"
    assert store.revision_count("wd_1") == 2
    with pytest.raises(ContractError):
        draft.with_status("PUBLISHABLE")  # CREATED -> PUBLISHABLE invalid


@pytest.mark.unit
def test_draft_store_revision_restore() -> None:
    store = DraftStore()
    store.create("wd_2")
    loaded = store.require("wd_2")
    assert loaded.revision == 1
    with pytest.raises(DraftNotFound):
        store.load_revision("wd_2", 5)


@pytest.mark.unit
def test_coverage_assessment() -> None:
    draft = WorldDraft(
        draft_id="wd_3",
        revision=1,
        status="DISTILLING",
        selected_domains=("family", "household"),
        entities=(("alice", "Alice"),),
        relations=(("alice", "bob", "spouse"),),
        places=("Beijing",),
        events=(("e1", "1980"),),
        rules=("ritual",),
    )
    report = CoverageAssessor().assess(draft, _registry())
    assert report.coverage > 0
    assert not report.has_blocking_gap


@pytest.mark.unit
def test_scenario_mining_and_genesis() -> None:
    draft = WorldDraft(
        draft_id="wd_4",
        revision=1,
        status="FUSING",
        selected_domains=("family",),
        events=(("e1", "1980"), ("e2", "1980"), ("e3", "1982")),
        relations=(("alice", "bob", "spouse"),),
    )
    scenarios = ScenarioMiner().mine(draft)
    assert len(scenarios) == 2
    genesis = GenesisPlanBuilder().build(draft, scenarios[0])
    assert genesis.world_ref == "wd_4"
    assert genesis.scenario_ref == scenarios[0].scenario_id
    assert genesis.runtime_profile["scheduler"] == "deterministic"
