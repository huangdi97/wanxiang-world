"""G35E: Past/Character/Future canon compilation (mechanism; synthetic corpus).

Tests use an explicitly-labeled SYNTHETIC fixture ONLY - never real
《红楼梦》 canon. Real full-text acquisition remains EXTERNAL_BLOCKED (G35A).
"""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.sources.canon import CanonCompiler, CompiledCanon, scenario_at
from wanxiang_substrate.sources.locator import segment_source, source_slice

# Synthetic corpus ONLY - never real《红楼梦》canon text.
SYNTHETIC = (
    "第一回\n"
    "林黛玉进贾府。贾宝玉与林黛玉相见。\n"
    "第二回\n"
    "贾宝玉梦游太虚幻境。林黛玉居潇湘馆。\n"
    "第三回\n"
    "元妃省亲。贾府设宴。\n"
)

# Synthetic-only claim rules (edition-agnostic mechanism; rules are caller-supplied).
CLAIM_RULES: dict[str, tuple[str, str | None]] = {
    "林黛玉进贾府": ("林黛玉进贾府", "lin_daiyu"),
    "贾宝玉与林黛玉相见": ("贾宝玉与林黛玉相见", None),
    "贾宝玉梦游太虚幻境": ("贾宝玉梦游太虚幻境", "jia_baoyu"),
    "林黛玉居潇湘馆": ("林黛玉居潇湘馆", "lin_daiyu"),
    "元妃省亲": ("元妃省亲", None),
    "贾府设宴": ("贾府设宴", "jia_household"),
}


def extract_claims(text: str) -> tuple[tuple[str, str | None], ...]:
    return tuple(rule for token, rule in CLAIM_RULES.items() if token in text)


def compile_at_second_chapter() -> CompiledCanon:
    locators = segment_source("src_rc_synth", SYNTHETIC)
    scenario = scenario_at(locators, chapter="第二回", scenario_id="scn_002")
    return CanonCompiler(extract_claims=extract_claims).compile(
        scenario=scenario,
        source_id="src_rc_synth",
        text=SYNTHETIC,
    )


@pytest.mark.unit
def test_past_character_future_classification() -> None:
    compiled = compile_at_second_chapter()
    assert compiled.scenario.time_ref == "第二回"
    assert len(compiled.past) == 2
    assert len(compiled.character) == 2
    assert len(compiled.future) == 2
    assert all(claim.temporal == "past" for claim in compiled.past)
    assert all(claim.temporal == "present" for claim in compiled.character)
    assert all(claim.temporal == "future" for claim in compiled.future)


@pytest.mark.unit
def test_future_canon_is_control_plane_only() -> None:
    compiled = compile_at_second_chapter()
    # The running world's runtime view never contains FutureCanon.
    assert all(claim.temporal != "future" for claim in compiled.runtime_view)
    # The control plane sees the full canon including FutureCanon.
    control = compiled.control_plane_view
    assert any(claim.temporal == "future" for claim in control)
    assert len(control) == len(compiled.runtime_view) + len(compiled.future)


@pytest.mark.unit
def test_character_canon_is_per_character_and_excludes_future() -> None:
    compiled = compile_at_second_chapter()
    lin = compiled.character_canon("lin_daiyu")
    propositions = {claim.proposition for claim in lin}
    assert "林黛玉进贾府" in propositions
    assert "林黛玉居潇湘馆" in propositions
    assert "元妃省亲" not in propositions  # future never leaks into character canon
    assert all(claim.character_key == "lin_daiyu" for claim in lin)
    bao = compiled.character_canon("jia_baoyu")
    assert {claim.proposition for claim in bao} == {"贾宝玉梦游太虚幻境"}


@pytest.mark.unit
def test_scenario_at_selects_concrete_time_point() -> None:
    locators = segment_source("src_rc_synth", SYNTHETIC)
    scenario = scenario_at(locators, chapter="第三回")
    assert scenario.time_ref == "第三回"
    assert scenario.locator.chapter == "第三回"
    with pytest.raises(ContractError):
        scenario_at(locators, chapter="第十回")


@pytest.mark.unit
def test_canon_claims_carry_resolvable_evidence() -> None:
    compiled = compile_at_second_chapter()
    for claim in compiled.control_plane_view:
        assert claim.locators
        locator = claim.locators[0]
        assert source_slice(SYNTHETIC, locator).strip()


@pytest.mark.unit
def test_compile_is_deterministic() -> None:
    first = compile_at_second_chapter()
    second = compile_at_second_chapter()
    assert first == second
