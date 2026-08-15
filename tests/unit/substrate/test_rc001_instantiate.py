"""G36A: RC-001 instantiation + fixed initial snapshot (mechanism; synthetic).

Synthetic anonymized content ONLY - never real《红楼梦》canon.
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
from wanxiang_substrate.rc001 import (
    instantiate_rc001,
    record_lineage_root,
    resolve_rc001_profile,
)
from wanxiang_substrate.worldpack import AssembledWorldPack, GenesisSpec, WorldPackAssembler

# Synthetic corpus ONLY - never real《红楼梦》canon text.
SYNTHETIC = "第一回\nc1 进府。c2 居园。\n第二回\nc3 探望 c2。\n"

INSTANCE = WorldInstanceId("wld_rc001")
BRANCH = BranchId("br_rc001")
WORLDLINE = WorldlineId("wl_rc001")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)


def _definition() -> AssembledWorldPack:
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


def _base_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


@pytest.mark.unit
def test_instantiate_rc001_via_single_commit_authority() -> None:
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    instance = instantiate_rc001(
        authority=authority,
        state=_base_state(),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        worldline_id=WORLDLINE,
        rule_version=RULES,
        world_time=WorldTime(1),
        definition=_definition(),
    )
    assert instance.identity.definition_ref == "wd_rc001"
    assert instance.identity.genesis_ref == "gen_rc001"
    assert instance.identity.constitution_ref == "con_literary_historical"
    assert instance.profile.runtime_ref == "runtime:deterministic"
    assert instance.profile.domain_refs == ("narrative_domain",)
    # Exactly one genesis event on the single authority path.
    assert len(store.load(INSTANCE, BRANCH)) == 1
    assert instance.snapshot.revision == 1
    assert instance.snapshot.entity_count >= 7


@pytest.mark.unit
def test_initial_snapshot_is_fixed_and_reproducible() -> None:
    hashes: list[str] = []
    for _ in range(2):
        store = InMemoryEventStore()
        authority = CommitAuthority(store, RULES, SCHEMA)
        instance = instantiate_rc001(
            authority=authority,
            state=_base_state(),
            instance_id=INSTANCE,
            branch_id=BRANCH,
            worldline_id=WORLDLINE,
            rule_version=RULES,
            world_time=WorldTime(1),
            definition=_definition(),
        )
        hashes.append(instance.snapshot.content_hash)
    assert hashes[0] == hashes[1]
    assert len(hashes[0]) == 64


@pytest.mark.unit
def test_lineage_root_recorded() -> None:
    from wanxiang_domain.lineage import LineageGraph

    graph = LineageGraph()
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    instantiate_rc001(
        authority=authority,
        state=_base_state(),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        worldline_id=WORLDLINE,
        rule_version=RULES,
        world_time=WorldTime(1),
        definition=_definition(),
    )
    record_lineage_root(
        graph,
        instance_id=INSTANCE,
        definition_id=WorldDefinitionId("wd_rc001"),
    )
    node = graph.get_node(INSTANCE.value)
    assert node is not None
    assert node.kind == "worldline"
    assert node.definition_ref == "wd_rc001"


@pytest.mark.unit
def test_resolve_profile_is_deterministic() -> None:
    first = resolve_rc001_profile()
    second = resolve_rc001_profile()
    assert first == second
