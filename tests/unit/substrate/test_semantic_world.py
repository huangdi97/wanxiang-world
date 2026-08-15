"""M37: full semantic world (mechanism; synthetic)."""

from __future__ import annotations

from pathlib import Path

import pytest
from wanxiang_domain.ids import WorldDefinitionId
from wanxiang_substrate.canon_graph import build_canon_graph
from wanxiang_substrate.semantic_world import (
    CharacterPackage,
    HistoricalChinaRules,
    HouseholdSociety,
    SemanticWorld,
    SpatialWorld,
    build_full_semantic_world,
    multi_scenario_dry_run,
    scan_core_proper_nouns,
)
from wanxiang_substrate.worldpack import GenesisSpec, WorldPackAssembler

SYNTHETIC = "第一回\nc1 进府。\n第二回\nc2 病于室。\n"


def _definition():
    genesis = GenesisSpec(
        genesis_id="gen_rc001",
        name="RC-001 Synthetic Genesis",
        source_id="src_rc_synth",
        scenario_ref="第二回",
        distilled_refs=("identity:c1",),
        initial_facts=("c1 进府",),
    ).with_hash()
    return WorldPackAssembler(secret="test").assemble(
        definition_id=WorldDefinitionId("wd_rc001"),
        name="RC-001 (synthetic mechanism world)",
        source_id="src_rc_synth",
        text=SYNTHETIC,
        scenario_chapter="第二回",
        genesis=genesis,
    )


def _world() -> SemanticWorld:
    canon = build_canon_graph(claims=(("cl1", "c1 进府", "event", "shared", ("loc://1",)),))
    coverage = None
    return build_full_semantic_world(
        definition=_definition(),
        characters=(
            CharacterPackage(
                character_key="c1",
                identity=("c1a",),
                life_arc=("arrival",),
                goals=("settle",),
                relations=("c2",),
                knowledge=("place:garden",),
                capabilities=("move", "rest"),
                evidence=("loc://1",),
                persona=("dutiful",),
                state=(("location", "garden"),),
            ),
            CharacterPackage(
                character_key="c2",
                identity=("c2a",),
                life_arc=("illness",),
                goals=("recover",),
                relations=("c1",),
                knowledge=("place:sickroom",),
                capabilities=("rest",),
                evidence=("loc://2",),
                persona=("reserved",),
                state=(("location", "sickroom"),),
            ),
        ),
        household=HouseholdSociety(
            duties=(("c1", "greeting", 5),),
            norms=("morning_greeting",),
            permissions=(("c1", "narrative.visit", "sickroom"),),
            reputation=(("c1", "courtesy", 0.9),),
        ),
        history_rules=HistoricalChinaRules(
            time_rules=("day_night_cycle",),
            identity_rules=("household_rank",),
            transport_rules=("walking", "sedan"),
            life_rules=("meal", "rest"),
            secrets=("secret_draft",),
            scenes=("garden_scene",),
            arcs=("rise_arc",),
        ),
        spatial=SpatialWorld(
            rooms=("garden", "sickroom"),
            portals=(("garden", "sickroom", "open"),),
            routes=(("garden", "sickroom", ("portal_hs",)),),
            visibility=(("garden", "sickroom"),),
            acoustic=(("garden", "sickroom"),),
            access=(("c1", "sickroom", "narrative.visit"),),
        ),
        material_bindings=(("letter_1", "letter", "c1"),),
        schedules=(("c1", ((6, "meal"), (8, "duty"))),),
        canon=canon,
        coverage=coverage,  # type: ignore[arg-type]
    )


@pytest.mark.unit
def test_full_world_definition_refs() -> None:
    world = _world()
    assert world.definition.manifest.kind == "world"
    assert world.definition.definition.constitution_ref == "con_literary_historical"
    assert world.definition.definition.genesis_ref == "gen_rc001"


@pytest.mark.unit
def test_character_package_persona_vs_state() -> None:
    world = _world()
    c1 = world.characters[0]
    assert c1.persona == ("dutiful",)  # interpretive, never state
    assert c1.state == (("location", "garden"),)  # current state fields
    assert "loc://1" in c1.evidence


@pytest.mark.unit
def test_household_reputation_and_rules() -> None:
    world = _world()
    assert ("c1", "courtesy", 0.9) in world.household.reputation
    assert ("c1", "greeting", 5) in world.household.duties
    assert "morning_greeting" in world.household.norms


@pytest.mark.unit
def test_history_rules_propose_only() -> None:
    world = _world()
    assert "secret_draft" in world.history_rules.secrets
    assert "garden_scene" in world.history_rules.scenes
    assert "rise_arc" in world.history_rules.arcs
    assert "day_night_cycle" in world.history_rules.time_rules


@pytest.mark.unit
def test_spatial_and_material_bindings() -> None:
    world = _world()
    assert ("garden", "sickroom", "open") in world.spatial.portals
    assert ("letter_1", "letter", "c1") in world.material_bindings


@pytest.mark.unit
def test_multi_scenario_dry_run() -> None:
    world = _world()
    results = multi_scenario_dry_run(world, ("c1", "nonexistent_scenario"))
    by_name = dict(results)
    assert by_name["c1"] is True
    assert by_name["nonexistent_scenario"] is False


@pytest.mark.unit
def test_core_proper_noun_scan_empty() -> None:
    root = Path(__file__).resolve().parents[2]
    found = scan_core_proper_nouns((str(root / "packages/runtime"), str(root / "packages/domain")))
    assert found == ()
