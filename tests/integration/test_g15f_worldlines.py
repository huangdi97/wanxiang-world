"""G15F: branch, time-travel & counterfactual worldline comparison.

Three worldlines from shared history: baseline (no intervention), intervention
(deliver the letter), and a second intervention (read the letter). Each is
independently replayable; the semantic diff highlights causal differences;
parent history is unchanged; historical reads are consistent with revision.
"""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.material.fixture import (
    INSTANCE,
    LETTER,
    MESSENGER,
    RECIPIENT,
    build_package_fixture_commands,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.resolver import (
    ACTION_READ,
    ACTION_TRANSFER,
    register_material_resolvers,
)


def _cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: dict[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


def _runtime(path: pathlib.Path) -> WorldRuntime:
    return make_world_runtime(path, extra_resolvers=register_material_resolvers)


def test_three_worldlines_compare_causally(persist_db_path: pathlib.Path) -> None:
    runtime = _runtime(persist_db_path)
    w = runtime.create_world(instance_id=INSTANCE)
    branch = w.root_branch_id
    for command in build_package_fixture_commands(branch):
        runtime.submit_command(command)
    fork_revision = runtime.current_state(INSTANCE, branch).revision.value
    parent_hash = runtime.current_state(INSTANCE, branch).semantic_hash()

    # Baseline worldline: no intervention.
    baseline = runtime.create_branch(INSTANCE, branch)
    assert baseline.ancestry.parent_branch_id == branch

    # Intervention 1: deliver the letter to the recipient.
    deliver = runtime.create_branch(INSTANCE, branch)
    runtime.submit_command(
        _cmd(
            deliver.branch_id,
            fork_revision,
            ACTION_TRANSFER,
            {
                "item_id": LETTER.value,
                "from_custodian": MESSENGER.value,
                "to_custodian": RECIPIENT.value,
            },
            "w1_deliver",
        )
    )

    # Intervention 2: deliver then read.
    read_branch = runtime.create_branch(INSTANCE, branch)
    runtime.submit_command(
        _cmd(
            read_branch.branch_id,
            fork_revision,
            ACTION_TRANSFER,
            {
                "item_id": LETTER.value,
                "from_custodian": MESSENGER.value,
                "to_custodian": RECIPIENT.value,
            },
            "w2_deliver",
        )
    )
    runtime.submit_command(
        _cmd(
            read_branch.branch_id,
            fork_revision + 1,
            ACTION_READ,
            {"item_id": LETTER.value, "reader_id": RECIPIENT.value},
            "w2_read",
        )
    )

    # Parent history is unchanged by all three worldlines.
    assert runtime.current_state(INSTANCE, branch).semantic_hash() == parent_hash

    # Distinct causal outcomes.
    h_base = runtime.current_state(INSTANCE, baseline.branch_id).semantic_hash()
    h_deliver = runtime.current_state(INSTANCE, deliver.branch_id).semantic_hash()
    h_read = runtime.current_state(INSTANCE, read_branch.branch_id).semantic_hash()
    # Baseline (no intervention) is identical to the parent; interventions diverge.
    assert h_base == parent_hash
    assert h_deliver != h_base
    assert h_read != h_deliver
    # Baseline custodian is unchanged; delivered branches moved custody.
    assert (
        MaterialQuery(runtime.current_state(INSTANCE, baseline.branch_id)).custodian(LETTER)
        == MESSENGER
    )
    assert (
        MaterialQuery(runtime.current_state(INSTANCE, deliver.branch_id)).custodian(LETTER)
        == RECIPIENT
    )

    # Each worldline replays independently to its own hash.
    engine = ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
    base_state = runtime.current_state(INSTANCE, baseline.branch_id)
    parent_state = runtime.current_state(INSTANCE, branch)
    # Baseline has no new events: replay from the parent baseline reproduces it.
    replay_base = engine.replay((), baseline=parent_state, start_seq=1)
    assert replay_base.semantic_hash() == h_base
    for branch_id in (deliver.branch_id, read_branch.branch_id):
        child_state = runtime.current_state(INSTANCE, branch_id)
        events = runtime.persistence.event_store.load(INSTANCE, branch_id)
        replay = engine.replay(events, baseline=base_state, start_seq=1)
        assert replay.semantic_hash() == child_state.semantic_hash()

    # Diff highlights causal differences (delivered branch has the custody update).
    diff = runtime.diff(INSTANCE, baseline.branch_id, deliver.branch_id)
    assert len(diff.updated_entities) >= 1 or len(diff.added_entities) >= 1

    # Historical read projection is consistent with the fork revision: the
    # parent at the fork revision still shows messenger custody (time-travel/read-only).
    historical = runtime.current_state(INSTANCE, branch)
    assert MaterialQuery(historical).custodian(LETTER) == MESSENGER
    assert historical.revision.value == fork_revision
