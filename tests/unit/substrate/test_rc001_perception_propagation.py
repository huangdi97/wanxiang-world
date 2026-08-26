"""G36E: perception / belief / memory + message propagation (mechanism; synthetic).

Synthetic corpus ONLY - never real《红楼梦》canon.
"""

from __future__ import annotations

import pytest
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.epistemic.propagation import (
    PerceptionEnvelope,
    perceive,
    propagatable_claims,
    propagate_message,
    rumour_distortion,
)
from wanxiang_substrate.sources.canon import CanonCompiler, scenario_at
from wanxiang_substrate.sources.locator import segment_source

# Synthetic corpus ONLY - never real《红楼梦》canon text.
SYNTHETIC = "第一回\nc1 进府。\n第二回\nc2 病于室。\n第三回\nc1 将远行。\n"

CLAIM_RULES: dict[str, tuple[str, str | None]] = {
    "c1 进府": ("c1进府", "c1"),
    "c2 病于室": ("c2病于室", "c2"),
    "c1 将远行": ("c1将远行", "c1"),
}


def extract_claims(text: str) -> tuple[tuple[str, str | None], ...]:
    return tuple(rule for token, rule in CLAIM_RULES.items() if token in text)


@pytest.mark.unit
def test_perception_forms_observation_memory() -> None:
    envelope = PerceptionEnvelope(
        envelope_id="env_1",
        observer_id=EntityId("c3"),
        content_ref="c2病于室",
        channel="acoustic",
        confidence=0.8,
        at_ticks=5,
        source_event_ref="evt_1",
    )
    memory = perceive(envelope, memory_id=EntityId("mem_1"))
    assert memory.kind == "observation"
    assert memory.actor_id == EntityId("c3")
    assert memory.content_ref == "c2病于室"
    assert memory.salience == 0.8
    assert memory.source_perception_refs == ("env_1",)


@pytest.mark.unit
def test_message_propagation_is_deterministic_with_decay() -> None:
    first = propagate_message(
        message_id="msg_1", origin="c1", chain=("c2", "c3", "c4"), content="c2病于室", seed=1
    )
    second = propagate_message(
        message_id="msg_1", origin="c1", chain=("c2", "c3", "c4"), content="c2病于室", seed=1
    )
    assert first == second
    assert first.hops == ("c2", "c3", "c4")
    assert first.confidence < 1.0  # misunderstanding decays confidence
    assert first.confidence == round(1.0 * 0.9 * 0.9 * 0.9, 4)


@pytest.mark.unit
def test_rumour_distortion_is_deterministic() -> None:
    assert rumour_distortion("a", 1, 3) == "a"  # (3+1) % 3 != 0
    assert rumour_distortion("a", 2, 1) == "a (rumoured)"  # (1+2) % 3 == 0
    assert rumour_distortion("a", 2, 1) == rumour_distortion("a", 2, 1)


@pytest.mark.unit
def test_future_canon_never_propagates() -> None:
    locators = segment_source("src_rc_synth", SYNTHETIC)
    scenario = scenario_at(locators, chapter="第二回")
    canon = CanonCompiler(extract_claims=extract_claims).compile(
        scenario=scenario,
        source_id="src_rc_synth",
        text=SYNTHETIC,
    )
    claims = propagatable_claims(canon)
    assert not any(c.temporal == "future" for c in claims)
    assert {c.proposition for c in claims} == {"c1进府", "c2病于室"}
