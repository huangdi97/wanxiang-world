"""G37A: RC-001 seven-day automated scenario (mechanism; synthetic).

Deterministic reference run; optional LLM run separated and EXTERNAL_BLOCKED.
"""

from __future__ import annotations

import pytest
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, WorldDefinitionId, WorldInstanceId, WorldlineId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.authority import CommitAuthority
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.rc001 import SevenDayReferenceRun, instantiate_rc001, optional_llm_run
from wanxiang_substrate.worldpack import GenesisSpec, WorldPackAssembler

INSTANCE = WorldInstanceId("wld_rc001")
BRANCH = BranchId("br_rc001")
WORLDLINE = WorldlineId("wl_rc001")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)

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


def _instance():
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    base = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    return instantiate_rc001(
        authority=authority,
        state=base,
        instance_id=INSTANCE,
        branch_id=BRANCH,
        worldline_id=WORLDLINE,
        rule_version=RULES,
        world_time=WorldTime(1),
        definition=_definition(),
    )


@pytest.mark.unit
def test_seven_day_reference_run_is_deterministic() -> None:
    first = SevenDayReferenceRun().run(_instance())
    second = SevenDayReferenceRun().run(_instance())
    assert first == second
    assert first.final_hash == second.final_hash
    assert len(first.final_hash) == 64


@pytest.mark.unit
def test_day1_embody_and_relay_recorded() -> None:
    result = SevenDayReferenceRun().run(_instance())
    kinds = [(e.day, e.kind) for e in result.days]
    assert (1, "snapshot") in kinds
    assert (1, "embody") in kinds
    assert (1, "relay") in kinds
    assert any("daiyu" in e.detail for e in result.days if e.kind == "embody")
    assert any("zijuan" in e.detail for e in result.days if e.kind == "relay")


@pytest.mark.unit
def test_day3_release_and_fork() -> None:
    result = SevenDayReferenceRun().run(_instance(), fork_day=3, horizon_days=7)
    assert result.fork_branch_id is not None
    kinds = [e.kind for e in result.days]
    assert "release" in kinds
    assert "fork" in kinds
    assert result.final_revision == 700


@pytest.mark.unit
def test_optional_llm_run_is_separate_and_blocked() -> None:
    marker = optional_llm_run()
    assert marker.startswith("EXTERNAL_BLOCKED")
