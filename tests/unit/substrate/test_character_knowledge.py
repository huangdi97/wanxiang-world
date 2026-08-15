"""G35G: character relation / knowledge-boundary distillation (mechanism).

Uses an ANONYMIZED key-choice fixture (c1/c2/c3) - NOT real《红楼梦》names or
canon - proving the mechanism is identity-agnostic. Real text remains
EXTERNAL_BLOCKED (G35A).
"""

from __future__ import annotations

from collections.abc import Callable

import pytest
from wanxiang_substrate.sources.canon import scenario_at
from wanxiang_substrate.sources.character import (
    CharacterCanon,
    CharacterDistiller,
    CharacterFact,
    FactKind,
    FactScope,
)
from wanxiang_substrate.sources.locator import segment_source, source_slice

# Anonymized synthetic corpus ONLY - never real《红楼梦》canon text.
SYNTHETIC = (
    "第一回\n"
    "c1 进府。c1 少时失怙。\n"
    "第二回\n"
    "c2 病于室。c3 探望 c2。c2 性情孤高。\n"
    "第三回\n"
    "c1 之后将远行。\n"
)

# Anonymized rules: (proposition, character_key, kind, scope).
FACT_RULES: dict[str, tuple[str, str, FactKind, FactScope]] = {
    "c1 进府": ("c1进府", "c1", "life_stage", "public"),
    "c1 少时失怙": ("c1少时失怙", "c1", "life_stage", "private"),
    "c2 病于室": ("c2病于室", "c2", "life_stage", "private"),
    "c2 性情孤高": ("c2性情孤高", "c2", "persona", "public"),
    "c1 之后将远行": ("c1将远行", "c1", "world", "public"),
}

RELATION_RULES: dict[str, tuple[str, str, str, FactScope]] = {
    "c3 探望 c2": ("c3", "c2", "visits", "public"),
}


def extract_facts(text: str) -> tuple[tuple[str, str, FactKind, FactScope], ...]:
    return tuple(rule for token, rule in FACT_RULES.items() if token in text)


def extract_relations(text: str) -> tuple[tuple[str, str, str, FactScope], ...]:
    return tuple(rule for token, rule in RELATION_RULES.items() if token in text)


def _grant_c1_private(_key: str) -> frozenset[str]:
    return frozenset({"c3"}) if _key == "c1" else frozenset()


def distill(
    *,
    private_knowers: Callable[[str], frozenset[str]] | None = None,
    completion_notes: tuple[str, ...] = (),
) -> CharacterCanon:
    locators = segment_source("src_rc_synth", SYNTHETIC)
    scenario = scenario_at(locators, chapter="第二回", scenario_id="scn_002")
    return CharacterDistiller(
        extract_facts=extract_facts,
        extract_relations=extract_relations,
        private_knowers=private_knowers,
    ).distill(
        scenario=scenario,
        source_id="src_rc_synth",
        text=SYNTHETIC,
        completion_notes=completion_notes,
    )


@pytest.mark.unit
def test_life_stage_persona_world_facts_classified() -> None:
    canon = distill()
    by_prop = {fact.proposition: fact for fact in canon.facts}
    assert by_prop["c1进府"].kind == "life_stage"
    assert by_prop["c1进府"].temporal == "past"
    assert by_prop["c2病于室"].temporal == "present"
    assert by_prop["c2性情孤高"].kind == "persona"
    assert by_prop["c1将远行"].temporal == "future"
    # Evidence locators resolve.
    for fact in canon.facts:
        assert source_slice(SYNTHETIC, fact.locators[0]).strip()


@pytest.mark.unit
def test_private_facts_hidden_from_other_characters() -> None:
    canon = distill()
    c3_view = {fact.proposition for fact in canon.visible_to("c3")}
    assert "c1进府" in c3_view  # public
    assert "c1少时失怙" not in c3_view  # private of c1
    assert "c2病于室" not in c3_view  # private of c2
    assert "c1将远行" not in c3_view  # future
    c1_view = {fact.proposition for fact in canon.visible_to("c1")}
    assert "c1少时失怙" in c1_view  # own private fact is known to self
    assert "c2病于室" not in c1_view  # other character private


@pytest.mark.unit
def test_knowledge_leak_prevented_until_grant() -> None:
    # No grants: c3 knows none of c1 private facts.
    canon = distill()
    assert not any(fact.proposition == "c1少时失怙" for fact in canon.visible_to("c3"))
    # Grant c3 access to c1 private facts.
    granted = distill(private_knowers=_grant_c1_private)
    leak = {fact.proposition for fact in granted.visible_to("c3")}
    assert "c1少时失怙" in leak  # explicit grant lifts the boundary
    assert "c2病于室" not in leak  # c2 private facts still hidden


@pytest.mark.unit
def test_future_facts_never_visible_at_runtime() -> None:
    canon = distill()
    assert not any(fact.temporal == "future" for fact in canon.runtime_facts)
    assert not any(fact.proposition == "c1将远行" for fact in canon.visible_to("c1"))


@pytest.mark.unit
def test_relation_claims_distilled() -> None:
    canon = distill()
    rel = next(r for r in canon.relations if r.relation_type == "visits")
    assert (rel.source_key, rel.target_key) == ("c3", "c2")
    assert rel.scope == "public"
    assert source_slice(SYNTHETIC, rel.locators[0]).strip()
    assert any(r.relation_type == "visits" for r in canon.relations_for("c3"))


@pytest.mark.unit
def test_anonymized_key_choice_fixture_has_no_red_chamber_names() -> None:
    # The fixture is anonymized: keys c1/c2/c3, no Red Chamber proper nouns.
    forbidden = ("林黛玉", "贾宝玉", "潇湘馆", "怡红院", "红楼梦", "贾府")
    assert not any(name in SYNTHETIC for name in forbidden)
    canon = distill()
    assert {fact.character_key for fact in canon.facts} <= {"c1", "c2"}


@pytest.mark.unit
def test_completion_and_interpretive_separation() -> None:
    canon = distill(completion_notes=("c1幼年居所未在切片中证实 (Completion)",))
    # Interpretive persona facts are separated from factual kinds.
    assert {f.proposition for f in canon.facts_of_kind("persona")} == {"c2性情孤高"}
    assert {f.proposition for f in canon.facts_of_kind("life_stage")} >= {"c1进府", "c1少时失怙"}
    # Completion notes are strings, never facts.
    assert canon.completion_notes
    assert all(isinstance(f, CharacterFact) for f in canon.facts)


@pytest.mark.unit
def test_distillation_is_deterministic() -> None:
    first = distill()
    second = distill()
    assert first == second
