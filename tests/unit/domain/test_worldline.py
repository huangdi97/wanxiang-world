"""G31A: World Definition / Worldline identity model."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA, build_fixture_events
from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata, BranchRevision, EventSeq
from wanxiang_domain.ids import (
    BranchId,
    WorldDefinitionId,
    WorldInstanceId,
    WorldlineId,
)
from wanxiang_domain.worldline import (
    InstanceIdentity,
    WorldDefinition,
    WorldlineFork,
    WorldlineIdentity,
)
from wanxiang_runtime.branch import fork_branch
from wanxiang_runtime.replay import ReplayEngine

DEF = WorldDefinition(
    definition_id=WorldDefinitionId("wd_sf_world"),
    version=1,
    name="Synthetic Full World",
    constitution_ref="con_legacy_v5",
    genesis_ref="pack://sf-scenario@1.0.0",
    package_ref="pack://sf-world@1.0.0",
).with_hash()


@pytest.mark.unit
def test_world_definition_is_read_only_and_versioned() -> None:
    assert DEF.version == 1
    assert DEF.content_hash  # frozen fingerprint
    prim = DEF.to_primitive()
    assert prim["constitution_ref"] == "con_legacy_v5"
    assert prim["content_hash"] == DEF.content_hash
    # Read-only: no mutation API on the definition.
    with pytest.raises(FrozenInstanceError):
        DEF.name = "changed"  # type: ignore[misc]


@pytest.mark.unit
def test_worldpack_unchanged_by_running() -> None:
    """Running history never writes back to the World Definition."""
    before = DEF.content_hash
    state = ReplayEngine(RULES, SCHEMA).replay(build_fixture_events())
    # Instance identity references the definition, does not modify it.
    identity = InstanceIdentity(
        instance_id=INSTANCE,
        worldline_id=WorldlineId("wl_golden"),
        definition_ref=DEF.definition_id.value,
        genesis_ref=DEF.genesis_ref,
        constitution_ref=DEF.constitution_ref,
        runtime_ref=f"runtime:{RULES.value}",
    )
    assert identity.definition_ref == DEF.definition_id.value
    assert state.revision.value == 5
    assert DEF.content_hash == before  # WorldPack unchanged by running


@pytest.mark.unit
def test_branch_fork_is_a_worldline_fork_relationship() -> None:
    parent = WorldlineIdentity(
        worldline_id=WorldlineId("wl_parent"),
        instance_id=INSTANCE,
        root_branch_id=BRANCH,
        definition_ref=DEF.definition_id.value,
        constitution_ref=DEF.constitution_ref,
    )
    state = ReplayEngine(RULES, SCHEMA).replay(build_fixture_events())
    child = fork_branch(
        BranchMetadata(
            branch_id=BRANCH,
            instance_id=INSTANCE,
            ancestry=BranchAncestry(),
            schema_version=SCHEMA,
            rule_version=RULES,
        ),
        state,
        fork_revision=BranchRevision(5),
        fork_event_seq=EventSeq(5),
        snapshot_ref="mem://fork5",
        branch_id=BranchId("br_child"),
    )
    assert child.ancestry.fork_revision is not None
    assert child.ancestry.fork_event_seq is not None
    fork = WorldlineFork(
        parent_worldline_id=parent.worldline_id,
        parent_branch_id=BRANCH,
        child_branch_id=child.branch_id,
        fork_revision=child.ancestry.fork_revision.value,
        fork_event_seq=child.ancestry.fork_event_seq.value,
    )
    prim = fork.to_primitive()
    assert prim["parent_branch_id"] == BRANCH.value
    assert prim["child_branch_id"] == "br_child"
    assert prim["fork_revision"] == 5
    # Identity round-trip.
    parent_prim = parent.to_primitive()
    assert parent_prim["worldline_id"] == "wl_parent"
    assert parent_prim["root_branch_id"] == BRANCH.value


@pytest.mark.unit
def test_instance_identity_round_trip() -> None:
    identity = InstanceIdentity(
        instance_id=WorldInstanceId("wld_g31a"),
        worldline_id=WorldlineId("wl_g31a"),
        definition_ref="wd_sf_world",
        genesis_ref="pack://sf-scenario@1.0.0",
        constitution_ref="con_legacy_v5",
        runtime_ref="runtime:1",
    )
    prim = identity.to_primitive()
    assert prim["instance_id"] == "wld_g31a"
    assert prim["worldline_id"] == "wl_g31a"
    assert prim["genesis_ref"] == "pack://sf-scenario@1.0.0"
