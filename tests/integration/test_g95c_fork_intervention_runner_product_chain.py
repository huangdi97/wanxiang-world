"""G95C: real private source chain with explicit snapshot/event forks."""

from __future__ import annotations

import pathlib
from typing import cast

from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.reality.intervention import (
    ExperimentSetup,
    Intervention,
    InterventionTrigger,
)
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import ForkInterventionRunner


def _source() -> SourceRecord:
    content = "# G95C source\nCharacter: Alice\nrule: records are retained\n"
    return SourceRecord(
        source_id="g95c_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95c_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95c",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95c",
        access="private",
    )


def test_snapshot_event_forks_preserve_parent_and_resume_by_replay(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable = PlayableService(runtime)
    authored = OneClickAuthoring().run("job_g95c", (_source(),), profile="book")
    profile = playable.register_package(
        authored.package,
        owner_id="owner:g95c",
        visibility="private",
    )
    character = playable.entry.create_character(
        "owner:g95c",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g95c_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="owner:g95c",
        mode="embodiment",
        session_id="session:g95c",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    parent = BranchId(playable.store.get_instance(instance.value).branch_id)
    playable.action(
        instance.value,
        viewer_id="owner:g95c",
        action_type="set_status",
        payload={"entity_id": "ent_alice", "status": "baseline"},
    )
    parent_before = runtime.current_state(instance, parent)
    parent_hash = parent_before.semantic_hash()
    parent_events = runtime.events(instance, parent)
    assert len(parent_events) >= 2

    event_intervention = Intervention(
        intervention_id="intervention:g95c:event",
        kind="opportunity",
        trigger=InterventionTrigger.on_event(parent_events[0].event_id.value),
        parent_branch_ref=parent.value,
        artifact_ref="artifact:g95c:event",
    )
    time_intervention = Intervention(
        intervention_id="intervention:g95c:time",
        kind="pressure",
        trigger=InterventionTrigger.at_time(10),
        parent_branch_ref=parent.value,
        artifact_ref="artifact:g95c:time",
    )
    setup = (
        ExperimentSetup(
            setup_id="setup:g95c",
            baseline_instance_ref=instance.value,
            baseline_branch_ref=parent.value,
            artifact_ref="artifact:g95c:setup",
        )
        .add(event_intervention)
        .add(time_intervention)
    )
    runner = ForkInterventionRunner()

    event_run = runner.fork(
        runtime,
        instance,
        parent,
        setup,
        event_intervention,
    )
    time_run = runner.fork(
        runtime,
        instance,
        parent,
        setup,
        time_intervention,
        fork_revision=BranchRevision(1),
    )

    assert event_run.provenance.fork_revision == parent_events[0].revision.value
    assert event_run.provenance.fork_snapshot_ref
    assert time_run.provenance.fork_revision == 1
    assert len(runner.ledger.entries()) == 2
    assert runtime.events(instance, parent) == parent_events
    assert runtime.current_state(instance, parent).semantic_hash() == parent_hash

    child = BranchId(time_run.branch.branch_ref)
    child_state = runtime.current_state(instance, child)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_g95c_child"),
            instance_id=instance,
            branch_id=child,
            expected_revision=BranchRevision(child_state.revision.value),
            action_type="set_status",
            payload={"entity_id": "ent_alice", "status": "intervened"},
            world_time=WorldTime(10),
        )
    )
    resumed = runner.resume(runtime, time_run, expected_revision=2)

    assert resumed.status == "resumed"
    assert resumed.resume_count == 1
    assert resumed.replay_hash == runtime.current_state(instance, child).semantic_hash()
    assert runner.ledger.entries(time_run.run_id)[-1].status == "resumed"
    assert runtime.events(instance, parent) == parent_events
    assert runtime.current_state(instance, parent).semantic_hash() == parent_hash
