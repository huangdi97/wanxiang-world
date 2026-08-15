"""G36H: RC-001 Experience Studio minimal surface (mechanism; synthetic).

Reuses existing queries; synthetic corpus only - never real《红楼梦》canon.
"""

from __future__ import annotations

import pytest
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.actions.registry import ActionRegistry, register_reference_actions
from wanxiang_substrate.ledger.completion import (
    CompletionRecord,
    CompletionReviewLedger,
)
from wanxiang_substrate.rc001 import ExperienceStudio, genesis_delta
from wanxiang_substrate.rc001.strategies import compare_to_baseline
from wanxiang_substrate.sources.canon import CanonCompiler, CompiledCanon, scenario_at
from wanxiang_substrate.sources.locator import segment_source

INSTANCE = WorldInstanceId("wld_rc001")
BRANCH = BranchId("br_rc001")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)

SYNTHETIC = "第一回\nc1 进府。\n第二回\nc2 病于室。\n"

CLAIM_RULES: dict[str, tuple[str, str | None]] = {
    "c1 进府": ("c1进府", "c1"),
    "c2 病于室": ("c2病于室", "c2"),
}


def extract_claims(text: str) -> tuple[tuple[str, str | None], ...]:
    return tuple(rule for token, rule in CLAIM_RULES.items() if token in text)


def _state() -> InMemoryCanonicalState:
    base = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    return base.apply(genesis_delta())


def _canon() -> CompiledCanon:
    locators = segment_source("src_rc_synth", SYNTHETIC)
    scenario = scenario_at(locators, chapter="第二回")
    return CanonCompiler(extract_claims=extract_claims).compile(
        scenario=scenario, source_id="src_rc_synth", text=SYNTHETIC
    )


def _completions() -> CompletionReviewLedger:
    ledger = CompletionReviewLedger()
    ledger.submit(
        CompletionRecord(
            completion_id="c1",
            description="布局 (Completion)",
            support_refs=("loc://1",),
            confidence=0.8,
        )
    )
    return ledger


@pytest.mark.unit
def test_studio_map_characters_actions_views() -> None:
    actions = ActionRegistry()
    register_reference_actions(actions)
    studio = ExperienceStudio(state=_state(), actions=actions)
    views = studio.views()
    assert "place_garden" in views.places
    assert "place_hall" in views.places
    assert "c1" in views.characters
    assert "spatial.move" in views.actions


@pytest.mark.unit
def test_studio_source_and_completion_views() -> None:
    actions = ActionRegistry()
    studio = ExperienceStudio(
        state=_state(),
        actions=actions,
        events=("evt:evt_1",),
        canon=_canon(),
        completions=_completions(),
    )
    views = studio.views()
    assert views.events == ("evt:evt_1",)
    assert "c1进府" in views.source_claims
    assert "c2病于室" in views.source_claims
    assert views.completion_pending == ("c1",)


@pytest.mark.unit
def test_studio_branch_compare() -> None:
    actions = ActionRegistry()
    state = _state()
    baseline = state.semantic_hash()
    studio = ExperienceStudio(state=state, actions=actions)
    views = studio.views(baseline_hash=baseline, baseline_revision=state.revision.value)
    assert views.branch_matches_baseline is True
    # A diverged branch (different hash) reports a mismatch.
    comparison = compare_to_baseline(
        baseline_hash=baseline,
        current_hash="different",
        current_revision=state.revision.value + 1,
        baseline_revision=state.revision.value,
    )
    assert comparison.diverged is True
